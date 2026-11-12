"""
Tests for TraceBack Execution API endpoints.
Tests validation rules, size limits, error codes, and successful requests using FastAPI TestClient.
"""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_post_execute_run_success() -> None:
    """Test 15: POST /execute/run succeeds with valid payload."""
    payload = {
        "source_code": "a, b = map(int, input().split())\nprint(a + b)",
        "stdin": "10 20",
        "language": "python",
        "time_limit": 5,
    }
    response = client.post("/execute/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["exit_code"] == 0
    assert data["is_simulated"] is True
    assert data["provider"] == "mock"
    assert "10 20" in data["stdout"]


def test_post_execute_check_custom_tests_success() -> None:
    """Test 16: POST /execute/check-custom-tests succeeds with valid payload."""
    payload = {
        "source_code": "a, b = map(int, input().split())\nprint(a + b)",
        "language": "python",
        "time_limit": 5,
        "checker": "trim",
        "tests": [
            {"input": "10 20", "expected_output": "30"},
            {"input": "5 7", "expected_output": "12"},
        ],
    }
    response = client.post("/execute/check-custom-tests", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "accepted"
    assert data["total_tests"] == 2
    assert data["passed_tests"] == 2
    assert data["failed_tests"] == 0
    assert data["is_simulated"] is True
    assert len(data["tests"]) == 2
    assert data["tests"][0]["verdict"] == "accepted"
    assert data["tests"][0]["expected_output"] == "30"


def test_missing_source_code_rejection() -> None:
    """Test 17: Missing, empty, or whitespace-only source code is rejected with 422."""
    # Blank string
    res1 = client.post("/execute/run", json={"source_code": "   ", "language": "python"})
    assert res1.status_code == 422

    # Empty string
    res2 = client.post("/execute/run", json={"source_code": "", "language": "python"})
    assert res2.status_code == 422

    # Missing field
    res3 = client.post("/execute/run", json={"language": "python"})
    assert res3.status_code == 422


def test_unsupported_language_rejection() -> None:
    """Test 18: Non-python languages are rejected with 422."""
    payload = {
        "source_code": "console.log('hello')",
        "language": "javascript",
    }
    response = client.post("/execute/run", json=payload)
    assert response.status_code == 422
    assert "Unsupported language" in response.text


def test_invalid_checker_rejection() -> None:
    """Test 19: Invalid checker type is rejected with 422."""
    payload = {
        "source_code": "print('hello')",
        "language": "python",
        "checker": "regex_fuzzy_match",
        "tests": [{"input": "1", "expected_output": "1"}],
    }
    response = client.post("/execute/check-custom-tests", json=payload)
    assert response.status_code == 422
    assert "Invalid checker" in response.text


def test_empty_test_list_rejection() -> None:
    """Test 20: Empty test list (tests=[]) is rejected with 422."""
    payload = {
        "source_code": "print('hello')",
        "language": "python",
        "tests": [],
    }
    response = client.post("/execute/check-custom-tests", json=payload)
    assert response.status_code == 422


def test_excessive_test_count_rejection() -> None:
    """Test 21: More tests than ONLINECOMPILER_MAX_TESTS_PER_REQUEST (8) rejected with 422."""
    tests = [{"input": str(i), "expected_output": str(i)} for i in range(9)]
    payload = {
        "source_code": "print(input())",
        "language": "python",
        "tests": tests,
    }
    response = client.post("/execute/check-custom-tests", json=payload)
    assert response.status_code == 422
    assert "Too many test cases" in response.text


def test_oversized_source_code_rejection() -> None:
    """Test 22: Source code exceeding 100 KB in UTF-8 bytes is rejected with 422."""
    huge_code = "# Comment\n" + ("x = 1\n" * 20000)  # ~120 KB > 100 KB
    payload = {
        "source_code": huge_code,
        "language": "python",
    }
    response = client.post("/execute/run", json=payload)
    assert response.status_code == 422
    assert "maximum allowed size" in response.text


def test_oversized_stdin_rejection() -> None:
    """Test 23: Stdin exceeding 100 KB in UTF-8 bytes is rejected with 422."""
    huge_stdin = "A" * (101 * 1024)  # 101 KB
    payload = {
        "source_code": "print(input())",
        "stdin": huge_stdin,
        "language": "python",
    }
    response = client.post("/execute/run", json=payload)
    assert response.status_code == 422
    assert "Standard input exceeds maximum allowed size" in response.text


def test_invalid_execution_time_rejection() -> None:
    """Test 24: Time limit < 1 or > 30 seconds is rejected with 422."""
    # Zero time limit
    res1 = client.post(
        "/execute/run",
        json={"source_code": "print(1)", "time_limit": 0},
    )
    assert res1.status_code == 422

    # Negative time limit
    res2 = client.post(
        "/execute/run",
        json={"source_code": "print(1)", "time_limit": -2},
    )
    assert res2.status_code == 422

    # Exceeding maximum (35s)
    res3 = client.post(
        "/execute/run",
        json={"source_code": "print(1)", "time_limit": 35},
    )
    assert res3.status_code == 422
