"""
FastAPI Backend API Client for TraceBack frontend.
Provides synchronous HTTP communication with the backend using HTTPX.
Includes error handling, timeout control, and data extraction.
"""

from typing import Any, Dict, List, Optional, Tuple
import httpx
from frontend.config import BACKEND_BASE_URL


class BackendAPIClient:
    """Client for communicating with the TraceBack FastAPI backend."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: float = 5.0,
        transport: Optional[httpx.BaseTransport] = None,
    ) -> None:
        self.base_url = (base_url or BACKEND_BASE_URL).rstrip("/")
        self.timeout = timeout
        self.transport = transport

    def _get_client(self, timeout: Optional[float] = None) -> httpx.Client:
        return httpx.Client(
            base_url=self.base_url,
            timeout=timeout if timeout is not None else self.timeout,
            transport=self.transport,
        )

    def check_health(self) -> bool:
        """
        Verify backend availability by probing GET /health.
        Returns True if backend is healthy, False otherwise.
        """
        try:
            with self._get_client() as client:
                response = client.get("/health")
                if response.status_code == 200:
                    data = response.json()
                    return data.get("status") == "healthy"
                return False
        except Exception:
            return False

    def get_problems(
        self,
        skip: int = 0,
        limit: int = 50,
        difficulty: Optional[str] = None,
        tag: Optional[str] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[Dict[str, Any]], int, Optional[str]]:
        """
        Fetch problem summaries with optional filtering, search, and pagination.
        Returns:
            Tuple of (problems_list, total_count, error_message)
        """
        params: Dict[str, Any] = {"skip": skip, "limit": limit}
        if difficulty and difficulty.strip() and difficulty.lower() != "all":
            params["difficulty"] = difficulty.strip().capitalize()
        if tag and tag.strip() and tag.lower() != "all":
            params["tag"] = tag.strip()
        if search and search.strip():
            params["search"] = search.strip()

        try:
            with self._get_client() as client:
                response = client.get("/problems", params=params)

                if response.status_code == 200:
                    data = response.json()
                    total_header = response.headers.get("X-Total-Count")
                    total_count = int(total_header) if total_header and total_header.isdigit() else len(data)
                    return data, total_count, None

                error_detail = f"Backend returned status {response.status_code}"
                try:
                    err_json = response.json()
                    if "detail" in err_json:
                        error_detail = err_json["detail"]
                except Exception:
                    pass
                return [], 0, error_detail

        except (httpx.ConnectError, httpx.TimeoutException) as exc:
            return [], 0, (
                f"Cannot connect to TraceBack backend at {self.base_url}. "
                "Please verify that the FastAPI backend server is running."
            )
        except Exception as exc:
            return [], 0, f"Unexpected error while querying problems: {str(exc)}"

    def get_problem_by_id(
        self, problem_id: int
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Fetch full problem details including public sample examples by ID.
        Returns:
            Tuple of (problem_dict, error_message)
        """
        try:
            with self._get_client() as client:
                response = client.get(f"/problems/{problem_id}")

                if response.status_code == 200:
                    return response.json(), None
                if response.status_code == 404:
                    return None, f"Problem #{problem_id} was not found."

                error_detail = f"Backend returned status {response.status_code}"
                try:
                    err_json = response.json()
                    if "detail" in err_json:
                        error_detail = err_json["detail"]
                except Exception:
                    pass
                return None, error_detail

        except (httpx.ConnectError, httpx.TimeoutException):
            return None, (
                f"Cannot connect to TraceBack backend at {self.base_url}. "
                "Please verify that the FastAPI backend server is running."
            )
        except Exception as exc:
            return None, f"Unexpected error while fetching problem: {str(exc)}"

    def get_problem_by_slug(
        self, slug: str
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Fetch full problem details by unique slug.
        Returns:
            Tuple of (problem_dict, error_message)
        """
        try:
            with self._get_client() as client:
                response = client.get(f"/problems/slug/{slug}")

                if response.status_code == 200:
                    return response.json(), None
                if response.status_code == 404:
                    return None, f"Problem with slug '{slug}' was not found."

                error_detail = f"Backend returned status {response.status_code}"
                try:
                    err_json = response.json()
                    if "detail" in err_json:
                        error_detail = err_json["detail"]
                except Exception:
                    pass
                return None, error_detail

        except (httpx.ConnectError, httpx.TimeoutException):
            return None, (
                f"Cannot connect to TraceBack backend at {self.base_url}. "
                "Please verify that the FastAPI backend server is running."
            )
        except Exception as exc:
            return None, f"Unexpected error while fetching problem: {str(exc)}"

    def get_statistics(self) -> Tuple[Dict[str, int], Optional[str]]:
        """
        Calculate actual problem statistics by difficulty directly from the backend.
        Never fabricates or hardcodes numbers.
        Returns:
            Tuple of (stats_dict, error_message)
        """
        problems, total, error = self.get_problems(skip=0, limit=100)
        if error:
            return {"total": 0, "easy": 0, "medium": 0, "hard": 0}, error

        # If there are more problems than 100, fetch the remaining batches
        all_problems = list(problems)
        while len(all_problems) < total and len(all_problems) < 1000:
            batch, _, batch_err = self.get_problems(skip=len(all_problems), limit=100)
            if batch_err or not batch:
                break
            all_problems.extend(batch)

        easy_count = sum(1 for p in all_problems if p.get("difficulty", "").lower() == "easy")
        med_count = sum(1 for p in all_problems if p.get("difficulty", "").lower() == "medium")
        hard_count = sum(1 for p in all_problems if p.get("difficulty", "").lower() == "hard")

        return {
            "total": total,
            "easy": easy_count,
            "medium": med_count,
            "hard": hard_count,
        }, None

    def run_code(
        self,
        source_code: str,
        stdin: str = "",
        language: str = "python",
        time_limit: int = 5,
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Execute source code remotely with standard input.
        Returns:
            Tuple of (response_dict, error_message)
        """
        payload = {
            "source_code": source_code,
            "stdin": stdin,
            "language": language,
            "time_limit": time_limit,
        }
        try:
            with self._get_client() as client:
                response = client.post("/execute/run", json=payload)
                if response.status_code == 200:
                    return response.json(), None
                error_detail = f"Execution failed with status {response.status_code}"
                try:
                    err_json = response.json()
                    if "detail" in err_json:
                        error_detail = err_json["detail"]
                except Exception:
                    pass
                return None, error_detail
        except (httpx.ConnectError, httpx.TimeoutException):
            return None, (
                f"Cannot connect to execution backend at {self.base_url}. "
                "Ensure FastAPI backend server is active."
            )
        except Exception as exc:
            return None, f"Execution request error: {str(exc)}"

    def check_custom_tests(
        self,
        source_code: str,
        tests: List[Dict[str, str]],
        checker: str = "trim",
        language: str = "python",
        time_limit: int = 5,
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Execute source code against custom test cases.
        Returns:
            Tuple of (response_dict, error_message)
        """
        payload = {
            "source_code": source_code,
            "language": language,
            "time_limit": time_limit,
            "checker": checker,
            "tests": tests,
        }
        try:
            with self._get_client() as client:
                response = client.post("/execute/check-custom-tests", json=payload)
                if response.status_code == 200:
                    return response.json(), None
                error_detail = f"Custom test evaluation failed ({response.status_code})"
                try:
                    err_json = response.json()
                    if "detail" in err_json:
                        error_detail = err_json["detail"]
                except Exception:
                    pass
                return None, error_detail
        except (httpx.ConnectError, httpx.TimeoutException):
            return None, (
                f"Cannot connect to execution backend at {self.base_url}. "
                "Ensure FastAPI backend server is active."
            )
        except Exception as exc:
            return None, f"Custom test request error: {str(exc)}"

    def submit_solution(
        self,
        problem_id: int,
        source_code: str,
        language: str = "python",
        time_limit: int = 5,
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Submit solution for judging against official problem test cases.
        Returns:
            Tuple of (response_dict, error_message)
        """
        payload = {
            "problem_id": problem_id,
            "source_code": source_code,
            "language": language,
            "time_limit": time_limit,
        }
        try:
            with self._get_client() as client:
                response = client.post("/execute/submit", json=payload)
                if response.status_code == 200:
                    return response.json(), None
                error_detail = f"Submission judging failed ({response.status_code})"
                try:
                    err_json = response.json()
                    if "detail" in err_json:
                        error_detail = err_json["detail"]
                except Exception:
                    pass
                return None, error_detail
        except (httpx.ConnectError, httpx.TimeoutException):
            return None, (
                f"Cannot connect to execution backend at {self.base_url}. "
                "Ensure FastAPI backend server is active."
            )
        except Exception as exc:
            return None, f"Submission request error: {str(exc)}"

    def request_ai_debug(
        self,
        source_code: str,
        problem_title: str = "",
        problem_description: str = "",
        error_message: Optional[str] = None,
        stdout: Optional[str] = "",
        stderr: Optional[str] = "",
        stdin: Optional[str] = "",
        language: str = "python",
        help_mode: str = "find_bug",
        failure_type: str = "unknown",
        expected_output: Optional[str] = None,
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Request AI debugging diagnosis and guidance from Gemini.

        Returns:
            Tuple of (response_dict, error_message)
        """

        payload = {
            "problem_title": problem_title,
            "problem_description": problem_description,
            "source_code": source_code,
            "error_message": error_message,
            "stdout": stdout or "",
            "stderr": stderr or "",
            "stdin": stdin or "",
            "language": language,
            "help_mode": help_mode,
            "failure_type": failure_type,
            "expected_output": expected_output,
        }

        try:
            with self._get_client(timeout=45.0) as client:
                response = client.post("/ai/debug", json=payload)

                if response.status_code == 200:
                    return response.json(), None

                error_detail = (
                    f"AI Debugging request failed ({response.status_code})"
                )

                try:
                    err_json = response.json()
                    if "detail" in err_json:
                        error_detail = err_json["detail"]
                except Exception:
                    pass

                return None, error_detail

        except (httpx.ConnectError, httpx.TimeoutException):
            return None, (
                f"Cannot connect to AI service at {self.base_url}. "
                "Ensure FastAPI backend server is active."
            )

        except Exception as exc:
            return None, f"AI Debug request error: {str(exc)}"


# Default shared client instance
api_client = BackendAPIClient()
