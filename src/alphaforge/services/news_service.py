from alphaforge.providers.yahoo_finance import get_latest_news


def get_news(ticker: str):

    return get_latest_news(ticker)