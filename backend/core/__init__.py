"""
Application core configurations, settings, constants, and exceptions.
"""

from backend.core.config import settings
from backend.core.exceptions import (
    AuthenticationError,
    ConfigurationError,
    ExecutionTimeoutError,
    ExternalServiceError,
    RateLimitError,
    TraceBackError,
    ProblemNotFoundError,
    DuplicateSlugError,
    InvalidProblemDataError,
)

__all__ = [
    "settings",
    "TraceBackError",
    "ConfigurationError",
    "AuthenticationError",
    "RateLimitError",
    "ExecutionTimeoutError",
    "ExternalServiceError",
    "ProblemNotFoundError",
    "DuplicateSlugError",
    "InvalidProblemDataError",
]
