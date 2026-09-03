from src.rag.evaluation import (
    RAGEvaluator,
    evaluate_test_dataset,
)


class MockDocument:
    def __init__(
        self,
        content,
        source="test_document.pdf",
        page=0,
    ):
        self.page_content = content

        self.metadata = {
            "source": source,
            "page": page,
        }


# ============================================================
# TEST DATASET
# ============================================================

test_cases = [

    {
        "question": (
            "What is the area of the rectangle "
            "in the worked example?"
        ),

        "answer": (
            "The area of the rectangle is 60 cm²."
        ),

        "expected_answer": "60 cm²",

        "retrieved_documents": [
            MockDocument(
                (
                    "Suppose a rectangle has "
                    "length 12 cm and width 5 cm. "
                    "Its area is 12 × 5 = 60 cm²."
                )
            )
        ],
    },

    {
        "question": (
            "What is the perimeter of "
            "the example rectangle?"
        ),

        "answer": (
            "The perimeter is 34 cm."
        ),

        "expected_answer": "34 cm",

        "retrieved_documents": [
            MockDocument(
                (
                    "The rectangle has length "
                    "12 cm and width 5 cm. "
                    "Its perimeter is "
                    "2(12 + 5) = 34 cm."
                )
            )
        ],
    },

    {
        "question": (
            "What is the discriminant "
            "of ax² + bx + c?"
        ),

        "answer": (
            "The discriminant is b² - 4ac."
        ),

        "expected_answer": "b² - 4ac",

        "retrieved_documents": [
            MockDocument(
                (
                    "For ax² + bx + c, "
                    "the discriminant is b² - 4ac."
                )
            )
        ],
    },
]


# ============================================================
# RUN EVALUATION
# ============================================================

def main():

    evaluator = RAGEvaluator()

    report = evaluate_test_dataset(
        evaluator,
        test_cases,
    )

    print()
    print("=" * 50)
    print("MathMind-AI RAG Evaluation")
    print("=" * 50)

    print(
        "Total Questions:",
        report["total_questions"],
    )

    print(
        "Correct Answers:",
        report["correct_answers"],
    )

    print(
        "Retrieval Success Rate:",
        report["retrieval_success_rate"],
    )

    print(
        "Answer Success Rate:",
        report["answer_success_rate"],
    )

    print(
        "Average Score:",
        report["average_score"],
    )

    print()
    print("Individual Results:")
    print("-" * 50)

    for index, result in enumerate(
        report["results"],
        start=1,
    ):

        print()
        print(f"Question {index}:")
        print(
            result["question"]
        )

        print(
            "Expected:",
            result["expected_answer"],
        )

        print(
            "Generated:",
            result["generated_answer"],
        )

        print(
            "Answer Correct:",
            result["answer_correct"],
        )

        print(
            "Retrieval Success:",
            result["retrieval_success"],
        )

        print(
            "Context Relevance:",
            result["context_relevance"],
        )

        print(
            "Answer Grounding:",
            result["answer_grounding"],
        )

        print(
            "Score:",
            result["score"],
        )

    print()
    print("=" * 50)
    print("RAG EVALUATION COMPLETE")
    print("=" * 50)


if __name__ == "__main__":
    main()