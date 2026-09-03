from pathlib import Path


def save_text(text):

    folder = Path("data/ocr")

    folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    file = folder / "ocr_output.txt"

    with open(
        file,
        "w",
        encoding="utf-8",
    ) as f:

        f.write(text)

    return file