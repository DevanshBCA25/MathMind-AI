from typing import Any, Dict, Optional

from src.llm.router import LLMRouter


class MathTeacher:
    """
    MathMind-AI Teacher Agent.

    Converts a mathematical solution into a clear,
    beginner-friendly explanation.
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
        solution: Any = "",
    ) -> str:
        """Build the teaching/explanation prompt."""

        return f"""
You are the Math Teacher Agent of MathMind-AI.

Your job is to explain a mathematical solution clearly
so that a student can understand it.

ORIGINAL QUESTION:
{question}

MATHEMATICAL SOLUTION:
{solution}

INSTRUCTIONS:

1. Start with a short explanation of what the problem asks.
2. Identify the mathematical concept being used.
3. Explain the formula or method.
4. Explain the calculation step by step.
5. Explain why each important step is performed.
6. Keep the explanation beginner-friendly.
7. Verify the final result.
8. Clearly state the final answer.

IMPORTANT:

- Do not change the mathematical result.
- Do not invent values.
- Do not skip important reasoning.
- Use simple and clear language.
- Use mathematical notation where useful.
- If an assumption is required, clearly mention it.

Return a complete educational explanation.
"""

    def teach(
        self,
        question: str,
        solution: Any = "",
    ) -> Dict[str, Any]:
        """Generate a student-friendly explanation."""

        if not question or not question.strip():
            return {
                "status": "ERROR",
                "explanation": "",
                "message": "Question cannot be empty.",
            }

        prompt = self.build_prompt(
            question=question,
            solution=solution,
        )

        try:
            response = self.router.ask(
                self.provider,
                prompt,
            )

            if response is None:
                return {
                    "status": "ERROR",
                    "explanation": "",
                    "provider": self.provider,
                    "message": "LLM returned no response.",
                }

            explanation = str(response).strip()

            if not explanation:
                return {
                    "status": "ERROR",
                    "explanation": "",
                    "provider": self.provider,
                    "message": "LLM returned an empty response.",
                }

            return {
                "status": "SUCCESS",
                "explanation": explanation,
                "provider": self.provider,
            }

        except Exception as error:
            return {
                "status": "API_ERROR",
                "explanation": "",
                "provider": self.provider,
                "message": str(error),
            }

    # Compatibility method
    def explain(
        self,
        question: str,
        solution: Any = "",
    ) -> Dict[str, Any]:
        """Compatibility wrapper."""

        return self.teach(
            question=question,
            solution=solution,
        )


# Backward compatibility
MathTeacherAgent = MathTeacher
Teacher = MathTeacher


__all__ = [
    "MathTeacher",
    "MathTeacherAgent",
    "Teacher",
]