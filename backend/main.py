"""
TraceBack API - Main Application Entrypoint
FastAPI application for TraceBack: The Intelligent Coding & Debugging Assistant.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.core.config import settings
from backend.routes.execution import router as execution_router
from backend.routes.problems import router as problems_router
from backend.schemas.system import HealthResponse, RootResponse
from database.connection import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context: initialize database tables safely on startup."""
    init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Mount API routers
app.include_router(execution_router, prefix="/execute", tags=["Execution"])
app.include_router(problems_router)



@app.get(
    "/",
    response_model=RootResponse,
    summary="Root Endpoint",
    description="Returns welcome message and operational status of the TraceBack API.",
    tags=["System"],
)
async def read_root() -> dict[str, str]:
    """Root endpoint greeting and API status."""
    return {
        "message": "Welcome to TraceBack API",
        "status": "running",
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Returns health status of the TraceBack application.",
    tags=["System"],
)
async def health_check() -> dict[str, str]:
    """Health check endpoint to verify backend operational readiness."""
    return {
        "status": "healthy",
        "application": "TraceBack",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
