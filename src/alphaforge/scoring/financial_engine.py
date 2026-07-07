from alphaforge.models.financial import FinancialSnapshot

from alphaforge.scoring.models import (
    ScoreItem,
    ScoreResult,
)


class FinancialScoringEngine:

    MAXIMUM_SCORE = 40

    def score(
        self,
        financial: FinancialSnapshot,
    ) -> ScoreResult:

        result = ScoreResult(
            name="Financial",
            maximum=self.MAXIMUM_SCORE,
            total=0,
            grade="",
        )

        #
        # ROE
        #

        if financial.roe is not None:

            if financial.roe >= 20:

                result.total += 10

                result.items.append(

                    ScoreItem(

                        name="Return on Equity",

                        value=f"{financial.roe:.2f}%",

                        score=10,

                        category="Profitability",

                        reason=(
                            "ROE above 20% indicates outstanding "
                            "capital efficiency."
                        ),

                    )

                )

            elif financial.roe >= 15:

                result.total += 8

                result.items.append(

                    ScoreItem(

                        name="Return on Equity",

                        value=f"{financial.roe:.2f}%",

                        score=8,

                        category="Profitability",

                        reason=(
                            "ROE indicates healthy profitability."
                        ),

                    )

                )

        #
        # Gross Margin
        #

        if financial.gross_margin is not None:

            if financial.gross_margin >= 60:

                result.total += 10

                result.items.append(

                    ScoreItem(

                        name="Gross Margin",

                        value=f"{financial.gross_margin:.2f}%",

                        score=10,

                        category="Profitability",

                        reason=(
                            "Excellent pricing power."
                        ),

                    )

                )

        #
        # Cash vs Debt
        #

        if (
            financial.cash is not None
            and financial.debt is not None
        ):

            if financial.cash > financial.debt:

                result.total += 10

                result.items.append(

                    ScoreItem(

                        name="Balance Sheet",

                        value="Cash > Debt",

                        score=10,

                        category="Financial Health",

                        reason=(
                            "Strong balance sheet with net cash."
                        ),

                    )

                )

            else:

                result.items.append(

                    ScoreItem(

                        name="Balance Sheet",

                        value="Debt > Cash",

                        score=0,

                        category="Financial Health",

                        reason=(
                            "Debt exceeds cash."
                        ),

                    )

                )

        #
        # Free Cash Flow
        #

        if (
            financial.free_cash_flow is not None
            and financial.free_cash_flow > 0
        ):

            result.total += 10

            result.items.append(

                ScoreItem(

                    name="Free Cash Flow",

                    value="Positive",

                    score=10,

                    category="Cash Flow",

                    reason=(
                        "Business generates positive free cash flow."
                    ),

                )

            )

        #
        # Grade
        #

        if result.total >= 36:
            result.grade = "Excellent"

        elif result.total >= 30:
            result.grade = "Very Good"

        elif result.total >= 24:
            result.grade = "Good"

        elif result.total >= 16:
            result.grade = "Average"

        else:
            result.grade = "Weak"

        return result