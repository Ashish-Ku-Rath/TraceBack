"""
Tests for MockProvider.
Verifies simulated responses (Success, Wrong Answer, Runtime Error, Time Limit Exceeded)
and confirms submitted code is NEVER executed.
"""

import asyncio
import pytest
from backend.schemas.execution import (
    CustomTestCheckRequest,
    ExecutionVerdict,
    RunCodeRequest,
    TestCaseInput,
)
from backend.services.providers.mock_provider import MockProvider


@pytest.fixture
def mock_provider() -> MockProvider:
    return MockProvider()


def test_mock_provider_successful_run_and_tests(mock_provider: MockProvider) -> None:
    """Test 1: Successful simulated response for run_code and run_tests."""
    async def _run() -> None:
        # Run code
        run_req = RunCodeRequest(
            source_code="print('Hello World')",
            stdin="test input",
            language="python",
            time_limit=5,
        )
        run_res = await mock_provider.run_code(run_req)
        assert run_res.status == "success"
        assert run_res.exit_code == 0
        assert run_res.is_simulated is True
        assert run_res.provider == "mock"
        assert "test input" in run_res.stdout

        # Run tests
        test_req = CustomTestCheckRequest(
            source_code="a = int(input())\nprint(a * 2)",
            language="python",
            time_limit=5,
            checker="trim",
            tests=[
                TestCaseInput(input="5", expected_output="10"),
                TestCaseInput(input="7", expected_output="14"),
            ],
        )
        test_res = await mock_provider.run_tests(test_req)
        assert test_res.verdict == ExecutionVerdict.ACCEPTED.value
        assert test_res.total_tests == 2
        assert test_res.passed_tests == 2
        assert test_res.failed_tests == 0
        assert test_res.is_simulated is True
        assert test_res.provider == "mock"
        assert test_res.tests[0].verdict == ExecutionVerdict.ACCEPTED.value
        assert test_res.tests[0].actual_output == "10"

    asyncio.run(_run())


def test_mock_provider_simulated_wrong_answer(mock_provider: MockProvider) -> None:
    """Test 2: Simulated Wrong Answer."""
    async def _run() -> None:
        test_req = CustomTestCheckRequest(
            source_code="# mock:wrong_answer\nprint('wrong')",
            language="python",
            time_limit=5,
            checker="trim",
            tests=[TestCaseInput(input="1", expected_output="100")],
        )
        test_res = await mock_provider.run_tests(test_req)
        assert test_res.verdict == ExecutionVerdict.WRONG_ANSWER.value
        assert test_res.passed_tests == 0
        assert test_res.failed_tests == 1
        assert test_res.is_simulated is True
        assert test_res.tests[0].verdict == ExecutionVerdict.WRONG_ANSWER.value
        assert "[Simulated Incorrect Output" in test_res.tests[0].actual_output

    asyncio.run(_run())


def test_mock_provider_simulated_runtime_error(mock_provider: MockProvider) -> None:
    """Test 3: Simulated Runtime Error."""
    async def _run() -> None:
        # In run_code
        run_req = RunCodeRequest(
            source_code="# mock:runtime_error\nprint(1/0)",
            language="python",
            time_limit=5,
        )
        run_res = await mock_provider.run_code(run_req)
        assert run_res.status == "runtime_error"
        assert run_res.exit_code == 1
        assert run_res.is_simulated is True
        assert "ZeroDivisionError" in run_res.stderr

        # In run_tests
        test_req = CustomTestCheckRequest(
            source_code="# mock:runtime_error\n1/0",
            language="python",
            time_limit=5,
            checker="trim",
            tests=[TestCaseInput(input="1", expected_output="2")],
        )
        test_res = await mock_provider.run_tests(test_req)
        assert test_res.verdict == ExecutionVerdict.RUNTIME_ERROR.value
        assert test_res.passed_tests == 0
        assert test_res.is_simulated is True
        assert "ZeroDivisionError" in test_res.tests[0].error

    asyncio.run(_run())


def test_mock_provider_simulated_time_limit_exceeded(mock_provider: MockProvider) -> None:
    """Test 4: Simulated Time Limit Exceeded."""
    async def _run() -> None:
        # In run_code
        run_req = RunCodeRequest(
            source_code="# mock:time_limit_exceeded\nwhile True: pass",
            language="python",
            time_limit=4,
        )
        run_res = await mock_provider.run_code(run_req)
        assert run_res.status == "time_limit_exceeded"
        assert run_res.exit_code == 124
        assert run_res.execution_time == 4.0
        assert run_res.is_simulated is True

        # In run_tests
        test_req = CustomTestCheckRequest(
            source_code="# mock:tle\nwhile True: pass",
            language="python",
            time_limit=3,
            checker="trim",
            tests=[TestCaseInput(input="1", expected_output="2")],
        )
        test_res = await mock_provider.run_tests(test_req)
        assert test_res.verdict == ExecutionVerdict.TIME_LIMIT_EXCEEDED.value
        assert test_res.passed_tests == 0
        assert test_res.execution_time == 3.0
        assert test_res.is_simulated is True

    asyncio.run(_run())


def test_mock_provider_never_executes_code(mock_provider: MockProvider) -> None:
    """
    Test 5: Confirm submitted code is NEVER executed.
    Submitting code that would raise exceptions, create side effects,
    or call exit() must NOT execute locally.
    """
    async def _run() -> None:
        malicious_code = """
import sys
# If executed locally, this would crash the test process with exit(99)
sys.exit(99)
"""
        run_req = RunCodeRequest(
            source_code=malicious_code,
            language="python",
            time_limit=5,
        )
        # If exec() or subprocess were used, this would exit the Python process or crash
        run_res = await mock_provider.run_code(run_req)
        assert run_res.status == "success"
        assert run_res.exit_code == 0
        assert run_res.is_simulated is True

    asyncio.run(_run())
