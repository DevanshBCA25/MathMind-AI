from pathlib import Path
from typing import Any, Dict, List

from src.rag.evaluation_dataset import (
    RETRIEVAL_EVALUATION_DATASET_V2,
)
from src.rag.retriever import RetrieverEngine
from src.rag.vector_store import VectorDatabase


VECTOR_STORE_PATH = Path(
    "data/vector_store"
)

TOP_K = 4


def normalize_text(text: str) -> str:
    """
    Normalize text for simple keyword matching.
    """

    return (
        text.lower()
        .replace("²", "2")
        .replace("'", "")
        .replace("(", " ")
        .replace(")", " ")
        .replace(",", " ")
        .replace(".", " ")
        .replace(":", " ")
        .replace(";", " ")
        .split()
    )


def calculate_relevance(
    expected_answer: str,
    retrieved_content: str,
) -> bool:
    """
    Simple retrieval relevance check.

    A retrieval result is considered relevant when
    important answer terms appear in the retrieved
    chunk.
    """

    expected_tokens = normalize_text(
        expected_answer
    )

    retrieved_tokens = set(
        normalize_text(
            retrieved_content
        )
    )

    if not expected_tokens:
        return False

    matches = sum(
        1
        for token in expected_tokens
        if token in retrieved_tokens
    )

    # Require at least one meaningful match.
    return matches >= max(
        1,
        min(2, len(expected_tokens)),
    )


def evaluate_question(
    retriever: RetrieverEngine,
    item: Dict[str, Any],
) -> Dict[str, Any]:

    question = item["question"]
    expected_answer = item["expected_answer"]

    results = (
        retriever.similarity_search_with_score(
            query=question,
            k=TOP_K,
        )
    )

    if not results:

        return {
            "id": item["id"],
            "question": question,
            "expected_answer": expected_answer,
            "retrieved_count": 0,
            "top1_relevant": False,
            "top3_relevant": False,
            "best_score": None,
        }

    top1_relevant = calculate_relevance(
        expected_answer,
        results[0][0].page_content,
    )

    top3_relevant = any(
        calculate_relevance(
            expected_answer,
            document.page_content,
        )
        for document, _ in results[:3]
    )

    best_score = float(
        results[0][1]
    )

    return {
        "id": item["id"],
        "question": question,
        "expected_answer": expected_answer,
        "retrieved_count": len(results),
        "top1_relevant": top1_relevant,
        "top3_relevant": top3_relevant,
        "best_score": best_score,
    }


def print_result(
    result: Dict[str, Any],
):

    print()
    print("-" * 70)

    print(
        f"Question {result['id']}: "
        f"{result['question']}"
    )

    print(
        f"Best Score: "
        f"{result['best_score']}"
        if result["best_score"] is not None
        else "Best Score: N/A"
    )

    print(
        "Top-1 Relevant: "
        f"{'YES' if result['top1_relevant'] else 'NO'}"
    )

    print(
        "Top-3 Relevant: "
        f"{'YES' if result['top3_relevant'] else 'NO'}"
    )


def main():

    print()
    print("=" * 70)
    print(
        "MathMind-AI Retrieval Evaluation Dataset v2"
    )
    print("=" * 70)

    # ---------------------------------------------------------
    # Check database
    # ---------------------------------------------------------

    if not VECTOR_STORE_PATH.exists():

        print()
        print(
            "ERROR: Existing FAISS database "
            "was not found."
        )

        print(
            f"Expected path: {VECTOR_STORE_PATH}"
        )

        return

    # ---------------------------------------------------------
    # Load existing database
    # ---------------------------------------------------------

    try:

        database = VectorDatabase()

        vector_db = database.load(
            str(VECTOR_STORE_PATH)
        )

    except Exception as error:

        print()
        print(
            "ERROR loading FAISS database:"
        )

        print(error)

        return

    print()
    print(
        "FAISS database loaded successfully."
    )

    # ---------------------------------------------------------
    # Create retriever
    # ---------------------------------------------------------

    retriever = RetrieverEngine(
        vector_db
    )

    # ---------------------------------------------------------
    # Evaluate dataset
    # ---------------------------------------------------------

    results: List[
        Dict[str, Any]
    ] = []

    for item in RETRIEVAL_EVALUATION_DATASET_V2:

        result = evaluate_question(
            retriever,
            item,
        )

        results.append(result)

        print_result(result)

    # ---------------------------------------------------------
    # Calculate metrics
    # ---------------------------------------------------------

    total = len(results)

    top1_hits = sum(
        result["top1_relevant"]
        for result in results
    )

    top3_hits = sum(
        result["top3_relevant"]
        for result in results
    )

    valid_scores = [
        result["best_score"]
        for result in results
        if result["best_score"] is not None
    ]

    average_best_score = (
        sum(valid_scores)
        / len(valid_scores)
        if valid_scores
        else None
    )

    top1_accuracy = (
        top1_hits / total * 100
        if total
        else 0
    )

    top3_accuracy = (
        top3_hits / total * 100
        if total
        else 0
    )

    # ---------------------------------------------------------
    # Final report
    # ---------------------------------------------------------

    print()
    print()
    print("=" * 70)
    print("FINAL RETRIEVAL EVALUATION")
    print("=" * 70)

    print(
        f"Total Questions: {total}"
    )

    print(
        f"Top-1 Relevant: "
        f"{top1_hits}/{total}"
    )

    print(
        f"Top-1 Retrieval Accuracy: "
        f"{top1_accuracy:.2f}%"
    )

    print(
        f"Top-3 Relevant: "
        f"{top3_hits}/{total}"
    )

    print(
        f"Top-3 Retrieval Accuracy: "
        f"{top3_accuracy:.2f}%"
    )

    if average_best_score is not None:

        print(
            f"Average Best FAISS Score: "
            f"{average_best_score:.4f}"
        )

    print("=" * 70)

    print()
    print(
        "Retrieval evaluation completed successfully."
    )


if __name__ == "__main__":
    main()