from pathlib import Path
from typing import List

from langchain_core.documents import Document


def ensure_directory(path):

    path = Path(path)

    path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return path


def get_document_count(
    documents: List[Document],
) -> int:

    return len(documents)


def get_total_characters(
    documents: List[Document],
) -> int:

    return sum(
        len(document.page_content)
        for document in documents
    )


def get_source_name(document: Document) -> str:

    source = document.metadata.get(
        "source",
        "Unknown",
    )

    return Path(source).name


def get_page_number(document: Document):

    page = document.metadata.get(
        "page",
        None,
    )

    if page is None:
        return None

    return page + 1


def format_document_source(
    document: Document,
) -> str:

    source = get_source_name(document)

    page = get_page_number(document)

    if page is not None:

        return f"{source} — Page {page}"

    return source


def combine_documents(
    documents: List[Document],
) -> str:

    return "\n\n".join(
        document.page_content
        for document in documents
    )