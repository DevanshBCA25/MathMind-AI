from typing import Any, Dict, List

from langchain_core.documents import Document


class RAGEvaluator:
    """
    Evaluates the quality of RAG retrieval and answers.

    Metrics:
    - Retrieval hit
    - Context relevance
    - Answer grounding
    """

    def __init__(self):
        pass

    @staticmethod
    def normalize(text: str) -> str:
        return " ".join(
            str(text).lower().strip().split()
        )

    # ============================================================
    # RETRIEVAL HIT
    # ============================================================

    def retrieval_hit(
        self,
        retrieved_documents: List[Document],
        expected_source: str,
    ) -> bool:

        if not retrieved_documents:
            return False

        if not expected_source:
            return True

        expected_source = self.normalize(
            expected_source
        )

        for document in retrieved_documents:

            source = document.metadata.get(
                "source",
                "",
            )

            if expected_source in self.normalize(
                source
            ):
                return True

        return False

    # ============================================================
    # CONTEXT RELEVANCE
    # ============================================================

    def context_relevance(
        self,
        question: str,
        documents: List[Document],
    ) -> float:

        if not question or not documents:
            return 0.0

        question_words = set(
            self.normalize(question).split()
        )

        if not question_words:
            return 0.0

        scores = []

        for document in documents:

            content_words = set(
                self.normalize(
                    document.page_content
                ).split()
            )

            overlap = (
                question_words
                & content_words
            )

            score = (
                len(overlap)
                / len(question_words)
            )

            scores.append(score)

        return round(
            sum(scores) / len(scores),
            3,
        )

    # ============================================================
    # ANSWER GROUNDING
    # ============================================================

    def answer_grounding(
        self,
        answer: str,
        documents: List[Document],
    ) -> float:

        if not answer or not documents:
            return 0.0

        answer_words = set(
            self.normalize(answer).split()
        )

        if not answer_words:
            return 0.0

        context = " ".join(
            document.page_content
            for document in documents
        )

        context_words = set(
            self.normalize(context).split()
        )

        overlap = (
            answer_words
            & context_words
        )

        score = (
            len(overlap)
            / len(answer_words)
        )

        return round(
            score,
            3,
        )

    # ============================================================
    # SINGLE EVALUATION
    # ============================================================

    def evaluate(
        self,
        question: str,
        answer: str,
        documents: List[Document],
        expected_source: str = "",
    ) -> Dict[str, Any]:

        retrieval_score = (
            self.retrieval_hit(
                documents,
                expected_source,
            )
            if expected_source
            else None
        )

        relevance_score = (
            self.context_relevance(
                question,
                documents,
            )
        )

        grounding_score = (
            self.answer_grounding(
                answer,
                documents,
            )
        )

        return {
            "retrieval_hit": retrieval_score,
            "context_relevance": relevance_score,
            "answer_grounding": grounding_score,
            "retrieved_documents": len(
                documents
            ),
        }


# ================================================================
# TEST DATASET EVALUATION
# ================================================================

def evaluate_test_dataset(
    evaluator: RAGEvaluator,
    test_cases: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Evaluate multiple predefined RAG test cases.

    Each test case should contain:

    question
    answer
    expected_answer
    retrieved_documents
    """

    results = []

    correct_answers = 0
    retrieval_successes = 0
    total_score = 0.0

    for test_case in test_cases:

        question = test_case.get(
            "question",
            "",
        )

        answer = test_case.get(
            "answer",
            "",
        )

        expected_answer = test_case.get(
            "expected_answer",
            "",
        )

        documents = test_case.get(
            "retrieved_documents",
            [],
        )

        # --------------------------------------------------------
        # Answer correctness
        # --------------------------------------------------------

        normalized_answer = (
            evaluator.normalize(answer)
        )

        normalized_expected = (
            evaluator.normalize(expected_answer)
        )

        answer_correct = (
            normalized_expected
            in normalized_answer
        )

        if answer_correct:
            correct_answers += 1

        # --------------------------------------------------------
        # Retrieval success
        # --------------------------------------------------------

        retrieval_success = (
            len(documents) > 0
        )

        if retrieval_success:
            retrieval_successes += 1

        # --------------------------------------------------------
        # Context relevance
        # --------------------------------------------------------

        relevance_score = (
            evaluator.context_relevance(
                question,
                documents,
            )
        )

        # --------------------------------------------------------
        # Answer grounding
        # --------------------------------------------------------

        grounding_score = (
            evaluator.answer_grounding(
                answer,
                documents,
            )
        )

        # --------------------------------------------------------
        # Overall score
        # --------------------------------------------------------

        score = round(
            (
                relevance_score
                + grounding_score
                + (1.0 if answer_correct else 0.0)
            )
            / 3,
            3,
        )

        total_score += score

        # --------------------------------------------------------
        # Store result
        # --------------------------------------------------------

        results.append(
            {
                "question": question,
                "expected_answer": expected_answer,
                "generated_answer": answer,
                "answer_correct": answer_correct,
                "retrieval_success": retrieval_success,
                "context_relevance": relevance_score,
                "answer_grounding": grounding_score,
                "score": score,
            }
        )

    # ============================================================
    # FINAL REPORT
    # ============================================================

    total_questions = len(
        test_cases
    )

    if total_questions == 0:

        return {
            "total_questions": 0,
            "correct_answers": 0,
            "retrieval_success_rate": 0.0,
            "answer_success_rate": 0.0,
            "average_score": 0.0,
            "results": [],
        }

    retrieval_success_rate = round(
        retrieval_successes
        / total_questions,
        3,
    )

    answer_success_rate = round(
        correct_answers
        / total_questions,
        3,
    )

    average_score = round(
        total_score
        / total_questions,
        3,
    )

    return {
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "retrieval_success_rate": retrieval_success_rate,
        "answer_success_rate": answer_success_rate,
        "average_score": average_score,
        "results": results,
    }