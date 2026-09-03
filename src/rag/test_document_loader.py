from pathlib import Path

from src.rag.document_loader import (
    DocumentLoader,
)


DOCUMENTS_DIR = Path(
    "data/documents"
)


def main():

    print()
    print("=" * 75)
    print("MathMind-AI — Document Loader Test")
    print("=" * 75)

    pdf_files = sorted(
        DOCUMENTS_DIR.glob("*.pdf")
    )

    if not pdf_files:

        print(
            "\n❌ No PDF files found in:"
        )

        print(
            DOCUMENTS_DIR
        )

        return

    print(
        f"\nFound {len(pdf_files)} PDF file(s).\n"
    )

    loader = DocumentLoader(
        ocr_dpi=150
    )

    total_documents = 0
    total_ocr_pages = 0
    total_normal_pages = 0

    # ========================================================
    # PROCESS ALL PDFs
    # ========================================================

    for pdf_file in pdf_files:

        print(
            "-" * 75
        )

        print(
            f"Processing: {pdf_file.name}"
        )

        try:

            documents = loader.load(
                str(pdf_file)
            )

            print(
                f"✅ Loaded successfully: "
                f"{len(documents)} page document(s)"
            )

            for document in documents:

                page_number = document.metadata.get(
                    "page_number",
                    "Unknown",
                )

                ocr = document.metadata.get(
                    "ocr",
                    False,
                )

                loader_type = document.metadata.get(
                    "loader",
                    "Unknown",
                )

                text = (
                    document.page_content
                    .replace("\n", " ")
                    .strip()
                )

                if ocr:

                    total_ocr_pages += 1

                    method = "OCR / EasyOCR"

                else:

                    total_normal_pages += 1

                    method = "PyMuPDF"

                print()

                print(
                    f"   Page       : {page_number}"
                )

                print(
                    f"   Method     : {method}"
                )

                print(
                    f"   Loader     : {loader_type}"
                )

                print(
                    f"   Text chars : {len(text)}"
                )

                print(
                    f"   Preview    : {text[:180]}..."
                )

            total_documents += len(
                documents
            )

        except Exception as error:

            print(
                f"❌ Failed: {error}"
            )

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print()
    print("=" * 75)
    print("DOCUMENT LOADER TEST COMPLETE")
    print("=" * 75)

    print(
        f"Total LangChain Documents : "
        f"{total_documents}"
    )

    print(
        f"Normal PDF Pages          : "
        f"{total_normal_pages}"
    )

    print(
        f"OCR Pages                 : "
        f"{total_ocr_pages}"
    )

    print("=" * 75)

    if total_documents > 0:

        print(
            "\n✅ DOCUMENT LOADER SUCCESSFUL"
        )

        print(
            "Normal PDFs and scanned PDFs "
            "are now supported."
        )

    else:

        print(
            "\n❌ No documents were loaded."
        )


if __name__ == "__main__":

    main()