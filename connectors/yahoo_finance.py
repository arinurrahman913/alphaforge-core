import yfinance as yf


class YahooFinanceConnector:

    def get_company(self, ticker):

        stock = yf.Ticker(ticker)

        info = stock.info

        return {
            "ticker": ticker,
            "company": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "market_cap": info.get("marketCap"),
            "current_price": info.get("currentPrice"),
        }