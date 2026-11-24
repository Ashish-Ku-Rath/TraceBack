"""
Tests for TraceBack AI Debug Assistant API endpoints and service.
Verifies error diagnosis, code suggestions, simulated mock fallbacks,
and graceful handling when GEMINI_API_KEY is unconfigured.
"""

from fastapi.testclient import TestClient
from backend.main import app
from backend.core.config import settings

client = TestClient(app)


def test_ai_debug_endpoint_unconfigured_or_success() -> None:
    """Test AI debug endpoint returns structured diagnosis without crashing."""
    payload = {
        "source_code": "def solve():\n    nums = [1, 2]\n    return nums[5]\nsolve()",
        "stderr": "IndexError: list index out of range\n  File 'solution.py', line 3",
        "stdout": "",
        "problem_title": "Two Sum",
        "problem_description": "Given an array of integers...",
    }
    response = client.post("/ai/debug", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "explanation" in data
    assert "likely_cause" in data
    assert "responsible_code" in data
    assert "suggested_fix" in data
    assert data["status"] in ("success", "unconfigured", "error")


def test_ai_debug_endpoint_simulated_with_mock_key(monkeypatch) -> None:
    """Test simulated diagnosis when GEMINI_API_KEY is 'mock'."""
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "mock")

    payload = {
        "source_code": "def solve():\n    nums = [1, 2]\n    return nums[5]\nsolve()",
        "stderr": "IndexError: list index out of range",
        "stdout": "",
        "problem_title": "Two Sum",
    }
    response = client.post("/ai/debug", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "IndexError" in data["explanation"]
    assert data["is_mock"] is True
    assert data["corrected_code"] is not None


def test_ai_debug_endpoint_empty_stderr_handling() -> None:
    """Test AI debug endpoint works even if stderr is empty (e.g. wrong answer or logic error)."""
    payload = {
        "source_code": "print('wrong answer')",
        "stderr": "",
        "stdout": "wrong answer",
        "problem_title": "Two Sum",
    }
    response = client.post("/ai/debug", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["explanation"]) > 0


def test_ai_debug_endpoint_validation() -> None:
    """Test AI debug endpoint rejects missing required source_code."""
    payload = {
        "stderr": "Some error",
    }
    response = client.post("/ai/debug", json=payload)
    assert response.status_code == 422
