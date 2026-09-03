from __future__ import annotations

import importlib


def test_core_modules():

    modules = [
        "src.core.unified_solver",
        "src.calculator",
        "src.rag",
        "src.agents",
        "src.llm",
        "src.config",
    ]

    for module_name in modules:

        module = importlib.import_module(
            module_name
        )

        assert module is not None


def test_agent_modules():

    modules = [
        "src.agents.planner",
        "src.agents.solver",
        "src.agents.reviewer",
        "src.agents.teacher",
        "src.agents.agent_graph",
    ]

    for module_name in modules:

        module = importlib.import_module(
            module_name
        )

        assert module is not None


def test_rag_modules():

    modules = [
        "src.rag.document_loader",
        "src.rag.chunking",
        "src.rag.vector_store",
        "src.rag.pipeline",
        "src.rag.memory",
        "src.rag.evaluation_runner",
    ]

    for module_name in modules:

        module = importlib.import_module(
            module_name
        )

        assert module is not None


def test_llm_modules():

    modules = [
        "src.llm.provider_health",
        "src.llm.providers.openai_provider",
        "src.llm.providers.gemini_provider",
        "src.llm.providers.groq_provider",
        "src.llm.providers.ollama_provider",
    ]

    for module_name in modules:

        module = importlib.import_module(
            module_name
        )

        assert module is not None


def test_unified_solver():

    from src.core.unified_solver import (
        UnifiedSolver,
    )

    solver = UnifiedSolver()

    assert solver is not None


def test_provider_health():

    from src.llm.provider_health import (
        check_all_providers,
    )

    results = check_all_providers()

    assert isinstance(
        results,
        dict,
    )

    assert "Gemini" in results
    assert "OpenAI" in results
    assert "Groq" in results
    assert "Ollama" in results


def test_ollama_configuration():

    from src.config.settings import (
        has_api_key,
    )

    assert (
        has_api_key("Ollama")
        is True
    )


def test_agent_graph_import():

    from src.agents.agent_graph import (
        MathMindAgentGraph,
    )

    assert MathMindAgentGraph is not None


def test_rag_pipeline_import():

    from src.rag.pipeline import (
        RAGPipeline,
    )

    assert RAGPipeline is not None


def test_vector_database_import():

    from src.rag.vector_store import (
        VectorDatabase,
    )

    assert VectorDatabase is not None


def test_ui_modules():

    modules = [
        "src.ui.agents_ui",
        "src.ui.rag_agent_ui",
        "src.ui.provider_health_ui",
    ]

    for module_name in modules:

        module = importlib.import_module(
            module_name
        )

        assert module is not None


if __name__ == "__main__":

    print()
    print(
        "=============================================="
    )

    print(
        "       MathMind AI System Integration"
    )

    print(
        "=============================================="
    )

    tests = [
        (
            "Core modules",
            test_core_modules,
        ),
        (
            "Agent modules",
            test_agent_modules,
        ),
        (
            "RAG modules",
            test_rag_modules,
        ),
        (
            "LLM modules",
            test_llm_modules,
        ),
        (
            "Unified Solver",
            test_unified_solver,
        ),
        (
            "Provider Health",
            test_provider_health,
        ),
        (
            "Ollama Configuration",
            test_ollama_configuration,
        ),
        (
            "Agent Graph",
            test_agent_graph_import,
        ),
        (
            "RAG Pipeline",
            test_rag_pipeline_import,
        ),
        (
            "Vector Database",
            test_vector_database_import,
        ),
        (
            "UI modules",
            test_ui_modules,
        ),
    ]

    passed = 0

    for name, test in tests:

        try:

            test()

            print(
                f"✅ {name}"
            )

            passed += 1

        except Exception as error:

            print(
                f"❌ {name}"
            )

            print(
                f"   Error: {error}"
            )

            raise

    print()
    print(
        "=============================================="
    )

    print(
        f"Integration Tests Passed: "
        f"{passed}/{len(tests)}"
    )

    print(
        "=============================================="
    )

    print(
        "🎉 All system integration tests passed."
    )