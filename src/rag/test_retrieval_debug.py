from src.rag.retrieval_debug import (
    RetrievalDebugger,
)


def test_score_classification():

    debugger = RetrievalDebugger(
        retriever=None
    )

    test_scores = [
        0.20,
        0.50,
        0.90,
        1.20,
        1.50,
    ]

    print()
    print("=" * 50)
    print("Retrieval Score Classification Test")
    print("=" * 50)

    for score in test_scores:

        confidence = (
            debugger._classify_score(
                score
            )
        )

        print(
            f"Score: {score:.2f}"
            f" → {confidence.upper()}"
        )

    print("=" * 50)


if __name__ == "__main__":
    test_score_classification()