from src.utils.error_handler import (
    classify_error,
    user_friendly_error,
    safe_execute,
    success_response,
    error_response,
)


def test_api_error():

    error = Exception(
        "API key not valid"
    )

    assert (
        classify_error(error)
        == "API_ERROR"
    )


def test_connection_error():

    error = Exception(
        "Failed to connect to Ollama"
    )

    assert (
        classify_error(error)
        == "CONNECTION_ERROR"
    )


def test_import_error():

    error = Exception(
        "cannot import name MathSolver"
    )

    assert (
        classify_error(error)
        == "IMPORT_ERROR"
    )


def test_file_error():

    error = Exception(
        "could not open index.faiss"
    )

    assert (
        classify_error(error)
        == "FILE_ERROR"
    )


def test_application_error():

    error = Exception(
        "Something unexpected happened"
    )

    assert (
        classify_error(error)
        == "APPLICATION_ERROR"
    )


def test_safe_execute_success():

    def add(a, b):

        return a + b

    result = safe_execute(
        add,
        10,
        20,
    )

    assert (
        result["status"]
        == "SUCCESS"
    )

    assert (
        result["result"]
        == 30
    )


def test_safe_execute_error():

    def failing_function():

        raise Exception(
            "API key not valid"
        )

    result = safe_execute(
        failing_function
    )

    assert (
        result["status"]
        == "API_ERROR"
    )

    assert result["result"] is None


def test_success_response():

    result = success_response(
        result=50
    )

    assert (
        result["status"]
        == "SUCCESS"
    )

    assert (
        result["result"]
        == 50
    )


def test_error_response():

    result = error_response(
        Exception(
            "API key not valid"
        )
    )

    assert (
        result["status"]
        == "API_ERROR"
    )


if __name__ == "__main__":

    test_api_error()
    test_connection_error()
    test_import_error()
    test_file_error()
    test_application_error()

    test_safe_execute_success()
    test_safe_execute_error()

    test_success_response()
    test_error_response()

    print()
    print(
        "======================================"
    )
    print(
        "   Error Handler Tests"
    )
    print(
        "======================================"
    )
    print(
        "All tests passed successfully."
    )