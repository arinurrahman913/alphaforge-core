from core.base_engine import BaseEngine
from core.base_package import BasePackage

from enums.package_type import PackageType
from enums.company_category import CompanyCategory

from models.knowledge import Knowledge


class KnowledgeEngine(BaseEngine):

    def process(self, package: BasePackage) -> BasePackage:

        company = package.data

        market_cap = company.market_cap or 0

        if market_cap >= 200_000_000_000:
            category = CompanyCategory.MEGA_CAP

        elif market_cap >= 10_000_000_000:
            category = CompanyCategory.LARGE_CAP

        elif market_cap >= 2_000_000_000:
            category = CompanyCategory.MID_CAP

        else:
            category = CompanyCategory.SMALL_CAP

        knowledge = Knowledge(
            ticker=company.ticker,
            company=company.name,
            exchange=company.exchange,
            sector=company.sector,
            industry=company.industry,
            category=category,
        )

        return BasePackage(
            package_type=PackageType.KNOWLEDGE,
            source="KnowledgeEngine",
            data=knowledge,
        )