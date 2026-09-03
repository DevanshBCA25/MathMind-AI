from pathlib import Path

from src.rag.config import VECTOR_DB_DIR, TOP_K
from src.rag.vector_store import VectorDatabase
from src.rag.pipeline import RAGPipeline
from src.rag.memory import ConversationMemory


def main():
    print("\n" + "=" * 60)
    print("MathMind-AI — End-to-End RAG Pipeline Test")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. Check vector database
    # ---------------------------------------------------------

    vector_db_path = Path(VECTOR_DB_DIR)

    print("\n[1/5] Checking vector database...")

    if not vector_db_path.exists():
        print("❌ Vector database not found.")
        print(
            "Please build the vector database "
            "from the Streamlit application first."
        )
        return

    print("✅ Vector database directory found.")

    # ---------------------------------------------------------
    # 2. Load vector database
    # ---------------------------------------------------------

    print("\n[2/5] Loading vector database...")

    try:
        vector_db_manager = VectorDatabase()

        vector_db = vector_db_manager.load(
            str(VECTOR_DB_DIR)
        )

        print("✅ Vector database loaded successfully.")

    except Exception as error:
        print(
            f"❌ Failed to load vector database:\n{error}"
        )
        return

    # ---------------------------------------------------------
    # 3. Create RAG pipeline
    # ---------------------------------------------------------

    print("\n[3/5] Creating RAG pipeline...")

    try:
        memory = ConversationMemory(
            max_messages=10
        )

        pipeline = RAGPipeline(
            vector_db=vector_db,
            provider="OpenAI",
            retrieval_method="similarity",
            top_k=TOP_K,
            memory=memory,
        )

        print("✅ RAG pipeline created successfully.")

    except Exception as error:
        print(
            f"❌ Failed to create RAG pipeline:\n{error}"
        )
        return

    # ---------------------------------------------------------
    # 4. Test retrieval only
    # ---------------------------------------------------------

    print("\n[4/5] Testing document retrieval...")

    question = (
        "What is the area of the rectangle "
        "in the worked example?"
    )

    print("\nQuestion:")
    print(question)

    try:
        documents = pipeline.retrieve(
            question
        )

        if not documents:
            print(
                "\n⚠️ No relevant documents retrieved."
            )
            return

        print(
            f"\n✅ Retrieved {len(documents)} document chunk(s)."
        )

        print("\nRetrieved Sources:")

        for index, document in enumerate(
            documents,
            start=1,
        ):

            source = document.metadata.get(
                "source",
                "Unknown",
            )

            page = document.metadata.get(
                "page",
                None,
            )

            if page is not None:
                page_display = page + 1
            else:
                page_display = "Unknown"

            print(
                f"\n--- Document {index} ---"
            )

            print(
                f"Source: {source}"
            )

            print(
                f"Page: {page_display}"
            )

            print(
                "Content:"
            )

            print(
                document.page_content[:500]
            )

    except Exception as error:
        print(
            f"❌ Retrieval test failed:\n{error}"
        )
        return

    # ---------------------------------------------------------
    # 5. Full RAG test
    # ---------------------------------------------------------

    print("\n[5/5] Testing complete RAG pipeline...")

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

        print("\n" + "=" * 60)
        print("RAG RESULT")
        print("=" * 60)

        print("\nQuestion:")
        print(question)

        print("\nAnswer:")
        print(answer)

        print("\nSources:")

        if sources:

            for source in sources:

                print(
                    f"\nSource: "
                    f"{source.get('source', 'Unknown')}"
                )

                page = source.get(
                    "page",
                    None,
                )

                if page is not None:
                    print(
                        f"Page: {page + 1}"
                    )

                print(
                    "Content:"
                )

                print(
                    source.get(
                        "content",
                        "",
                    )[:300]
                )

        else:

            print(
                "No sources returned."
            )

        print("\n" + "=" * 60)
        print("END-TO-END RAG TEST COMPLETE")
        print("=" * 60)

    except Exception as error:

        print(
            "\n❌ Full RAG pipeline test failed:"
        )

        print(error)


if __name__ == "__main__":
    main()