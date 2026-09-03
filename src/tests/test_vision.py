from PIL import Image

from src.vision.image_processor import (
    ImageMathProcessor,
    preprocess_image,
)

from src.vision.math_ocr import (
    normalize_math_text,
    extract_math_text,
)


def test_normalize_math_text():

    result = normalize_math_text(
        "2 × x − 5 = 10"
    )

    assert "*" in result

    assert "-" in result

    assert "=" in result


def test_extract_math_text():

    result = extract_math_text(
        "2x + 5 = 15"
    )

    assert (
        result["status"]
        == "SUCCESS"
    )

    assert result["text"]

    assert (
        len(
            result["expressions"]
        )
        > 0
    )


def test_empty_extraction():

    result = extract_math_text(
        ""
    )

    assert (
        result["status"]
        == "ERROR"
    )


def test_image_processing():

    image = Image.new(
        "RGB",
        (100, 100),
        "white",
    )

    processed = preprocess_image(
        image,
    )

    assert processed is not None

    assert processed.width > 0

    assert processed.height > 0


def test_image_processor_class():

    image = Image.new(
        "RGB",
        (100, 100),
        "white",
    )

    processor = ImageMathProcessor()

    assert processor.validate(
        image
    )

    result = processor.process(
        image
    )

    assert result is not None


def test_invalid_image():

    processor = ImageMathProcessor()

    assert (
        processor.validate(
            "this_file_does_not_exist.png"
        )
        is False
    )


if __name__ == "__main__":

    test_normalize_math_text()

    test_extract_math_text()

    test_empty_extraction()

    test_image_processing()

    test_image_processor_class()

    test_invalid_image()

    print()
    print(
        "======================================"
    )

    print(
        "        Vision Module Tests"
    )

    print(
        "======================================"
    )

    print(
        "All tests passed successfully."
    )