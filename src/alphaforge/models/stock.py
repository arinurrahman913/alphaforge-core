from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class StockQuote:
    ticker: str
    price: float
    change: float
    change_percent: float
    volume: int
    market_cap: Optional[float]
    currency: str
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    previous_close: Optional[float] = None


@dataclass
class StockFundamentals:
    ticker: str
    pe_ratio: Optional[float] = None
    forward_pe: Optional[float] = None
    eps: Optional[float] = None
    dividend_yield: Optional[float] = None
    profit_margin: Optional[float] = None
    revenue_growth: Optional[float] = None
    debt_to_equity: Optional[float] = None
    roe: Optional[float] = None
    beta: Optional[float] = None


@dataclass
class PriceBar:
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int


@dataclass
class PriceHistory:
    ticker: str
    bars: list[PriceBar] = field(default_factory=list)
