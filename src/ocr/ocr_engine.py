from pathlib import Path

import easyocr


_reader = None


def get_reader():
    """
    Create EasyOCR reader only once.
    This prevents the model from loading again
    for every page/document.
    """

    global _reader

    if _reader is None:
        _reader = easyocr.Reader(
            ["en"],
            gpu=False,
        )

    return _reader


def extract_text(image):
    """
    Extract text from an IMAGE using EasyOCR.

    IMPORTANT:
    EasyOCR does not read PDF files directly.
    The PDF page must first be converted to an image.
    """

    if image is None:
        raise ValueError(
            "OCR received an empty image."
        )

    reader = get_reader()

    results = reader.readtext(
        image,
        detail=0,
        paragraph=True,
    )

    text = "\n".join(
        str(item).strip()
        for item in results
        if str(item).strip()
    )

    return text