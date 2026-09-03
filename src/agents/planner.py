from typing import Any, Dict, List


class Planner:
    """
    Planner Agent for MathMind-AI.

    Analyzes a mathematical problem and creates
    a structured plan for solving it.
    """

    def __init__(self):
        self.name = "Planner"

    def identify_problem_type(self, question: str) -> str:
        """Identify the general mathematical problem type."""

        text = question.lower()

        if any(
            word in text
            for word in [
                "integral",
                "integrate",
                "integration",
            ]
        ):
            return "calculus"

        if any(
            word in text
            for word in [
                "derivative",
                "differentiate",
                "differentiation",
            ]
        ):
            return "calculus"

        if any(
            word in text
            for word in [
                "matrix",
                "determinant",
                "eigenvalue",
                "eigenvector",
            ]
        ):
            return "linear_algebra"

        if any(
            word in text
            for word in [
                "probability",
                "probable",
                "chance",
            ]
        ):
            return "probability"

        if any(
            word in text
            for word in [
                "mean",
                "median",
                "mode",
                "variance",
                "standard deviation",
            ]
        ):
            return "statistics"

        if any(
            word in text
            for word in [
                "triangle",
                "circle",
                "rectangle",
                "square",
                "geometry",
                "angle",
                "area",
                "perimeter",
                "volume",
            ]
        ):
            return "geometry"

        if any(
            word in text
            for word in [
                "equation",
                "polynomial",
                "quadratic",
                "linear",
                "factor",
                "factorize",
                "solve for x",
            ]
        ):
            return "algebra"

        return "general_mathematics"

    def extract_information(
        self,
        question: str,
    ) -> Dict[str, Any]:
        """Extract basic information from the question."""

        return {
            "question": question.strip(),
            "problem_type": self.identify_problem_type(
                question
            ),
            "has_question": bool(
                question.strip()
            ),
        }

    def create_steps(
        self,
        problem_type: str,
    ) -> List[str]:
        """Create a generic solving strategy."""

        steps = [
            "Understand the given problem.",
            "Identify the required mathematical concept.",
            "Extract the known values and unknown values.",
            "Select the appropriate mathematical method.",
            "Perform the required calculations.",
            "Verify the result.",
            "Prepare a clear final explanation.",
        ]

        return steps

    def plan(
        self,
        question: str,
    ) -> Dict[str, Any]:
        """Create a complete solution plan."""

        if not question or not question.strip():
            return {
                "status": "ERROR",
                "problem_type": "unknown",
                "question": "",
                "steps": [],
                "message": "Question cannot be empty.",
            }

        information = self.extract_information(
            question
        )

        problem_type = information[
            "problem_type"
        ]

        steps = self.create_steps(
            problem_type
        )

        return {
            "status": "SUCCESS",
            "agent": self.name,
            "problem_type": problem_type,
            "question": question.strip(),
            "steps": steps,
            "step_count": len(steps),
        }

    # Compatibility methods
    def analyze(
        self,
        question: str,
    ) -> Dict[str, Any]:
        """Compatibility wrapper."""

        return self.plan(question)

    def create_plan(
        self,
        question: str,
    ) -> Dict[str, Any]:
        """Compatibility wrapper."""

        return self.plan(question)


__all__ = [
    "Planner",
]