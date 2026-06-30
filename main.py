from connectors.yahoo_finance import YahooFinanceConnector

connector = YahooFinanceConnector()

company = connector.get_company("NVDA")

print(company)
print(company.summary())