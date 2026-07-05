from alphaforge.services.news_service import get_news

tickers = [
    "RKLB",
    "ASTS",
    "PLTR",
    "NVDA",
    "TSLA",
    "AAPL",
    "META",
    "MSFT",
    "GOOGL",
    "AMZN",
    "TSM",
    "ASML",
    "FSLR",
    "ENPH",
    "NBIS",
    "BMRI.JK",
    "BBRI.JK",
    "PTBA.JK",
    "ADRO.JK",
    "PGAS.JK",
]

print("=" * 80)
print("AlphaForge News Test")
print("=" * 80)

for ticker in tickers:

    print(f"\n{'=' * 80}")
    print(f"{ticker}")
    print("=" * 80)

    try:

        news = get_news(ticker)

        if not news:
            print("No news found.")
            continue

        for i, article in enumerate(news[:5], start=1):
            print(f"{i}. {article.title}")
            print(f"   Publisher : {article.publisher}")

    except Exception as e:
        print(f"FAILED : {e}")