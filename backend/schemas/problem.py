"""
Pydantic schemas for DSA Problems and Sample Examples.
Provides request validation, response serialization, and normalized difficulty/tag handling.
"""

from datetime import datetime
from enum import Enum
import re
from typing import Any, List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProblemDifficulty(str, Enum):
    """Allowed problem difficulty levels."""
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class ProblemExampleBase(BaseModel):
    """Base schema for a sample public test case example."""
    input: str = Field(..., description="Sample input passed to the solution")
    expected_output: str = Field(..., description="Expected sample output")
    explanation: Optional[str] = Field(
        default=None, description="Optional conceptual explanation of this sample case"
    )

    @field_validator("input")
    @classmethod
    def validate_input(cls, v: str) -> str:
        if v is None or not str(v).strip():
            raise ValueError("Sample input cannot be empty.")
        return str(v).strip()

    @field_validator("expected_output")
    @classmethod
    def validate_expected_output(cls, v: str) -> str:
        if v is None or not str(v).strip():
            raise ValueError("Expected output cannot be empty.")
        return str(v).strip()


class ProblemExampleCreate(ProblemExampleBase):
    """Payload schema for creating a new sample example."""
    pass


class ProblemExampleResponse(ProblemExampleBase):
    """Response schema for public sample example."""
    id: int = Field(..., description="Unique example ID")
    problem_id: int = Field(..., description="ID of the associated problem")

    model_config = ConfigDict(from_attributes=True)


class ProblemBase(BaseModel):
    """Common attributes for Problem creation and display."""
    title: str = Field(..., description="Problem title")
    slug: Optional[str] = Field(
        default=None, description="Unique URL-friendly slug identifier"
    )
    description: str = Field(..., description="Full problem statement/description")
    difficulty: str = Field(
        ..., description="Difficulty rating: 'Easy', 'Medium', or 'Hard'"
    )
    constraints: Optional[str] = Field(
        default="", description="Algorithmic input/output constraints"
    )
    tags: List[str] = Field(
        default_factory=list, description="Categorization tags (e.g. Array, Hash Map)"
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Problem title cannot be empty.")
        return v.strip()

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Problem description cannot be empty.")
        return v.strip()

    @field_validator("difficulty")
    @classmethod
    def validate_difficulty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Problem difficulty cannot be empty.")
        normalized = v.strip().capitalize()
        allowed = {
            ProblemDifficulty.EASY.value,
            ProblemDifficulty.MEDIUM.value,
            ProblemDifficulty.HARD.value,
        }
        if normalized not in allowed:
            raise ValueError(
                f"Invalid difficulty '{v}'. Allowed values are: {', '.join(sorted(allowed))}."
            )
        return normalized

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        cleaned = re.sub(r"[^a-z0-9\-]+", "-", v.strip().lower()).strip("-")
        if not cleaned:
            raise ValueError("Problem slug cannot be empty or consist solely of special characters.")
        return cleaned

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: List[str]) -> List[str]:
        """Deduplicate tags while preserving original casing and order."""
        seen = set()
        cleaned: List[str] = []
        for tag in v:
            if isinstance(tag, str):
                t = tag.strip()
                if t and t.lower() not in seen:
                    seen.add(t.lower())
                    cleaned.append(t)
        return cleaned

    @field_validator("constraints", mode="before")
    @classmethod
    def coerce_constraints(cls, v: Any) -> str:
        if isinstance(v, list):
            return "\n".join(str(item) for item in v)
        return str(v).strip() if v is not None else ""


class ProblemCreate(ProblemBase):
    """Payload schema for creating a new DSA problem."""
    examples: List[ProblemExampleCreate] = Field(
        default_factory=list, description="List of public sample test cases"
    )


class ProblemSummaryResponse(BaseModel):
    """
    Clean summary response for problem listing endpoints.
    Excludes lengthy descriptions and full example lists to minimize network payload.
    """
    id: int = Field(..., description="Unique problem ID")
    title: str = Field(..., description="Problem title")
    slug: str = Field(..., description="Unique URL slug")
    difficulty: str = Field(..., description="Problem difficulty")
    tags: List[str] = Field(default_factory=list, description="Problem tags")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ProblemDetailResponse(BaseModel):
    """
    Full problem details response including description, constraints, and public sample examples.
    """
    id: int = Field(..., description="Unique problem ID")
    title: str = Field(..., description="Problem title")
    slug: str = Field(..., description="Unique URL slug")
    description: str = Field(..., description="Full problem description")
    difficulty: str = Field(..., description="Problem difficulty")
    constraints: Optional[str] = Field(default=None, description="Problem constraints")
    tags: List[str] = Field(default_factory=list, description="Problem tags")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Record last updated timestamp")
    examples: List[ProblemExampleResponse] = Field(
        default_factory=list, description="Public sample examples"
    )

    model_config = ConfigDict(from_attributes=True)

