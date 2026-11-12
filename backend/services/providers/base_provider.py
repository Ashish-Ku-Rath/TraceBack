"""
Base Execution Provider Interface.
Defines abstract contracts for executing code and evaluating test cases.
"""

from abc import ABC, abstractmethod
from backend.schemas.execution import (
    CustomTestCheckRequest,
    CustomTestCheckResponse,
    RunCodeRequest,
    RunCodeResponse,
)


class BaseExecutionProvider(ABC):
    """Abstract execution provider contract."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the unique provider name identifier."""
        pass

    @abstractmethod
    async def run_code(self, request: RunCodeRequest) -> RunCodeResponse:
        """
        Execute source code with optional standard input.
        Does not perform correctness verification against test cases.
        """
        pass

    @abstractmethod
    async def run_tests(
        self, request: CustomTestCheckRequest
    ) -> CustomTestCheckResponse:
        """
        Execute source code against a batch of test cases and return verdicts.
        """
        pass

