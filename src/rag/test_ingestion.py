from pathlib import Path

from src.rag.document_loader import DocumentLoader
from src.rag.chunking import Chunker
from src.rag.vector_store import VectorDatabase
from src.rag.config import VECTOR_DB_DIR


DOCUMENTS_DIR = Path("data/documents")


def main():

    print()
    print("=" * 75)
    print("MathMind-AI — RAG INGESTION TEST")
    print("=" * 75)

    # ========================================================
    # 1. FIND PDFs
    # ========================================================

    pdf_files = sorted(
        DOCUMENTS_DIR.glob("*.pdf")
    )

    if not pdf_files:

        print()
        print(
            "❌ No PDF files found."
        )

        print(
            f"Expected directory: {DOCUMENTS_DIR}"
        )

        return

    print()
    print(
        f"Found {len(pdf_files)} PDF file(s)."
    )

    # ========================================================
    # 2. INITIALIZE COMPONENTS
    # ========================================================

    loader = DocumentLoader()

    chunker = Chunker()

    vector_database = VectorDatabase()

    all_chunks = []

    total_documents = 0

    # ========================================================
    # 3. LOAD + CHUNK EVERY PDF
    # ========================================================

    for pdf_file in pdf_files:

        print()
        print("-" * 75)

        print(
            f"Processing: {pdf_file.name}"
        )

        try:

            # ------------------------------------------------
            # DOCUMENT LOADING
            # ------------------------------------------------

            documents = loader.load(
                str(pdf_file)
            )

            print(
                f"   Documents loaded: "
                f"{len(documents)}"
            )

            if not documents:

                print(
                    "   ⚠️ No documents extracted."
                )

                continue

            total_documents += len(
                documents
            )

            # ------------------------------------------------
            # CHUNKING
            # ------------------------------------------------

            chunks = chunker.split(
                documents
            )

            print(
                f"   Chunks created: "
                f"{len(chunks)}"
            )

            # ------------------------------------------------
            # VERIFY METADATA
            # ------------------------------------------------

            for chunk in chunks:

                metadata = dict(
                    chunk.metadata or {}
                )

                metadata["source"] = (
                    pdf_file.name
                )

                metadata["file_name"] = (
                    pdf_file.name
                )

                if "page" in metadata:

                    try:

                        metadata[
                            "page_number"
                        ] = (
                            int(
                                metadata["page"]
                            )
                            + 1
                        )

                    except (
                        TypeError,
                        ValueError,
                    ):

                        pass

                chunk.metadata = metadata

            all_chunks.extend(
                chunks
            )

        except Exception as error:

            print()
            print(
                f"   ❌ Failed: {error}"
            )

    # ========================================================
    # 4. CHECK CHUNKS
    # ========================================================

    print()
    print("=" * 75)

    print(
        f"Total LangChain Documents: "
        f"{total_documents}"
    )

    print(
        f"Total Chunks: "
        f"{len(all_chunks)}"
    )

    if not all_chunks:

        print()
        print(
            "❌ No chunks available."
        )

        print(
            "Ingestion stopped."
        )

        return

    # ========================================================
    # 5. SHOW SAMPLE CHUNKS
    # ========================================================

    print()
    print(
        "Sample Chunk Metadata:"
    )

    for index, chunk in enumerate(
        all_chunks[:3],
        start=1,
    ):

        print()
        print(
            f"Chunk {index}"
        )

        print(
            f"Source: "
            f"{chunk.metadata.get('source')}"
        )

        print(
            f"Page: "
            f"{chunk.metadata.get('page_number')}"
        )

        print(
            f"OCR: "
            f"{chunk.metadata.get('ocr', False)}"
        )

        preview = (
            chunk.page_content
            .replace("\n", " ")
            .strip()
        )

        print(
            f"Content: "
            f"{preview[:200]}..."
        )

    # ========================================================
    # 6. CREATE FAISS DATABASE
    # ========================================================

    print()
    print("=" * 75)

    print(
        "Creating FAISS vector database..."
    )

    try:

        db = vector_database.create(
            all_chunks
        )

        print(
            "✅ FAISS database created."
        )

    except Exception as error:

        print()
        print(
            f"❌ FAISS creation failed: "
            f"{error}"
        )

        return

    # ========================================================
    # 7. SAVE FAISS DATABASE
    # ========================================================

    print()
    print(
        "Saving FAISS database..."
    )

    try:

        vector_database.save(
            db,
            str(VECTOR_DB_DIR),
        )

        print(
            "✅ FAISS database saved."
        )

    except Exception as error:

        print()
        print(
            f"❌ FAISS save failed: "
            f"{error}"
        )

        return

    # ========================================================
    # 8. VERIFY DATABASE
    # ========================================================

    print()
    print(
        "Verifying saved database..."
    )

    try:

        exists = vector_database.exists(
            VECTOR_DB_DIR
        )

        if exists:

            print(
                "✅ FAISS database exists."
            )

        else:

            print(
                "❌ FAISS database verification failed."
            )

            return

    except Exception as error:

        print(
            f"❌ Verification failed: "
            f"{error}"
        )

        return

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print()
    print("=" * 75)
    print("RAG INGESTION TEST COMPLETE")
    print("=" * 75)

    print(
        f"PDF Files              : "
        f"{len(pdf_files)}"
    )

    print(
        f"LangChain Documents    : "
        f"{total_documents}"
    )

    print(
        f"Total Chunks           : "
        f"{len(all_chunks)}"
    )

    print(
        f"FAISS Database         : "
        f"{VECTOR_DB_DIR}"
    )

    print()
    print(
        "✅ PDF → OCR/Text → "
        "LangChain → Chunking → "
        "Embeddings → FAISS"
    )

    print(
        "✅ INGESTION SUCCESSFUL"
    )

    print("=" * 75)


if __name__ == "__main__":

    main()