from dataclasses import dataclass


@dataclass
class NewsArticle:
    title: str
    publisher: str
    link: str