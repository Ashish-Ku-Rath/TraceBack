"""
Execution request and response schemas for TraceBack.
Includes payload validation, size bounds checks, and normalized response structures.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator
from backend.core.config import settings


class ExecutionLanguage(str, Enum):
    """Supported programming languages (Python only for Milestone 2)."""
    PYTHON = "python"


class CheckerType(str, Enum):
    """Supported test output comparison checkers."""
    TRIM = "trim"
    EXACT = "exact"
    TOKENS = "tokens"
    FLOAT = "float"
    ROWS = "rows"


class ExecutionVerdict(str, Enum):
    """Normalized execution verdicts across all providers."""
    ACCEPTED = "accepted"
    WRONG_ANSWER = "wrong_answer"
    RUNTIME_ERROR = "runtime_error"
    COMPILATION_ERROR = "compilation_error"
    TIME_LIMIT_EXCEEDED = "time_limit_exceeded"
    MEMORY_LIMIT_EXCEEDED = "memory_limit_exceeded"
    OUTPUT_LIMIT_EXCEEDED = "output_limit_exceeded"
    SKIPPED = "skipped"
    INCOMPLETE = "incomplete"
    INTERNAL_ERROR = "internal_error"


class TestCaseInput(BaseModel):
    """Input definition for an individual test case."""
    __test__ = False  # Prevent pytest from collecting this model as a test case

    input: str = Field(default="", description="Standard input supplied to the program")
    expected_output: str = Field(..., description="Expected standard output to compare against")

    @field_validator("input")
    @classmethod
    def validate_input(cls, v: str) -> str:
        if "\x00" in v:
            raise ValueError("Test case input must not contain NUL (\\x00) characters.")
        encoded_bytes = len(v.encode("utf-8"))
        if encoded_bytes > settings.MAX_STDIN_BYTES:
            raise ValueError(
                f"Test input exceeds maximum allowed size of {settings.MAX_STDIN_BYTES} bytes."
            )
        return v

    @field_validator("expected_output")
    @classmethod
    def validate_expected_output(cls, v: str) -> str:
        if "\x00" in v:
            raise ValueError("Expected output must not contain NUL (\\x00) characters.")
        encoded_bytes = len(v.encode("utf-8"))
        if encoded_bytes > settings.MAX_EXPECTED_OUTPUT_BYTES:
            raise ValueError(
                f"Expected output exceeds maximum allowed size of {settings.MAX_EXPECTED_OUTPUT_BYTES} bytes."
            )
        return v


class RunCodeRequest(BaseModel):
    """Request payload for running code with arbitrary standard input."""
    source_code: str = Field(..., description="Source code to execute remotely")
    stdin: str = Field(default="", description="Standard input passed to the program")
    language: str = Field(default="python", description="Programming language identifier")
    time_limit: int = Field(
        default=settings.ONLINECOMPILER_DEFAULT_TIME_LIMIT,
        ge=settings.MIN_TIME_LIMIT,
        le=settings.MAX_TIME_LIMIT,
        description="Execution time limit in seconds",
    )

    @field_validator("source_code")
    @classmethod
    def validate_source_code(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Source code cannot be empty.")
        if "\x00" in v:
            raise ValueError("Source code must not contain NUL (\\x00) characters.")
        encoded_bytes = len(v.encode("utf-8"))
        if encoded_bytes > settings.MAX_SOURCE_CODE_BYTES:
            raise ValueError(
                f"Source code exceeds maximum allowed size of {settings.MAX_SOURCE_CODE_BYTES} bytes."
            )
        return v

    @field_validator("stdin")
    @classmethod
    def validate_stdin(cls, v: str) -> str:
        if "\x00" in v:
            raise ValueError("Standard input must not contain NUL (\\x00) characters.")
        encoded_bytes = len(v.encode("utf-8"))
        if encoded_bytes > settings.MAX_STDIN_BYTES:
            raise ValueError(
                f"Standard input exceeds maximum allowed size of {settings.MAX_STDIN_BYTES} bytes."
            )
        return v

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        normalized = v.strip().lower()
        if normalized != ExecutionLanguage.PYTHON.value:
            raise ValueError(
                f"Unsupported language '{v}'. Only '{ExecutionLanguage.PYTHON.value}' is supported in this milestone."
            )
        return normalized


class CustomTestCheckRequest(BaseModel):
    """Request payload for executing code against custom test cases."""
    source_code: str = Field(..., description="Source code to execute remotely")
    language: str = Field(default="python", description="Programming language identifier")
    time_limit: int = Field(
        default=settings.ONLINECOMPILER_DEFAULT_TIME_LIMIT,
        ge=settings.MIN_TIME_LIMIT,
        le=settings.MAX_TIME_LIMIT,
        description="Execution time limit in seconds",
    )
    checker: str = Field(
        default=CheckerType.TRIM.value,
        description="Output comparison checker strategy",
    )
    tests: List[TestCaseInput] = Field(
        ...,
        min_length=1,
        description="List of custom test cases to evaluate against",
    )

    @field_validator("source_code")
    @classmethod
    def validate_source_code(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Source code cannot be empty.")
        if "\x00" in v:
            raise ValueError("Source code must not contain NUL (\\x00) characters.")
        encoded_bytes = len(v.encode("utf-8"))
        if encoded_bytes > settings.MAX_SOURCE_CODE_BYTES:
            raise ValueError(
                f"Source code exceeds maximum allowed size of {settings.MAX_SOURCE_CODE_BYTES} bytes."
            )
        return v

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        normalized = v.strip().lower()
        if normalized != ExecutionLanguage.PYTHON.value:
            raise ValueError(
                f"Unsupported language '{v}'. Only '{ExecutionLanguage.PYTHON.value}' is supported in this milestone."
            )
        return normalized

    @field_validator("checker")
    @classmethod
    def validate_checker(cls, v: str) -> str:
        normalized = v.strip().lower()
        valid_checkers = {c.value for c in CheckerType}
        if normalized not in valid_checkers:
            raise ValueError(
                f"Invalid checker '{v}'. Supported checkers are: {', '.join(sorted(valid_checkers))}."
            )
        return normalized

    @field_validator("tests")
    @classmethod
    def validate_tests_count(cls, v: List[TestCaseInput]) -> List[TestCaseInput]:
        if not v:
            raise ValueError("Test case list cannot be empty.")
        if len(v) > settings.ONLINECOMPILER_MAX_TESTS_PER_REQUEST:
            raise ValueError(
                f"Too many test cases. Maximum allowed is {settings.ONLINECOMPILER_MAX_TESTS_PER_REQUEST}, received {len(v)}."
            )
        return v

    @model_validator(mode="after")
    def validate_combined_payload_size(self) -> "CustomTestCheckRequest":
        total_size = sum(
            len(t.input.encode("utf-8")) + len(t.expected_output.encode("utf-8"))
            for t in self.tests
        )
        if total_size > settings.MAX_COMBINED_TESTS_BYTES:
            raise ValueError(
                f"Combined test cases payload size exceeds limit of {settings.MAX_COMBINED_TESTS_BYTES} bytes."
            )
        return self


# ==============================================================================
# Response Schemas
# ==============================================================================

class RunCodeResponse(BaseModel):
    """Normalized response schema for a single run-code execution."""
    status: str = Field(..., description="Process execution status (e.g. success, runtime_error)")
    stdout: str = Field(default="", description="Standard output captured from the program")
    stderr: str = Field(default="", description="Standard error captured from the program")
    exit_code: Optional[int] = Field(default=0, description="Process termination exit code")
    execution_time: Optional[float] = Field(default=None, description="Execution time in seconds")
    memory_kb: Optional[int] = Field(default=None, description="Peak memory usage in kilobytes")
    provider: str = Field(..., description="Identifier of the execution provider")
    is_simulated: bool = Field(..., description="Whether this execution was simulated")
    truncated: bool = Field(default=False, description="Whether output was truncated by provider")


class TestCaseResult(BaseModel):
    """Normalized outcome for a single test case evaluation."""
    __test__ = False  # Prevent pytest from collecting this model as a test case

    test_index: int = Field(..., description="0-based index of the test case")
    input: Optional[str] = Field(default=None, description="Input provided to the test case")
    expected_output: Optional[str] = Field(default=None, description="Expected output for this test case")
    actual_output: Optional[str] = Field(default=None, description="Actual output captured")
    error: Optional[str] = Field(default=None, description="Error stream or diagnostic information")
    verdict: str = Field(..., description="Normalized verdict for this specific test case")
    execution_time: Optional[float] = Field(default=None, description="Execution time in seconds")
    memory_kb: Optional[int] = Field(default=None, description="Memory used in kilobytes")
    exit_code: Optional[int] = Field(default=None, description="Exit code returned by test execution")
    hidden: bool = Field(default=False, description="Whether this test case was hidden")
    truncated: bool = Field(default=False, description="Whether output was truncated")


class CustomTestCheckResponse(BaseModel):
    """Normalized response schema for multiple custom test case evaluations."""
    verdict: str = Field(..., description="Overall test suite verdict")
    total_tests: int = Field(..., description="Total number of evaluated test cases")
    passed_tests: int = Field(..., description="Number of passed test cases")
    failed_tests: int = Field(..., description="Number of failed test cases")
    tests: List[TestCaseResult] = Field(..., description="Detailed results per test case")
    execution_time: Optional[float] = Field(default=None, description="Total or peak execution time")
    memory_kb: Optional[int] = Field(default=None, description="Peak memory used in kilobytes")
    provider: str = Field(..., description="Identifier of the execution provider")
    is_simulated: bool = Field(..., description="Whether this execution was simulated")


class SubmitCodeRequest(BaseModel):
    """Request payload for submitting code against predefined problem test cases."""
    problem_id: int = Field(..., description="Target problem ID to judge against")
    source_code: str = Field(..., description="Source code to execute remotely")
    language: str = Field(default="python", description="Programming language identifier")
    time_limit: int = Field(
        default=settings.ONLINECOMPILER_DEFAULT_TIME_LIMIT,
        ge=settings.MIN_TIME_LIMIT,
        le=settings.MAX_TIME_LIMIT,
        description="Execution time limit in seconds",
    )

    @field_validator("source_code")
    @classmethod
    def validate_source_code(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Source code cannot be empty.")
        if "\x00" in v:
            raise ValueError("Source code must not contain NUL (\\x00) characters.")
        encoded_bytes = len(v.encode("utf-8"))
        if encoded_bytes > settings.MAX_SOURCE_CODE_BYTES:
            raise ValueError(
                f"Source code exceeds maximum allowed size of {settings.MAX_SOURCE_CODE_BYTES} bytes."
            )
        return v

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        normalized = v.strip().lower()
        if normalized != ExecutionLanguage.PYTHON.value:
            raise ValueError(
                f"Unsupported language '{v}'. Only '{ExecutionLanguage.PYTHON.value}' is supported in this milestone."
            )
        return normalized


class SubmitCodeResponse(BaseModel):
    """Normalized response schema for official problem submission evaluation."""
    problem_id: int = Field(..., description="Target problem ID evaluated")
    verdict: str = Field(..., description="Overall evaluation verdict (accepted, wrong_answer, runtime_error)")
    total_tests: int = Field(..., description="Total number of evaluated test cases")
    passed_tests: int = Field(..., description="Number of passed test cases")
    failed_tests: int = Field(..., description="Number of failed test cases")
    tests: List[TestCaseResult] = Field(..., description="Detailed per-test outcomes")
    execution_time: Optional[float] = Field(default=None, description="Peak execution time in seconds")
    memory_kb: Optional[int] = Field(default=None, description="Peak memory used in kilobytes")
    provider: str = Field(..., description="Identifier of the execution provider")
    is_simulated: bool = Field(..., description="Whether this execution was simulated")
