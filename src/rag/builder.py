"""
Build a FAISS vector database from PDF files.

UI-independent: returns the database plus a short report, so any
front end can show progress and problems its own way.
"""

from pathlib import Path


def _with_page_numbers(documents, file_name):

    for document in documents:

        metadata = dict(document.metadata or {})

        metadata["source"] = file_name
        metadata["file_name"] = file_name

        if "page" in metadata:

            try:
                metadata["page_number"] = int(metadata["page"]) + 1
            except (TypeError, ValueError):
                pass

        document.metadata = metadata

    return documents


def build_vector_database(pdf_paths):
    """
    Return (vector_db or None, report dict).

    report = {"files": n, "chunks": n, "problems": [str, ...]}
    """

    from src.rag.chunking import Chunker
    from src.rag.document_loader import DocumentLoader
    from src.rag.vector_store import VectorDatabase

    loader = DocumentLoader()
    chunker = Chunker()

    chunks = []
    problems = []

    for path in pdf_paths:

        name = Path(path).name

        try:

            documents = [
                doc
                for doc in loader.load(str(path))
                if doc.page_content and doc.page_content.strip()
            ]

            if not documents:
                problems.append(f"{name}: no readable text found.")
                continue

            _with_page_numbers(documents, name)

            chunks.extend(
                _with_page_numbers(chunker.split(documents), name)
            )

        except Exception as error:

            problems.append(f"{name}: {error}")

    report = {
        "files": len(pdf_paths),
        "chunks": len(chunks),
        "problems": problems,
    }

    if not chunks:
        return None, report

    return VectorDatabase().create(chunks), report
