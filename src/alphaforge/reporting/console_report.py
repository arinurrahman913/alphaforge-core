from alphaforge.foundation.formatter import (
    format_money,
    format_number,
    format_percent,
)


class ConsoleReport:

    def render(self, result: dict):

        ticker = result["ticker"]
        company = result["company"]
        quote = result["quote"]
        financial = result["financial"]
        summary = result["price_summary"]
        technical = result["technical"]
        analysis = result["technical_analysis"]
        news = result["news"]
        financial_score = result.get("financial_score")

        print("=" * 80)
        print("AlphaForge Core v0.1.0".center(80))
        print("=" * 80)
        print()

        print("Investment Intelligence Operating System")
        print()

        print(f"Ticker  : {ticker}")
        print(f"Company : {company.name if company else '-'}")
        print()

        print("=" * 80)
        print("QUOTE")
        print("=" * 80)

        if quote is None:
            print("Quote data not available.")
        else:
            print(f"Current Price  : {format_money(quote.current_price)}")
            print(f"Previous Close : {format_money(quote.previous_close)}")
            print(f"Change         : {format_money(quote.change)} ({format_percent(quote.change_percent)})")
            print(f"Market State   : {quote.market_state}")
        print()

        print("=" * 80)
        print("COMPANY PROFILE")
        print("=" * 80)

        if company is None:
            print("Company profile not available.")
        else:
            print(f"Sector   : {company.sector}")
            print(f"Industry : {company.industry}")
            print(f"Country  : {company.country}")
        print()

        print("=" * 80)
        print("FINANCIAL SNAPSHOT")
        print("=" * 80)

        if financial is None:
            print("Financial data not available.")
        else:
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

        if financial_score is not None:
            print("=" * 80)
            print("FINANCIAL SCORE")
            print("=" * 80)
            print()
            print(f"Overall Score : {financial_score.total}/{financial_score.maximum}")
            print(f"Grade         : {financial_score.grade}")
            print()
            print("-" * 80)
            for item in financial_score.items:
                print(f"✓ {item.name}")
                print(f"Value  : {item.value}")
                print(f"Score  : +{item.score}")
                print(f"Reason : {item.reason}")
                print()
                print("-" * 80)
            print()

        print("=" * 80)
        print("PRICE SUMMARY")
        print("=" * 80)

        if summary is None:
            print("Price summary not available.")
        else:
            print(f"Current Price  : {format_money(summary.current_price)}")
            print(f"6M Return      : {format_percent(summary.total_return)}")
            print(f"Highest Price  : {format_money(summary.highest_price)}")
            print(f"Lowest Price   : {format_money(summary.lowest_price)}")
            print(f"Average Volume : {summary.average_volume:,.0f}")
        print()

        print("=" * 80)
        print("TECHNICAL ANALYSIS")
        print("=" * 80)
        print()

        if analysis is None or technical is None:
            print("Technical analysis not available.")
        else:
            print(f"Trend      : {analysis.trend}")
            print(f"Confidence : {analysis.confidence}%")
            print()
            print("Evidence")
            print("--------")
            for item in analysis.evidence:
                print(f"✓ {item}")
            print()
            print("Recommendation")
            print("--------------")
            print(analysis.recommendation)
            print()
            print("Indicators")
            print("----------")
            print(f"SMA20 : {format_money(technical.sma20.value)}")
            print(f"SMA50 : {format_money(technical.sma50.value)}")
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
