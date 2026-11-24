"""
AI Debugging Routes for TraceBack API.
Provides endpoints for requesting AI error diagnostics and code fix assistance.
"""

from fastapi import APIRouter, status
from backend.schemas.ai_debug import AIDebugRequest, AIDebugResponse
from backend.services.ai_debug_service import AIDebugService

router = APIRouter(prefix="/ai", tags=["AI Debugging"])


@router.post(
    "/debug",
    response_model=AIDebugResponse,
    summary="Request AI Code Debugging Assistance",
    description="Analyzes code execution failures, errors, or wrong answers using Gemini AI.",
    status_code=status.HTTP_200_OK,
)
async def debug_code(request: AIDebugRequest) -> AIDebugResponse:
    """
    Diagnose user code failures and generate guidance.
    Handles missing API keys gracefully without returning 500 error codes.
    """
    service = AIDebugService()
    return await service.analyze_failure(request)

