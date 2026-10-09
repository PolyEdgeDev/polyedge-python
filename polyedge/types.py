from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Literal, Dict, Any

Side = Literal["BUY", "SELL"]
TokenIndex = Literal[0, 1]

@dataclass
class ActiveSessionInfo:
    """Data model for ActiveSessionInfo"""
    api_key: Optional[str] = None
    client_ip: Optional[str] = None
    connected_at: Optional[str] = None
    duration_seconds: Optional[int] = None
    pushed_tx_count: Optional[int] = None
    stream_id: Optional[str] = None
    user_agent: Optional[str] = None

@dataclass
class CreateAPIKeyRequest:
    """Data model for CreateAPIKeyRequest"""
    key: Optional[str] = None
    name: Optional[str] = None

@dataclass
class DeleteKeyResponse:
    """Data model for DeleteKeyResponse"""
    id: Optional[str] = None

@dataclass
class DeleteStreamResponse:
    """Data model for DeleteStreamResponse"""
    id: Optional[str] = None

@dataclass
class DepositItem:
    """Data model for DepositItem"""
    address: Optional[str] = None
    deposit_count: Optional[int] = None
    first_deposit_at: Optional[str] = None
    first_trade_at: Optional[str] = None
    last_deposit_at: Optional[str] = None
    last_trade_at: Optional[str] = None
    total_deposit: Optional[str] = None

@dataclass
class DepositQueryResult:
    """Data model for DepositQueryResult"""
    items: Optional[List[DepositItem]] = None
    total: Optional[int] = None
    updated_at: Optional[str] = None

@dataclass
class ErrorResponse:
    """Data model for ErrorResponse"""
    error: Optional[str] = None
    message: Optional[str] = None

@dataclass
class HistoryMarket:
    """Data model for HistoryMarket"""
    icon: Optional[str] = None
    id: Optional[int] = None
    outcomes: Optional[Tuple[str, str]] = None
    question: Optional[str] = None
    resolved_at: Optional[str] = None
    result: Optional[int] = None
    series_slug: Optional[str] = None
    slug: Optional[str] = None

@dataclass
class HourlyStat:
    """Data model for HourlyStat"""
    cost_basis: Optional[int] = None
    fee: Optional[int] = None
    hour: Optional[str] = None
    maker_volume: Optional[int] = None
    market_count: Optional[int] = None
    pnl: Optional[int] = None
    taker_volume: Optional[int] = None
    win_count: Optional[int] = None

@dataclass
class LeaderboardResponse:
    """Data model for LeaderboardResponse"""
    total_count: Optional[int] = None
    traders: Optional[List[TraderSummary]] = None

@dataclass
class LiveOrder:
    """Data model for LiveOrder"""
    fee: Optional[str] = None
    order: Optional[OrderInfo] = None
    outcome: Optional[str] = None
    shares: Optional[str] = None
    side: Optional[Side] = None
    token_ids_index: Optional[TokenIndex] = None
    usdc: Optional[str] = None
    user: Optional[MonitorTrader] = None

@dataclass
class LiveTransaction:
    """Data model for LiveTransaction"""
    makers: Optional[List[LiveOrder]] = None
    market: Optional[Market] = None
    taker: Optional[LiveOrder] = None
    timestamp: Optional[str] = None
    tx_hash: Optional[str] = None

@dataclass
class Market:
    """Data model for Market"""
    condition_id: Optional[str] = None
    event_slug: Optional[str] = None
    group_item_title: Optional[str] = None
    id: Optional[int] = None
    neg_risk: Optional[bool] = None
    outcomes: Optional[Tuple[str, str]] = None
    question: Optional[str] = None
    series_slug: Optional[str] = None
    slug: Optional[str] = None
    sports_market_type: Optional[str] = None
    start_date: Optional[str] = None
    tags_slug: Optional[List[str]] = None
    token_ids: Optional[Tuple[str, str]] = None

@dataclass
class MarketDetailResponse:
    """Data model for MarketDetailResponse"""
    market: Optional[MarketMetadata] = None
    top_earners: Optional[List[MarketEarner]] = None
    total_fees: Optional[int] = None
    total_pnl_distributed: Optional[int] = None
    total_traders: Optional[int] = None
    total_volume: Optional[int] = None
    total_winners: Optional[int] = None

