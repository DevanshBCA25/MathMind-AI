from typing import Any, Dict, List


class RAGConfidence:

    def __init__(
        self,
        high_threshold: float = 0.75,
        medium_threshold: float = 0.45,
    ):
        self.high_threshold = high_threshold
        self.medium_threshold = medium_threshold

    @staticmethod
    def _clamp(value: float) -> float:

        return max(
            0.0,
            min(1.0, value),
        )

    def calculate(
        self,
        context_relevance: float,
        answer_grounding: float,
        retrieval_hit: bool = True,
    ) -> Dict[str, Any]:

        context_relevance = self._clamp(
            context_relevance
        )

        answer_grounding = self._clamp(
            answer_grounding
        )

        retrieval_score = (
            1.0
            if retrieval_hit
            else 0.0
        )

        # Weighted confidence
        confidence_score = (
            0.35 * retrieval_score
            + 0.30 * context_relevance
            + 0.35 * answer_grounding
        )

        confidence_score = self._clamp(
            confidence_score
        )

        if confidence_score >= self.high_threshold:

            level = "HIGH"

        elif confidence_score >= self.medium_threshold:

            level = "MEDIUM"

        else:

            level = "LOW"

        return {
            "score": round(
                confidence_score,
                3,
            ),
            "level": level,
            "retrieval_score": round(
                retrieval_score,
                3,
            ),
            "context_relevance": round(
                context_relevance,
                3,
            ),
            "answer_grounding": round(
                answer_grounding,
                3,
            ),
        }

    def evaluate_result(
        self,
        evaluation: Dict[str, Any],
    ) -> Dict[str, Any]:

        retrieval_hit = evaluation.get(
            "retrieval_hit",
            True,
        )

        if retrieval_hit is None:
            retrieval_hit = True

        return self.calculate(
            context_relevance=float(
                evaluation.get(
                    "context_relevance",
                    0.0,
                )
            ),
            answer_grounding=float(
                evaluation.get(
                    "answer_grounding",
                    0.0,
                )
            ),
            retrieval_hit=bool(
                retrieval_hit
            ),
        )