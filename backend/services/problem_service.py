"""
Problem Service.
Orchestrates business logic for problem creation, querying, filtering, and retrieval.
Decouples database operations from FastAPI route controllers.
"""

import re
from typing import List, Optional
from sqlalchemy import String, cast, func
from sqlalchemy.orm import Session
from backend.core.exceptions import DuplicateSlugError, ProblemNotFoundError
from backend.models.problem import Problem, ProblemExample
from backend.schemas.problem import ProblemCreate


class ProblemService:
    """Service handling DSA problem operations."""

    @staticmethod
    def _generate_slug(title: str) -> str:
        """Derive clean URL slug from title."""
        slug = re.sub(r"[^a-z0-9\-]+", "-", title.strip().lower()).strip("-")
        return slug or "problem"

    @classmethod
    def create_problem(cls, db: Session, problem_in: ProblemCreate) -> Problem:
        """
        Create and persist a new problem with associated sample examples.
        Validates slug uniqueness to prevent collisions.
        """
        target_slug = (
            problem_in.slug.strip().lower()
            if problem_in.slug
            else cls._generate_slug(problem_in.title)
        )

        # Check for slug collision
        existing = db.query(Problem).filter(Problem.slug == target_slug).first()
        if existing is not None:
            raise DuplicateSlugError(
                f"A problem with slug '{target_slug}' already exists."
            )

        problem = Problem(
            title=problem_in.title,
            slug=target_slug,
            description=problem_in.description,
            difficulty=problem_in.difficulty,
            constraints=problem_in.constraints or "",
            tags=problem_in.tags,
        )
        db.add(problem)
        db.flush()  # Obtain auto-generated problem.id

        # Insert associated sample examples
        for ex in problem_in.examples:
            example = ProblemExample(
                problem_id=problem.id,
                input=ex.input,
                expected_output=ex.expected_output,
                explanation=ex.explanation,
            )
            db.add(example)

        db.commit()
        db.refresh(problem)
        return problem

    @staticmethod
    def get_problems(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        difficulty: Optional[str] = None,
        tag: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[Problem]:
        """
        Retrieve problems with optional filtering, search, and pagination.
        """
        query = db.query(Problem)

        if difficulty:
            norm_difficulty = difficulty.strip().lower()
            query = query.filter(func.lower(Problem.difficulty) == norm_difficulty)

        if tag:
            norm_tag = tag.strip().lower()
            query = query.filter(
                func.lower(cast(Problem.tags, String)).like(f"%{norm_tag}%")
            )

        if search:
            norm_search = search.strip().lower()
            query = query.filter(
                func.lower(Problem.title).like(f"%{norm_search}%")
            )

        return query.order_by(Problem.id.asc()).offset(skip).limit(limit).all()

    @staticmethod
    def count_problems(
        db: Session,
        difficulty: Optional[str] = None,
        tag: Optional[str] = None,
        search: Optional[str] = None,
    ) -> int:
        """Count total matching problems matching filters."""
        query = db.query(func.count(Problem.id))

        if difficulty:
            norm_difficulty = difficulty.strip().lower()
            query = query.filter(func.lower(Problem.difficulty) == norm_difficulty)

        if tag:
            norm_tag = tag.strip().lower()
            query = query.filter(
                func.lower(cast(Problem.tags, String)).like(f"%{norm_tag}%")
            )

        if search:
            norm_search = search.strip().lower()
            query = query.filter(
                func.lower(Problem.title).like(f"%{norm_search}%")
            )

        count = query.scalar()
        return int(count) if count is not None else 0

    @staticmethod
    def get_problem_by_id(db: Session, problem_id: int) -> Optional[Problem]:
        """Retrieve problem by primary key ID."""
        return db.query(Problem).filter(Problem.id == problem_id).first()

    @staticmethod
    def get_problem_by_slug(db: Session, slug: str) -> Optional[Problem]:
        """Retrieve problem by unique slug."""
        clean_slug = slug.strip().lower()
        return db.query(Problem).filter(Problem.slug == clean_slug).first()

