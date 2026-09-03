from src.agents.agent_graph import (
    MathMindAgentGraph,
)


def main():

    print()
    print("=" * 70)
    print("MathMind-AI — Agent Orchestration Test")
    print("=" * 70)

    question = (
        "Solve the quadratic equation "
        "x² - 5x + 6 = 0 and explain the solution."
    )

    print()
    print("Question:")
    print(question)

    print()
    print("Starting agent workflow...")
    print()

    graph = MathMindAgentGraph()

    result = graph.run(
        question
    )

    print("=" * 70)
    print("PLANNER")
    print("=" * 70)

    print(
        result.get(
            "plan",
            "No plan generated.",
        )
    )

    print()
    print("=" * 70)
    print("SOLVER")
    print("=" * 70)

    print(
        result.get(
            "solution",
            "No solution generated.",
        )
    )

    print()
    print("=" * 70)
    print("REVIEWER")
    print("=" * 70)

    print(
        result.get(
            "review",
            "No review generated.",
        )
    )

    print()
    print("=" * 70)
    print("TEACHER / FINAL ANSWER")
    print("=" * 70)

    print(
        result.get(
            "final_answer",
            "No final answer generated.",
        )
    )

    print()
    print("=" * 70)
    print(
        "STATUS:",
        result.get(
            "status",
            "unknown",
        ),
    )
    print("=" * 70)
    print()


if __name__ == "__main__":

    main()