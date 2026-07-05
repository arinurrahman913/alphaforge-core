import yfinance as yf

from alphaforge.models.company import Company
from alphaforge.models.news import NewsArticle


def get_company_profile(ticker: str) -> Company:
    """
    Fetch company profile from Yahoo Finance.
    """

    stock = yf.Ticker(ticker)
    info = stock.info

    return Company(
        ticker=ticker.upper(),
        name=(
            info.get("longName")
            or info.get("shortName")
            or info.get("displayName")
            or "Unknown"
        ),
        sector=info.get("sector", "-"),
        industry=info.get("industry", "-"),
        country=info.get("country", "-"),
    )


def get_latest_news(ticker: str) -> list[NewsArticle]:
    """
    Fetch latest news from Yahoo Finance.
    """

    stock = yf.Ticker(ticker)

    articles = []

    try:

        news = stock.news

        for item in news[:5]:

            content = item.get("content", {})

            provider = content.get("provider", {})

            click = content.get("clickThroughUrl") or {}

            articles.append(
                NewsArticle(
                    title=content.get("title", "No Title"),
                    publisher=provider.get("displayName", "Unknown"),
                    link=click.get("url", ""),
                )
            )

    except Exception as e:
        print(f"Failed to fetch news: {e}")

    return articles

if __name__ == "__main__":
    news = get_latest_news("RKLB")

    for article in news:
        print(article.title)
        print(article.publisher)
        print(article.link)
        print("-" * 50)