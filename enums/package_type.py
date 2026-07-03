from enum import Enum


class PackageType(Enum):
    COMPANY = "Company"
    KNOWLEDGE = "Knowledge"
    EVENT = "Event"
    CONTEXT = "Context"
    EVIDENCE = "Evidence"
    REASONING = "Reasoning"
    DECISION = "Decision"