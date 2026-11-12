"""
Tests for TraceBack API core endpoints.
"""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    """Test GET / returns 200 OK and expected greeting message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to TraceBack API",
        "status": "running",
    }


def test_health_endpoint() -> None:
    """Test GET /health returns 200 OK and expected health status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "application": "TraceBack",
    }

