"""
Tests for OnlineCompilerProvider and OnlineCompilerClient.
Uses httpx.MockTransport to test without any external API calls or quota consumption.
"""

import asyncio
import json
import pytest
import httpx
from backend.core.exceptions import (
    AuthenticationError,
    ConfigurationError,
    ExecutionTimeoutError,
    ExternalServiceError,
    RateLimitError,
)
from backend.integrations.onlinecompiler_client import OnlineCompilerClient
from backend.schemas.execution import (
    CustomTestCheckRequest,
    ExecutionVerdict,
    RunCodeRequest,
    TestCaseInput,
)
from backend.services.providers.onlinecompiler_provider import OnlineCompilerProvider


def test_authorization_header_construction() -> None:
    """Test 6: Correct Authorization header construction with raw API key."""
    captured_headers = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured_headers.update(dict(request.headers))
        return httpx.Response(200, json={"output": "ok", "status": "success", "exit_code": 0})

    transport = httpx.MockTransport(handler)

    async def _run() -> None:
        async with httpx.AsyncClient(transport=transport) as http_client:
            provider = OnlineCompilerProvider(
                api_key="test_secret_api_key_123",
                http_client=http_client,
            )
            req = RunCodeRequest(source_code="print('hi')", language="python")
            await provider.run_code(req)

    asyncio.run(_run())

    # OnlineCompiler requires raw API key in Authorization header without RapidAPI or Bearer prefixes
    assert captured_headers.get("authorization") == "test_secret_api_key_123"
    assert captured_headers.get("content-type") == "application/json"


def test_run_code_endpoint_and_payload() -> None:
    """Test 7: Correct Run Code endpoint (/api/run-code-sync/) and request payload."""
    captured_request = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured_request["url"] = str(request.url)
        captured_request["body"] = json.loads(request.content.decode("utf-8"))
        return httpx.Response(
            200,
            json={
                "output": "42\n",
                "error": "",
                "status": "success",
                "exit_code": 0,
                "time": "0.023",
                "memory": "8500",
                "truncated": False,
            },
        )

    transport = httpx.MockTransport(handler)

    async def _run() -> None:
        async with httpx.AsyncClient(transport=transport) as http_client:
            provider = OnlineCompilerProvider(
                api_key="test_key",
                compiler_id="python-3.14",
                http_client=http_client,
            )
            req = RunCodeRequest(
                source_code="print(42)",
                stdin="input_data",
                language="python",
                time_limit=7,
            )
            return await provider.run_code(req)

    res = asyncio.run(_run())

    assert captured_request["url"] == "https://api.onlinecompiler.io/api/run-code-sync/"
    assert captured_request["body"] == {
        "compiler": "python-3.14",
        "code": "print(42)",
        "input": "input_data",
        "time_limit": 7,
    }
    assert res.status == "success"
    assert res.stdout == "42\n"
    assert res.exit_code == 0
    assert res.execution_time == 0.023
    assert res.memory_kb == 8500
    assert res.provider == "onlinecompiler"
    assert res.is_simulated is False


def test_custom_tests_endpoint_and_payload() -> None:
    """Test 8: Correct Custom Tests endpoint (/api/run-tests/) and request payload."""
    captured_request = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured_request["url"] = str(request.url)
        captured_request["body"] = json.loads(request.content.decode("utf-8"))
        return httpx.Response(
            200,
            json={
                "verdict": "accepted",
                "score": 100.0,
                "passed": 2,
                "total": 2,
                "tests": [
                    {
                        "verdict": "accepted",
                        "output": "30\n",
                        "error": "",
                        "time": "0.015",
                        "memory": "8000",
                        "exit_code": 0,
                        "hidden": False,
                    },
                    {
                        "verdict": "accepted",
                        "output": "12\n",
                        "error": "",
                        "time": "0.016",
                        "memory": "8000",
                        "exit_code": 0,
                        "hidden": False,
                    },
                ],
            },
        )

    transport = httpx.MockTransport(handler)

    async def _run() -> None:
        async with httpx.AsyncClient(transport=transport) as http_client:
            provider = OnlineCompilerProvider(
                api_key="test_key",
                compiler_id="python-3.14",
                http_client=http_client,
            )
            req = CustomTestCheckRequest(
                source_code="a, b = map(int, input().split()); print(a + b)",
                language="python",
                time_limit=5,
                checker="trim",
                tests=[
                    TestCaseInput(input="10 20", expected_output="30"),
                    TestCaseInput(input="5 7", expected_output="12"),
                ],
            )
            return await provider.run_tests(req)

    res = asyncio.run(_run())

    assert captured_request["url"] == "https://api.onlinecompiler.io/api/run-tests/"
    assert captured_request["body"]["compiler"] == "python-3.14"
    assert captured_request["body"]["checker"] == "trim"
    assert len(captured_request["body"]["tests"]) == 2
    assert res.verdict == ExecutionVerdict.ACCEPTED.value
    assert res.passed_tests == 2
    assert res.total_tests == 2
    assert res.is_simulated is False
    assert res.provider == "onlinecompiler"


