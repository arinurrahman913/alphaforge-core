from __future__ import annotations

from time import perf_counter

from alphaforge.services.company_service import get_company_profile
from alphaforge.services.financial_service import get_financial
from alphaforge.services.news_service import get_news
from alphaforge.services.price_summary_service import get_price_summary
from alphaforge.services.quote_service import get_quote
from alphaforge.services.technical_service import get_technical_summary

from alphaforge.services.knowledge_service import build_knowledge
from alphaforge.services.evidence_service import build_evidence
from alphaforge.services.reasoning_service import build_reasoning


class AnalysisEngine:
    """
    AlphaForge Analysis Engine

    Central orchestration layer.

    Sprint 004A
    - Error isolation
    - Stage timing
    - Metadata collection
    - Backward compatible output
    """

    def __init__(self):

        self.metadata = {}

    def run(self, ticker: str) -> dict:

        ticker = ticker.upper()

        company = self._safe_execute(
            "company",
            lambda: get_company_profile(ticker),
        )

        quote = self._safe_execute(
            "quote",
            lambda: get_quote(ticker),
        )

        financial = self._safe_execute(
            "financial",
            lambda: get_financial(ticker),
        )

        summary = self._safe_execute(
            "price_summary",
            lambda: get_price_summary(ticker),
        )

        technical = None
        technical_analysis = None

        technical_result = self._safe_execute(
            "technical",
            lambda: get_technical_summary(ticker),
        )

        if technical_result is not None:
            technical, technical_analysis = technical_result

        news = self._safe_execute(
            "news",
            lambda: get_news(ticker),
        )

        knowledge = None

        if financial is not None:
            knowledge = self._safe_execute(
                "knowledge",
                lambda: build_knowledge(financial),
            )

        evidence = None

        if knowledge is not None:
            evidence = self._safe_execute(
                "evidence",
                lambda: build_evidence(knowledge),
            )

        reasoning = None

        if evidence is not None:
            reasoning = self._safe_execute(
                "reasoning",
                lambda: build_reasoning(evidence),
            )

        return {
            "ticker": ticker,
            "company": company,
            "quote": quote,
            "financial": financial,
            "price_summary": summary,
            "technical": technical,
            "technical_analysis": technical_analysis,
            "news": news,
            "knowledge": knowledge,
            "evidence": evidence,
            "reasoning": reasoning,
            "metadata": self.metadata,
        }

    def _safe_execute(self, stage: str, func):

        started = perf_counter()

        try:

            result = func()

            self.metadata[stage] = {
                "status": "success",
                "duration": round(perf_counter() - started, 3),
            }

            return result

        except Exception as ex:

            self.metadata[stage] = {
                "status": "failed",
                "duration": round(perf_counter() - started, 3),
                "error": str(ex),
            }

            return None