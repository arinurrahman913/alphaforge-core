from dataclasses import dataclass, field
from typing import Any


@dataclass
class AnalysisContext:
    """
    Internal object used by AnalysisEngine.

    Sprint 004A:
    This class is internal only.
    External API still returns dict.
    """

    ticker: str

    company: Any = None
    quote: Any = None
    financial: Any = None

    price_summary: Any = None

    technical: Any = None
    technical_analysis: Any = None

    news: Any = None

    knowledge: Any = None
    evidence: Any = None
    reasoning: Any = None

    metadata: dict = field(default_factory=dict)

    def to_dict(self):

        return {
            "ticker": self.ticker,
            "company": self.company,
            "quote": self.quote,
            "financial": self.financial,
            "price_summary": self.price_summary,
            "technical": self.technical,
            "technical_analysis": self.technical_analysis,
            "news": self.news,
            "knowledge": self.knowledge,
            "evidence": self.evidence,
            "reasoning": self.reasoning,
            "metadata": self.metadata,
        }