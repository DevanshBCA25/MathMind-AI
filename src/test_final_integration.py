"""
MathMind-AI
Final Integration Test

Checks the major project modules without
requiring external API calls.
"""

import traceback


def test_imports():

    print()
    print("==============================")
    print("MathMind-AI Final Integration")
    print("==============================")

    tests = []

    # --------------------------------------------------
    # Calculator
    # --------------------------------------------------

    try:
        from src.calculator.basic import (
            add,
            subtract,
            multiply,
            divide,
        )

        assert add(2, 3) == 5
        assert subtract(5, 2) == 3
        assert multiply(2, 3) == 6
        assert divide(6, 2) == 3

        tests.append(
            ("Basic Calculator", True)
        )

    except Exception as error:

        print(
            "Basic Calculator Error:",
            error,
        )

        tests.append(
            ("Basic Calculator", False)
        )

    # --------------------------------------------------
    # RAG
    # --------------------------------------------------

    try:

        from src.rag.retriever import (
            RetrieverEngine,
        )

        from src.rag.relevance_filter import (
            RelevanceFilter,
        )

        from src.rag.evaluation import (
            RAGEvaluator,
        )

        from src.rag.confidence import (
            RAGConfidence,
        )

        from src.rag.evaluation_runner import (
            RAGEvaluationRunner,
        )

        from src.rag.pipeline import (
            RAGPipeline,
        )

        tests.append(
            ("RAG Module", True)
        )

    except Exception as error:

        print(
            "RAG Error:",
            error,
        )

        tests.append(
            ("RAG Module", False)
        )

    # --------------------------------------------------
    # Agents
    # --------------------------------------------------

    try:

        from src.agents.planner import (
            Planner,
        )

        from src.agents.reviewer import (
            Reviewer,
        )

        from src.agents.solver import (
            MathSolver,
        )

        from src.agents.teacher import (
            MathTeacher,
        )

        from src.agents.agent_graph import (
            MathMindAgentGraph,
        )

        tests.append(
            ("Agent System", True)
        )

    except Exception as error:

        print(
            "Agent System Error:",
            error,
        )

        tests.append(
            ("Agent System", False)
        )

    # --------------------------------------------------
    # LLM Router
    # --------------------------------------------------

    try:

        from src.llm.router import (
            LLMRouter,
        )

        tests.append(
            ("LLM Router", True)
        )

    except Exception as error:

        print(
            "LLM Router Error:",
            error,
        )

        tests.append(
            ("LLM Router", False)
        )

    # --------------------------------------------------
    # Embeddings
    # --------------------------------------------------

    try:

        from src.rag.embeddings import (
            EmbeddingModel,
        )

        tests.append(
            ("Embedding System", True)
        )

    except Exception as error:

        print(
            "Embedding Error:",
            error,
        )

        tests.append(
            ("Embedding System", False)
        )

    # --------------------------------------------------
    # UI
    # --------------------------------------------------

    try:

        import streamlit

        tests.append(
            ("Streamlit", True)
        )

    except Exception as error:

        print(
            "Streamlit Error:",
            error,
        )

        tests.append(
            ("Streamlit", False)
        )

    # --------------------------------------------------
    # RESULTS
    # --------------------------------------------------

    print()
    print("------------------------------")
    print("Integration Test Results")
    print("------------------------------")

    passed = 0
    failed = 0

    for name, status in tests:

        if status:

            print(
                f"✅ {name}"
            )

            passed += 1

        else:

            print(
                f"❌ {name}"
            )

            failed += 1

    total = len(tests)

    print()
    print("------------------------------")
    print(
        f"Passed: {passed}/{total}"
    )

    print(
        f"Failed: {failed}/{total}"
    )

    print("------------------------------")

    if failed == 0:

        print()
        print(
            "🎉 ALL INTEGRATION TESTS PASSED"
        )

        print(
            "MathMind-AI core architecture "
            "is successfully integrated."
        )

    else:

        print()
        print(
            "⚠️ Some integration tests failed."
        )

        print(
            "Check the error messages above."
        )

    print()
    print("==============================")
    print("Final Integration Test Complete")
    print("==============================")


if __name__ == "__main__":

    try:

        test_imports()

    except Exception:

        print()
        print(
            "Unexpected integration error:"
        )

        traceback.print_exc()