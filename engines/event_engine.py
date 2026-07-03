from core.base_engine import BaseEngine
from core.base_package import BasePackage

from enums.package_type import PackageType

from packages.event_package import EventPackage

from models.event import Event


class EventEngine(BaseEngine):

    def process(self, package: BasePackage) -> BasePackage:

        news = package.data

        event = Event(

            company=news.ticker,

            title=news.title,

            category="News",

            source=news.publisher,

            published_at=news.published_at,

            sentiment="Neutral",

            summary=news.content
        )

        event_package = EventPackage(event=event)

        return BasePackage(

            package_type=PackageType.EVENT,

            source="EventEngine",

            data=event_package
        )