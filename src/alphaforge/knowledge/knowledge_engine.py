from dataclasses import dataclass
from typing import List

from alphaforge.models.financial import FinancialSnapshot


@dataclass
class KnowledgeItem:
    category: str
    title: str
    description: str
    confidence: int


class KnowledgeEngine:

    def build(self, financial: FinancialSnapshot) -> List[KnowledgeItem]:

        items: List[KnowledgeItem] = []

        if financial.gross_margin is not None:
            if financial.gross_margin >= 60:
                items.append(
                    KnowledgeItem(
                        "Profitability",
                        "Excellent Gross Margin",
                        "Gross margin above 60% indicates exceptional pricing power.",
                        95,
                    )
                )
            elif financial.gross_margin >= 40:
                items.append(
                    KnowledgeItem(
                        "Profitability",
                        "Healthy Gross Margin",
                        "Gross margin supports long-term profitability.",
                        85,
                    )
                )

        if financial.roe is not None and financial.roe >= 20:
            items.append(
                KnowledgeItem(
                    "Management",
                    "High Return on Equity",
                    "The company generates outstanding shareholder returns.",
                    90,
                )
            )

        if (
            financial.cash is not None
            and financial.debt is not None
            and financial.cash > financial.debt
        ):
            items.append(
                KnowledgeItem(
                    "Financial Health",
                    "Strong Balance Sheet",
                    "Cash exceeds debt, giving the company strong financial flexibility.",
                    92,
                )
            )

        if (
            financial.pe is not None
            and financial.forward_pe is not None
            and financial.forward_pe < financial.pe
        ):
            items.append(
                KnowledgeItem(
                    "Valuation",
                    "Forward Valuation Improving",
                    "Forward PE is lower than current PE, indicating expected earnings growth.",
                    88,
                )
            )

        return items