def test_response_normalization() -> None:
    """Test 9: Response normalization across various verdict types and hidden tests."""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "verdict": "runtime_error",
                "score": 50.0,
                "passed": 1,
                "total": 2,
                "tests": [
                    {
                        "verdict": "wrong_answer",
                        "output": "wrong\n",
                        "error": "",
                        "time": "0.02",
                        "memory": "9000",
                        "exit_code": 0,
                        "hidden": False,
                    },
                    {
                        "verdict": "runtime_error",
                        "hidden": True,  # Hidden test case: output/error must remain None
                    },
                ],
            },
        )

    transport = httpx.MockTransport(handler)

    async def _run() -> None:
        async with httpx.AsyncClient(transport=transport) as http_client:
            provider = OnlineCompilerProvider(api_key="test_key", http_client=http_client)
            req = CustomTestCheckRequest(
                source_code="print('test')",
                language="python",
                tests=[
                    TestCaseInput(input="1", expected_output="ans1"),
                    TestCaseInput(input="2", expected_output="ans2"),
                ],
            )
            return await provider.run_tests(req)

    res = asyncio.run(_run())

    assert res.verdict == ExecutionVerdict.RUNTIME_ERROR.value
    assert res.passed_tests == 1
    assert res.failed_tests == 1
    # First test is visible
    assert res.tests[0].verdict == ExecutionVerdict.WRONG_ANSWER.value
    assert res.tests[0].actual_output == "wrong\n"
    assert res.tests[0].hidden is False
    # Second test is hidden: output and error must not be fabricated
    assert res.tests[1].verdict == ExecutionVerdict.RUNTIME_ERROR.value
    assert res.tests[1].actual_output is None
    assert res.tests[1].error is None
    assert res.tests[1].hidden is True


def test_missing_api_key_handling() -> None:
    """Test 10: Missing API key raises ConfigurationError."""
    with pytest.raises(ConfigurationError) as exc_info:
        OnlineCompilerClient(api_key="")
    assert "OnlineCompiler API key is missing" in str(exc_info.value)


def test_http_401_handling() -> None:
    """Test 11: HTTP 401 returns AuthenticationError without leaking secrets."""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"error": "Invalid API key"})

    transport = httpx.MockTransport(handler)

    async def _run() -> None:
        async with httpx.AsyncClient(transport=transport) as http_client:
            client = OnlineCompilerClient(api_key="invalid_key", http_client=http_client)
            await client.run_code_sync({"code": "pass"}, timeout_seconds=5)

    with pytest.raises(AuthenticationError) as exc_info:
        asyncio.run(_run())

    # Secret key must not appear in exception message
    assert "invalid_key" not in str(exc_info.value)
    assert "Authentication failed" in str(exc_info.value)


def test_http_429_handling() -> None:
    """Test 12: HTTP 429 returns RateLimitError."""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, json={"error": "Rate limit exceeded"})

    transport = httpx.MockTransport(handler)

    async def _run() -> None:
        async with httpx.AsyncClient(transport=transport) as http_client:
            client = OnlineCompilerClient(api_key="test_key", http_client=http_client)
            await client.run_code_sync({"code": "pass"}, timeout_seconds=5)

    with pytest.raises(RateLimitError) as exc_info:
        asyncio.run(_run())

    assert "rate limit or execution quota exceeded" in str(exc_info.value)


def test_network_timeout_handling() -> None:
    """Test 13: Network timeout raises ExecutionTimeoutError."""
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("Connection timed out during test")

    transport = httpx.MockTransport(handler)

    async def _run() -> None:
        async with httpx.AsyncClient(transport=transport) as http_client:
            client = OnlineCompilerClient(api_key="test_key", http_client=http_client)
            await client.run_code_sync({"code": "pass"}, timeout_seconds=2)

    with pytest.raises(ExecutionTimeoutError) as exc_info:
        asyncio.run(_run())

    assert "timed out" in str(exc_info.value)


def test_invalid_json_handling() -> None:
    """Test 14: Non-JSON / corrupt response raises ExternalServiceError."""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text="<html>502 Bad Gateway</html>")

    transport = httpx.MockTransport(handler)

    async def _run() -> None:
        async with httpx.AsyncClient(transport=transport) as http_client:
            client = OnlineCompilerClient(api_key="test_key", http_client=http_client)
            await client.run_code_sync({"code": "pass"}, timeout_seconds=5)

    with pytest.raises(ExternalServiceError) as exc_info:
        asyncio.run(_run())

    assert "invalid non-JSON response" in str(exc_info.value)
