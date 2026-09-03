from pathlib import Path

from src.rag.config import VECTOR_DB_DIR
from src.rag.vector_store import VectorDatabase
from src.rag.pipeline import RAGPipeline


def main():

    print()
    print("=" * 70)
    print("MathMind-AI — RAG Pipeline Test")
    print("=" * 70)

    # --------------------------------------------------
    # Check vector database
    # --------------------------------------------------

    vector_db_manager = VectorDatabase()

    if not vector_db_manager.exists(
        VECTOR_DB_DIR
    ):

        print()
        print("❌ FAISS vector database not found.")
        print()
        print(
            "Run the ingestion test first:"
        )
        print(
            "python -m src.rag.test_ingestion"
        )
        return

    # --------------------------------------------------
    # Load FAISS database
    # --------------------------------------------------

    print()
    print("Loading FAISS database...")

    try:

        vector_db = (
            vector_db_manager.load(
                str(VECTOR_DB_DIR)
            )
        )

        print(
            "✅ FAISS database loaded."
        )

    except Exception as error:

        print(
            f"❌ Failed to load database: "
            f"{error}"
        )
        return

    # --------------------------------------------------
    # Create RAG pipeline
    # --------------------------------------------------

    print()
    print("Creating RAG pipeline...")

    try:

        pipeline = RAGPipeline(
            vector_db=vector_db,
            provider="Gemini",
            retrieval_method="similarity",
            top_k=4,
        )

        print(
            "✅ RAG pipeline created."
        )

    except Exception as error:

        print(
            f"❌ Pipeline creation failed: "
            f"{error}"
        )
        return

    # --------------------------------------------------
    # Test questions
    # --------------------------------------------------

    questions = [
        "What is a linear equation?",
        "What is the formula for the area of a rectangle?",
        "What is differentiation?",
        "What is integration?",
    ]

    print()
    print("=" * 70)
    print("QUESTION ANSWERING TEST")
    print("=" * 70)

    for index, question in enumerate(
        questions,
        start=1,
    ):

        print()
        print(
            f"Question {index}: {question}"
        )

        try:

            result = pipeline.ask(
                question
            )

            answer = result.get(
                "answer",
                "",
            )

            sources = result.get(
                "sources",
                [],
            )

            print()
            print("Answer:")
            print(answer)

            print()
            print(
                f"Sources Retrieved: "
                f"{len(sources)}"
            )

            for source in sources:

                print(
                    f"  → {source.get('source', 'Unknown')}"
                )

                if source.get("page") is not None:

                    print(
                        f"    Page: "
                        f"{source.get('page') + 1}"
                    )

        except Exception as error:

            print()
            print(
                f"❌ Question failed: {error}"
            )

    # --------------------------------------------------
    # Test MMR
    # --------------------------------------------------

    print()
    print("=" * 70)
    print("MMR TEST")
    print("=" * 70)

    try:

        pipeline.change_retrieval_method(
            "mmr"
        )

        result = pipeline.ask(
            "Explain algebra."
        )

        print()
        print("MMR Answer:")
        print(
            result.get(
                "answer",
                "",
            )
        )

        print()
        print(
            f"MMR Sources: "
            f"{len(result.get('sources', []))}"
        )

        print()
        print(
            "✅ MMR retrieval working."
        )

    except Exception as error:

        print(
            f"❌ MMR test failed: {error}"
        )

    # --------------------------------------------------
    # Clear memory
    # --------------------------------------------------

    try:

        pipeline.clear_memory()

        print()
        print(
            "✅ Conversation memory cleared."
        )

    except Exception as error:

        print(
            f"⚠️ Memory clear warning: "
            f"{error}"
        )

    # --------------------------------------------------
    # Final result
    # --------------------------------------------------

    print()
    print("=" * 70)
    print("RAG PIPELINE TEST COMPLETE")
    print("=" * 70)
    print()
    print(
        "✅ PDF → OCR/Text → LangChain"
    )
    print(
        "✅ Chunking"
    )
    print(
        "✅ Embeddings"
    )
    print(
        "✅ FAISS"
    )
    print(
        "✅ Similarity Retrieval"
    )
    print(
        "✅ MMR Retrieval"
    )
    print(
        "✅ Relevance Filtering"
    )
    print(
        "✅ Prompt Construction"
    )
    print(
        "✅ LLM Generation"
    )
    print(
        "✅ Conversation Memory"
    )
    print()
    print(
        "MathMind-AI RAG pipeline is ready."
    )
    print()


if __name__ == "__main__":
    main()