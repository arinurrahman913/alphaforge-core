from dataclasses import dataclass
from typing import List


@dataclass
class KnowledgeItem:
    category: str
    title: str
    description: str
    confidence: int


class KnowledgeEngine:

    def build(self, financial) -> List[KnowledgeItem]:

        knowledge = []

        #
        # Gross Margin
        #

        if financial.gross_margin is not None:

            if financial.gross_margin >= 60:

                knowledge.append(
                    KnowledgeItem(
                        category="Profitability",
                        title="Excellent Gross Margin",
                        description="Gross margin is above 60%, indicating exceptional pricing power.",
                        confidence=95,
                    )
                )

            elif financial.gross_margin >= 40:

                knowledge.append(
                    KnowledgeItem(
                        category="Profitability",
                        title="Healthy Gross Margin",
                        description="Gross margin supports strong profitability.",
                        confidence=85,
                    )
                )

        #
        # ROE
        #

        if financial.roe is not None:

            if financial.roe >= 20:

                knowledge.append(
                    KnowledgeItem(
                        category="Management",
                        title="High Return on Equity",
                        description="Company generates excellent shareholder returns.",
                        confidence=90,
                    )
                )

        #
        # Balance Sheet
        #

        if financial.cash is not None and financial.debt is not None:

            if financial.cash > financial.debt:

                knowledge.append(
                    KnowledgeItem(
                        category="Financial Health",
                        title="Strong Balance Sheet",
                        description="Cash exceeds debt, providing financial flexibility.",
                        confidence=92,
                    )
                )

        #
        # Forward PE
        #

        if (
            financial.pe is not None
            and financial.forward_pe is not None
            and financial.forward_pe < financial.pe
        ):

            knowledge.append(
                KnowledgeItem(
                    category="Valuation",
                    title="Forward Valuation Improving",
                    description="Forward PE is lower than current PE, suggesting earnings growth.",
                    confidence=88,
                )
            )

        return knowledge