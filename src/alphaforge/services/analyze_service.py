from alphaforge.services.company_service import get_company_profile
from alphaforge.services.financial_service import get_financial
from alphaforge.services.news_service import get_news
from alphaforge.services.price_summary_service import get_price_summary
from alphaforge.services.quote_service import get_quote
from alphaforge.services.technical_service import get_technical_summary
from alphaforge.services.knowledge_service import build_knowledge
from alphaforge.services.evidence_service import build_evidence
from alphaforge.services.reasoning_service import build_reasoning


class AnalyzeService:
    """
    Main orchestration service for AlphaForge analysis.

    This service coordinates every analysis component and returns
    a single structured result.

    Business logic should gradually move here instead of remaining
    inside CLI commands.
    """

    def run(self, ticker: str) -> dict:

        ticker = ticker.upper()

        company = get_company_profile(ticker)
        quote = get_quote(ticker)
        financial = get_financial(ticker)
        summary = get_price_summary(ticker)
        technical, analysis = get_technical_summary(ticker)
        news = get_news(ticker)
        knowledge = build_knowledge(financial)
        evidence = build_evidence(knowledge)
        reasoning = build_reasoning(evidence)

        return {
            "ticker": ticker,
            "company": company,
            "quote": quote,
            "financial": financial,
            "price_summary": summary,
            "technical": technical,
            "technical_analysis": analysis,
            "news": news,
            "knowledge": knowledge,
            "evidence": evidence,
            "reasoning": reasoning,
        }