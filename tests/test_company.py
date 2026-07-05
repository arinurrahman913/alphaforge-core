from alphaforge.services.company_service import get_company_profile

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
print("AlphaForge Company Profile Test")
print("=" * 80)

for ticker in tickers:
    try:
        company = get_company_profile(ticker)

        print(f"\n[{ticker}]")
        print(f"Name     : {company.name}")
        print(f"Sector   : {company.sector}")
        print(f"Industry : {company.industry}")
        print(f"Country  : {company.country}")

    except Exception as e:
        print(f"\n[{ticker}] FAILED")
        print(e)