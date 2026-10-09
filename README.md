# PolyEdge Python SDK

[![PyPI version](https://img.shields.io/pypi/v/polyedge.svg?color=blue&cache=1)](https://pypi.org/project/polyedge/)
[![Python versions](https://img.shields.io/pypi/pyversions/polyedge.svg?cache=1)](https://pypi.org/project/polyedge/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-polyedge.dev-cyan)](https://polyedge.dev/docs)
[![Benchmark](https://img.shields.io/badge/benchmark-100%2B_nodes-green)](https://github.com/PolyEdgeDev/polyedge-stream-benchmark)

Official Python SDK for **[PolyEdge](https://polyedge.dev)** — **Ultra-Low-Latency Polymarket Mempool Trade Streaming & Real-Time On-Chain Analytics API.**

> Engineered for Polymarket copy-trading bots, professional traders, and prediction market builders. Capture pending trades pre-block and track smart money with institutional-grade on-chain analytics.

---

## Key Features

- **4 First-Class Namespaces**: Aligned with OpenAPI 3.1:
  - `client.streams`: Real-time SSE trade streaming, sessions & filter management.
  - `client.analytics`: Polymarket on-chain trade attribution, trader leaderboards, market settlement audit.
  - `client.account`: User profile, API keys, request telemetry, and ledger.
  - `client.subscription`: Pricing tier catalog, upgrade quotes, and promo codes.
- **Asynchronous SSE Stream Engine**:
  - **45s Keep-Alive Watchdog**: Native `httpx` read-timeout detection automatically cleans up dead socket half-open connections.
  - **Automatic Resume with `Last-Event-ID`**: Seamlessly retrieves buffered trades on reconnection.
  - **Fail-Fast Policy**: Immediate non-retry termination on fatal HTTP 401/403/404 errors.
  - **Pythonic Async Iterator**: Streamlined `async for tx in stream.subscribe():` interface.
- **Pre-Block Polymarket Trade Streaming**: Peered with 100+ Polygon nodes to capture pending Polymarket trades pre-block. The World's Fastest — [verify yourself](https://github.com/PolyEdgeDev/polyedge-stream-benchmark).

---

## Installation

```bash
pip install polyedge
```

---

## Quick Start

### 1. Initialize Client

```python
import os
from polyedge import PolyEdgeClient

client = PolyEdgeClient(api_key=os.environ.get("POLYEDGE_API_KEY", "your_polyedge_api_key"))
```

### 2. Real-Time Mempool Trade Stream (SSE)

```python
import asyncio
from polyedge import PolyEdgeClient

async def main():
    client = PolyEdgeClient(api_key="your_polyedge_api_key")

    stream = client.streams.connect("your_stream_id", heartbeat_timeout=45.0)

    # Optional heartbeat listener
    stream.on_heartbeat(lambda: print("💓 Server heartbeat received"))

    async for tx in stream.subscribe():
        tx_hash = tx.get("tx_hash", "")[:18]
        question = tx.get("market", {}).get("question", "")
        taker = tx.get("taker", {})
        outcome = taker.get("outcome")
        side = taker.get("side")
        shares = taker.get("shares")
        makers_count = len(tx.get("makers", []))

        print(f"⚡ [Live Trade] Tx: {tx_hash}...")
        print(f"   Market: \"{question}\"")
        print(f"   Taker: {outcome} ({side}) | Shares: {shares}")
        print(f"   Matched Makers: {makers_count} orders")

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. Analytics: Leaderboard & Trader Dossier

```python
# Leaderboard
leaderboard = client.analytics.get_leaderboard(limit=5)
print(f"Total active traders tracked: {leaderboard.get('total_count')}")

for i, t in enumerate(leaderboard.get("traders", [])):
    addr = t.get("profile", {}).get("address")
    name = t.get("profile", {}).get("name") or "Anonymous"
    pnl_usd = (t.get("total_pnl", 0)) / 1e6
    print(f"#{i + 1} {addr} ({name}) - Realized PnL: ${pnl_usd:,.2f}")

# Deep Trader Profile
profile = client.analytics.get_trader("0x51698a47f840a242abc2ca0351371c7ffac41842")
print(f"Taker Rebate Tier: {profile.get('taker_tier_name')}")
```

### 4. Account Profile & Telemetry

```python
# Account info
profile = client.account.get_profile()
print(f"Email: {profile.get('email')}, Tier: {profile.get('tier')}")

# Daily telemetry
telemetry = client.account.get_telemetry()
print(f"Total API calls today: {telemetry.get('total_requests')}")
```

---

## Complete API Service Reference (28 Methods)

### 1. Streams Service (`client.streams`)

| Method | HTTP | Description |
| :--- | :--- | :--- |
| `connect(stream_id, heartbeat_timeout)` | `GET /streams/{id}` (SSE) | Connect to ultra-low-latency real-time SSE mempool trade stream |
| `list()` | `GET /streams` | List all configured data streams |
| `create(req)` | `POST /streams` | Provision a new targeted filter stream (tags, addresses, series) |
| `get(id)` | `GET /streams/{id}` | Get stream metadata and configuration by ID |
| `update_metadata(id, req)` | `PUT /streams/{id}/meta` | Update stream name and description |
| `update_subscription(id, req)` | `PUT /streams/{id}/subscription` | Hot-reload market filters (addresses, tags, series) on active stream |
| `delete(id)` | `DELETE /streams/{id}` | Delete stream by ID |
| `get_active_sessions()` | `GET /sessions` | List all active live SSE connections across streams |
| `get_session_history(limit, offset)` | `GET /sessions/history` | Query historical SSE connection logs and durations |

### 2. Analytics Service (`client.analytics`)

| Method | HTTP | Description |
| :--- | :--- | :--- |
| `get_leaderboard(limit, offset)` | `GET /v2/analytics/leaderboard` | Top profitable traders ranked by realized PnL, volume, and ROI |
| `get_trader(address)` | `GET /v2/traders/{address}` | Comprehensive trader intelligence profile, taker tier, and top tags |
| `get_trader_hourly_stats(address)` | `GET /v2/traders/{address}/hourly_stats` | 24-hour hourly trading PnL and volume breakdown |
| `get_trader_markets(address, limit, offset)` | `GET /v2/traders/{address}/markets` | Historical market positions and settled outcomes by trader |
| `get_trader_market_orders(addr, id, limit, offset)` | `GET /v2/traders/{address}/markets/{id}/orders` | Order fill details for a specific trader in a specific market |
| `get_market(id)` | `GET /v2/markets/{id}` | Prediction market detail, top 20 earners, and volume attribution |
| `get_deposits(limit, offset)` | `GET /v2/analytics/deposits` | 60-day aggregated trader deposit summaries (>= 100 pUSD) |

### 3. Account Service (`client.account`)

| Method | HTTP | Description |
| :--- | :--- | :--- |
| `get_profile()` | `GET /v2/user/me` | Current user profile, active tier, and deposit balance |
| `list_keys()` | `GET /v2/user/keys` | List all active API keys and statuses |
| `create_key(req)` | `POST /v2/user/keys` | Generate a new API key with custom name |
| `update_key(key, req)` | `PATCH /v2/user/keys/{key}` | Enable, disable, or rename an API key |
| `delete_key(key)` | `DELETE /v2/user/keys/{key}` | Revoke and delete an API key |
| `get_ledger(limit, offset)` | `GET /v2/user/ledger` | Balance ledger transaction records |
| `get_telemetry()` | `GET /v2/user/telemetry` | Daily request count and per-endpoint usage telemetry |
| `withdraw(req)` | `POST /v2/user/withdraw` | Request balance withdrawal |

### 4. Subscription Service (`client.subscription`)

| Method | HTTP | Description |
| :--- | :--- | :--- |
| `list_tiers()` | `GET /v2/tiers` | Public tier catalog, feature allowances, and pricing specifications |
| `get_quote(req)` | `POST /v2/user/subscribe/quote` | Calculate quote for plan upgrade or billing cycle change |
| `subscribe(req)` | `POST /v2/user/subscribe` | Purchase or upgrade tier subscription |
| `validate_promo_code(req)` | `POST /v2/user/promo-codes/validate` | Validate promotional discount code |

---

## License

[MIT](LICENSE) © 2026 [PolyEdge Labs](https://polyedge.dev)
