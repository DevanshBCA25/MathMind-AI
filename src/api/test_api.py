from fastapi.testclient import TestClient

from src.api.app import app


client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["application"] == "MathMind AI"

    assert data["status"] == "running"


def test_health():

    response = client.get(
        "/api/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_add():

    response = client.post(
        "/api/calculator",
        json={
            "operation": "add",
            "num1": 10,
            "num2": 20,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["result"] == 30


def test_subtract():

    response = client.post(
        "/api/calculator",
        json={
            "operation": "subtract",
            "num1": 20,
            "num2": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["result"] == 15


def test_multiply():

    response = client.post(
        "/api/calculator",
        json={
            "operation": "multiply",
            "num1": 5,
            "num2": 4,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["result"] == 20


def test_divide():

    response = client.post(
        "/api/calculator",
        json={
            "operation": "divide",
            "num1": 20,
            "num2": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["result"] == 4


def test_invalid_operation():

    response = client.post(
        "/api/calculator",
        json={
            "operation": "unknown",
            "num1": 10,
            "num2": 5,
        },
    )

    assert response.status_code == 400


def test_division_by_zero():

    response = client.post(
        "/api/calculator",
        json={
            "operation": "divide",
            "num1": 10,
            "num2": 0,
        },
    )

    assert response.status_code == 400


if __name__ == "__main__":

    print(
        "Running MathMind AI API tests..."
    )

    test_root()
    print("✓ Root endpoint")

    test_health()
    print("✓ Health endpoint")

    test_add()
    print("✓ Addition")

    test_subtract()
    print("✓ Subtraction")

    test_multiply()
    print("✓ Multiplication")

    test_divide()
    print("✓ Division")

    test_invalid_operation()
    print("✓ Invalid operation handling")

    test_division_by_zero()
    print("✓ Division by zero handling")

    print()
    print(
        "===================================="
    )
    print(
        "MathMind AI API Tests Passed"
    )
    print(
        "===================================="
    )