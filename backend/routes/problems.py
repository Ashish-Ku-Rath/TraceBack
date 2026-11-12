"""
Problem Management Routes for TraceBack API.
Provides endpoints for creating, retrieving, filtering, and searching DSA problems.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from backend.core.exceptions import DuplicateSlugError
from backend.schemas.problem import (
    ProblemCreate,
    ProblemDetailResponse,
    ProblemDifficulty,
    ProblemSummaryResponse,
)
from backend.services.problem_service import ProblemService
from database.connection import get_db

router = APIRouter(prefix="/problems", tags=["Problems"])


@router.post(
    "",
    response_model=ProblemDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Problem",
    description="Registers a new DSA problem with statement, difficulty, constraints, tags, and public sample examples.",
)
def create_problem(
    problem_in: ProblemCreate,
    db: Session = Depends(get_db),
) -> ProblemDetailResponse:
    """Create a new problem record in the database."""
    try:
        problem = ProblemService.create_problem(db=db, problem_in=problem_in)
        return ProblemDetailResponse.model_validate(problem)
    except DuplicateSlugError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.message,
        ) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the problem.",
        ) from exc


@router.get(
    "",
    response_model=List[ProblemSummaryResponse],
    status_code=status.HTTP_200_OK,
    summary="List Problems",
    description="Retrieves a paginated list of problems with optional filtering by difficulty, tag, or title search.",
)
def list_problems(
    response: Response,
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return"),
    difficulty: Optional[str] = Query(
        None, description="Filter by difficulty level: Easy, Medium, or Hard"
    ),
    tag: Optional[str] = Query(None, description="Filter by category tag"),
    search: Optional[str] = Query(None, description="Search term matching problem title"),
    db: Session = Depends(get_db),
) -> List[ProblemSummaryResponse]:
    """Retrieve filtered problem summaries."""
    # Validate difficulty filter if provided
    if difficulty:
        normalized_diff = difficulty.strip().capitalize()
        allowed = {d.value for d in ProblemDifficulty}
        if normalized_diff not in allowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid difficulty '{difficulty}'. Allowed values: {', '.join(sorted(allowed))}.",
            )
        difficulty = normalized_diff

    total = ProblemService.count_problems(
        db=db, difficulty=difficulty, tag=tag, search=search
    )
    problems = ProblemService.get_problems(
        db=db,
        skip=skip,
        limit=limit,
        difficulty=difficulty,
        tag=tag,
        search=search,
    )

    response.headers["X-Total-Count"] = str(total)
    return [ProblemSummaryResponse.model_validate(p) for p in problems]


@router.get(
    "/{problem_id}",
    response_model=ProblemDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Problem by ID",
    description="Retrieves full problem details including description, constraints, and public sample examples.",
)
def get_problem_by_id(
    problem_id: int,
    db: Session = Depends(get_db),
) -> ProblemDetailResponse:
    """Retrieve an individual problem by its primary key ID."""
    problem = ProblemService.get_problem_by_id(db=db, problem_id=problem_id)
    if problem is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Problem with ID {problem_id} not found.",
        )
    return ProblemDetailResponse.model_validate(problem)


@router.get(
    "/slug/{slug}",
    response_model=ProblemDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Problem by Slug",
    description="Retrieves full problem details using its unique URL slug identifier.",
)
def get_problem_by_slug(
    slug: str,
    db: Session = Depends(get_db),
) -> ProblemDetailResponse:
    """Retrieve an individual problem by unique slug."""
    clean_slug = slug.strip().lower()
    problem = ProblemService.get_problem_by_slug(db=db, slug=clean_slug)
    if problem is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Problem with slug '{slug}' not found.",
        )
    return ProblemDetailResponse.model_validate(problem)

