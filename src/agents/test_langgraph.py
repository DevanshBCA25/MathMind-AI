from src.agents.agent_graph import (
    MathMindAgentGraph,
)


def main():

    print()
    print("=" * 70)
    print("MathMind-AI LangGraph Agent Test")
    print("=" * 70)

    question = (
        "What is the area of a rectangle "
        "with length 12 cm and width 5 cm?"
    )

    print()
    print("Question:")
    print(question)

    print()
    print("Initializing LangGraph...")

    graph = MathMindAgentGraph()

    print("✅ LangGraph initialized.")

    print()
    print("Running workflow...")
    print()

    result = graph.run(
        question
    )

    print("=" * 70)
    print("FINAL GRAPH STATE")
    print("=" * 70)

    print()
    print("Question:")
    print(
        result.get(
            "question",
            "",
        )
    )

    print()
    print("Plan:")
    print(
        result.get(
            "plan",
            "",
        )
    )

    print()
    print("Solution:")
    print(
        result.get(
            "solution",
            "",
        )
    )

    print()
    print("Review:")
    print(
        result.get(
            "review",
            "",
        )
    )

    print()
    print("Final Answer:")
    print(
        result.get(
            "final_answer",
            "",
        )
    )

    print()
    print("Status:")
    print(
        result.get(
            "status",
            "unknown",
        )
    )

    print()
    print("=" * 70)
    print("LangGraph Agent Test Complete")
    print("=" * 70)
    print()


if __name__ == "__main__":

    main()