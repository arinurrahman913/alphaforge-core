class KnowledgePackage:

    def __init__(
        self,
        ticker,
        company,
        sector,
        industry,
        market_cap,
        current_price,
    ):
        self.ticker = ticker
        self.company = company
        self.sector = sector
        self.industry = industry
        self.market_cap = market_cap
        self.current_price = current_price