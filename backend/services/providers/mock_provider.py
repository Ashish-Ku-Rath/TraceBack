"""
Mock Execution Provider.
Provides deterministic, synthetic responses for development and testing.

SECURITY MANDATE:
MockProvider NEVER executes submitted source code.
No exec(), eval(), or local subprocess calls are ever permitted.
All responses explicitly flag is_simulated=True.
"""

from typing import List
from backend.schemas.execution import (
    CustomTestCheckRequest,
    CustomTestCheckResponse,
    ExecutionVerdict,
    RunCodeRequest,
    RunCodeResponse,
    TestCaseResult,
)
from backend.services.providers.base_provider import BaseExecutionProvider


class MockProvider(BaseExecutionProvider):
    """
    Simulation provider for offline development and testing.
    Never executes user code locally.
    """

    @property
    def provider_name(self) -> str:
        return "mock"

    def _detect_simulation_directive(self, code: str) -> str:
        """
        Inspect code comments for deterministic simulation instructions.
        Does not execute or interpret code.
        """
        code_lower = code.lower()
        if "# mock:wrong_answer" in code_lower or "# mock:wa" in code_lower:
            return ExecutionVerdict.WRONG_ANSWER.value
        if "# mock:runtime_error" in code_lower or "# mock:re" in code_lower:
            return ExecutionVerdict.RUNTIME_ERROR.value
        if "# mock:time_limit_exceeded" in code_lower or "# mock:tle" in code_lower:
            return ExecutionVerdict.TIME_LIMIT_EXCEEDED.value
        if (
            "# mock:compilation_error" in code_lower
            or "# mock:ce" in code_lower
            or "# mock:compile_error" in code_lower
        ):
            return ExecutionVerdict.COMPILATION_ERROR.value
        if "# mock:memory_limit_exceeded" in code_lower or "# mock:mle" in code_lower:
            return ExecutionVerdict.MEMORY_LIMIT_EXCEEDED.value
        return "success"

    async def run_code(self, request: RunCodeRequest) -> RunCodeResponse:
        """
        Generate synthetic Run Code response without executing source code.
        """
        directive = self._detect_simulation_directive(request.source_code)

        if directive == ExecutionVerdict.RUNTIME_ERROR.value:
            return RunCodeResponse(
                status="runtime_error",
                stdout="",
                stderr="Traceback (most recent call last):\n  File \"solution.py\", line 2, in <module>\nZeroDivisionError: division by zero (Simulated)",
                exit_code=1,
                execution_time=0.015,
                memory_kb=8192,
                provider=self.provider_name,
                is_simulated=True,
                truncated=False,
            )

        if directive == ExecutionVerdict.COMPILATION_ERROR.value:
            return RunCodeResponse(
                status="compilation_error",
                stdout="",
                stderr="  File \"solution.py\", line 1\n    invalid syntax python code\n                   ^^^^^^\nSyntaxError: invalid syntax (Simulated)",
                exit_code=1,
                execution_time=0.0,
                memory_kb=0,
                provider=self.provider_name,
                is_simulated=True,
                truncated=False,
            )

        if directive == ExecutionVerdict.TIME_LIMIT_EXCEEDED.value:
            return RunCodeResponse(
                status="time_limit_exceeded",
                stdout="",
                stderr=f"Execution timed out after {request.time_limit} seconds (Simulated)",
                exit_code=124,
                execution_time=float(request.time_limit),
                memory_kb=10240,
                provider=self.provider_name,
                is_simulated=True,
                truncated=False,
            )

        # Default: Simulated successful execution
        simulated_stdout = (
            f"[Simulated Output] Standard input received: '{request.stdin.strip()}'\n"
            if request.stdin.strip()
            else "[Simulated Output] Program executed successfully.\n"
        )

        return RunCodeResponse(
            status="success",
            stdout=simulated_stdout,
            stderr="",
            exit_code=0,
            execution_time=0.02,
            memory_kb=8192,
            provider=self.provider_name,
            is_simulated=True,
            truncated=False,
        )

    async def run_tests(
        self, request: CustomTestCheckRequest
    ) -> CustomTestCheckResponse:
        """
        Generate synthetic custom test case evaluation results.
        Never executes source code.
        """
        directive = self._detect_simulation_directive(request.source_code)
        results: List[TestCaseResult] = []

        if directive == ExecutionVerdict.COMPILATION_ERROR.value:
            for idx, test in enumerate(request.tests):
                results.append(
                    TestCaseResult(
                        test_index=idx,
                        input=test.input,
                        expected_output=test.expected_output,
                        actual_output=None,
                        error="SyntaxError: invalid syntax (Simulated)",
                        verdict=ExecutionVerdict.COMPILATION_ERROR.value,
                        execution_time=0.0,
                        memory_kb=0,
                        exit_code=1,
                        hidden=False,
                        truncated=False,
                    )
                )
            return CustomTestCheckResponse(
                verdict=ExecutionVerdict.COMPILATION_ERROR.value,
                total_tests=len(request.tests),
                passed_tests=0,
                failed_tests=len(request.tests),
                tests=results,
                execution_time=0.0,
                memory_kb=0,
                provider=self.provider_name,
                is_simulated=True,
            )

        if directive == ExecutionVerdict.TIME_LIMIT_EXCEEDED.value:
            for idx, test in enumerate(request.tests):
                results.append(
                    TestCaseResult(
                        test_index=idx,
                        input=test.input,
                        expected_output=test.expected_output,
                        actual_output=None,
                        error=f"Time limit exceeded after {request.time_limit}s (Simulated)",
                        verdict=ExecutionVerdict.TIME_LIMIT_EXCEEDED.value,
                        execution_time=float(request.time_limit),
                        memory_kb=10240,
                        exit_code=124,
                        hidden=False,
                        truncated=False,
                    )
                )
            return CustomTestCheckResponse(
                verdict=ExecutionVerdict.TIME_LIMIT_EXCEEDED.value,
                total_tests=len(request.tests),
                passed_tests=0,
                failed_tests=len(request.tests),
                tests=results,
                execution_time=float(request.time_limit),
                memory_kb=10240,
                provider=self.provider_name,
                is_simulated=True,
            )

        if directive == ExecutionVerdict.RUNTIME_ERROR.value:
            for idx, test in enumerate(request.tests):
                results.append(
                    TestCaseResult(
                        test_index=idx,
                        input=test.input,
                        expected_output=test.expected_output,
                        actual_output=None,
                        error="ZeroDivisionError: division by zero (Simulated)",
                        verdict=ExecutionVerdict.RUNTIME_ERROR.value,
                        execution_time=0.015,
                        memory_kb=8192,
                        exit_code=1,
                        hidden=False,
                        truncated=False,
                    )
                )
            return CustomTestCheckResponse(
                verdict=ExecutionVerdict.RUNTIME_ERROR.value,
                total_tests=len(request.tests),
                passed_tests=0,
                failed_tests=len(request.tests),
                tests=results,
                execution_time=0.015,
                memory_kb=8192,
                provider=self.provider_name,
                is_simulated=True,
            )

        if directive == ExecutionVerdict.WRONG_ANSWER.value:
            for idx, test in enumerate(request.tests):
                results.append(
                    TestCaseResult(
                        test_index=idx,
                        input=test.input,
                        expected_output=test.expected_output,
                        actual_output=f"[Simulated Incorrect Output for Test {idx + 1}]",
                        error="",
                        verdict=ExecutionVerdict.WRONG_ANSWER.value,
                        execution_time=0.02,
                        memory_kb=8192,
                        exit_code=0,
                        hidden=False,
                        truncated=False,
                    )
                )
            return CustomTestCheckResponse(
                verdict=ExecutionVerdict.WRONG_ANSWER.value,
                total_tests=len(request.tests),
                passed_tests=0,
                failed_tests=len(request.tests),
                tests=results,
                execution_time=0.02 * len(request.tests),
                memory_kb=8192,
                provider=self.provider_name,
                is_simulated=True,
            )

        # Default: Simulated Accepted (tests pass)
        for idx, test in enumerate(request.tests):
            results.append(
                TestCaseResult(
                    test_index=idx,
                    input=test.input,
                    expected_output=test.expected_output,
                    actual_output=test.expected_output,
                    error="",
                    verdict=ExecutionVerdict.ACCEPTED.value,
                    execution_time=0.018,
                    memory_kb=8192,
                    exit_code=0,
                    hidden=False,
                    truncated=False,
                )
            )

        return CustomTestCheckResponse(
            verdict=ExecutionVerdict.ACCEPTED.value,
            total_tests=len(request.tests),
            passed_tests=len(request.tests),
            failed_tests=0,
            tests=results,
            execution_time=0.018 * len(request.tests),
            memory_kb=8192,
            provider=self.provider_name,
            is_simulated=True,
        )

