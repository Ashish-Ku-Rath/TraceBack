"""
Automated unit tests for TraceBack Frontend API Client (Day 4).
Tests problem retrieval, query construction, filters, single problem retrieval,
error handling, and backend connectivity using httpx.MockTransport.
"""

import json
from typing import Dict
import httpx
import pytest
from frontend.api_client import BackendAPIClient

MOCK_PROBLEMS = [
    {
        "id": 1,
        "title": "Two Sum",
        "slug": "two-sum",
        "difficulty": "Easy",
        "tags": ["Array", "Hash Map"],
    },
    {
        "id": 2,
        "title": "Reverse String",
        "slug": "reverse-string",
        "difficulty": "Easy",
        "tags": ["String", "Two Pointers"],
    },
    {
        "id": 3,
        "title": "Valid Parentheses",
        "slug": "valid-parentheses",
        "difficulty": "Medium",
        "tags": ["String", "Stack"],
    },
]

MOCK_PROBLEM_DETAIL = {
    "id": 1,
    "title": "Two Sum",
    "slug": "two-sum",
    "description": "Given an array of integers nums and an integer target...",
    "difficulty": "Easy",
    "constraints": "2 <= nums.length <= 10^4",
    "tags": ["Array", "Hash Map"],
    "created_at": "2026-11-05T12:00:00Z",
    "updated_at": "2026-11-05T12:00:00Z",
    "examples": [
        {
            "id": 1,
            "problem_id": 1,
            "input": "nums = [2,7,11,15], target = 9",
            "expected_output": "[0, 1]",
            "explanation": "Because nums[0] + nums[1] == 9",
        }
    ],
}


def test_successful_problem_retrieval():
    """Test 1: Verify successful problem retrieval with X-Total-Count header."""
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/problems"
        return httpx.Response(
            status_code=200,
            headers={"X-Total-Count": "3"},
            json=MOCK_PROBLEMS,
        )

    client = BackendAPIClient(transport=httpx.MockTransport(handler))
    problems, total, error = client.get_problems()

    assert error is None
    assert len(problems) == 3
    assert total == 3
    assert problems[0]["title"] == "Two Sum"
    assert problems[1]["difficulty"] == "Easy"


def test_search_query_construction():
    """Test 2: Verify search keyword is correctly appended to query parameters."""
    captured_params: Dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured_params.update(dict(request.url.params))
        filtered = [p for p in MOCK_PROBLEMS if "two" in p["title"].lower()]
        return httpx.Response(status_code=200, headers={"X-Total-Count": str(len(filtered))}, json=filtered)

    client = BackendAPIClient(transport=httpx.MockTransport(handler))
    problems, total, error = client.get_problems(search="two")

    assert error is None
    assert captured_params.get("search") == "two"
    assert len(problems) == 1
    assert problems[0]["title"] == "Two Sum"


def test_difficulty_filter():
    """Test 3: Verify difficulty filter param is properly constructed and capitalized."""
    captured_params: Dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured_params.update(dict(request.url.params))
        diff = request.url.params.get("difficulty", "")
        filtered = [p for p in MOCK_PROBLEMS if p["difficulty"].lower() == diff.lower()]
        return httpx.Response(status_code=200, headers={"X-Total-Count": str(len(filtered))}, json=filtered)

    client = BackendAPIClient(transport=httpx.MockTransport(handler))
    problems, total, error = client.get_problems(difficulty="easy")

    assert error is None
    assert captured_params.get("difficulty") == "Easy"
    assert len(problems) == 2
    for p in problems:
        assert p["difficulty"] == "Easy"


def test_tag_filter():
    """Test 4: Verify category tag filter parameter is properly attached."""
    captured_params: Dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured_params.update(dict(request.url.params))
        return httpx.Response(status_code=200, headers={"X-Total-Count": "1"}, json=[MOCK_PROBLEMS[2]])

    client = BackendAPIClient(transport=httpx.MockTransport(handler))
    problems, total, error = client.get_problems(tag="Stack")

    assert error is None
    assert captured_params.get("tag") == "Stack"
    assert len(problems) == 1
    assert "Stack" in problems[0]["tags"]


