from alphaforge.scoring.financial_engine import FinancialScoringEngine
from alphaforge.services.financial_service import get_financial


def score(ticker: str):

    ticker = ticker.upper()

    financial = get_financial(ticker)

    engine = FinancialScoringEngine()

    result = engine.score(financial)

    print("=" * 80)
    print("FINANCIAL SCORE")
    print("=" * 80)
    print()

    print(f"Score : {result.total}/{result.maximum}")
    print(f"Grade : {result.grade}")

    print()
    print("-" * 80)

    for item in result.items:

        print(item.name)
        print(f"Value  : {item.value}")
        print(f"Score  : +{item.score}")
        print(f"Reason : {item.reason}")
        print()

        print("-" * 80)