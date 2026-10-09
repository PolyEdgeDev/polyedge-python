from __future__ import annotations
from typing import Optional, Dict, Any, List
import httpx
from .stream import PolyEdgeStream
from . import types

class StreamsService:
    """Service client for Streams operations."""
    def __init__(self, client: PolyEdgeClient):
        self._client = client

    def connect(self, stream_id: str, heartbeat_timeout: float = 45.0) -> PolyEdgeStream:
        """Connects to real-time SSE order stream with watchdog keep-alive."""
        return PolyEdgeStream(
            stream_id=stream_id,
            api_key=self._client.api_key,
            stream_base_url=self._client.stream_base_url,
            heartbeat_timeout=heartbeat_timeout,
        )

    def list(self) -> Dict[str, Any]:
        """List User Streams
        Returns custom and managed real-time trade streams configured by the user.
        """
        return self._client._request(self._client.stream_base_url, 'GET', f"/streams", json_body=None, params=None)

    def create(self, req: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create Filtered Order Stream
        Provisions a new custom real-time stream with optional address, tag, or series filters.
        :param req: Request payload dictionary
        """
        return self._client._request(self._client.stream_base_url, 'POST', f"/streams", json_body=req, params=None)

    def get(self, id: str) -> Dict[str, Any]:
        """Get Stream Metadata
        Fetches metadata, active sessions count, and filter configuration for a specific stream.
        :param id: Stream unique ID
        """
        return self._client._request(self._client.stream_base_url, 'GET', f"/streams/{id}/meta", json_body=None, params=None)

    def delete(self, id: str) -> Dict[str, Any]:
        """Delete Stream
        Permanently removes a stream and gracefully disconnects all connected listener sessions.
        :param id: Stream unique ID
        """
        return self._client._request(self._client.stream_base_url, 'DELETE', f"/streams/{id}", json_body=None, params=None)

    def update_metadata(self, id: str, req: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Update Stream Metadata
        Updates operational attributes of the stream, such as nickname or enabled/disabled status.
        :param id: Stream unique ID
        :param req: Request payload dictionary
        """
        return self._client._request(self._client.stream_base_url, 'PUT', f"/streams/{id}/meta", json_body=req, params=None)

    def update_subscription(self, id: str, req: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Update Stream Filter Subscription
        Dynamically mutates monitored wallet addresses, market tags, or series slugs without disconnecting SSE clients.
        :param id: Stream unique ID
        :param req: Request payload dictionary
        """
        return self._client._request(self._client.stream_base_url, 'PUT', f"/streams/{id}/subscription", json_body=req, params=None)

    def get_active_sessions(self) -> Dict[str, Any]:
        """List All User Active Sessions
        Returns all currently connected active SSE listeners for this account.
        """
        return self._client._request(self._client.stream_base_url, 'GET', f"/sessions", json_body=None, params=None)

    def get_session_history(self, limit: Optional[int] = None, offset: Optional[int] = None) -> Dict[str, Any]:
        """List User Stream Session History
        Returns historical SSE connection logs including duration and pushed transactions count.
        :param limit: Max records to return
        :param offset: Pagination offset
        """
        params = {}
        if limit is not None: params['limit'] = limit
        if offset is not None: params['offset'] = offset
        return self._client._request(self._client.stream_base_url, 'GET', f"/sessions/history", json_body=None, params=params)

class AnalyticsService:
    """Service client for Analytics operations."""
    def __init__(self, client: PolyEdgeClient):
        self._client = client

    def get_deposits(self, limit: Optional[int] = None, offset: Optional[int] = None) -> Dict[str, Any]:
        """60-Day Trader Deposit Analytics
        Returns 60-day aggregated deposit summary and individual transaction breakdown for top traders.
        :param limit: Max records to return
        :param offset: Pagination offset
        """
        params = {}
        if limit is not None: params['limit'] = limit
        if offset is not None: params['offset'] = offset
        return self._client._request(self._client.api_base_url, 'GET', f"/v2/analytics/deposits", json_body=None, params=params)

    def get_leaderboard(self, limit: Optional[int] = None, offset: Optional[int] = None) -> Dict[str, Any]:
        """Top Traders PnL Leaderboard
        Queries ranked traders across timeframes with PnL, volume, win rate, and performance metrics.
        :param limit: Max traders to return
        :param offset: Pagination offset
        """
        params = {}
        if limit is not None: params['limit'] = limit
        if offset is not None: params['offset'] = offset
        return self._client._request(self._client.api_base_url, 'GET', f"/v2/analytics/leaderboard", json_body=None, params=params)

    def get_market(self, id: str) -> Dict[str, Any]:
        """Get Prediction Market Detail
        Fetches standardized market metadata matching on-chain condition IDs and NegRisk parameters.
        :param id: Market numeric ID or condition ID
        """
        return self._client._request(self._client.api_base_url, 'GET', f"/v2/markets/{id}", json_body=None, params=None)

    def get_trader(self, address: str) -> Dict[str, Any]:
        """Get Trader Intelligence Profile
        Fetches trader identity dossier, pUSD balance, total PnL, win rates, and ranking metrics.
        :param address: Trader Polygon/Ethereum wallet address
        """
        return self._client._request(self._client.api_base_url, 'GET', f"/v2/traders/{address}", json_body=None, params=None)

    def get_trader_hourly_stats(self, address: str) -> Dict[str, Any]:
        """Get Hourly PnL Equity Curve
        Provides 1-hour bucketed historical equity curves and trade metrics for a specific trader.
        :param address: Trader Polygon/Ethereum wallet address
        """
        return self._client._request(self._client.api_base_url, 'GET', f"/v2/traders/{address}/hourly_stats", json_body=None, params=None)

    def get_trader_markets(self, address: str, limit: Optional[int] = None, offset: Optional[int] = None) -> Dict[str, Any]:
        """Get Trader Market Participation History
        Queries resolved and active prediction markets traded by the specified wallet address.
        :param address: Trader Polygon/Ethereum wallet address
        :param limit: Max markets to return
        :param offset: Pagination offset
        """
        params = {}
        if limit is not None: params['limit'] = limit
        if offset is not None: params['offset'] = offset
        return self._client._request(self._client.api_base_url, 'GET', f"/v2/traders/{address}/markets", json_body=None, params=params)

    def get_trader_market_orders(self, address: str, id: str, limit: Optional[int] = None, offset: Optional[int] = None) -> Dict[str, Any]:
        """Get Trader Orders in Market
        Retrieves granular fill events, side, price, and token outcomes for a trader in a given market.
        :param address: Trader wallet address
        :param id: Market numeric ID
        :param limit: Max orders to return
        :param offset: Pagination offset
        """
        params = {}
        if limit is not None: params['limit'] = limit
        if offset is not None: params['offset'] = offset
        return self._client._request(self._client.api_base_url, 'GET', f"/v2/traders/{address}/markets/{id}/orders", json_body=None, params=params)

class AccountService:
    """Service client for Account operations."""
    def __init__(self, client: PolyEdgeClient):
        self._client = client

    def get_profile(self) -> Dict[str, Any]:
        """Get Current Profile
        Retrieves the authenticated user profile, tier subscription status, and available USDC balance.
        """
        return self._client._request(self._client.api_base_url, 'GET', f"/v2/user/me", json_body=None, params=None)

    def list_keys(self) -> Dict[str, Any]:
        """List API Keys
        Lists all active and revoked API keys issued to the authenticated account.
        """
        return self._client._request(self._client.api_base_url, 'GET', f"/v2/user/keys", json_body=None, params=None)

    def create_key(self, req: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create API Key
        Generates a new authenticated API key token with optional memo label.
        :param req: Request payload dictionary
        """
        return self._client._request(self._client.api_base_url, 'POST', f"/v2/user/keys", json_body=req, params=None)

    def update_key(self, key: str, req: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Update API Key
        Modifies label memo or operational status of an existing API key.
        :param key: API key string
        :param req: Request payload dictionary
        """
        return self._client._request(self._client.api_base_url, 'PATCH', f"/v2/user/keys/{key}", json_body=req, params=None)

    def delete_key(self, key: str) -> Dict[str, Any]:
        """Revoke API Key
        Permanently revokes and deactivates an API key token.
        :param key: API key string
        """
        return self._client._request(self._client.api_base_url, 'DELETE', f"/v2/user/keys/{key}", json_body=None, params=None)

    def get_ledger(self, limit: Optional[int] = None, offset: Optional[int] = None) -> Dict[str, Any]:
        """List User Balance Ledger
        Lists chronological ledger entries (subscription billing charges, deposits, withdrawals).
        :param limit: Max entries to return
        :param offset: Pagination offset
        """
        params = {}
        if limit is not None: params['limit'] = limit
        if offset is not None: params['offset'] = offset
        return self._client._request(self._client.api_base_url, 'GET', f"/v2/user/ledger", json_body=None, params=params)

    def get_telemetry(self) -> Dict[str, Any]:
        """Get Account Telemetry & Limits
        Provides live usage statistics, quota limits, and remaining streaming bandwidth.
        """
        return self._client._request(self._client.api_base_url, 'GET', f"/v2/user/telemetry", json_body=None, params=None)

    def withdraw(self, req: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Request Balance Withdrawal
        Submits a request to withdraw unspent USDC balance to a designated Polygon address.
        :param req: Request payload dictionary
        """
        return self._client._request(self._client.api_base_url, 'POST', f"/v2/user/withdraw", json_body=req, params=None)

class SubscriptionService:
    """Service client for Subscription operations."""
    def __init__(self, client: PolyEdgeClient):
        self._client = client

    def list_tiers(self) -> Dict[str, Any]:
        """List Public Tiers Catalog
        Returns plan tiers (Free, Starter, Pro, Growth, Whale) with limits and pricing details.
        """
        return self._client._request(self._client.api_base_url, 'GET', f"/v2/tiers", json_body=None, params=None)

    def get_quote(self, req: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get Subscription Quote
        Calculates prorated billing amounts for subscribing to or upgrading a tier plan.
        :param req: Request payload dictionary
        """
        return self._client._request(self._client.api_base_url, 'POST', f"/v2/user/subscribe/quote", json_body=req, params=None)

    def subscribe(self, req: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Purchase / Upgrade Tier Subscription
        Executes purchase, renewal, or upgrade of an active subscription tier plan.
        :param req: Request payload dictionary
        """
        return self._client._request(self._client.api_base_url, 'POST', f"/v2/user/subscribe", json_body=req, params=None)

    def validate_promo_code(self, req: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Validate Promo Code
        Verifies validity, discount percentage, and applicable plans for a promotion coupon code.
        :param req: Request payload dictionary
        """
        return self._client._request(self._client.api_base_url, 'POST', f"/v2/user/promo-codes/validate", json_body=req, params=None)

class PolyEdgeClient:
    """PolyEdge official API client."""
    def __init__(
        self,
        api_key: str,
        api_base_url: str = "https://api.polyedge.dev",
        stream_base_url: str = "https://stream.polyedge.dev",
    ):
        if not api_key: raise ValueError("api_key is required")
        self.api_key = api_key
        self.api_base_url = api_base_url.rstrip("/")
        self.stream_base_url = stream_base_url.rstrip("/")

        self.streams = StreamsService(self)
        self.analytics = AnalyticsService(self)
        self.account = AccountService(self)
        self.subscription = SubscriptionService(self)

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-PolyEdge-Key": self.api_key,
        }

    def _request(self, base_url: str, method: str, endpoint: str, json_body: Optional[Any] = None, params: Optional[Dict[str, Any]] = None) -> Any:
        with httpx.Client(base_url=base_url, headers=self._get_headers(), trust_env=False) as client:
            resp = client.request(method, endpoint, json=json_body, params=params)
            resp.raise_for_status()
            return resp.json()

    def stream(self, stream_id: str, heartbeat_timeout: float = 45.0) -> PolyEdgeStream:
        """Direct helper to connect to real-time SSE order stream."""
        return self.streams.connect(stream_id, heartbeat_timeout=heartbeat_timeout)
