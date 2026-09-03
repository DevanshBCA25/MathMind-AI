from pathlib import Path

from langchain_core.documents import Document

from src.ocr.pdf_reader import read_pdf
from src.ocr.ocr_engine import extract_text


DOCUMENTS_DIR = Path("data/documents")


def main():

    print("=" * 70)
    print("MathMind-AI — OCR Pipeline Test")
    print("=" * 70)

    pdf_files = sorted(
        DOCUMENTS_DIR.glob("*.pdf")
    )

    print(
        f"\nFound {len(pdf_files)} PDF file(s).\n"
    )

    all_documents = []

    for index, pdf_path in enumerate(
        pdf_files,
        start=1,
    ):

        print(
            f"--- PDF {index}: "
            f"{pdf_path.name}"
        )

        try:

            pages = read_pdf(
                pdf_path
            )

            pdf_documents = []

            for page_data in pages:

                page_number = (
                    page_data["page"]
                )

                existing_text = (
                    page_data["text"]
                )

                ocr_text = extract_text(
                    page_data["image"]
                )

                # Combine native PDF text
                # and OCR text.
                combined_text = (
                    existing_text.strip()
                    + "\n"
                    + ocr_text.strip()
                ).strip()

                if not combined_text:
                    continue

                document = Document(
                    page_content=combined_text,
                    metadata={
                        "source": pdf_path.name,
                        "page": page_number,
                        "page_number": page_number + 1,
                        "ocr": True,
                    },
                )

                pdf_documents.append(
                    document
                )

                all_documents.append(
                    document
                )

            print(
                f"✅ OCR successful"
            )

            print(
                f"Pages processed: "
                f"{len(pages)}"
            )

            print(
                f"Documents created: "
                f"{len(pdf_documents)}"
            )

            if pdf_documents:

                preview = (
                    pdf_documents[0]
                    .page_content[:500]
                )

                print(
                    "\nPreview:"
                )

                print(preview)

        except Exception as error:

            print(
                f"❌ OCR failed: {error}"
            )

        print()

    print("=" * 70)
    print(
        "OCR PIPELINE TEST COMPLETE"
    )

    print(
        f"Total LangChain Documents: "
        f"{len(all_documents)}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()