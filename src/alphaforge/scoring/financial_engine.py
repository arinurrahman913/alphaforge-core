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

        self._evaluate_roe(result, financial)
        self._evaluate_gross_margin(result, financial)
        self._evaluate_balance_sheet(result, financial)
        self._evaluate_free_cash_flow(result, financial)
        self._calculate_grade(result)

        return result

    def _evaluate_roe(self, result: ScoreResult, financial: FinancialSnapshot):

        if financial.roe is None:
            return

        score = 0
        reason = "ROE below preferred threshold."

        if financial.roe >= 20:
            score = 10
            reason = "ROE above 20% indicates outstanding capital efficiency."
        elif financial.roe >= 15:
            score = 8
            reason = "ROE indicates healthy profitability."

        result.total += score

        if score > 0:
            result.items.append(
                ScoreItem(
                    name="Return on Equity",
                    value=f"{financial.roe:.2f}%",
                    score=score,
                    category="Profitability",
                    reason=reason,
                )
            )

    def _evaluate_gross_margin(self, result: ScoreResult, financial: FinancialSnapshot):

        if financial.gross_margin is None:
            return

        if financial.gross_margin >= 60:
            result.total += 10
            result.items.append(
                ScoreItem(
                    name="Gross Margin",
                    value=f"{financial.gross_margin:.2f}%",
                    score=10,
                    category="Profitability",
                    reason="Excellent pricing power.",
                )
            )

    def _evaluate_balance_sheet(self, result: ScoreResult, financial: FinancialSnapshot):

        if financial.cash is None or financial.debt is None:
            return

        if financial.cash > financial.debt:
            result.total += 10
            score = 10
            value = "Cash > Debt"
            reason = "Strong balance sheet with net cash."
        else:
            score = 0
            value = "Debt > Cash"
            reason = "Debt exceeds cash."

        result.items.append(
            ScoreItem(
                name="Balance Sheet",
                value=value,
                score=score,
                category="Financial Health",
                reason=reason,
            )
        )

    def _evaluate_free_cash_flow(self, result: ScoreResult, financial: FinancialSnapshot):

        if financial.free_cash_flow is None:
            return

        if financial.free_cash_flow > 0:
            result.total += 10
            result.items.append(
                ScoreItem(
                    name="Free Cash Flow",
                    value="Positive",
                    score=10,
                    category="Cash Flow",
                    reason="Business generates positive free cash flow.",
                )
            )

    def _calculate_grade(self, result: ScoreResult):

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
