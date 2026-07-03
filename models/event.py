from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:

    company: str

    title: str

    category: str

    source: str

    published_at: datetime

    sentiment: str

    summary: str

    def summary_text(self):

        return (
            "========== EVENT ==========\n"
            f"Company      : {self.company}\n"
            f"Title        : {self.title}\n"
            f"Category     : {self.category}\n"
            f"Source       : {self.source}\n"
            f"Published At : {self.published_at}\n"
            f"Sentiment    : {self.sentiment}\n"
            f"Summary      : {self.summary}\n"
        )

    def __str__(self):
        return self.summary_text()