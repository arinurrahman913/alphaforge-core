from connectors.yahoo_finance import YahooFinanceConnector


def main():

    print("=" * 50)
    print(" AlphaForge Investment Intelligence OS")
    print(" Prototype v0.2")
    print("=" * 50)

    print()
    print("Connecting to Yahoo Finance...")
    print()

    connector = YahooFinanceConnector()

    company = connector.get_company("MSFT")

    print("Company    :", company["company"])
    print("Ticker     :", company["ticker"])
    print("Sector     :", company["sector"])
    print("Industry   :", company["industry"])
    print("Price      :", company["current_price"])
    print("Market Cap :", company["market_cap"])

    print()
    print("Knowledge Package Created.")


if __name__ == "__main__":
    main()