@dataclass
class MarketEarner:
    """Data model for MarketEarner"""
    orders: Optional[List[UserOrder]] = None
    pnl: Optional[int] = None
    profile: Optional[TraderIdentity] = None
    rank: Optional[int] = None
    roi: Optional[float] = None
    volume: Optional[int] = None

@dataclass
class MarketMetadata:
    """Data model for MarketMetadata"""
    condition_id: Optional[str] = None
    created_at: Optional[str] = None
    description: Optional[str] = None
    end_date: Optional[str] = None
    event_slug: Optional[str] = None
    fee_schedule: Optional[Dict[str, Any]] = None
    fee_type: Optional[str] = None
    fees_enabled: Optional[bool] = None
    group_item_threshold: Optional[int] = None
    group_item_title: Optional[str] = None
    icon: Optional[str] = None
    id: Optional[int] = None
    neg_risk: Optional[bool] = None
    outcomes: Optional[Tuple[str, str]] = None
    question: Optional[str] = None
    resolution_source: Optional[str] = None
    resolved_at: Optional[str] = None
    result: Optional[int] = None
    series_slug: Optional[str] = None
    slug: Optional[str] = None
    sports_market_type: Optional[str] = None
    start_date: Optional[str] = None
    tags_slug: Optional[List[str]] = None
    token_ids: Optional[Tuple[str, str]] = None

@dataclass
class MarketSettlementDetail:
    """Data model for MarketSettlementDetail"""
    last_trade_at: Optional[str] = None
    market: Optional[HistoryMarket] = None
    orders: Optional[List[UserOrder]] = None
    pnl: Optional[int] = None
    roi: Optional[float] = None
    volume: Optional[int] = None

@dataclass
class MonitorTrader:
    """Data model for MonitorTrader"""
    address: Optional[str] = None
    name: Optional[str] = None

@dataclass
class OrderInfo:
    """Data model for OrderInfo"""
    order_hash: Optional[str] = None
    shares: Optional[str] = None
    signature_type: Optional[int] = None
    timestamp: Optional[str] = None
    usdc: Optional[str] = None

@dataclass
class QuoteSubscriptionRequest:
    """Data model for QuoteSubscriptionRequest"""
    billing_cycle: Optional[str] = None
    promo_code: Optional[str] = None
    tier: Optional[str] = None

@dataclass
class QuoteSubscriptionResponse:
    """Data model for QuoteSubscriptionResponse"""
    amount_to_pay: Optional[int] = None
    billing_cycle: Optional[str] = None
    can_afford: Optional[bool] = None
    current_balance: Optional[int] = None
    current_billing_cycle: Optional[str] = None
    current_license: Optional[str] = None
    current_tier: Optional[str] = None
    discount_amount: Optional[int] = None
    duration_days: Optional[int] = None
    is_active: Optional[bool] = None
    license: Optional[str] = None
    message: Optional[str] = None
    original_price: Optional[int] = None
    prorated_credit: Optional[int] = None
    tier: Optional[str] = None

@dataclass
class SubscribeRequest:
    """Data model for SubscribeRequest"""
    billing_cycle: Optional[str] = None
    idempotency_key: Optional[str] = None
    promo_code: Optional[str] = None
    tier: Optional[str] = None

@dataclass
class SubscribeResponse:
    """Data model for SubscribeResponse"""
    subscription: Optional[UserSubscription] = None
    user: Optional[UserProfile] = None

@dataclass
class TagStat:
    """Data model for TagStat"""
    maker_volume: Optional[int] = None
    markets_count: Optional[int] = None
    pnl: Optional[int] = None
    roi: Optional[float] = None
    slug: Optional[str] = None
    taker_volume: Optional[int] = None
    volume: Optional[int] = None
    win_rate: Optional[float] = None
    wins_count: Optional[int] = None

