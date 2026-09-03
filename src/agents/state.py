from typing import TypedDict


class MathMindState(TypedDict, total=False):
    """
    Shared state passed between all MathMind AI agents.
    """

    question: str

    plan: str

    solution: str

    review: str

    final_answer: str

    status: str