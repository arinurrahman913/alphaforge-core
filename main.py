from connectors.yahoo_finance import YahooFinanceConnector
from connectors.reuters_connector import ReutersConnector

from core.base_package import BasePackage

from engines.knowledge_engine import KnowledgeEngine
from engines.event_engine import EventEngine

from enums.package_type import PackageType

from repositories.knowledge_repository import KnowledgeRepository
from repositories.event_repository import EventRepository


# ======================================
# Repository
# ======================================

knowledge_repository = KnowledgeRepository()
event_repository = EventRepository()


# ======================================
# Yahoo -> Company -> Knowledge
# ======================================

company_connector = YahooFinanceConnector()

company = company_connector.get_company("AAPL")

company_package = BasePackage(
    package_type=PackageType.COMPANY,
    source="YahooFinanceConnector",
    data=company
)

knowledge_engine = KnowledgeEngine()

knowledge_package = knowledge_engine.process(company_package)

knowledge_repository.save(knowledge_package.data)

print("✓ Knowledge Saved")


# ======================================
# Reuters -> News -> Event
# ======================================

reuters = ReutersConnector()

news = reuters.get_latest_news("AAPL")

news_package = BasePackage(
    package_type=PackageType.EVENT,
    source="ReutersConnector",
    data=news
)

event_engine = EventEngine()

processed_event = event_engine.process(news_package)

event_repository.save(processed_event.data.event)

print("✓ Event Saved")


# ======================================
# Read Knowledge
# ======================================

print()
print("========== KNOWLEDGE ==========")

print(
    knowledge_repository.get("AAPL")
)


# ======================================
# Read Events
# ======================================

print()
print("========== EVENTS ==========")

for event in event_repository.get("AAPL"):
    print(event)

print()
print("========== KNOWLEDGE HISTORY ==========")

for item in knowledge_repository.history("AAPL"):

    print(item["timestamp"])
    print(item["data"])
    print()

print()
print("========== EVENT HISTORY ==========")

for item in event_repository.history("AAPL"):

    print(item["timestamp"])
    print(item["data"])
    print()