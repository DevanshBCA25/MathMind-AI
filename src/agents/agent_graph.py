from typing import Any, Dict

from src.agents.planner import Planner
from src.agents.solver import Solver
from src.agents.reviewer import Reviewer
from src.agents.teacher import Teacher


class MathMindAgentGraph:
    """
    MathMind-AI Multi-Agent Workflow

    Workflow:

        Planner
           ↓
        Solver
           ↓
        Reviewer
           ↓
        Teacher
    """

    def __init__(
        self,
        provider: str = "Gemini",
    ):
        self.provider = provider

        self.planner = Planner()

        self.solver = Solver(
            provider=provider
        )

        self.reviewer = Reviewer()

        self.teacher = Teacher(
            provider=provider
        )

    def set_provider(
        self,
        provider: str,
    ) -> None:
        """
        Change provider for LLM-based agents.
        """

        self.provider = provider

        self.solver.set_provider(
            provider
        )

        self.teacher.set_provider(
            provider
        )

    def run(
        self,
        question: str,
    ) -> Dict[str, Any]:
        """
        Execute the complete agent workflow.
        """

        if not question or not question.strip():

            return {
                "status": "ERROR",
                "question": question,
                "message": (
                    "Question cannot be empty."
                ),
            }

        # ==================================================
        # 1. PLANNER
        # ==================================================

        try:

            plan = self.planner.plan(
                question
            )

        except Exception as error:

            return {
                "status": "ERROR",
                "question": question,
                "stage": "planner",
                "message": str(error),
            }

        # ==================================================
        # 2. SOLVER
        # ==================================================

        solver_result = self.solver.solve(
            question=question,
            plan=plan,
        )

        solution = solver_result.get(
            "solution",
            "",
        )

        # If API is unavailable, stop here gracefully.
        if not solution:

            return {
                "status": "API_ERROR",
                "question": question,
                "plan": plan,
                "solver": solver_result,
                "solution": "",
                "review": {
                    "status": "SKIPPED",
                    "message": (
                        "Reviewer skipped because "
                        "solver did not produce a solution."
                    ),
                },
                "teacher": {
                    "status": "SKIPPED",
                    "message": (
                        "Teacher skipped because "
                        "solver did not produce a solution."
                    ),
                },
                "explanation": "",
            }

        # ==================================================
        # 3. REVIEWER
        # ==================================================

        try:

            review = self.reviewer.review(
                question=question,
                solution=solution,
            )

        except TypeError:

            try:

                review = self.reviewer.review(
                    solution
                )

            except Exception as error:

                review = {
                    "status": "ERROR",
                    "message": str(error),
                }

        except Exception as error:

            review = {
                "status": "ERROR",
                "message": str(error),
            }

        # ==================================================
        # 4. TEACHER
        # ==================================================

        teacher_result = self.teacher.teach(
            question=question,
            solution=solution,
            review=review,
        )

        explanation = teacher_result.get(
            "explanation",
            "",
        )

        # ==================================================
        # FINAL RESULT
        # ==================================================

        return {
            "status": "SUCCESS",
            "question": question,

            "plan": plan,

            "solver": solver_result,

            "solution": solution,

            "review": review,

            "teacher": teacher_result,

            "explanation": explanation,
        }