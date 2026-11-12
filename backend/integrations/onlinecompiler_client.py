"""
OnlineCompiler REST API Client.
Handles secure HTTP communication with https://api.onlinecompiler.io.

SECURITY MANDATES:
1. Never log or leak the Authorization header or API key.
2. Cleanly map network and HTTP error codes to domain exceptions.
3. No automatic retries on code execution requests (prevents quota exhaustion).
"""

import json
from typing import Any, Dict, Optional
import httpx
from backend.core.config import settings
from backend.core.exceptions import (
    AuthenticationError,
    ConfigurationError,
    ExecutionTimeoutError,
    ExternalServiceError,
    RateLimitError,
)


class OnlineCompilerClient:
    """Async HTTP Client for OnlineCompiler.io REST API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        self.api_key = api_key or settings.ONLINECOMPILER_API_KEY
        if not self.api_key or not self.api_key.strip():
            raise ConfigurationError(
                "OnlineCompiler API key is missing. Set ONLINECOMPILER_API_KEY in environment or use mock provider."
            )

        self.base_url = (base_url or settings.ONLINECOMPILER_API_URL).rstrip("/")
        self._http_client = http_client

    def _get_headers(self) -> Dict[str, str]:
        """
        Construct headers without logging secret credentials.
        OnlineCompiler expects the raw API key directly in the Authorization header.
        """
        return {
            "Authorization": self.api_key.strip(),
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def _post_request(
        self,
        endpoint: str,
        payload: Dict[str, Any],
        timeout_seconds: float,
    ) -> Dict[str, Any]:
        """
        Send POST request to OnlineCompiler and handle HTTP and network failure modes.
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()

        # If a client was injected (e.g. for testing with MockTransport), use it without closing
        should_close = False
        client = self._http_client
        if client is None:
            client = httpx.AsyncClient(timeout=timeout_seconds)
            should_close = True

        try:
            response = await client.post(
                url,
                json=payload,
                headers=headers,
                timeout=timeout_seconds,
            )
        except httpx.TimeoutException as exc:
            raise ExecutionTimeoutError(
                f"Execution request to OnlineCompiler timed out after {timeout_seconds} seconds."
            ) from exc
        except httpx.NetworkError as exc:
            raise ExternalServiceError(
                "Network failure while connecting to OnlineCompiler API."
            ) from exc
        except Exception as exc:
            raise ExternalServiceError(
                f"Unexpected error communicating with execution provider: {str(exc)}"
            ) from exc
        finally:
            if should_close:
                await client.aclose()

        # Handle HTTP status codes
        if response.status_code in (401, 403):
            raise AuthenticationError(
                "Authentication failed with OnlineCompiler. Please check your API key."
            )

        if response.status_code == 429:
            raise RateLimitError(
                "OnlineCompiler API rate limit or execution quota exceeded. Please wait before retrying."
            )

        if response.status_code >= 500:
            raise ExternalServiceError(
                f"OnlineCompiler service returned an internal server error (HTTP {response.status_code})."
            )

        if response.status_code >= 400:
            try:
                err_data = response.json()
                detail = err_data.get("error") or err_data.get("detail") or response.text
            except Exception:
                detail = response.text
            raise ExternalServiceError(
                f"OnlineCompiler rejected the request (HTTP {response.status_code}): {detail}"
            )

        try:
            return response.json()
        except (json.JSONDecodeError, ValueError) as exc:
            raise ExternalServiceError(
                "OnlineCompiler returned an invalid non-JSON response."
            ) from exc

    async def run_code_sync(
        self,
        payload: Dict[str, Any],
        timeout_seconds: float,
    ) -> Dict[str, Any]:
        """Call POST /api/run-code-sync/"""
        return await self._post_request(
            endpoint="/api/run-code-sync/",
            payload=payload,
            timeout_seconds=timeout_seconds,
        )

    async def run_tests(
        self,
        payload: Dict[str, Any],
        timeout_seconds: float,
    ) -> Dict[str, Any]:
        """Call POST /api/run-tests/"""
        return await self._post_request(
            endpoint="/api/run-tests/",
            payload=payload,
            timeout_seconds=timeout_seconds,
        )

