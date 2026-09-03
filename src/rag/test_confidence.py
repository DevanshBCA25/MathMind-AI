from src.rag.confidence import RAGConfidence


def main():
    confidence = RAGConfidence()

    test_cases = [
        {
            "name": "High Confidence",
            "context_relevance": 0.90,
            "answer_grounding": 0.95,
            "retrieval_hit": True,
        },
        {
            "name": "Medium Confidence",
            "context_relevance": 0.60,
            "answer_grounding": 0.55,
            "retrieval_hit": True,
        },
        {
            "name": "Low Confidence",
            "context_relevance": 0.20,
            "answer_grounding": 0.25,
            "retrieval_hit": False,
        },
    ]

    print("\n" + "=" * 50)
    print("MathMind-AI — RAG Confidence Test")
    print("=" * 50)

    for test_case in test_cases:

        result = confidence.calculate(
            context_relevance=test_case[
                "context_relevance"
            ],
            answer_grounding=test_case[
                "answer_grounding"
            ],
            retrieval_hit=test_case[
                "retrieval_hit"
            ],
        )

        print("\nTest:", test_case["name"])

        print(
            "Context Relevance:",
            test_case["context_relevance"],
        )

        print(
            "Answer Grounding:",
            test_case["answer_grounding"],
        )

        print(
            "Retrieval Hit:",
            test_case["retrieval_hit"],
        )

        print(
            "Confidence Score:",
            result["score"],
        )

        print(
            "Confidence Level:",
            result["level"],
        )


if __name__ == "__main__":
    main()