"""
System and health check schemas for TraceBack API.
"""

from pydantic import BaseModel, Field


class RootResponse(BaseModel):
    """Response schema for the root endpoint."""
    message: str = Field(..., description="Greeting message from the API")
    status: str = Field(..., description="Operational status of the API")


class HealthResponse(BaseModel):
    """Response schema for the health check endpoint."""
    status: str = Field(..., description="Health status indicator")
    application: str = Field(..., description="Application name")

