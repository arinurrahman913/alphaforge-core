import yfinance as yf

from alphaforge.models.company import Company
from alphaforge.models.news import NewsArticle
from alphaforge.models.financial import FinancialSnapshot
from alphaforge.models.price import PriceBar
from alphaforge.models.quote import StockQuote


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

def get_financial_snapshot(ticker: str) -> FinancialSnapshot:
    """
    Fetch financial snapshot from Yahoo Finance.
    """

    stock = yf.Ticker(ticker)
    info = stock.info

    return FinancialSnapshot(
        ticker=ticker.upper(),

        market_cap=info.get("marketCap"),
        revenue=info.get("totalRevenue"),
        net_income=info.get("netIncomeToCommon"),

        eps=info.get("trailingEps"),

        pe=info.get("trailingPE"),
        forward_pe=info.get("forwardPE"),

        roe=info.get("returnOnEquity"),

        gross_margin=info.get("grossMargins"),
        operating_margin=info.get("operatingMargins"),

        cash=info.get("totalCash"),
        debt=info.get("totalDebt"),

        free_cash_flow=info.get("freeCashflow"),
    )

def get_price_history(
    ticker: str,
    period: str = "6mo",
) -> list[PriceBar]:

    stock = yf.Ticker(ticker)

    history = stock.history(period=period)

    prices = []

    for date, row in history.iterrows():

        prices.append(
            PriceBar(
                date=date,

                open=float(row["Open"]),
                high=float(row["High"]),
                low=float(row["Low"]),
                close=float(row["Close"]),

                volume=int(row["Volume"]),
            )
        )

    return prices

def get_stock_quote(ticker: str) -> StockQuote:

    stock = yf.Ticker(ticker)

    info = stock.fast_info

    current = float(info.get("lastPrice", 0))
    previous = float(info.get("previousClose", current))

    change = current - previous

    if previous != 0:
        change_percent = change / previous
    else:
        change_percent = 0

    market_state = "OPEN"

    return StockQuote(
        ticker=ticker.upper(),
        current_price=current,
        previous_close=previous,
        change=change,
        change_percent=change_percent,
        market_state=market_state,
    )