from alphaforge.foundation.formatter import (
    format_money,
    format_number,
    format_percent,
)

from alphaforge.services.company_service import get_company_profile
from alphaforge.services.financial_service import get_financial
from alphaforge.services.news_service import get_news
from alphaforge.services.price_summary_service import get_price_summary
from alphaforge.services.quote_service import get_quote


def analyze(ticker: str):

    ticker = ticker.upper()

    company = get_company_profile(ticker)
    quote = get_quote(ticker)
    financial = get_financial(ticker)
    summary = get_price_summary(ticker)
    news = get_news(ticker)

    print("=" * 80)
    print("AlphaForge Core v0.1.0".center(80))
    print("=" * 80)
    print()

    print("Investment Intelligence Operating System")
    print()

    print(f"Ticker  : {ticker}")
    print(f"Company : {company.name}")

    print()

    print("=" * 80)
    print("QUOTE")
    print("=" * 80)

    print(f"Current Price  : {format_money(quote.current_price)}")
    print(f"Previous Close : {format_money(quote.previous_close)}")
    print(f"Change         : {format_money(quote.change)} ({format_percent(quote.change_percent)})")

    print()

    print("=" * 80)
    print("COMPANY PROFILE")
    print("=" * 80)

    print(f"Sector   : {company.sector}")
    print(f"Industry : {company.industry}")
    print(f"Country  : {company.country}")

    print()

    print("=" * 80)
    print("FINANCIAL SNAPSHOT")
    print("=" * 80)

    print(f"Market Cap       : {format_money(financial.market_cap)}")
    print(f"Revenue          : {format_money(financial.revenue)}")
    print(f"Net Income       : {format_money(financial.net_income)}")
    print(f"EPS              : {format_number(financial.eps)}")
    print(f"PE               : {format_number(financial.pe)}")
    print(f"Forward PE       : {format_number(financial.forward_pe)}")
    print(f"ROE              : {format_percent(financial.roe)}")
    print(f"Gross Margin     : {format_percent(financial.gross_margin)}")
    print(f"Operating Margin : {format_percent(financial.operating_margin)}")
    print(f"Cash             : {format_money(financial.cash)}")
    print(f"Debt             : {format_money(financial.debt)}")
    print(f"Free Cash Flow   : {format_money(financial.free_cash_flow)}")

    print()

    print("=" * 80)
    print("PRICE SUMMARY")
    print("=" * 80)

    print(f"Current Price  : {format_money(summary.current_price)}")
    print(f"6M Return      : {format_percent(summary.total_return)}")
    print(f"Highest Price  : {format_money(summary.highest_price)}")
    print(f"Lowest Price   : {format_money(summary.lowest_price)}")
    print(f"Average Volume : {summary.average_volume:,.0f}")

    print()

    print("=" * 80)
    print("LATEST NEWS")
    print("=" * 80)

    if not news:
        print("No news available.")

    else:

        for i, article in enumerate(news[:5], start=1):

            print(f"{i}. {article.title}")
            print(f"   {article.publisher}")
            print()