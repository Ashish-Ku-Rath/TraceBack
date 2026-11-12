"""
OnlineCompiler Execution Provider.
Communicates with https://api.onlinecompiler.io for remote sandboxed execution.
"""

from typing import Any, Dict, List, Optional
import httpx
from backend.core.config import settings
from backend.integrations.onlinecompiler_client import OnlineCompilerClient
from backend.schemas.execution import (
    CustomTestCheckRequest,
    CustomTestCheckResponse,
    ExecutionVerdict,
    RunCodeRequest,
    RunCodeResponse,
    TestCaseResult,
)
from backend.services.providers.base_provider import BaseExecutionProvider


class OnlineCompilerProvider(BaseExecutionProvider):
    """
    Real execution provider interacting with OnlineCompiler API.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        compiler_id: Optional[str] = None,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        self.compiler_id = compiler_id or settings.ONLINECOMPILER_PYTHON_COMPILER
        self.client = OnlineCompilerClient(
            api_key=api_key,
            base_url=api_url,
            http_client=http_client,
        )

    @property
    def provider_name(self) -> str:
        return "onlinecompiler"

    @staticmethod
    def _parse_float(value: Any) -> Optional[float]:
        """Safely parse float values from provider output."""
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _parse_int(value: Any) -> Optional[int]:
        """Safely parse integer values from provider output."""
        if value is None:
            return None
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _normalize_verdict(raw_verdict: Optional[str]) -> str:
        """Map raw provider verdict string to canonical TraceBack ExecutionVerdict."""
        if not raw_verdict:
            return ExecutionVerdict.INTERNAL_ERROR.value

        cleaned = str(raw_verdict).strip().lower()
        if cleaned in ("accepted", "ac"):
            return ExecutionVerdict.ACCEPTED.value
        if cleaned in ("wrong_answer", "wa"):
            return ExecutionVerdict.WRONG_ANSWER.value
        if cleaned in ("runtime_error", "re"):
            return ExecutionVerdict.RUNTIME_ERROR.value
        if cleaned in ("time_limit_exceeded", "tle", "timeout"):
            return ExecutionVerdict.TIME_LIMIT_EXCEEDED.value
        if cleaned in ("compile_error", "compilation_error", "ce"):
            return ExecutionVerdict.COMPILATION_ERROR.value
        if cleaned in ("memory_limit_exceeded", "mle"):
            return ExecutionVerdict.MEMORY_LIMIT_EXCEEDED.value
        if cleaned in ("output_limit_exceeded", "ole"):
            return ExecutionVerdict.OUTPUT_LIMIT_EXCEEDED.value
        if cleaned in ("skipped",):
            return ExecutionVerdict.SKIPPED.value
        if cleaned in ("incomplete",):
            return ExecutionVerdict.INCOMPLETE.value

        return cleaned

    async def run_code(self, request: RunCodeRequest) -> RunCodeResponse:
        """
        Execute code via POST /api/run-code-sync/ and normalize result.
        """
        payload: Dict[str, Any] = {
            "compiler": self.compiler_id,
            "code": request.source_code,
            "input": request.stdin,
            "time_limit": request.time_limit,
        }
        timeout_seconds = request.time_limit + settings.HTTP_TIMEOUT_BUFFER_SECONDS

        raw_data = await self.client.run_code_sync(
            payload=payload,
            timeout_seconds=timeout_seconds,
        )

        stdout = str(raw_data.get("output") or "")
        stderr = str(raw_data.get("error") or "")
        exit_code = raw_data.get("exit_code")
        execution_time = self._parse_float(raw_data.get("time"))
        memory_kb = self._parse_int(raw_data.get("memory"))
        truncated = bool(raw_data.get("truncated", False))
        raw_status = str(raw_data.get("status") or "").lower()

        # Distinguish execution success from failure
        if raw_status == "timeout" or raw_data.get("signal") in ("SIGKILL", "SIGXCPU"):
            status = "time_limit_exceeded"
        elif exit_code == 0 and not raw_status.startswith("error"):
            status = "success"
        elif raw_status in ("compile_error", "compilation_error") or "SyntaxError" in stderr:
            status = "compilation_error"
        else:
            status = "runtime_error"

        return RunCodeResponse(
            status=status,
            stdout=stdout,
            stderr=stderr,
            exit_code=exit_code,
            execution_time=execution_time,
            memory_kb=memory_kb,
            provider=self.provider_name,
            is_simulated=False,
            truncated=truncated,
        )

    async def run_tests(
        self, request: CustomTestCheckRequest
    ) -> CustomTestCheckResponse:
        """
        Execute code against custom test cases via POST /api/run-tests/.
        """
        payload: Dict[str, Any] = {
            "compiler": self.compiler_id,
            "code": request.source_code,
            "tests": [
                {"input": t.input, "expected_output": t.expected_output}
                for t in request.tests
            ],
            "checker": request.checker,
            "time_limit": request.time_limit,
            "scoring": "all_or_nothing",
        }
        timeout_seconds = (
            request.time_limit * len(request.tests)
            + settings.HTTP_TIMEOUT_BUFFER_SECONDS
        )

        raw_data = await self.client.run_tests(
            payload=payload,
            timeout_seconds=timeout_seconds,
        )

        # Normalize overall verdict
        if raw_data.get("compile_error"):
            overall_verdict = ExecutionVerdict.COMPILATION_ERROR.value
        else:
            overall_verdict = self._normalize_verdict(raw_data.get("verdict"))

        raw_tests = raw_data.get("tests") or []
        normalized_tests: List[TestCaseResult] = []

        for idx, user_test in enumerate(request.tests):
            test_data = raw_tests[idx] if idx < len(raw_tests) else {}
            is_hidden = bool(test_data.get("hidden", False))

            # Never fabricate missing output or error for hidden tests
            actual_output = None if is_hidden else test_data.get("output")
            error_output = None if is_hidden else test_data.get("error")

            test_verdict = self._normalize_verdict(test_data.get("verdict"))
            t_time = self._parse_float(test_data.get("time"))
            t_mem = self._parse_int(test_data.get("memory"))
            t_exit = test_data.get("exit_code")
            t_trunc = bool(test_data.get("truncated", False))

            normalized_tests.append(
                TestCaseResult(
                    test_index=idx,
                    input=user_test.input,
                    expected_output=user_test.expected_output,
                    actual_output=actual_output,
                    error=error_output,
                    verdict=test_verdict,
                    execution_time=t_time,
                    memory_kb=t_mem,
                    exit_code=t_exit,
                    hidden=is_hidden,
                    truncated=t_trunc,
                )
            )

        total_tests = int(raw_data.get("total", len(request.tests)))
        passed_tests = int(
            raw_data.get(
                "passed",
                sum(1 for t in normalized_tests if t.verdict == ExecutionVerdict.ACCEPTED.value),
            )
        )
        failed_tests = max(0, total_tests - passed_tests)

        # Calculate peak memory and cumulative execution time if not provided at root
        times = [t.execution_time for t in normalized_tests if t.execution_time is not None]
        mems = [t.memory_kb for t in normalized_tests if t.memory_kb is not None]

        return CustomTestCheckResponse(
            verdict=overall_verdict,
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            tests=normalized_tests,
            execution_time=sum(times) if times else None,
            memory_kb=max(mems) if mems else None,
            provider=self.provider_name,
            is_simulated=False,
        )

