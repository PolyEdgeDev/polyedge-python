from __future__ import annotations
import asyncio
import json
import random
from typing import AsyncGenerator, Optional, Dict, Any, Callable
import httpx

class PolyEdgeStreamError(Exception):
    """Base error for PolyEdge stream."""
    pass

class PolyEdgeFatalStreamError(PolyEdgeStreamError):
    """Fatal stream error (401, 403, 404) which should not be retried."""
    pass

class PolyEdgeStream:
    def __init__(
        self,
        stream_id: str,
        api_key: str,
        stream_base_url: str = "https://stream.polyedge.dev",
        heartbeat_timeout: float = 45.0,
        initial_backoff: float = 1.0,
        max_backoff: float = 30.0,
    ):
        if not stream_id:
            raise ValueError("stream_id must not be empty")
        if not api_key:
            raise ValueError("api_key must not be empty")

        self.stream_id = stream_id
        self.api_key = api_key
        self.stream_base_url = stream_base_url.rstrip("/")
        self.heartbeat_timeout = heartbeat_timeout
        self.initial_backoff = initial_backoff
        self.max_backoff = max_backoff

        self.last_event_id: Optional[str] = None
        self._is_closed = False
        self._on_heartbeat: Optional[Callable[[], None]] = None

    def on_heartbeat(self, callback: Callable[[], None]) -> None:
        """Register a callback when an SSE server heartbeat (': heartbeat') is received."""
        self._on_heartbeat = callback

    def close(self) -> None:
        """Gracefully close the stream and stop auto-reconnect."""
        self._is_closed = True

    async def subscribe(self) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Continuously streams real-time trades as dicts.
        Automatically handles Watchdog keep-alive timeout, Last-Event-ID resumption,
        and exponential backoff reconnects.
        """
        backoff = self.initial_backoff

        # Timeout config: read=heartbeat_timeout ensures that if no bytes (not even heartbeat)
        # arrive within 45s, httpx raises ReadTimeout so we can cleanly reconnect.
        timeout_config = httpx.Timeout(
            connect=10.0,
            read=self.heartbeat_timeout,
            write=10.0,
            pool=None,
        )

        headers = {
            "Accept": "text/event-stream",
            "X-PolyEdge-Key": self.api_key,
            "Cache-Control": "no-cache",
        }

        while not self._is_closed:
            req_headers = dict(headers)
            params = {}
            if self.last_event_id:
                req_headers["Last-Event-ID"] = self.last_event_id
                params["lastEventId"] = self.last_event_id

            url = f"{self.stream_base_url}/streams/{self.stream_id}"

            try:
                async with httpx.AsyncClient(timeout=timeout_config, trust_env=False) as client:
                    async with client.stream("GET", url, headers=req_headers, params=params) as response:
                        # Fail-fast on fatal non-retryable HTTP errors
                        if response.status_code in (400, 401, 403, 404):
                            body = await response.aread()
                            raise PolyEdgeFatalStreamError(
                                f"Fatal HTTP {response.status_code} on stream {self.stream_id}: {body.decode('utf-8', errors='replace')}"
                            )

                        response.raise_for_status()

                        # Reset backoff on successful connection
                        backoff = self.initial_backoff

                        cur_id: Optional[str] = None
                        cur_event = "message"
                        cur_data: list[str] = []

                        async for raw_line in response.aiter_lines():
                            if self._is_closed:
                                return

                            line = raw_line.strip()
                            if not line:
                                # End of an SSE event block
                                if cur_id:
                                    self.last_event_id = cur_id

                                if cur_event == "tx" and cur_data:
                                    payload = json.loads("\n".join(cur_data))
                                    yield payload

                                cur_id = None
                                cur_event = "message"
                                cur_data = []
                                continue

                            # Server heartbeat comment: resets httpx socket read timer
                            if line.startswith(":"):
                                if self._on_heartbeat:
                                    self._on_heartbeat()
                                continue
                            elif line.startswith("id:"):
                                cur_id = line[3:].strip()
                            elif line.startswith("event:"):
                                cur_event = line[6:].strip()
                            elif line.startswith("data:"):
                                cur_data.append(raw_line[raw_line.find("data:") + 5:].lstrip())

            except PolyEdgeFatalStreamError:
                # Do not retry fatal errors
                raise
            except (httpx.ReadTimeout, httpx.NetworkError, httpx.HTTPStatusError, Exception):
                if self._is_closed:
                    return

                # Calculate exponential backoff with random jitter
                jitter = backoff * (0.8 + random.random() * 0.4)
                await asyncio.sleep(jitter)
                backoff = min(self.max_backoff, backoff * 2.0)