@dataclass
class Tier:
    """Data model for Tier"""
    allow_rest_api: Optional[bool] = None
    allow_stream: Optional[bool] = None
    allow_trial: Optional[bool] = None
    created_at: Optional[str] = None
    id: Optional[str] = None
    level: Optional[int] = None
    license: Optional[str] = None
    max_daily_requests: Optional[int] = None
    max_daily_stream_seconds: Optional[int] = None
    max_filter_addrs: Optional[int] = None
    max_filter_series: Optional[int] = None
    max_filter_tags: Optional[int] = None
    max_keys: Optional[int] = None
    max_naked_streams: Optional[int] = None
    max_qps: Optional[int] = None
    max_sessions: Optional[int] = None
    max_streams: Optional[int] = None
    monthly_credits: Optional[int] = None
    name: Optional[str] = None
    price_monthly: Optional[int] = None
    price_quarterly: Optional[int] = None
    price_trial: Optional[int] = None
    price_yearly: Optional[int] = None
    trial_duration_days: Optional[int] = None
    updated_at: Optional[str] = None

@dataclass
class TraderHistoryResponse:
    """Data model for TraderHistoryResponse"""
    history: Optional[List[MarketSettlementDetail]] = None
    total_count: Optional[int] = None

@dataclass
class TraderHourlyStatsResponse:
    """Data model for TraderHourlyStatsResponse"""
    stats: Optional[List[HourlyStat]] = None

@dataclass
class TraderIdentity:
    """Data model for TraderIdentity"""
    address: Optional[str] = None
    name: Optional[str] = None
    profile_created_at: Optional[str] = None
    profile_image: Optional[str] = None
    x_username: Optional[str] = None

@dataclass
class TraderProfileResponse:
    """Data model for TraderProfileResponse"""
    last_trade_at: Optional[str] = None
    profile: Optional[TraderIdentity] = None
    pusd_balance: Optional[int] = None
    taker_tier: Optional[int] = None
    taker_tier_name: Optional[str] = None
    top_tags: Optional[List[TagStat]] = None
    weighted_volume: Optional[float] = None

@dataclass
class TraderSummary:
    """Data model for TraderSummary"""
    last_trade_at: Optional[str] = None
    markets_count: Optional[int] = None
    profile: Optional[TraderIdentity] = None
    rank: Optional[int] = None
    roi: Optional[float] = None
    total_pnl: Optional[int] = None
    total_volume: Optional[int] = None
    win_rate: Optional[float] = None
    wins_count: Optional[int] = None

@dataclass
class UpdateSubscriptionRequest:
    """Data model for UpdateSubscriptionRequest"""
    addresses: Optional[List[str]] = None
    series: Optional[List[str]] = None
    tags: Optional[List[str]] = None

@dataclass
class UserAPIKey:
    """Data model for UserAPIKey"""
    created_at: Optional[str] = None
    key: Optional[str] = None
    name: Optional[str] = None
    status: Optional[int] = None

@dataclass
class UserActiveSessionsResponse:
    """Data model for UserActiveSessionsResponse"""
    data: Optional[List[ActiveSessionInfo]] = None
    total_count: Optional[int] = None

@dataclass
class UserCreateStreamRequest:
    """Data model for UserCreateStreamRequest"""
    addresses: Optional[List[str]] = None
    name: Optional[str] = None
    series: Optional[List[str]] = None
    tags: Optional[List[str]] = None

@dataclass
class UserKeysResponse:
    """Data model for UserKeysResponse"""
    data: Optional[List[UserAPIKey]] = None
    total_count: Optional[int] = None

@dataclass
class UserLedgerEntry:
    """Data model for UserLedgerEntry"""
    amount: Optional[int] = None
    balance_after: Optional[int] = None
    created_at: Optional[str] = None
    reference_id: Optional[str] = None
    type: Optional[str] = None

@dataclass
class UserLedgerResponse:
    """Data model for UserLedgerResponse"""
    data: Optional[List[UserLedgerEntry]] = None
    total_count: Optional[int] = None

@dataclass
class UserOrder:
    """Data model for UserOrder"""
    fee: Optional[int] = None
    is_taker: Optional[bool] = None
    outcome: Optional[str] = None
    shares: Optional[int] = None
    side: Optional[Side] = None
    time: Optional[str] = None
    usdc: Optional[int] = None

@dataclass
class UserOrdersResponse:
    """Data model for UserOrdersResponse"""
    orders: Optional[List[UserOrder]] = None

