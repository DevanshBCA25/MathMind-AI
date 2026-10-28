import io

import streamlit as st
from PIL import Image

from src.ui.common import current_provider, page_header


IMAGE_TYPES = ["png", "jpg", "jpeg", "bmp", "webp"]


@st.cache_data(show_spinner=False)
def ocr_image(data: bytes) -> str:

    from src.ocr.ocr_engine import extract_text

    image = Image.open(io.BytesIO(data)).convert("RGB")

    return extract_text(image)


@st.cache_data(show_spinner=False)
def ocr_pdf(data: bytes) -> str:

    from src.ocr.ocr_engine import extract_text
    from src.ocr.pdf_reader import read_pdf

    pages = read_pdf(io.BytesIO(data))

    texts = []

    for number, page in enumerate(pages, start=1):

        text = extract_text(page)

        if text and text.strip():
            texts.append(f"--- Page {number} ---\n{text}")

    return "\n\n".join(texts)


def solve_section(text):
    """
    Let the user correct the OCR text, then solve it.
    """

    st.subheader("Extracted Text")

    question = st.text_area(
        "Check and correct the text if needed, then solve it",
        text,
        height=160,
        key="ocr_question",
    )

    col1, col2 = st.columns(2)

    with col1:

        solve = st.button(
            "🧠 Solve with MathMind",
            type="primary",
            width="stretch",
        )

    with col2:

        st.download_button(
            "⬇ Download text",
            data=question,
            file_name="ocr_text.txt",
            width="stretch",
        )

    if not solve:
        return

    from src.core.unified_solver import UnifiedSolver

    with st.spinner("Solving..."):

        result = UnifiedSolver(
            provider=current_provider()
        ).solve(question)

    details = result.get("result", {}) or {}

    st.caption(
        f"Solved with the **{result.get('module', '?')}** engine"
    )

    if details.get("latex"):
        st.latex(details["latex"])

    elif result.get("answer"):
        st.markdown(result["answer"])

    else:
        st.warning(
            details.get("message")
            or "Could not solve this text. Try editing it above."
        )


def show():

    page_header(
        "📷",
        "Scan & Solve",
        "Read a question from a photo or PDF, then solve it",
    )

    source = st.radio(
        "Input",
        ["Upload a file", "Use camera"],
        horizontal=True,
    )

    if source == "Use camera":

        uploaded_file = st.camera_input(
            "Take a clear photo of the question"
        )

    else:

        uploaded_file = st.file_uploader(
            "Upload Image or PDF",
            type=IMAGE_TYPES + ["pdf"],
        )

    if uploaded_file is None:
        st.info(
            "Tip: crop the photo to just the question and use "
            "good lighting for the best results."
        )
        return

    data = uploaded_file.getvalue()

    name = (uploaded_file.name or "camera.jpg").lower()

    try:

        if name.endswith(".pdf"):

            with st.spinner("Reading PDF with OCR (first run downloads the model)..."):
                text = ocr_pdf(data)

        else:

            col1, col2 = st.columns([1, 1])

            with col1:
                st.image(data, caption="Input image", width="stretch")

            with col2:
                with st.spinner("Reading text (first run downloads the model)..."):
                    text = ocr_image(data)

        if not text.strip():
            st.warning("No text detected. Try a clearer or closer photo.")
            return

        solve_section(text)

    except Exception as e:

        st.error(f"OCR Error: {str(e)}")
