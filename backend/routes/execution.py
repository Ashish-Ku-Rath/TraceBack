"""
Execution Routes for TraceBack API.
Provides endpoints for executing code with custom input, evaluating custom test cases,
and judging official submissions against predefined problem test cases.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.core.exceptions import (
    AuthenticationError,
    ConfigurationError,
    ExecutionTimeoutError,
    ExternalServiceError,
    ProblemNotFoundError,
    RateLimitError,
)
from backend.schemas.execution import (
    CustomTestCheckRequest,
    CustomTestCheckResponse,
    RunCodeRequest,
    RunCodeResponse,
    SubmitCodeRequest,
    SubmitCodeResponse,
)
from backend.services.execution_service import ExecutionService
from database.connection import get_db

router = APIRouter()


@router.post(
    "/run",
    response_model=RunCodeResponse,
    summary="Run Code with Input",
    description="Executes user-submitted source code with optional standard input and returns actual output.",
    status_code=status.HTTP_200_OK,
)
async def run_code(request: RunCodeRequest) -> RunCodeResponse:
    """
    Execute code remotely or via configured provider.
    Never executes user code on the local host.
    """
    try:
        service = ExecutionService()
        return await service.execute_run(request)
    except ConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=exc.message,
        ) from exc
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=exc.message,
        ) from exc
    except RateLimitError as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=exc.message,
        ) from exc
    except ExecutionTimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=exc.message,
        ) from exc
    except ExternalServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=exc.message,
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during code execution.",
        ) from exc


@router.post(
    "/check-custom-tests",
    response_model=CustomTestCheckResponse,
    summary="Evaluate Custom Test Cases",
    description="Evaluates user code against multiple custom test cases and compares actual with expected outputs.",
    status_code=status.HTTP_200_OK,
)
async def check_custom_tests(
    request: CustomTestCheckRequest,
) -> CustomTestCheckResponse:
    """
    Evaluate multiple custom test cases against the user solution.
    Never executes user code on the local host.
    """
    try:
        service = ExecutionService()
        return await service.execute_custom_tests(request)
    except ConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=exc.message,
        ) from exc
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=exc.message,
        ) from exc
    except RateLimitError as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=exc.message,
        ) from exc
    except ExecutionTimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=exc.message,
        ) from exc
    except ExternalServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=exc.message,
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during test evaluation.",
        ) from exc


@router.post(
    "/submit",
    response_model=SubmitCodeResponse,
    summary="Submit Solution for Judging",
    description="Evaluates user code against official predefined test cases for the specified problem.",
    status_code=status.HTTP_200_OK,
)
async def submit_solution(
    request: SubmitCodeRequest,
    db: Session = Depends(get_db),
) -> SubmitCodeResponse:
    """
    Submit problem solution for official judging against database test cases.
    Never executes user code on the local host.
    """
    try:
        service = ExecutionService()
        return await service.submit_problem(request, db=db)
    except ProblemNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.message,
        ) from exc
    except ConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=exc.message,
        ) from exc
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=exc.message,
        ) from exc
    except RateLimitError as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=exc.message,
        ) from exc
    except ExecutionTimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=exc.message,
        ) from exc
    except ExternalServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=exc.message,
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during solution judging.",
        ) from exc
