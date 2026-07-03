from datetime import datetime

from models.event import Event


class NewsConnector:

    def get_latest_event(self, ticker):

        return Event(
            company=ticker,
            title="Apple announces new AI partnership",
            category="Partnership",
            source="Reuters",
            published_at=datetime.now(),
            sentiment="Positive",
            summary="Apple announced a strategic partnership to strengthen its AI ecosystem."
        )