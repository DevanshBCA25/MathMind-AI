from pathlib import Path
from typing import List

from langchain_core.documents import Document

from src.ocr.pdf_reader import read_pdf
from src.ocr.ocr_engine import extract_text
from src.ocr.ocr_documents import (
    ocr_text_to_documents,
)


def process_pdf_with_ocr(
    pdf_path: str,
) -> List[Document]:
    """
    Read a PDF, run OCR page-by-page,
    and convert extracted text into
    LangChain Documents.
    """

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    if path.suffix.lower() != ".pdf":
        raise ValueError(
            "Only PDF files are supported."
        )

    # --------------------------------------------------
    # Read PDF pages
    # --------------------------------------------------

    pages = read_pdf(
        str(path)
    )

    if not pages:
        return []

    ocr_pages = []

    # --------------------------------------------------
    # OCR every page
    # --------------------------------------------------

    for page in pages:

        text = extract_text(
            page
        )

        if text:
            ocr_pages.append(
                text
            )

        else:
            ocr_pages.append(
                ""
            )

    # --------------------------------------------------
    # Convert OCR output to Documents
    # --------------------------------------------------

    documents = ocr_text_to_documents(
        pages=ocr_pages,
        source_name=path.name,
    )

    return documents