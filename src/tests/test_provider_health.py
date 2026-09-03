from src.llm.provider_health import (
    SUPPORTED_PROVIDERS,
    check_provider_configuration,
    check_all_providers,
    provider_status,
    is_provider_ready,
    masked_api_key_status,
)


def test_supported_providers():

    assert "Gemini" in SUPPORTED_PROVIDERS

    assert "OpenAI" in SUPPORTED_PROVIDERS

    assert "Groq" in SUPPORTED_PROVIDERS

    assert "Ollama" in SUPPORTED_PROVIDERS


def test_ollama_configuration():

    result = check_provider_configuration(
        "Ollama"
    )

    assert (
        result["provider"]
        == "Ollama"
    )

    assert (
        result["configured"]
        is True
    )

    assert (
        result["status"]
        == "CONFIGURED"
    )


def test_unknown_provider():

    result = check_provider_configuration(
        "UnknownProvider"
    )

    assert (
        result["configured"]
        is False
    )

    assert (
        result["status"]
        == "UNSUPPORTED"
    )


def test_all_providers():

    results = check_all_providers()

    assert isinstance(
        results,
        dict,
    )

    for provider in SUPPORTED_PROVIDERS:

        assert provider in results

        assert (
            "status"
            in results[provider]
        )

        assert (
            "model"
            in results[provider]
        )


def test_provider_status():

    status = provider_status(
        "Ollama"
    )

    assert (
        status
        == "CONFIGURED"
    )


def test_provider_ready():

    assert (
        is_provider_ready(
            "Ollama"
        )
        is True
    )


def test_masked_key():

    result = masked_api_key_status(
        "Ollama"
    )

    assert (
        result["has_api_key"]
        is False
    )

    assert (
        result["display"]
        == "Not required"
    )


def test_no_api_key_exposure():

    results = check_all_providers()

    for provider, result in results.items():

        text = str(result)

        assert "sk-" not in text

        assert "AIza" not in text


if __name__ == "__main__":

    test_supported_providers()

    test_ollama_configuration()

    test_unknown_provider()

    test_all_providers()

    test_provider_status()

    test_provider_ready()

    test_masked_key()

    test_no_api_key_exposure()

    print()
    print(
        "======================================"
    )
    print(
        "     Provider Health Tests"
    )
    print(
        "======================================"
    )
    print(
        "All tests passed successfully."
    )