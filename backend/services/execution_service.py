"""
Execution Service.
Orchestrates code execution workflows and decouples routing from specific provider implementations.
"""

from typing import Optional
import httpx
from backend.schemas.execution import (
    CustomTestCheckRequest,
    CustomTestCheckResponse,
    RunCodeRequest,
    RunCodeResponse,
)
from backend.services.providers.base_provider import BaseExecutionProvider
from backend.services.providers.provider_factory import ProviderFactory


class ExecutionService:
    """Service handling code execution and test evaluation."""

    def __init__(
        self,
        provider: Optional[BaseExecutionProvider] = None,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        self.provider = provider or ProviderFactory.get_provider(http_client=http_client)

    async def execute_run(self, request: RunCodeRequest) -> RunCodeResponse:
        """
        Execute code with user-supplied standard input.
        """
        return await self.provider.run_code(request)

    async def execute_custom_tests(
        self, request: CustomTestCheckRequest
    ) -> CustomTestCheckResponse:
        """
        Evaluate code against custom user test cases.
        """
        return await self.provider.run_tests(request)

    async def submit_problem(
        self, problem_id: str, source_code: str, language: str = "python"
    ) -> None:
        """
        Reserved for Milestone 3+ official problem submission.
        Official hidden test cases will be fetched internally from the database
        and never accepted or exposed via frontend endpoints.
        """
        raise NotImplementedError(
            "Official problem submission workflow requires problem database integration (Milestone 3+)."
        )

