import streamlit as st
from PIL import Image

from src.ocr.ocr_engine import extract_text
from src.ocr.pdf_reader import read_pdf


def show():
    st.title("📝 OCR - Optical Character Recognition")

    st.write(
        "Upload an image or PDF and extract text using OCR."
    )

    uploaded_file = st.file_uploader(
        "Upload Image or PDF",
        type=[
            "png",
            "jpg",
            "jpeg",
            "bmp",
            "webp",
            "pdf",
        ],
    )

    if uploaded_file is None:
        st.info("Upload an image or PDF to start OCR.")
        return

    try:
        file_name = uploaded_file.name.lower()

        # ==================================================
        # IMAGE
        # ==================================================
        if file_name.endswith(
            (".png", ".jpg", ".jpeg", ".bmp", ".webp")
        ):

            st.subheader("Uploaded Image")

            image = Image.open(uploaded_file).convert("RGB")

            st.image(
                image,
                caption="Input Image",
                use_container_width=True,
            )

            with st.spinner("Extracting text from image..."):
                text = extract_text(image)

            st.subheader("Extracted Text")

            if text and text.strip():
                st.text_area(
                    "OCR Result",
                    text,
                    height=250,
                )
            else:
                st.warning("No text detected in the image.")

        # ==================================================
        # PDF
        # ==================================================
        elif file_name.endswith(".pdf"):

            st.subheader("Uploaded PDF")

            with st.spinner("Reading PDF..."):
                pages = read_pdf(uploaded_file)

            st.success(
                f"PDF loaded successfully: {len(pages)} page(s)"
            )

            all_text = []

            for page_number, page_image in enumerate(pages, start=1):

                st.markdown(f"### Page {page_number}")

                st.image(
                    page_image,
                    caption=f"PDF Page {page_number}",
                    use_container_width=True,
                )

                with st.spinner(
                    f"Running OCR on page {page_number}..."
                ):
                    page_text = extract_text(page_image)

                if page_text and page_text.strip():
                    all_text.append(
                        f"--- Page {page_number} ---\n"
                        f"{page_text}"
                    )

            final_text = "\n\n".join(all_text)

            st.subheader("Extracted Text")

            if final_text.strip():
                st.text_area(
                    "OCR Result",
                    final_text,
                    height=400,
                )
            else:
                st.warning("No text detected in the PDF.")

        else:
            st.error("Unsupported file type.")

    except Exception as e:
        st.error(f"OCR Error: {str(e)}")
        st.exception(e)
