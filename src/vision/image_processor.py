from __future__ import annotations

from pathlib import Path
from typing import Union

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


ImageInput = Union[
    str,
    Path,
    Image.Image,
]


def load_image(
    image: ImageInput,
) -> Image.Image:
    """
    Load an image from a path or return
    a copy of an existing PIL image.
    """

    if isinstance(
        image,
        Image.Image,
    ):
        return image.copy()

    path = Path(image)

    if not path.exists():

        raise FileNotFoundError(
            f"Image not found: {path}"
        )

    if not path.is_file():

        raise ValueError(
            f"Path is not a file: {path}"
        )

    try:

        with Image.open(path) as img:

            return img.convert(
                "RGB"
            )

    except Exception as error:

        raise ValueError(
            f"Unable to load image: {error}"
        ) from error


def preprocess_image(
    image: ImageInput,
    grayscale: bool = True,
    enhance_contrast: bool = True,
    sharpen: bool = True,
    scale: float = 1.5,
) -> Image.Image:
    """
    Preprocess an image for mathematical
    OCR / vision processing.
    """

    img = load_image(
        image
    )

    if grayscale:

        img = ImageOps.grayscale(
            img
        )

    if enhance_contrast:

        enhancer = ImageEnhance.Contrast(
            img
        )

        img = enhancer.enhance(
            1.5
        )

    if sharpen:

        img = img.filter(
            ImageFilter.SHARPEN
        )

    if scale <= 0:

        raise ValueError(
            "Scale must be greater than zero."
        )

    if scale != 1.0:

        width = max(
            1,
            int(
                img.width * scale
            ),
        )

        height = max(
            1,
            int(
                img.height * scale
            ),
        )

        img = img.resize(
            (
                width,
                height,
            )
        )

    return img


class ImageMathProcessor:
    """
    Image processing layer for MathMind AI.

    This module intentionally handles image
    preprocessing separately from the LLM/OCR layer.
    """

    def __init__(
        self,
        grayscale: bool = True,
        enhance_contrast: bool = True,
        sharpen: bool = True,
        scale: float = 1.5,
    ):

        self.grayscale = grayscale

        self.enhance_contrast = (
            enhance_contrast
        )

        self.sharpen = sharpen

        self.scale = scale

    def process(
        self,
        image: ImageInput,
    ) -> Image.Image:

        return preprocess_image(
            image=image,
            grayscale=self.grayscale,
            enhance_contrast=(
                self.enhance_contrast
            ),
            sharpen=self.sharpen,
            scale=self.scale,
        )

    def validate(
        self,
        image: ImageInput,
    ) -> bool:

        try:

            img = load_image(
                image
            )

            return (
                img.width > 0
                and img.height > 0
            )

        except Exception:

            return False