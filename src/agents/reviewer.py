from typing import Any, Dict, List


class Reviewer:
    """
    Reviewer Agent for MathMind-AI.

    Reviews a mathematical solution for basic
    correctness, completeness and structure.
    """

    def __init__(self):
        self.name = "Reviewer"

    def check_solution_presence(
        self,
        solution: Any,
    ) -> bool:
        """Check whether a solution exists."""

        if solution is None:
            return False

        if isinstance(solution, str):
            return bool(solution.strip())

        if isinstance(solution, dict):
            return bool(solution)

        return True

    def check_solution_structure(
        self,
        solution: Any,
    ) -> List[str]:
        """Perform basic structural checks."""

        feedback = []

        if not self.check_solution_presence(
            solution
        ):
            feedback.append(
                "No solution was provided."
            )
            return feedback

        if isinstance(solution, str):

            text = solution.lower()

            if len(text.strip()) < 10:
                feedback.append(
                    "Solution appears too short."
                )

            if not any(
                keyword in text
                for keyword in [
                    "answer",
                    "result",
                    "therefore",
                    "=",
                ]
            ):
                feedback.append(
                    "Final result may not be clearly identified."
                )

        return feedback

    def review(
        self,
        question: str,
        solution: Any,
    ) -> Dict[str, Any]:
        """
        Review a mathematical solution.

        Returns:
            status
            score
            feedback
            approved
        """

        if not question or not question.strip():
            return {
                "status": "REJECTED",
                "score": 0.0,
                "approved": False,
                "feedback": [
                    "Question is empty."
                ],
            }

        if not self.check_solution_presence(
            solution
        ):
            return {
                "status": "REJECTED",
                "score": 0.0,
                "approved": False,
                "feedback": [
                    "No solution was provided."
                ],
            }

        feedback = self.check_solution_structure(
            solution
        )

        if feedback:
            score = 0.5
            approved = False
            status = "NEEDS_REVIEW"

        else:
            score = 1.0
            approved = True
            status = "APPROVED"

            feedback = [
                "Solution passed the initial structural review."
            ]

        return {
            "status": status,
            "score": score,
            "approved": approved,
            "feedback": feedback,
            "reviewer": self.name,
        }

    # Compatibility methods
    def verify(
        self,
        question: str,
        solution: Any,
    ) -> Dict[str, Any]:
        """Compatibility wrapper."""

        return self.review(
            question,
            solution,
        )

    def evaluate(
        self,
        question: str,
        solution: Any,
    ) -> Dict[str, Any]:
        """Compatibility wrapper."""

        return self.review(
            question,
            solution,
        )


__all__ = [
    "Reviewer",
]