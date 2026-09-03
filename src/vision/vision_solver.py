from __future__ import annotations

from typing import Any, Dict, Optional

from src.core.unified_solver import (
    UnifiedSolver,
)


class VisionMathSolver:
    """
    Connect extracted mathematical text
    with the existing UnifiedSolver.
    """

    def __init__(
        self,
        solver: Optional[
            UnifiedSolver
        ] = None,
    ):

        self.solver = (
            solver
            if solver is not None
            else UnifiedSolver()
        )

    def solve_text(
        self,
        text: str,
    ) -> Dict[str, Any]:

        if not text or not text.strip():

            return {
                "status": "ERROR",
                "module": "vision",
                "message": (
                    "No mathematical text available."
                ),
            }

        try:

            result = self.solver.solve(
                text
            )

            return {
                "status": result.get(
                    "status",
                    "SUCCESS",
                ),
                "module": "vision",
                "input_text": text,
                "solver_result": result,
                "answer": result.get(
                    "answer",
                    "",
                ),
            }

        except Exception as error:

            return {
                "status": "ERROR",
                "module": "vision",
                "input_text": text,
                "message": str(error),
            }