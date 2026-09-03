from pathlib import Path

import fitz


def render_pdf_pages(pdf_path, dpi=150):
    """
    Convert every PDF page into an image.

    Returns:
        List of dictionaries containing:
        - page number
        - rendered image
        - pdf path
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

    pdf_path = Path(str(pdf_path))

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    pages = []

    document = fitz.open(
        str(pdf_path)
    )

    try:

        zoom = dpi / 72.0

        matrix = fitz.Matrix(
            zoom,
            zoom,
        )

        for page_number, page in enumerate(
            document
        ):

            pixmap = page.get_pixmap(
                matrix=matrix,
                alpha=False,
            )

            image = pixmap.tobytes(
                "png"
            )

            pages.append(
                {
                    "page": page_number,
                    "image": image,
                    "path": str(pdf_path),
                }
            )

    finally:

        document.close()

    return pages


def read_pdf(pdf_path):
    """
    Backward-compatible PDF reader.

    Returns rendered PDF pages.
    """

    return render_pdf_pages(
        pdf_path
    )