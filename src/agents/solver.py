from typing import Any, Dict, Optional

from src.llm.router import LLMRouter


class MathSolver:
    """
    MathMind-AI Solver Agent.

    Responsible for generating a mathematical solution
    using the configured LLM provider.
    """

    def __init__(
        self,
        provider: str = "Gemini",
        router: Optional[LLMRouter] = None,
    ):
        self.provider = provider
        self.router = router or LLMRouter()

    def set_provider(self, provider: str) -> None:
        """Change the active LLM provider."""
        self.provider = provider

    def build_prompt(
        self,
        question: str,
        plan: Any = "",
    ) -> str:
        """Create the mathematical solving prompt."""

        return f"""
You are the Math Solver Agent of MathMind-AI.

Solve the following mathematical problem accurately
and step by step.

PROBLEM:
{question}

PLANNER ANALYSIS:
{plan}

INSTRUCTIONS:

1. Understand the problem.
2. Identify the mathematical concept.
3. Extract known and unknown values.
4. Select the appropriate mathematical method.
5. Perform the required calculations.
6. Show important intermediate steps.
7. Verify the result.
8. Clearly state the final answer.

IMPORTANT:
- Do not invent information.
- Do not skip important mathematical steps.
- Use correct mathematical notation.
- If the problem is ambiguous, state the assumption.
- Keep the solution clear and logically structured.

Return the complete mathematical solution.
"""

    def solve(
        self,
        question: str,
        plan: Any = "",
    ) -> Dict[str, Any]:
        """
        Generate a mathematical solution.
        """

        if not question or not question.strip():
            return {
                "status": "ERROR",
                "solution": "",
                "message": "Question cannot be empty.",
            }

        prompt = self.build_prompt(
            question=question,
            plan=plan,
        )

        try:
            response = self.router.ask(
                self.provider,
                prompt,
            )

            if response is None:
                return {
                    "status": "ERROR",
                    "solution": "",
                    "provider": self.provider,
                    "message": "LLM returned no response.",
                }

            solution = str(response).strip()

            if not solution:
                return {
                    "status": "ERROR",
                    "solution": "",
                    "provider": self.provider,
                    "message": "LLM returned an empty response.",
                }

            return {
                "status": "SUCCESS",
                "solution": solution,
                "provider": self.provider,
            }

        except Exception as error:
            return {
                "status": "API_ERROR",
                "solution": "",
                "provider": self.provider,
                "message": str(error),
            }

    # --------------------------------------------------------
    # Compatibility method
    # --------------------------------------------------------

    def generate_solution(
        self,
        question: str,
        plan: Any = "",
    ) -> Dict[str, Any]:
        """
        Compatibility wrapper for code that uses
        generate_solution().
        """

        return self.solve(
            question=question,
            plan=plan,
        )


# ------------------------------------------------------------
# Backward compatibility
# ------------------------------------------------------------

# Some existing files may import Solver instead of MathSolver.
Solver = MathSolver


__all__ = [
    "MathSolver",
    "Solver",
]