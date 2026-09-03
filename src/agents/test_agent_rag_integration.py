from src.agents.agent_rag_integration import (
    AgentRAGIntegration,
)


class MockAgentGraph:

    def run(self, question):

        return {
            "status": "SUCCESS",
            "mode": "agent",
            "final_answer": (
                f"Mock agent answer for: {question}"
            ),
        }


class MockRAGPipeline:

    def ask(self, question):

        return {
            "status": "SUCCESS",
            "mode": "rag",
            "answer": (
                f"Mock RAG answer for: {question}"
            ),
            "sources": [],
        }


def main():

    print()
    print("==============================")
    print("MathMind-AI Agent + RAG Test")
    print("==============================")

    agent = MockAgentGraph()

    rag = MockRAGPipeline()

    integration = AgentRAGIntegration(
        rag_pipeline=rag,
        agent_graph=agent,
    )

    # --------------------------------------------------
    # TEST 1 — NORMAL MATH QUESTION
    # --------------------------------------------------

    result = integration.run(
        "Solve 2x + 5 = 15",
        mode="auto",
    )

    print()
    print("Test 1 — Mathematical Question")
    print("Mode:", result.get("mode"))
    print("Status:", result.get("status"))
    print("Answer:", result.get("final_answer"))

    assert result["mode"] == "agent"

    # --------------------------------------------------
    # TEST 2 — DOCUMENT QUESTION
    # --------------------------------------------------

    result = integration.run(
        "According to the uploaded document, "
        "what is the area of the rectangle?",
        mode="auto",
    )

    print()
    print("Test 2 — Document Question")
    print("Mode:", result.get("mode"))
    print("Status:", result.get("status"))
    print("Answer:", result.get("answer"))

    assert result["mode"] == "rag"

    # --------------------------------------------------
    # TEST 3 — EXPLICIT AGENT
    # --------------------------------------------------

    result = integration.run(
        "Find the derivative of x²",
        mode="agent",
    )

    print()
    print("Test 3 — Explicit Agent")
    print("Mode:", result.get("mode"))
    print("Status:", result.get("status"))

    assert result["mode"] == "agent"

    # --------------------------------------------------
    # TEST 4 — EXPLICIT RAG
    # --------------------------------------------------

    result = integration.run(
        "What is written in the document?",
        mode="rag",
    )

    print()
    print("Test 4 — Explicit RAG")
    print("Mode:", result.get("mode"))
    print("Status:", result.get("status"))

    assert result["mode"] == "rag"

    # --------------------------------------------------
    # TEST 5 — EMPTY QUESTION
    # --------------------------------------------------

    result = integration.run(
        "",
        mode="auto",
    )

    print()
    print("Test 5 — Empty Question")
    print("Status:", result.get("status"))

    assert result["status"] == "ERROR"

    print()
    print("==============================")
    print("✅ All Agent + RAG Tests Passed")
    print("==============================")


if __name__ == "__main__":
    main()