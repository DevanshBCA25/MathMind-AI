import fitz
from PIL import Image


def render_pdf_pages(uploaded_file):
    """
    Render a Streamlit UploadedFile PDF directly from memory.
    No temporary local file path is required.
    """

    try:
        uploaded_file.seek(0)

        pdf_bytes = uploaded_file.read()

        if not pdf_bytes:
            raise FileNotFoundError(
                "Uploaded PDF is empty."
            )

        document = fitz.open(
            stream=pdf_bytes,
            filetype="pdf",
        )

        if document.page_count == 0:
            document.close()
            raise FileNotFoundError(
                "PDF contains no pages."
            )

        pages = []

        for page_number in range(document.page_count):

            page = document.load_page(page_number)

            matrix = fitz.Matrix(2, 2)

            pix = page.get_pixmap(
                matrix=matrix,
                alpha=False,
            )

            image = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples,
            )

            pages.append(image)

        document.close()

        return pages

    except Exception as e:
        raise RuntimeError(
            f"Unable to render PDF: {str(e)}"
        )


def read_pdf(uploaded_file):
    """
    Read uploaded PDF and return rendered page images.
    """

    return render_pdf_pages(uploaded_file)
