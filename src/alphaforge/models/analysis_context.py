from dataclasses import dataclass, field
from typing import Any


@dataclass
class AnalysisContext:
    """
    Shared object passed through every analysis stage.

    Every service writes its result into this object so the
    entire pipeline has a single source of truth.
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