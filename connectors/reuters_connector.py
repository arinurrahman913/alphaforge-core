from datetime import datetime

from models.news import News


class ReutersConnector:

    def get_latest_news(self, ticker: str):

        return News(

            ticker=ticker,

            title="Apple expands AI investment",

            content="Reuters reported that Apple plans to expand investment in generative AI.",

            publisher="Reuters",

            published_at=datetime.now(),

            url="https://www.reuters.com"
        )