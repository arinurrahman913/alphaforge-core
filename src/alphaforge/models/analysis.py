from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Signal(str, Enum):
    STRONG_BUY = "STRONG BUY"
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"
    STRONG_SELL = "STRONG SELL"


@dataclass
class TechnicalIndicators:
    rsi_14: Optional[float] = None
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    trend: str = "NEUTRAL"


@dataclass
class AnalysisScore:
    technical: float = 0.0
    fundamental: float = 0.0
    overall: float = 0.0
    signal: Signal = Signal.HOLD
    summary: str = ""
    highlights: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)


@dataclass
class StockAnalysis:
    ticker: str
    company_name: str
    market: str
    quote: Optional[object] = None
    fundamentals: Optional[object] = None
    technicals: Optional[TechnicalIndicators] = None
    score: Optional[AnalysisScore] = None
