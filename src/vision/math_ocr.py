from __future__ import annotations

import re
from typing import Optional


def normalize_math_text(
    text: Optional[str],
) -> str:
    """
    Normalize common OCR mathematical symbols.
    """

    if text is None:
        return ""

    text = str(text)

    replacements = {
        "×": "*",
        "÷": "/",
        "−": "-",
        "–": "-",
        "—": "-",
        "∕": "/",
        "＝": "=",
        "（": "(",
        "）": ")",
        "［": "[",
        "］": "]",
        "ｘ": "x",
        "²": "^2",
        "³": "^3",
    }

    for old, new in replacements.items():
        text = text.replace(
            old,
            new,
        )

    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text.strip()


def clean_ocr_text(
    text: str,
) -> str:

    text = normalize_math_text(
        text
    )

    text = re.sub(
        r"[^\w\s+\-*/=().,\[\]{}^%?:<>√π]",
        " ",
        text,
    )

    text = re.sub(
        r"[ ]{2,}",
        " ",
        text,
    )

    return text.strip()


def extract_math_text(
    text: Optional[str],
) -> dict:
    """
    Convert OCR text into structured
    mathematical expressions.
    """

    if not text or not str(text).strip():

        return {
            "status": "ERROR",
            "text": "",
            "expressions": [],
            "message": (
                "No mathematical text was provided."
            ),
        }

    cleaned = clean_ocr_text(
        text
    )

    lines = [
        line.strip()
        for line in cleaned.splitlines()
        if line.strip()
    ]

    expressions = []

    for line in lines:

        if (
            "=" in line
            or any(
                symbol in line
                for symbol in [
                    "+",
                    "-",
                    "*",
                    "/",
                    "^",
                ]
            )
        ):

            expressions.append(
                line
            )

    if not expressions:

        expressions.append(
            cleaned
        )

    return {
        "status": "SUCCESS",
        "text": cleaned,
        "expressions": expressions,
        "message": (
            "Mathematical text extracted "
            "successfully."
        ),
    }