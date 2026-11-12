"""
Database connection and session management for TraceBack.
Provides SQLAlchemy 2.x engine, sessionmaker, table initialization, and FastAPI dependency.
"""

from pathlib import Path
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from backend.core.config import settings
from database.base import Base

# Ensure parent directory for local SQLite database file exists
if settings.DATABASE_URL.startswith("sqlite:///"):
    raw_path = settings.DATABASE_URL.replace("sqlite:///", "")
    db_file = Path(raw_path.split("?")[0])
    if db_file.parent and not db_file.parent.exists():
        db_file.parent.mkdir(parents=True, exist_ok=True)

# Build SQLite-optimized engine
connect_args = (
    {"check_same_thread": False}
    if settings.DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False,
    future=True,
)

# Thread-safe session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)


def init_db(engine_override: Engine | None = None) -> None:
    """
    Safely create database tables if they do not already exist.
    Never drops, truncates, or overwrites existing data or tables.
    """
    target_engine = engine_override or engine

    # Ensure models are imported so their metadata is registered with Base
    import backend.models  # noqa: F401

    Base.metadata.create_all(bind=target_engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a SQLAlchemy database session per request
    and guarantees proper closing in all execution paths.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

