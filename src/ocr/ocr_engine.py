import numpy as np
import easyocr


_reader = None


def get_reader():
    global _reader

    if _reader is None:
        _reader = easyocr.Reader(
            ["en"],
            gpu=False,
        )

    return _reader


def extract_text(image):
    """
    Extract text from a PIL image or NumPy image.
    """

    if image is None:
        return ""

    # PIL Image -> NumPy array
    if hasattr(image, "convert"):
        image = image.convert("RGB")
        image = np.array(image)

    reader = get_reader()

    results = reader.readtext(
        image,
        detail=0,
        paragraph=True,
    )

    return "\n".join(results)
