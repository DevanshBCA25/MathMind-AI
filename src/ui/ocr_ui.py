import streamlit as st
import pandas as pd
from io import BytesIO

from src.ocr.ocr_engine import extract_text
from src.ocr.pdf_reader import read_pdf
from src.ocr.utils import save_text

from src.utils.helpers import (
    save_operation,
    log_error,
)


def show():

    st.title("📄 OCR - Optical Character Recognition")

    file = st.file_uploader(
        "Upload Image or PDF",
        type=["png", "jpg", "jpeg", "bmp", "pdf"],
    )

    if file is None:
        st.info("Upload a file to start OCR.")
        return

    if file.type == "application/pdf":

        text = read_pdf(file)

        st.subheader("Extracted Text")

        st.text_area(
            "",
            value=text,
            height=300,
        )

        output_file = save_text(text)

        st.download_button(
            "⬇ Download Text",
            data=text,
            file_name="ocr_output.txt",
            mime="text/plain",
        )

        save_operation(
            module="OCR",
            operation="PDF OCR",
            input_data=file.name,
            result="Success",
        )

        return

    try:

        extracted_text, confidence = extract_text(file)

        final_text = "\n".join(extracted_text)

        st.subheader("Extracted Text")

        st.text_area(
            "",
            value=final_text,
            height=250,
        )

        st.subheader("Confidence Score")

        df = pd.DataFrame(
            {
                "Text": extracted_text,
                "Confidence": confidence,
            }
        )

        st.dataframe(
            df,
            use_container_width=True,
        )

        output_file = save_text(final_text)

        st.download_button(
            "⬇ Download Text",
            data=final_text,
            file_name="ocr_output.txt",
            mime="text/plain",
        )

        save_operation(
            module="OCR",
            operation="Image OCR",
            input_data=file.name,
            result="Success",
        )

    except Exception as e:

        log_error(str(e))

        st.error(e)