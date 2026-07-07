from dataclasses import dataclass, field


@dataclass
class ScoreItem:
    """
    One scoring result.

    Example:
        ROE +10
    """

    name: str

    value: str

    score: int

    reason: str

    category: str


@dataclass
class ScoreResult:

    name: str

    maximum: int

    total: int

    grade: str

    items: list[ScoreItem] = field(default_factory=list)