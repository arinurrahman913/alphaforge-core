from dataclasses import dataclass, field


@dataclass
class ScanResult:
    """
    Combined signal summary for one ticker in a scan run.
    """

    ticker: str
    company_name: str

    financial_grade: str | None
    financial_score: int | None
    financial_max: int | None

    market_cap: float | None = None
    cap_category: str = "-"

    technical_trend: str | None = None

    institutional_new_positions: int = 0
    institutional_increased: int = 0
    institutional_decreased: int = 0
    institutional_sold_out: int = 0
    institutional_held_by: int = 0

    composite_score: float = 0.0

    errors: list[str] = field(default_factory=list)

    @property
    def has_data(self) -> bool:
        return (
            self.financial_grade is not None
            or self.technical_trend is not None
            or self.institutional_held_by > 0
        )
