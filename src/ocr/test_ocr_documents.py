from pathlib import Path

from src.ocr.ocr_documents import process_pdf


DOCUMENTS_DIR = Path("data/documents")


def main():

    print()
    print("=" * 70)
    print("MathMind-AI — OCR → LangChain Test")
    print("=" * 70)

    pdf_files = sorted(
        DOCUMENTS_DIR.glob("*.pdf")
    )

    print(
        f"\nFound {len(pdf_files)} PDF file(s).\n"
    )

    total_documents = 0

    for pdf_file in pdf_files:

        print(
            f"Processing: {pdf_file.name}"
        )

        try:

            documents = process_pdf(
                pdf_file
            )

            print(
                f"✅ OCR successful: "
                f"{len(documents)} LangChain document(s)"
            )

            for document in documents:

                page_number = document.metadata.get(
                    "page_number",
                    "Unknown",
                )

                text = (
                    document.page_content
                    .replace("\n", " ")
                    .strip()
                )

                print(
                    f"   Page: {page_number}"
                )

                print(
                    f"   Text: {text[:200]}..."
                )

            total_documents += len(
                documents
            )

        except Exception as error:

            print(
                f"❌ OCR failed: {error}"
            )

        print()

    print("=" * 70)
    print("OCR → LangChain test complete.")
    print(
        f"Total LangChain Documents: "
        f"{total_documents}"
    )
    print("=" * 70)


if __name__ == "__main__":
    main()