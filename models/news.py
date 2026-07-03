from dataclasses import dataclass
from datetime import datetime


@dataclass
class News:

    ticker: str

    title: str

    content: str

    publisher: str

    published_at: datetime

    url: str

    def summary(self):

        return (
            "========== NEWS ==========\n"
            f"Ticker       : {self.ticker}\n"
            f"Title        : {self.title}\n"
            f"Publisher    : {self.publisher}\n"
            f"Published At : {self.published_at}\n"
            f"URL          : {self.url}\n"
            f"Content      : {self.content}\n"
        )

    def __str__(self):

        return self.summary()