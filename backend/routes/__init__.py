"""
FastAPI route definitions and endpoints.
"""

from backend.routes.execution import router as execution_router
from backend.routes.problems import router as problems_router

__all__ = ["execution_router", "problems_router"]
