"""
Application core configuration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory pointing to workspace root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Database file location
DEFAULT_DB_PATH = BASE_DIR / "database" / "traceback.db"

# Load environment variables from .env if present
load_dotenv(BASE_DIR / ".env")


class Settings:
    """Core application settings."""
    PROJECT_NAME: str = "TraceBack API"
    VERSION: str = "0.3.0"
    DESCRIPTION: str = (
        "Backend API for TraceBack — The Intelligent Coding & Debugging Assistant"
    )

    # Database configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH.as_posix()}"
    )

    # Provider Selection: "mock" (default) or "onlinecompiler"
    EXECUTION_PROVIDER: str = os.getenv("EXECUTION_PROVIDER", "mock").strip().lower()

    # OnlineCompiler API configuration
    ONLINECOMPILER_API_URL: str = os.getenv(
        "ONLINECOMPILER_API_URL", "https://api.onlinecompiler.io"
    ).rstrip("/")
    ONLINECOMPILER_API_KEY: str | None = os.getenv("ONLINECOMPILER_API_KEY")
    ONLINECOMPILER_PYTHON_COMPILER: str = os.getenv(
        "ONLINECOMPILER_PYTHON_COMPILER", "python-3.14"
    )

    # Configurable limits based on execution provider specs
    ONLINECOMPILER_MAX_TESTS_PER_REQUEST: int = int(
        os.getenv("ONLINECOMPILER_MAX_TESTS_PER_REQUEST", "8")
    )
    ONLINECOMPILER_DEFAULT_TIME_LIMIT: int = int(
        os.getenv("ONLINECOMPILER_DEFAULT_TIME_LIMIT", "5")
    )

    # Payload limits (in bytes)
    MAX_SOURCE_CODE_BYTES: int = int(os.getenv("MAX_SOURCE_CODE_BYTES", str(100 * 1024)))  # 100 KB
    MAX_STDIN_BYTES: int = int(os.getenv("MAX_STDIN_BYTES", str(100 * 1024)))              # 100 KB
    MAX_EXPECTED_OUTPUT_BYTES: int = int(os.getenv("MAX_EXPECTED_OUTPUT_BYTES", str(64 * 1024))) # 64 KB
    MAX_COMBINED_TESTS_BYTES: int = int(os.getenv("MAX_COMBINED_TESTS_BYTES", str(512 * 1024))) # 512 KB

    # Time limits (seconds)
    MIN_TIME_LIMIT: int = 1
    MAX_TIME_LIMIT: int = 30
    HTTP_TIMEOUT_BUFFER_SECONDS: float = 5.0

    # Future integration settings (Milestone 3+)
        # Google Gemini AI configuration
    GEMINI_API_KEY: str | None = (
        (os.getenv("GEMINI_API_KEY") or "").strip() or None
    )

    GEMINI_MODEL: str = os.getenv(
        "GEMINI_MODEL", "gemini-3.8-flash"
    ).strip()

    GEMINI_TIMEOUT_SECONDS: float = float(
        os.getenv("GEMINI_TIMEOUT_SECONDS", "30")
    )

    # Judge0 configuration (future use)
    JUDGE0_API_URL: str | None = os.getenv("JUDGE0_API_URL")
    JUDGE0_API_KEY: str | None = os.getenv("JUDGE0_API_KEY")


settings = Settings()
