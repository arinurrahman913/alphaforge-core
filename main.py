from connectors.yahoo_finance import YahooFinanceConnector

from core.base_package import BasePackage

from engines.knowledge_engine import KnowledgeEngine

from enums.package_type import PackageType


connector = YahooFinanceConnector()

company = connector.get_company("crwv")

print("✓ Company Loaded")


package = BasePackage(
    package_type=PackageType.COMPANY,
    source="YahooFinanceConnector",
    data=company,
)

print("✓ Package Created")


engine = KnowledgeEngine()

knowledge = engine.process(package)

print("✓ Knowledge Created")

print()
print(knowledge.data)