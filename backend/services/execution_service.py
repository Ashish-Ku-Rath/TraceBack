"""
Execution Service.
Orchestrates code execution workflows and decouples routing from specific provider implementations.
"""

from typing import Optional
import httpx
from sqlalchemy.orm import Session
from backend.core.exceptions import ConfigurationError, ProblemNotFoundError
from backend.models.problem import Problem, ProblemExample
from backend.schemas.execution import (
    CustomTestCheckRequest,
    CustomTestCheckResponse,
    RunCodeRequest,
    RunCodeResponse,
    SubmitCodeRequest,
    SubmitCodeResponse,
    TestCaseInput,
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
        self, request: SubmitCodeRequest, db: Session
    ) -> SubmitCodeResponse:
        """
        Evaluate code against official predefined test cases from the database.
        Never executes user code on the local host.
        """
        problem = db.query(Problem).filter(Problem.id == request.problem_id).first()
        if not problem:
            raise ProblemNotFoundError(f"Problem #{request.problem_id} does not exist.")

        examples = (
            db.query(ProblemExample)
            .filter(ProblemExample.problem_id == problem.id)
            .order_by(ProblemExample.id)
            .all()
        )
        if not examples:
            raise ConfigurationError(
                f"No test cases configured in database for problem #{request.problem_id}."
            )

        test_inputs = [
            TestCaseInput(
                input=ex.input,
                expected_output=ex.expected_output,
            )
            for ex in examples
        ]

        custom_req = CustomTestCheckRequest(
            source_code=request.source_code,
            language=request.language,
            time_limit=request.time_limit,
            checker="trim",
            tests=test_inputs,
        )

        test_check_resp = await self.provider.run_tests(custom_req)

        return SubmitCodeResponse(
            problem_id=request.problem_id,
            verdict=test_check_resp.verdict,
            total_tests=test_check_resp.total_tests,
            passed_tests=test_check_resp.passed_tests,
            failed_tests=test_check_resp.failed_tests,
            tests=test_check_resp.tests,
            execution_time=test_check_resp.execution_time,
            memory_kb=test_check_resp.memory_kb,
            provider=test_check_resp.provider,
            is_simulated=test_check_resp.is_simulated,
        )
