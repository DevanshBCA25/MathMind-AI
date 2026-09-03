from __future__ import annotations

from typing import Any, Dict

from src.config.settings import (
    get_api_key,
    get_model_name,
    has_api_key,
    OLLAMA_BASE_URL,
)


SUPPORTED_PROVIDERS = [
    "Gemini",
    "OpenAI",
    "Groq",
    "Ollama",
]


def check_provider_configuration(
    provider: str,
) -> Dict[str, Any]:
    """
    Check provider configuration without
    exposing API keys.
    """

    provider = provider.strip()

    if provider not in SUPPORTED_PROVIDERS:

        return {
            "provider": provider,
            "configured": False,
            "status": "UNSUPPORTED",
            "model": "",
            "message": (
                "Provider is not supported."
            ),
        }

    model = get_model_name(
        provider
    )

    # Ollama does not require API key.
    if provider == "Ollama":

        return {
            "provider": provider,
            "configured": True,
            "status": "CONFIGURED",
            "model": model,
            "message": (
                "Ollama configuration is available."
            ),
            "base_url": OLLAMA_BASE_URL,
        }

    api_key = get_api_key(
        provider
    )

    if not api_key:

        return {
            "provider": provider,
            "configured": False,
            "status": "MISSING_API_KEY",
            "model": model,
            "message": (
                f"{provider} API key is not configured."
            ),
        }

    return {
        "provider": provider,
        "configured": True,
        "status": "CONFIGURED",
        "model": model,
        "message": (
            f"{provider} API key is configured."
        ),
    }


def check_all_providers() -> Dict[str, Any]:
    """
    Check configuration of all providers.
    """

    results = {}

    for provider in SUPPORTED_PROVIDERS:

        results[provider] = (
            check_provider_configuration(
                provider
            )
        )

    return results


def provider_status(
    provider: str,
) -> str:
    """
    Return simple provider status.
    """

    result = check_provider_configuration(
        provider
    )

    return result.get(
        "status",
        "UNKNOWN",
    )


def is_provider_ready(
    provider: str,
) -> bool:
    """
    Return whether provider has the minimum
    required configuration.
    """

    result = check_provider_configuration(
        provider
    )

    return bool(
        result.get(
            "configured",
            False,
        )
    )


def masked_api_key_status(
    provider: str,
) -> Dict[str, Any]:
    """
    Return safe API key information.

    The actual key is NEVER returned.
    """

    provider = provider.strip()

    if provider == "Ollama":

        return {
            "provider": provider,
            "has_api_key": False,
            "display": "Not required",
        }

    key = get_api_key(
        provider
    )

    if not key:

        return {
            "provider": provider,
            "has_api_key": False,
            "display": "Not configured",
        }

    return {
        "provider": provider,
        "has_api_key": True,
        "display": "Configured",
    }