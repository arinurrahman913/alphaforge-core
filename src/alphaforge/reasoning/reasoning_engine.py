from typing import List

from alphaforge.evidence.models import Evidence
from alphaforge.reasoning.models import Reasoning


class ReasoningEngine:

    def build(
        self,
        evidence: List[Evidence],
    ) -> List[Reasoning]:

        reasoning = []

        for item in evidence:

            if (
                item.category == "Financial"
                and item.conclusion == "Very Strong"
            ):

                reasoning.append(

                    Reasoning(

                        title="Financial Position",

                        summary=(
                            "The company has excellent profitability, "
                            "strong shareholder returns, and a healthy "
                            "balance sheet."
                        ),

                        confidence=94,

                        supporting_evidence=item.supporting_items,

                    )

                )

        return reasoning