import asyncio
import json
import unittest
from polyedge import PolyEdgeStream, PolyEdgeFatalStreamError

class TestPolyEdgeStream(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.received_headers = []
        self.request_count = 0

        async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
            self.request_count += 1
            request_line = await reader.readline()
            req_str = request_line.decode("utf-8", errors="replace")

            headers = {}
            while True:
                line = await reader.readline()
                if line in (b"\r\n", b"\n", b""):
                    break
                h_str = line.decode("utf-8", errors="replace").strip()
                if ":" in h_str:
                    k, v = h_str.split(":", 1)
                    headers[k.strip().lower()] = v.strip()

            self.received_headers.append(headers)

            if "fatal" in req_str:
                res = (
                    b"HTTP/1.1 401 Unauthorized\r\n"
                    b"Content-Type: application/json\r\n"
                    b"Content-Length: 25\r\n"
                    b"Connection: close\r\n\r\n"
                    b'{"error": "Unauthorized"}'
                )
                writer.write(res)
                await writer.drain()
                writer.close()
                return

            if "stream-1" in req_str:
                res_headers = (
                    b"HTTP/1.1 200 OK\r\n"
                    b"Content-Type: text/event-stream\r\n"
                    b"Cache-Control: no-cache\r\n"
                    b"Connection: close\r\n\r\n"
                )
                writer.write(res_headers)
                await writer.drain()

                # 1. Send heartbeat
                writer.write(b": heartbeat\n\n")
                await writer.drain()

                # 2. Send transaction event
                tx_data = {
                    "tx_hash": "0xpython_test",
                    "timestamp": "2026-10-09T00:00:00Z",
                    "market": {"id": 1, "outcomes": ["Yes", "No"], "token_ids": ["1", "2"]},
                }
                event_payload = f"id: 555\nevent: tx\ndata: {json.dumps(tx_data)}\n\n".encode("utf-8")
                writer.write(event_payload)
                await writer.drain()

                writer.close()
                return

            writer.write(b"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\nConnection: close\r\n\r\n")
            await writer.drain()
            writer.close()

        self.server = await asyncio.start_server(handle_client, "127.0.0.1", 0)
        port = self.server.sockets[0].getsockname()[1]
        self.base_url = f"http://127.0.0.1:{port}"

    async def asyncTearDown(self):
        self.server.close()
        await self.server.wait_closed()

    async def test_python_stream_receive(self):
        stream = PolyEdgeStream(
            stream_id="stream-1",
            api_key="test_key",
            stream_base_url=self.base_url,
            heartbeat_timeout=2.0,
            initial_backoff=0.05,
        )

        heartbeat_received = False
        def on_hb():
            nonlocal heartbeat_received
            heartbeat_received = True

        stream.on_heartbeat(on_hb)

        events = []
        async for tx in stream.subscribe():
            events.append(tx)
            stream.close()
            break

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["tx_hash"], "0xpython_test")
        self.assertEqual(stream.last_event_id, "555")
        self.assertTrue(heartbeat_received)

    async def test_python_stream_fatal_fail(self):
        stream = PolyEdgeStream(
            stream_id="fatal",
            api_key="bad_key",
            stream_base_url=self.base_url,
            heartbeat_timeout=2.0,
            initial_backoff=0.05,
        )

        with self.assertRaises(PolyEdgeFatalStreamError) as ctx:
            async for _ in stream.subscribe():
                pass

        self.assertIn("401", str(ctx.exception))
        self.assertEqual(self.request_count, 1)

    async def test_python_stream_watchdog_and_resume(self):
        # Dedicated server for watchdog test
        conns = []
        async def handle_watchdog(reader, writer):
            request_line = await reader.readline()
            headers = {}
            while True:
                line = await reader.readline()
                if line in (b"\r\n", b"\n", b""):
                    break
                h_str = line.decode("utf-8", errors="replace").strip()
                if ":" in h_str:
                    k, v = h_str.split(":", 1)
                    headers[k.strip().lower()] = v.strip()
            conns.append(headers)

            if len(conns) == 1:
                # First connection: send one message with id 777, then stall so watchdog fires
                writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: text/event-stream\r\nCache-Control: no-cache\r\n\r\n")
                await writer.drain()
                writer.write(b"id: 777\nevent: tx\ndata: {\"tx_hash\": \"0xfirst\"}\n\n")
                await writer.drain()
                # Do not write more; wait for client watchdog to timeout
                await asyncio.sleep(2.0)
                writer.close()
            else:
                # Reconnected connection: send tx and finish
                writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: text/event-stream\r\nCache-Control: no-cache\r\n\r\n")
                await writer.drain()
                writer.write(b": heartbeat\n\n")
                await writer.drain()
                writer.write(b"id: 778\nevent: tx\ndata: {\"tx_hash\": \"0xsecond\"}\n\n")
                await writer.drain()
                writer.close()

        server = await asyncio.start_server(handle_watchdog, "127.0.0.1", 0)
        port = server.sockets[0].getsockname()[1]

        try:
            stream = PolyEdgeStream(
                stream_id="watchdog-test",
                api_key="test_key",
                stream_base_url=f"http://127.0.0.1:{port}",
                heartbeat_timeout=0.3, # 300ms watchdog timeout
                initial_backoff=0.05,
            )

            txs = []
            async for tx in stream.subscribe():
                txs.append(tx)
                if len(txs) == 2:
                    stream.close()
                    break

            self.assertEqual(len(txs), 2)
            self.assertEqual(txs[0]["tx_hash"], "0xfirst")
            self.assertEqual(txs[1]["tx_hash"], "0xsecond")
            self.assertEqual(len(conns), 2, "Should have reconnected after watchdog timeout")
            self.assertNotIn("last-event-id", conns[0])
            self.assertEqual(conns[1].get("last-event-id"), "777", "Reconnect must carry Last-Event-ID: 777")
        finally:
            server.close()
            await server.wait_closed()

if __name__ == "__main__":
    unittest.main()
