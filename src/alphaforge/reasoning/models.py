from dataclasses import dataclass
from typing import List


@dataclass
class Reasoning:

    title: str

    summary: str

    confidence: int

    supporting_evidence: List[str]