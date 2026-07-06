from typing import List

from alphaforge.evidence.models import Evidence
from alphaforge.knowledge.knowledge_engine import KnowledgeItem


class EvidenceEngine:

    def build(
        self,
        knowledge: List[KnowledgeItem],
    ) -> List[Evidence]:

        evidence = []

        financial = []

        for item in knowledge:

            if item.category in [
                "Profitability",
                "Financial Health",
                "Management",
            ]:

                financial.append(item.title)

        if len(financial) >= 3:

            evidence.append(

                Evidence(

                    category="Financial",

                    conclusion="Very Strong",

                    confidence=93,

                    supporting_items=financial,

                )

            )

        return evidence