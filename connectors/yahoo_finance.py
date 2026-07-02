import yfinance as yf

from core.base_connector import BaseConnector
from models.company import Company


class YahooFinanceConnector(BaseConnector):

    def fetch(self, ticker):
        return self.get_company(ticker)

    def get_company(self, ticker):

        stock = yf.Ticker(ticker)
        info = stock.info

        return Company(
            ticker=ticker,
            name=info.get("longName"),
            exchange=info.get("exchange"),
            sector=info.get("sector"),
            industry=info.get("industry"),
            current_price=info.get("currentPrice"),
            market_cap=info.get("marketCap"),
        )