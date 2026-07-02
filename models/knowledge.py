from dataclasses import dataclass

from enums.company_category import CompanyCategory


@dataclass
class Knowledge:

    ticker: str
    company: str

    exchange: str

    sector: str
    industry: str

    category: CompanyCategory

    def summary(self):

        return (
            "========== KNOWLEDGE ==========\n"
            f"Company     : {self.company}\n"
            f"Ticker      : {self.ticker}\n"
            f"Exchange    : {self.exchange}\n"
            f"Sector      : {self.sector}\n"
            f"Industry    : {self.industry}\n"
            f"Category    : {self.category.value}\n"
        )

    def __str__(self):
        return self.summary()