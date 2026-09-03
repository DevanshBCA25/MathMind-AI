from src.core.unified_solver import UnifiedSolver


def test_empty_question():

    solver = UnifiedSolver()

    result = solver.solve("")

    assert result["status"] == "ERROR"

    assert result["module"] == "unknown"


def test_question_classifier():

    solver = UnifiedSolver()

    # Calculator
    assert (
        solver.classify_question(
            "Calculate 20 + 30"
        )
        == "calculator"
    )

    # Pure arithmetic
    assert (
        solver.classify_question(
            "20 + 30"
        )
        == "calculator"
    )

    # Symbolic equation
    assert (
        solver.classify_question(
            "Solve x = 10"
        )
        == "symbolic"
    )

    # Derivative
    assert (
        solver.classify_question(
            "Differentiate x^2"
        )
        == "symbolic"
    )

    # RAG
    assert (
        solver.classify_question(
            "What does the document say?"
        )
        == "rag"
    )

    # Agent
    assert (
        solver.classify_question(
            "Explain why the quadratic formula works"
        )
        == "agent"
    )


def test_calculator():

    solver = UnifiedSolver()

    result = solver.solve(
        "20 + 30"
    )

    assert result["status"] == "SUCCESS"

    assert result["module"] == "calculator"

    assert "50" in result["answer"]


def test_calculator_words():

    solver = UnifiedSolver()

    result = solver.solve(
        "Calculate 20 plus 30"
    )

    assert result["status"] == "SUCCESS"

    assert result["module"] == "calculator"

    assert "50" in result["answer"]


def test_symbolic():

    solver = UnifiedSolver()

    result = solver.solve(
        "x + 5 = 10"
    )

    assert result["status"] == "SUCCESS"

    assert result["module"] == "symbolic"

    assert "5" in result["answer"]


def test_symbolic_solve():

    solver = UnifiedSolver()

    result = solver.solve(
        "Solve x = 10"
    )

    assert result["status"] == "SUCCESS"

    assert result["module"] == "symbolic"

    assert "10" in result["answer"]


def test_derivative():

    solver = UnifiedSolver()

    result = solver.solve(
        "Differentiate x**2"
    )

    assert result["status"] == "SUCCESS"

    assert result["module"] == "symbolic"

    assert "2*x" in result["answer"]


def test_rag_classification():

    solver = UnifiedSolver()

    result = solver.solve(
        "What does the uploaded document say?"
    )

    assert result["module"] == "rag"

    assert result["status"] == "UNAVAILABLE"


def test_force_module():

    solver = UnifiedSolver()

    result = solver.solve(
        "20 + 30",
        force_module="calculator",
    )

    assert result["module"] == "calculator"

    assert result["status"] == "SUCCESS"


if __name__ == "__main__":

    test_empty_question()

    test_question_classifier()

    test_calculator()

    test_calculator_words()

    test_symbolic()

    test_symbolic_solve()

    test_derivative()

    test_rag_classification()

    test_force_module()

    print()
    print(
        "======================================"
    )
    print(
        "   Unified Solver Tests"
    )
    print(
        "======================================"
    )
    print(
        "All tests passed successfully."
    )