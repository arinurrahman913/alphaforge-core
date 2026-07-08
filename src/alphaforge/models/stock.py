from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from alphaforge.models.price import PriceBar


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
class PriceHistory:
    ticker: str
    bars: list[PriceBar] = field(default_factory=list)
