from dataclasses import dataclass
from typing import List


@dataclass
class Evidence:

    category: str

    conclusion: str

    confidence: int

    supporting_items: List[str]