"""
SQLAlchemy models for Problem and ProblemExample.
Defines normalized database structure for DSA problems and public sample examples.
"""

from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship
from database.base import Base


class Problem(Base):
    """
    DSA Problem database entity.
    Stores metadata, problem statement, constraints, difficulty, and tags.
    """
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String(50), nullable=False, index=True)
    constraints = Column(Text, nullable=True, default="")
    tags = Column(JSON, nullable=False, default=list)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationship to public sample examples
    examples = relationship(
        "ProblemExample",
        back_populates="problem",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="ProblemExample.id",
    )

    def __repr__(self) -> str:
        return f"<Problem id={self.id} slug='{self.slug}' difficulty='{self.difficulty}'>"


class ProblemExample(Base):
    """
    Public sample test case and explanation for a problem.
    Note: These are public examples displayed in the UI, NOT official hidden judge test cases.
    """
    __tablename__ = "problem_examples"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    problem_id = Column(
        Integer,
        ForeignKey("problems.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    input = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)

    problem = relationship("Problem", back_populates="examples")

    def __repr__(self) -> str:
        return f"<ProblemExample id={self.id} problem_id={self.problem_id}>"

