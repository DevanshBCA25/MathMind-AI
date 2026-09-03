from src.ocr.pdf_reader import read_pdf
from src.ocr.ocr_engine import extract_text
from src.ocr.ocr_documents import ocr_text_to_documents


PDF_PATH = "data/documents/your_scanned_pdf.pdf"


def main():

    print("=" * 60)
    print("MathMind-AI OCR → RAG Test")
    print("=" * 60)

    print("\n[1] Reading PDF...")

    pages = read_pdf(PDF_PATH)

    print(
        f"PDF pages detected: {len(pages)}"
    )

    all_text = []

    print("\n[2] Running OCR...")

    for index, page in enumerate(pages):

        try:

            text = extract_text(
                page
            )

            if text:

                all_text.append(
                    text
                )

            print(
                f"Page {index + 1}: "
                f"{len(text)} characters"
            )

        except Exception as error:

            print(
                f"Page {index + 1} OCR error: "
                f"{error}"
            )

    combined_text = "\n\n".join(
        all_text
    )

    print(
        f"\nTotal OCR text: "
        f"{len(combined_text)} characters"
    )

    print("\n[3] Converting OCR text to Documents...")

    documents = ocr_text_to_documents(
        text=combined_text,
        source_name="OCR_Test_Document.pdf",
    )

    print(
        f"LangChain Documents created: "
        f"{len(documents)}"
    )

    print("\n[4] Preview:")

    for index, document in enumerate(
        documents[:3],
        start=1,
    ):

        print("\n" + "-" * 50)

        print(
            f"Document {index}"
        )

        print(
            document.page_content[:500]
        )

        print(
            "\nMetadata:"
        )

        print(
            document.metadata
        )

    print("\n" + "=" * 60)
    print("OCR → RAG TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()