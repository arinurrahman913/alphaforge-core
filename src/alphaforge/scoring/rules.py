from dataclasses import dataclass
from typing import Callable


@dataclass
class Rule:

    name: str

    maximum: int

    evaluator: Callable