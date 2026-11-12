"""
Execution Provider Factory.
Instantiates and configures execution providers based on system configuration.

FACTORY RULES:
1. Default provider is MockProvider.
2. Never silently fallback from real execution to mock.
3. Raise ConfigurationError if OnlineCompiler is requested without an API key.
4. Keep provider selection decoupled from API clients.
"""

from typing import Optional
import httpx
from backend.core.config import settings
from backend.core.exceptions import ConfigurationError
from backend.services.providers.base_provider import BaseExecutionProvider
from backend.services.providers.mock_provider import MockProvider
from backend.services.providers.onlinecompiler_provider import OnlineCompilerProvider


class ProviderFactory:
    """Factory for creating execution provider instances."""

    @staticmethod
    def get_provider(
        provider_name: Optional[str] = None,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> BaseExecutionProvider:
        """
        Resolve and return the appropriate execution provider.
        Reads from settings.EXECUTION_PROVIDER by default.
        """
        selected = (provider_name or settings.EXECUTION_PROVIDER).strip().lower()

        if selected == "mock":
            return MockProvider()

        if selected == "onlinecompiler":
            api_key = settings.ONLINECOMPILER_API_KEY
            if not api_key or not api_key.strip():
                raise ConfigurationError(
                    "OnlineCompiler execution provider is selected, but ONLINECOMPILER_API_KEY is not configured. "
                    "Please provide an API key in the environment or set EXECUTION_PROVIDER=mock."
                )

            return OnlineCompilerProvider(
                api_key=api_key,
                api_url=settings.ONLINECOMPILER_API_URL,
                compiler_id=settings.ONLINECOMPILER_PYTHON_COMPILER,
                http_client=http_client,
            )

        raise ConfigurationError(
            f"Unsupported execution provider '{selected}'. Supported providers are: 'mock', 'onlinecompiler'."
        )

