from pathlib import Path
from typing import List

import fitz

from langchain_core.documents import Document

from src.ocr.ocr_engine import extract_text


class DocumentLoader:
    """
    Production-ready PDF document loader.

    Supports:

    1. Normal text-based PDFs
    2. Scanned/image-based PDFs
    3. Mixed PDFs
       - Some pages contain text
       - Some pages require OCR

    Pipeline:

        PDF
         ↓
        Page
         ↓
        Text extraction
         ↓
        Text found?
        ├── YES → LangChain Document
        │
        └── NO → Render page → EasyOCR
                         ↓
                   LangChain Document
    """

    def __init__(
        self,
        ocr_dpi: int = 150,
    ):

        self.ocr_dpi = ocr_dpi

    # ========================================================
    # PUBLIC METHOD
    # ========================================================

    def load(
        self,
        pdf_path: str,
    ) -> List[Document]:
        """
        Load a PDF and return LangChain Documents.

        Each PDF page becomes one LangChain Document.
        """

        if not pdf_path:

            raise ValueError(
                "PDF path cannot be empty."
            )

        pdf_path = Path(
            str(pdf_path)
        )

        if not pdf_path.exists():

            raise FileNotFoundError(
                f"PDF file not found: {pdf_path}"
            )

        if pdf_path.suffix.lower() != ".pdf":

            raise ValueError(
                f"Expected a PDF file, "
                f"received: {pdf_path.suffix}"
            )

        documents = []

        pdf = None

        try:

            pdf = fitz.open(
                str(pdf_path)
            )

            for page_number in range(
                len(pdf)
            ):

                page = pdf[
                    page_number
                ]

                document = self._process_page(
                    page=page,
                    pdf_path=pdf_path,
                    page_number=page_number,
                )

                if document is not None:

                    documents.append(
                        document
                    )

        finally:

            if pdf is not None:

                pdf.close()

        return documents

    # ========================================================
    # PROCESS SINGLE PAGE
    # ========================================================

    def _process_page(
        self,
        page,
        pdf_path: Path,
        page_number: int,
    ) -> Document | None:
        """
        Process one PDF page.

        First attempts normal PDF text extraction.
        If insufficient text is found, OCR is used.
        """

        # ----------------------------------------------------
        # STEP 1 — NORMAL PDF TEXT EXTRACTION
        # ----------------------------------------------------

        text = page.get_text(
            "text"
        )

        text = (
            text.strip()
            if text
            else ""
        )

        # ----------------------------------------------------
        # STEP 2 — NORMAL TEXT AVAILABLE
        # ----------------------------------------------------

        if text:

            return Document(

                page_content=text,

                metadata={
                    "source": pdf_path.name,
                    "file_name": pdf_path.name,
                    "page": page_number,
                    "page_number": page_number + 1,
                    "ocr": False,
                    "loader": "pymupdf",
                },
            )

        # ----------------------------------------------------
        # STEP 3 — NO TEXT → OCR
        # ----------------------------------------------------

        try:

            image = self._render_page(
                page
            )

            ocr_text = extract_text(
                image
            )

            ocr_text = (
                ocr_text.strip()
                if ocr_text
                else ""
            )

            if not ocr_text:

                return None

            return Document(

                page_content=ocr_text,

                metadata={
                    "source": pdf_path.name,
                    "file_name": pdf_path.name,
                    "page": page_number,
                    "page_number": page_number + 1,
                    "ocr": True,
                    "loader": "easyocr",
                },
            )

        except Exception as error:

            print(
                f"OCR failed for "
                f"{pdf_path.name} "
                f"page {page_number + 1}: "
                f"{error}"
            )

            return None

    # ========================================================
    # RENDER PDF PAGE
    # ========================================================

    def _render_page(
        self,
        page,
    ):
        """
        Convert PDF page into PNG bytes.
        EasyOCR can process the resulting image.
        """

        zoom = (
            self.ocr_dpi / 72.0
        )

        matrix = fitz.Matrix(
            zoom,
            zoom,
        )

        pixmap = page.get_pixmap(
            matrix=matrix,
            alpha=False,
        )

        image_bytes = pixmap.tobytes(
            "png"
        )

        return image_bytes