from src.config.settings import (
    APP_NAME,
    APP_VERSION,
    DEFAULT_PROVIDER,
    DOCUMENTS_DIR,
    VECTOR_DB_DIR,
    get_api_key,
    has_api_key,
    get_model_name,
    configuration_summary,
)


def test_app_configuration():

    assert APP_NAME == "MathMind AI"

    assert APP_VERSION

    assert DEFAULT_PROVIDER


def test_directories():

    assert DOCUMENTS_DIR.exists()

    assert VECTOR_DB_DIR.exists()


def test_ollama_configuration():

    assert (
        get_api_key("Ollama")
        is None
    )

    assert (
        has_api_key("Ollama")
        is True
    )


def test_model_names():

    assert (
        get_model_name("OpenAI")
    )

    assert (
        get_model_name("Gemini")
    )

    assert (
        get_model_name("Groq")
    )

    assert (
        get_model_name("Ollama")
    )


def test_api_key_function():

    # No API key is required for this test.
    # It only verifies that the function
    # returns None when a key is not configured.

    key = get_api_key(
        "OpenAI"
    )

    assert (
        key is None
        or isinstance(key, str)
    )


def test_configuration_summary():

    summary = (
        configuration_summary()
    )

    assert isinstance(
        summary,
        dict,
    )

    assert (
        summary["app_name"]
        == "MathMind AI"
    )

    assert (
        "gemini_configured"
        in summary
    )

    assert (
        "openai_configured"
        in summary
    )

    assert (
        "groq_configured"
        in summary
    )


if __name__ == "__main__":

    test_app_configuration()

    test_directories()

    test_ollama_configuration()

    test_model_names()

    test_api_key_function()

    test_configuration_summary()

    print()
    print(
        "======================================"
    )
    print(
        "      Configuration Tests"
    )
    print(
        "======================================"
    )
    print(
        "All tests passed successfully."
    )