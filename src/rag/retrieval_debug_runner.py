from pathlib import Path

from src.rag.retriever import RetrieverEngine
from src.rag.retrieval_debug import RetrievalDebugger
from src.rag.vector_store import VectorDatabase


VECTOR_STORE_PATH = Path(
    "data/vector_store"
)


TEST_QUESTIONS = [
    "What is the area of the rectangle in the worked example?",
    "What is the perimeter of the example rectangle?",
    "What is the discriminant of ax² + bx + c?",
    "How is the median calculated?",
    "What is the range of a valid probability?",
]


def main():

    print()
    print("=" * 70)
    print(
        "MathMind-AI - REAL FAISS RETRIEVAL ANALYSIS"
    )
    print("=" * 70)

    # --------------------------------------------------------
    # Check vector database
    # --------------------------------------------------------

    if not VECTOR_STORE_PATH.exists():

        print()
        print(
            "ERROR: Vector database was not found."
        )

        print(
            "Expected path:"
        )

        print(
            VECTOR_STORE_PATH
        )

        return

    # --------------------------------------------------------
    # Load existing FAISS database
    # --------------------------------------------------------

    try:

        vector_database = VectorDatabase()

        vector_db = vector_database.load(
            str(VECTOR_STORE_PATH)
        )

    except Exception as error:

        print()
        print(
            "ERROR loading vector database:"
        )

        print(error)

        return

    print()
    print(
        "Existing FAISS database loaded successfully."
    )

    # --------------------------------------------------------
    # Create retriever
    # --------------------------------------------------------

    retriever = RetrieverEngine(
        vector_db
    )

    debugger = RetrievalDebugger(
        retriever
    )

    # --------------------------------------------------------
    # Run real retrieval analysis
    # --------------------------------------------------------

    total_questions = len(
        TEST_QUESTIONS
    )

    for index, question in enumerate(
        TEST_QUESTIONS,
        start=1,
    ):

        print()
        print()
        print("-" * 70)

        print(
            f"TEST QUESTION "
            f"{index}/{total_questions}"
        )

        print(
            f"Question: {question}"
        )

        print("-" * 70)

        try:

            report = debugger.analyze_query(
                query=question,
            )

            debugger.print_report(
                report
            )

        except Exception as error:

            print()
            print(
                f"ERROR analyzing question: "
                f"{error}"
            )

    # --------------------------------------------------------
    # Finished
    # --------------------------------------------------------

    print()
    print("=" * 70)

    print(
        "REAL RETRIEVAL ANALYSIS COMPLETE"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()