def test_individual_problem_retrieval():
    """Test 5: Verify fetching single problem by ID and slug."""
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/problems/1":
            return httpx.Response(status_code=200, json=MOCK_PROBLEM_DETAIL)
        if request.url.path == "/problems/slug/two-sum":
            return httpx.Response(status_code=200, json=MOCK_PROBLEM_DETAIL)
        return httpx.Response(status_code=404, json={"detail": "Not found"})

    client = BackendAPIClient(transport=httpx.MockTransport(handler))

    # Test by ID
    p_by_id, err1 = client.get_problem_by_id(1)
    assert err1 is None
    assert p_by_id is not None
    assert p_by_id["title"] == "Two Sum"
    assert len(p_by_id["examples"]) == 1
    assert p_by_id["examples"][0]["expected_output"] == "[0, 1]"

    # Test by Slug
    p_by_slug, err2 = client.get_problem_by_slug("two-sum")
    assert err2 is None
    assert p_by_slug is not None
    assert p_by_slug["slug"] == "two-sum"


def test_backend_connection_failure():
    """Test 6: Verify client handles network and connection drops gracefully."""
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("Connection refused by target server")

    client = BackendAPIClient(transport=httpx.MockTransport(handler))

    # Health check should return False, not raise
    assert client.check_health() is False

    # Problem query should return empty list and error string, not crash
    problems, total, error = client.get_problems()
    assert problems == []
    assert total == 0
    assert error is not None
    assert "Cannot connect to TraceBack backend" in error

    # Detail query should return None and error string
    detail, det_err = client.get_problem_by_id(1)
    assert detail is None
    assert det_err is not None
    assert "Cannot connect to TraceBack backend" in det_err


def test_http_error_handling():
    """Test 7: Verify handling of HTTP 400 and 500 error responses."""
    def handler(request: httpx.Request) -> httpx.Response:
        if "invaliddiff" in str(request.url).lower():
            return httpx.Response(status_code=400, json={"detail": "Invalid difficulty 'InvalidDiff'."})
        return httpx.Response(status_code=500, json={"detail": "Database connection lost."})

    client = BackendAPIClient(transport=httpx.MockTransport(handler))

    problems, total, error = client.get_problems(difficulty="InvalidDiff")
    assert problems == []
    assert total == 0
    assert error == "Invalid difficulty 'InvalidDiff'."

    # Test 500 server error
    problems_500, _, err_500 = client.get_problems()
    assert err_500 == "Database connection lost."


def test_unexpected_response_handling():
    """Test 8: Verify handling of 404 not found and invalid JSON data."""
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/problems/9999":
            return httpx.Response(status_code=404, json={"detail": "Problem not found"})
        return httpx.Response(status_code=200, content=b"Non-JSON response text")

    client = BackendAPIClient(transport=httpx.MockTransport(handler))

    # 404 test
    prob, err_404 = client.get_problem_by_id(9999)
    assert prob is None
    assert "was not found" in err_404

    # Non-JSON test
    prob_list, _, err_json = client.get_problems()
    assert prob_list == []
    assert err_json is not None


def test_statistics_calculation():
    """Test 9: Verify difficulty statistics calculation from backend response."""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code=200, headers={"X-Total-Count": "3"}, json=MOCK_PROBLEMS)

    client = BackendAPIClient(transport=httpx.MockTransport(handler))
    stats, error = client.get_statistics()

    assert error is None
    assert stats["total"] == 3
    assert stats["easy"] == 2
    assert stats["medium"] == 1
    assert stats["hard"] == 0


def test_submit_solution_client():
    """Test 10: Verify BackendAPIClient.submit_solution."""
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/execute/submit"
        data = json.loads(request.content)
        assert data["problem_id"] == 1
        return httpx.Response(
            status_code=200,
            json={
                "problem_id": 1,
                "verdict": "accepted",
                "total_tests": 3,
                "passed_tests": 3,
                "failed_tests": 0,
                "tests": [],
                "is_simulated": True,
            },
        )

    client = BackendAPIClient(transport=httpx.MockTransport(handler))
    res, err = client.submit_solution(problem_id=1, source_code="print('0 1')")
    assert err is None
    assert res["verdict"] == "accepted"


def test_ai_debug_client():
    """Test 11: Verify BackendAPIClient.request_ai_debug."""
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/ai/debug"
        return httpx.Response(
            status_code=200,
            json={
                "explanation": "Off by one error",
                "likely_cause": "Index exceeds bounds",
                "responsible_code_lines": "Line 3",
                "suggested_fix": "Change < to <=",
                "provider": "simulated",
            },
        )

    client = BackendAPIClient(transport=httpx.MockTransport(handler))
    res, err = client.request_ai_debug(source_code="print(1)", stderr="IndexError")
    assert err is None
    assert "Off by one error" in res["explanation"]

