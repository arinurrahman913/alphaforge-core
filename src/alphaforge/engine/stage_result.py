from dataclasses import dataclass


@dataclass
class StageResult:

    stage: str

    success: bool

    duration: float

    error: str | None = None