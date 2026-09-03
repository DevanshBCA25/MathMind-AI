from pathlib import Path

from src.rag.config import VECTOR_DB_DIR, TOP_K
from src.rag.vector_store import VectorDatabase
from src.rag.retriever import RetrieverEngine


# ============================================================
# TEST QUERIES
# ============================================================

TEST_QUERIES = [
    "What is a linear equation?",
    "What is the range of a valid probability?",
    "What is integration?",
    "What is a matrix?",
]


# ============================================================
# LOAD DATABASE
# ============================================================

def load_database():

    print()
    print("=" * 70)
    print("MathMind AI — Retrieval Test")
    print("=" * 70)

    vector_store = VectorDatabase()

    if not vector_store.exists(
        VECTOR_DB_DIR
    ):

        raise FileNotFoundError(
            "FAISS vector database not found.\n"
            "Please run the ingestion test first."
        )

    print()
    print("Loading FAISS database...")

    vector_db = vector_store.load(
        str(VECTOR_DB_DIR)
    )

    print("✅ FAISS database loaded.")

    return vector_db


# ============================================================
# TEST SIMILARITY SEARCH
# ============================================================

def test_similarity(
    retriever,
    query,
):

    print()
    print("-" * 70)
    print("QUERY")
    print("-" * 70)

    print(query)

    results = retriever.similarity_search_with_score(
        query=query,
        k=TOP_K,
    )

    if not results:

        print()
        print("❌ No documents retrieved.")

        return False

    print()
    print(
        f"✅ Retrieved {len(results)} document chunk(s)"
    )

    print()

    for index, (
        document,
        score,
    ) in enumerate(
        results,
        start=1,
    ):

        metadata = (
            document.metadata
            or {}
        )

        source = metadata.get(
            "source",
            "Unknown",
        )

        page = metadata.get(
            "page_number",
            None,
        )

        if page is None:

            raw_page = metadata.get(
                "page",
                None,
            )

            if raw_page is not None:

                try:
                    page = (
                        int(raw_page) + 1
                    )
                except (
                    TypeError,
                    ValueError,
                ):
                    page = "Unknown"

            else:

                page = "Unknown"

        content = (
            document.page_content
            or ""
        ).strip()

        print(
            f"Result #{index}"
        )

        print(
            f"Source : {source}"
        )

        print(
            f"Page   : {page}"
        )

        print(
            f"Score  : {score:.6f}"
        )

        print(
            "Content:"
        )

        print(
            content[:500]
        )

        print()

    return True


# ============================================================
# TEST MMR
# ============================================================

def test_mmr(
    retriever,
    query,
):

    print()
    print("-" * 70)
    print("MMR TEST")
    print("-" * 70)

    print(
        f"Query: {query}"
    )

    results = retriever.mmr_search(
        query=query,
        k=TOP_K,
    )

    if not results:

        print(
            "❌ MMR returned no documents."
        )

        return False

    print()
    print(
        f"✅ MMR retrieved {len(results)} chunk(s)"
    )

    for index, document in enumerate(
        results,
        start=1,
    ):

        metadata = (
            document.metadata
            or {}
        )

        source = metadata.get(
            "source",
            "Unknown",
        )

        print()
        print(
            f"MMR Result #{index}"
        )

        print(
            f"Source: {source}"
        )

        print(
            (
                document.page_content
                or ""
            )[:300]
        )

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    vector_db = load_database()

    retriever = RetrieverEngine(
        vector_db
    )

    print()
    print("=" * 70)
    print("SIMILARITY RETRIEVAL")
    print("=" * 70)

    similarity_success = True

    for query in TEST_QUERIES:

        success = test_similarity(
            retriever,
            query,
        )

        if not success:

            similarity_success = False

    print()
    print("=" * 70)
    print("MMR RETRIEVAL")
    print("=" * 70)

    mmr_success = test_mmr(
        retriever,
        TEST_QUERIES[0],
    )

    print()
    print("=" * 70)
    print("RETRIEVAL TEST COMPLETE")
    print("=" * 70)

    print(
        f"Similarity Search : "
        f"{'✅ PASS' if similarity_success else '❌ FAIL'}"
    )

    print(
        f"MMR Search        : "
        f"{'✅ PASS' if mmr_success else '❌ FAIL'}"
    )

    if similarity_success and mmr_success:

        print()
        print(
            "✅ RETRIEVAL MODULE SUCCESSFUL"
        )

        print()
        print(
            "Pipeline:"
        )

        print(
            "PDF → Documents → Chunks → "
            "Embeddings → FAISS → Retrieval"
        )

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()