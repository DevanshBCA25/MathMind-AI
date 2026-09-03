from pathlib import Path

from langchain_core.documents import Document

from src.ocr.pdf_reader import render_pdf_pages
from src.ocr.ocr_engine import extract_text


def process_pdf(
    pdf_path,
    dpi=150,
):
    """
    Complete OCR pipeline:

        PDF
          ↓
        Render pages
          ↓
        EasyOCR
          ↓
        LangChain Documents
    """

    if isinstance(pdf_path, dict):

        pdf_path = (
            pdf_path.get("path")
            or pdf_path.get("file_path")
            or pdf_path.get("pdf_path")
        )

    if not pdf_path:
        raise ValueError(
            "PDF path is missing."
        )

    pdf_path = Path(
        str(pdf_path)
    )

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    pages = render_pdf_pages(
        pdf_path,
        dpi=dpi,
    )

    documents = []

    for page_data in pages:

        page_number = page_data[
            "page"
        ]

        image = page_data[
            "image"
        ]

        text = extract_text(
            image
        )

        text = text.strip()

        if not text:
            continue

        document = Document(

            page_content=text,

            metadata={
                "source": pdf_path.name,
                "file_name": pdf_path.name,
                "page": page_number,
                "page_number": page_number + 1,
                "ocr": True,
            },
        )

        documents.append(
            document
        )

    return documents