"""
Core exception classes for TraceBack application.
Guarantees clean error propagation without exposing secrets in logs or stacktraces.
"""


class TraceBackError(Exception):
    """Base exception for all TraceBack application errors."""
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class ConfigurationError(TraceBackError):
    """Raised when environment or provider configuration is missing or invalid."""
    pass


class AuthenticationError(TraceBackError):
    """Raised when authentication against external provider fails (401/403)."""
    pass


class RateLimitError(TraceBackError):
    """Raised when external provider rate limits or quotas are exceeded (429)."""
    pass


class ExecutionTimeoutError(TraceBackError):
    """Raised when code execution or network request times out."""
    pass


class ExternalServiceError(TraceBackError):
    """Raised when an external service returns 5xx or invalid payloads."""
    pass


class ProblemNotFoundError(TraceBackError):
    """Raised when a requested problem cannot be found (404)."""
    pass


class DuplicateSlugError(TraceBackError):
    """Raised when attempting to create a problem with an existing slug (400/409)."""
    pass


class InvalidProblemDataError(TraceBackError):
    """Raised when problem data violates business validation rules."""
    pass


