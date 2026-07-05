from dataclasses import dataclass


@dataclass
class MovingAverage:
    period: int
    value: float


@dataclass
class TechnicalSummary:
    sma20: MovingAverage
    sma50: MovingAverage


@dataclass
class TechnicalAnalysis:
    trend: str

    confidence: int

    evidence: list[str]

    recommendation: str