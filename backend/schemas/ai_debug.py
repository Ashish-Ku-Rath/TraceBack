"""
Schemas for TraceBack AI Debugging Assistant.
Supports multiple debugging assistance modes and structured AI responses.
"""

from typing import Literal, Optional
from pydantic import BaseModel, Field


# Assistance modes selected by the user
AIDebugMode = Literal[
    "explain_error",
    "hint",
    "explain_algorithm",
    "find_bug",
    "corrected_code",
]

# Types of programming failures
AIFailureType = Literal[
    "syntax_error",
    "runtime_error",
    "wrong_answer",
    "compilation_error",
    "time_limit_exceeded",
    "unknown",
]


class AIDebugRequest(BaseModel):
    """Request payload containing user code and debugging context."""

    problem_title: str = Field(
        ...,
        description="Title of the DSA problem",
    )

    problem_description: str = Field(
        default="",
        description="Problem statement and constraints",
    )

    source_code: str = Field(
        ...,
        description="Complete source code submitted by the user",
    )

    language: str = Field(
        default="python",
        description="Programming language",
    )

    help_mode: AIDebugMode = Field(
        default="find_bug",
        description="Type of debugging assistance requested",
    )

    failure_type: AIFailureType = Field(
        default="unknown",
        description="Category of programming failure",
    )

    error_message: Optional[str] = Field(
        default=None,
        description="Error message or execution verdict",
    )

    stdin: Optional[str] = Field(
        default="",
        description="Standard input provided to the program",
    )

    stdout: Optional[str] = Field(
        default="",
        description="Actual standard output",
    )

    stderr: Optional[str] = Field(
        default="",
        description="Runtime or syntax error traceback",
    )

    expected_output: Optional[str] = Field(
        default=None,
        description="Expected output, particularly useful for Wrong Answer",
    )


class AIDebugResponse(BaseModel):
    """Structured diagnostic response returned by TraceBack AI."""

    status: str = Field(
        ...,
        description="Diagnostic status: success, unconfigured, or error",
    )

    help_mode: AIDebugMode = Field(
        default="find_bug",
        description="Assistance mode used for the diagnosis",
    )

    explanation: str = Field(
        ...,
        description="Plain-English explanation of the issue",
    )

    likely_cause: str = Field(
        ...,
        description="Most probable root cause",
    )

    responsible_code: str = Field(
        ...,
        description="Problematic line or logic block",
    )

    suggested_fix: str = Field(
        ...,
        description="Step-by-step guidance to resolve the issue",
    )

    corrected_code: Optional[str] = Field(
        default=None,
        description="Corrected code when requested or useful",
    )

    is_mock: bool = Field(
        default=False,
        description="Whether the response is simulated",
    )