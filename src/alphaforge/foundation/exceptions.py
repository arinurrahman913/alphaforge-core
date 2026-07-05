"""
Custom exceptions used throughout AlphaForge.
"""


class AlphaForgeError(Exception):
    """Base exception for AlphaForge."""


class ConfigurationError(AlphaForgeError):
    """Raised when configuration is invalid."""


class DataError(AlphaForgeError):
    """Raised when data processing fails."""


class ResearchError(AlphaForgeError):
    """Raised when research fails."""


class ReasoningError(AlphaForgeError):
    """Raised when reasoning engine fails."""