@dataclass
class UserProfile:
    """Data model for UserProfile"""
    billing_cycle: Optional[str] = None
    created_at: Optional[str] = None
    deposit_address: Optional[str] = None
    deposit_balance: Optional[int] = None
    email: Optional[str] = None
    is_expired: Optional[bool] = None
    status: Optional[int] = None
    telegram_id: Optional[int] = None
    tier: Optional[str] = None
    tier_expires_at: Optional[str] = None
    updated_at: Optional[str] = None

@dataclass
class UserSessionHistoryResponse:
    """Data model for UserSessionHistoryResponse"""
    data: Optional[List[UserSessionRecord]] = None
    total_count: Optional[int] = None

@dataclass
class UserSessionRecord:
    """Data model for UserSessionRecord"""
    api_key: Optional[str] = None
    client_ip: Optional[str] = None
    close_reason: Optional[str] = None
    connected_at: Optional[str] = None
    disconnected_at: Optional[str] = None
    duration_seconds: Optional[int] = None
    pushed_tx_count: Optional[int] = None
    stream_id: Optional[str] = None
    user_agent: Optional[str] = None

@dataclass
class UserStreamResponse:
    """Data model for UserStreamResponse"""
    active_sessions: Optional[int] = None
    addresses: Optional[List[str]] = None
    created_at: Optional[str] = None
    enabled: Optional[bool] = None
    id: Optional[str] = None
    name: Optional[str] = None
    series: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    updated_at: Optional[str] = None

@dataclass
class UserStreamsResponse:
    """Data model for UserStreamsResponse"""
    data: Optional[List[UserStreamResponse]] = None
    total_count: Optional[int] = None

@dataclass
class UserSubscription:
    """Data model for UserSubscription"""
    amount_paid: Optional[int] = None
    billing_cycle: Optional[str] = None
    created_at: Optional[str] = None
    discount_amount: Optional[int] = None
    duration_days: Optional[int] = None
    expires_at: Optional[str] = None
    original_price: Optional[int] = None
    plan_tier: Optional[str] = None
    promo_code: Optional[str] = None
    prorated_credit: Optional[int] = None
    starts_at: Optional[str] = None
    status: Optional[str] = None

@dataclass
class UserTelemetryResponse:
    """Data model for UserTelemetryResponse"""
    date: Optional[str] = None
    endpoints: Optional[Dict[str, Any]] = None
    total_requests: Optional[int] = None

@dataclass
class UserUpdateKeyRequest:
    """Data model for UserUpdateKeyRequest"""
    name: Optional[str] = None
    status: Optional[int] = None

@dataclass
class UserUpdateStreamMetadataRequest:
    """Data model for UserUpdateStreamMetadataRequest"""
    enabled: Optional[bool] = None
    name: Optional[str] = None

@dataclass
class UserWithdrawRequest:
    """Data model for UserWithdrawRequest"""
    network: str
    to_address: str
    token: str

@dataclass
class UserWithdrawResponse:
    """Data model for UserWithdrawResponse"""
    user: Optional[UserProfile] = None
    withdrawal: Optional[Withdrawal] = None

@dataclass
class ValidatePromoCodeRequest:
    """Data model for ValidatePromoCodeRequest"""
    billing_cycle: Optional[str] = None
    code: Optional[str] = None
    tier: Optional[str] = None

@dataclass
class ValidatePromoCodeResponse:
    """Data model for ValidatePromoCodeResponse"""
    amount_to_pay: Optional[int] = None
    code: Optional[str] = None
    discount_amount: Optional[int] = None
    message: Optional[str] = None
    original_price: Optional[int] = None
    prorated_credit: Optional[int] = None
    valid: Optional[bool] = None

@dataclass
class Withdrawal:
    """Data model for Withdrawal"""
    amount: Optional[int] = None
    created_at: Optional[str] = None
    id: Optional[int] = None
    last_deposit_at: Optional[str] = None
    network: Optional[str] = None
    reject_reason: Optional[str] = None
    reviewed_at: Optional[str] = None
    status: Optional[str] = None
    to_address: Optional[str] = None
    token: Optional[str] = None
    tx_hash: Optional[str] = None
    updated_at: Optional[str] = None
    user_email: Optional[str] = None
    user_id: Optional[int] = None
