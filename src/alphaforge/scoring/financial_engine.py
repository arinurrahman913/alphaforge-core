from alphaforge.models.financial import FinancialSnapshot

from alphaforge.scoring.models import (
    ScoreItem,
    ScoreResult,
)


class FinancialScoringEngine:

    # Poin maksimal yang benar-benar achievable dari semua kriteria di bawah:
    # ROE (10) + Gross Margin (15) + Balance Sheet (10) + Free Cash Flow (10) = 45
    MAXIMUM_SCORE = 45

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

        roe = financial.roe * 100 if financial.roe is not None and financial.roe <= 1 else financial.roe

        if roe >= 20:
            score = 10
            reason = "ROE above 20% indicates outstanding capital efficiency."
        elif roe >= 15:
            score = 8
            reason = "ROE indicates healthy profitability."

        result.total += score

        if score > 0:
            result.items.append(
                ScoreItem(
                    name="Return on Equity",
                    value=f"{roe:.2f}%",
                    score=score,
                    category="Profitability",
                    reason=reason,
                )
            )

    def _evaluate_gross_margin(self, result: ScoreResult, financial: FinancialSnapshot):

        if financial.gross_margin is None:
            return

        margin = financial.gross_margin * 100 if financial.gross_margin is not None and financial.gross_margin <= 1 else financial.gross_margin

        if margin >= 60:
            result.total += 15
            result.items.append(
                ScoreItem(
                    name="Gross Margin",
                    value=f"{margin:.2f}%",
                    score=15,
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

        percent = (result.total / result.maximum) * 100

        if percent >= 90:
            result.grade = 'S'
        elif percent >= 80:
            result.grade = 'A'
        elif percent >= 70:
            result.grade = 'B'
        elif percent >= 60:
            result.grade = 'C'
        elif percent >= 40:
            result.grade = 'D'
        else:
            result.grade = 'F'
