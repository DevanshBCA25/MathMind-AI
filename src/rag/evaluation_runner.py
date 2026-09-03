from typing import Any, Dict, List, Optional

from src.rag.confidence import RAGConfidence
from src.rag.evaluation import RAGEvaluator
from src.rag.evaluation_dataset import TEST_DATASET


class RAGEvaluationRunner:
    """
    Runs the complete RAG evaluation dataset.

    Evaluates:
    - Retrieval
    - Context relevance
    - Answer grounding
    - Overall confidence
    """

    def __init__(self, pipeline):

        self.pipeline = pipeline

        self.evaluator = RAGEvaluator()

        self.confidence = RAGConfidence()

    # ============================================================
    # RUN SINGLE TEST CASE
    # ============================================================

    def run_case(
        self,
        test_case: Dict[str, Any],
    ) -> Dict[str, Any]:

        question = test_case.get(
            "question",
            "",
        )

        expected_source = test_case.get(
            "expected_source",
            "",
        )

        expected_answer = test_case.get(
            "expected_answer",
            "",
        )

        # --------------------------------------------------------
        # Validate question
        # --------------------------------------------------------

        if not question.strip():

            return {
                "question": question,
                "expected_answer": expected_answer,
                "answer": "",
                "evaluation": {
                    "retrieval_hit": False,
                    "context_relevance": 0.0,
                    "answer_grounding": 0.0,
                    "retrieved_documents": 0,
                },
                "confidence": {
                    "score": 0.0,
                    "level": "LOW",
                },
            }

        # --------------------------------------------------------
        # Run actual RAG pipeline
        # --------------------------------------------------------

        result = self.pipeline.ask(
            question
        )

        answer = result.get(
            "answer",
            "",
        )

        documents = result.get(
            "documents",
            [],
        )

        # --------------------------------------------------------
        # Evaluate RAG result
        # --------------------------------------------------------

        evaluation = self.evaluator.evaluate(
            question=question,
            answer=answer,
            documents=documents,
            expected_source=expected_source,
        )

        # --------------------------------------------------------
        # Calculate confidence
        # --------------------------------------------------------

        confidence = self.confidence.evaluate_result(
            evaluation
        )

        return {
            "question": question,
            "expected_answer": expected_answer,
            "answer": answer,
            "evaluation": evaluation,
            "confidence": confidence,
        }

    # ============================================================
    # RUN COMPLETE DATASET
    # ============================================================

    def run(
        self,
        dataset: Optional[
            List[Dict[str, Any]]
        ] = None,
    ) -> List[Dict[str, Any]]:

        if dataset is None:

            dataset = TEST_DATASET

        results = []

        for test_case in dataset:

            try:

                result = self.run_case(
                    test_case
                )

                results.append(
                    result
                )

            except Exception as error:

                results.append(
                    {
                        "question": test_case.get(
                            "question",
                            "",
                        ),
                        "expected_answer": test_case.get(
                            "expected_answer",
                            "",
                        ),
                        "answer": "",
                        "evaluation": {
                            "retrieval_hit": False,
                            "context_relevance": 0.0,
                            "answer_grounding": 0.0,
                            "retrieved_documents": 0,
                        },
                        "confidence": {
                            "score": 0.0,
                            "level": "LOW",
                        },
                        "error": str(error),
                    }
                )

        return results

    # ============================================================
    # SUMMARIZE RESULTS
    # ============================================================

    @staticmethod
    def summarize(
        results: List[Dict[str, Any]],
    ) -> Dict[str, Any]:

        if not results:

            return {
                "total_cases": 0,
                "retrieval_hits": 0,
                "retrieval_accuracy": None,
                "average_context_relevance": 0.0,
                "average_answer_grounding": 0.0,
                "average_confidence": 0.0,
                "high_confidence_cases": 0,
                "medium_confidence_cases": 0,
                "low_confidence_cases": 0,
            }

        # --------------------------------------------------------
        # Retrieval metrics
        # --------------------------------------------------------

        retrieval_values = [
            result.get(
                "evaluation",
                {},
            ).get(
                "retrieval_hit"
            )
            for result in results
            if result.get(
                "evaluation",
                {},
            ).get(
                "retrieval_hit"
            ) is not None
        ]

        retrieval_hits = sum(
            1
            for value in retrieval_values
            if value is True
        )

        retrieval_accuracy = (
            retrieval_hits
            / len(retrieval_values)
            if retrieval_values
            else None
        )

        # --------------------------------------------------------
        # Context relevance
        # --------------------------------------------------------

        relevance_values = [
            float(
                result.get(
                    "evaluation",
                    {},
                ).get(
                    "context_relevance",
                    0.0,
                )
            )
            for result in results
        ]

        average_relevance = (
            sum(relevance_values)
            / len(relevance_values)
            if relevance_values
            else 0.0
        )

        # --------------------------------------------------------
        # Answer grounding
        # --------------------------------------------------------

        grounding_values = [
            float(
                result.get(
                    "evaluation",
                    {},
                ).get(
                    "answer_grounding",
                    0.0,
                )
            )
            for result in results
        ]

        average_grounding = (
            sum(grounding_values)
            / len(grounding_values)
            if grounding_values
            else 0.0
        )

        # --------------------------------------------------------
        # Confidence
        # --------------------------------------------------------

        confidence_values = [
            float(
                result.get(
                    "confidence",
                    {},
                ).get(
                    "score",
                    0.0,
                )
            )
            for result in results
        ]

        average_confidence = (
            sum(confidence_values)
            / len(confidence_values)
            if confidence_values
            else 0.0
        )

        # --------------------------------------------------------
        # Confidence levels
        # --------------------------------------------------------

        high_cases = sum(
            1
            for result in results
            if result.get(
                "confidence",
                {},
            ).get(
                "level"
            ) == "HIGH"
        )

        medium_cases = sum(
            1
            for result in results
            if result.get(
                "confidence",
                {},
            ).get(
                "level"
            ) == "MEDIUM"
        )

        low_cases = sum(
            1
            for result in results
            if result.get(
                "confidence",
                {},
            ).get(
                "level"
            ) == "LOW"
        )

        # --------------------------------------------------------
        # Final summary
        # --------------------------------------------------------

        return {
            "total_cases": len(results),

            "retrieval_hits": retrieval_hits,

            "retrieval_accuracy": (
                round(
                    retrieval_accuracy,
                    3,
                )
                if retrieval_accuracy is not None
                else None
            ),

            "average_context_relevance": round(
                average_relevance,
                3,
            ),

            "average_answer_grounding": round(
                average_grounding,
                3,
            ),

            "average_confidence": round(
                average_confidence,
                3,
            ),

            "high_confidence_cases": high_cases,

            "medium_confidence_cases": medium_cases,

            "low_confidence_cases": low_cases,
        }