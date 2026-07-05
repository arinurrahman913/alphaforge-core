from alphaforge.services.company_service import get_company_profile

from alphaforge.services.news_service import get_news


def analyze(ticker: str) -> None:

    print()

    print(f"Analyzing {ticker.upper()}...")

    print()

    print("Fetching company profile...")

    company = get_company_profile(ticker)

    print()

    print(f"Company  : {company.name}")
    print(f"Sector   : {company.sector}")
    print(f"Industry : {company.industry}")
    print(f"Country  : {company.country}")

    print()
print("=" * 40)
print("Latest News")
print("=" * 40)

news = get_news(ticker)

for i, article in enumerate(news, start=1):
    print(f"{i}. {article.title}")
    print(f"   {article.publisher}")
    print()


    