from dataclasses import dataclass, field


@dataclass
class FundHolding:
    """
    One position from a single 13F filing (one fund, one quarter).
    """

    issuer_name: str
    cusip: str

    shares: int
    value_usd: float

    put_call: str | None = None


@dataclass
class FundPosition:
    """
    A tracked fund's position in a specific company, compared against
    the previous quarter's filing.
    """

    fund_name: str
    fund_cik: str

    current_holding: FundHolding | None
    previous_holding: FundHolding | None

    change_type: str = "UNKNOWN"
    # One of: "NEW_POSITION", "INCREASED", "DECREASED", "UNCHANGED", "SOLD_OUT"

    change_percent: float | None = None

    filing_quarter: str = ""


@dataclass
class InstitutionalOwnership:
    """
    Aggregated institutional ownership summary for a single ticker,
    across all tracked funds.
    """

    ticker: str
    company_name: str

    positions: list[FundPosition] = field(default_factory=list)

    @property
    def total_funds_holding(self) -> int:
        return len(
            [
                p for p in self.positions
                if p.current_holding is not None
            ]
        )

    @property
    def new_positions_count(self) -> int:
        return len(
            [
                p for p in self.positions
                if p.change_type == "NEW_POSITION"
            ]
        )
