from alphaforge.services.company_service import get_company_profile
from alphaforge.services.financial_service import get_financial
from alphaforge.services.news_service import get_news
from alphaforge.services.price_summary_service import get_price_summary
from alphaforge.services.quote_service import get_quote
from alphaforge.services.technical_service import get_technical_summary

from alphaforge.services.knowledge_service import build_knowledge
from alphaforge.services.evidence_service import build_evidence
from alphaforge.services.reasoning_service import build_reasoning


class ServiceRegistry:
    """
    Central registry for all services used by AnalysisEngine.
    """

    company = staticmethod(get_company_profile)

    financial = staticmethod(get_financial)

    quote = staticmethod(get_quote)

    price = staticmethod(get_price_summary)

    technical = staticmethod(get_technical_summary)

    news = staticmethod(get_news)

    knowledge = staticmethod(build_knowledge)

    evidence = staticmethod(build_evidence)

    reasoning = staticmethod(build_reasoning)