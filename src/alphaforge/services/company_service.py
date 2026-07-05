from alphaforge.models.company import Company
from alphaforge.providers.yahoo_finance import get_company_profile as yahoo_profile


def get_company_profile(ticker: str) -> Company:
    """
    Return company profile.
    """

    return yahoo_profile(ticker)