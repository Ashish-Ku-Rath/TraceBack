"""
Database declarative base model for TraceBack.
Uses SQLAlchemy 2.x DeclarativeBase.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy declarative database models."""
    pass

