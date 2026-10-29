import streamlit as st

from src.ui import pages


FEATURES = [
    (pages.ASK, "🧠", "Ask MathMind",
     "Type any question. It picks the calculator, algebra engine or AI agents for you."),
    (pages.CHAT, "💬", "AI Tutor Chat",
     "Chat with a maths tutor that explains every step and remembers the conversation."),
    (pages.DOCS, "📚", "Document Q&A",
     "Upload your notes or textbook PDF and ask questions about it (RAG)."),
    (pages.SYMBOLIC, "∫", "Algebra & Calculus",
     "Solve equations, factor, differentiate, integrate and find limits."),
    (pages.GRAPH, "📈", "Graph Plotter",
     "Plot one or many functions and see their shape instantly."),
    (pages.OCR, "📷", "Scan & Solve",
     "Take a photo of a question, read it with OCR and solve it."),
    (pages.MATRIX, "🔢", "Matrices & Linear Algebra",
     "Determinant, inverse, eigenvalues, LU/QR/SVD and more."),
    (pages.STATS, "📊", "Statistics",
     "Mean, median, variance, quartiles, z-scores and charts."),
    (pages.VISION, "🖼️", "Image Lab",
     "Filters, edge detection, thresholds and contours with OpenCV."),
]


def show():

    st.markdown(
        """
        <div class="mm-hero">
            <h1>🧠 MathMind AI</h1>
            <p>
                Your AI maths companion: solve, explain and visualise
                problems from basic arithmetic to calculus, matrices,
                statistics and your own study material.
            </p>
            <div class="mm-badges">
                <span class="mm-badge">SymPy</span>
                <span class="mm-badge">Multi-agent reasoning</span>
                <span class="mm-badge">RAG over PDFs</span>
                <span class="mm-badge">OCR</span>
                <span class="mm-badge">OpenCV</span>
                <span class="mm-badge">Gemini · Groq · OpenAI</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("What would you like to do?")

    for start in range(0, len(FEATURES), 3):

        columns = st.columns(3)

        for column, feature in zip(columns, FEATURES[start:start + 3]):

            page, icon, title, text = feature

            with column:

                st.markdown(
                    f"""
                    <div class="mm-card">
                        <div class="mm-card-icon">{icon}</div>
                        <h3>{title}</h3>
                        <p>{text}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.page_link(page, label=f"Open {title} →")

    st.divider()

    st.subheader("How it works")

    st.markdown(
        """
        1. **You ask** a question by typing, chatting, uploading a PDF or scanning a photo.
        2. **The router** decides whether it is arithmetic, algebra/calculus, a document
           question or a reasoning problem.
        3. **The right engine answers**: exact maths with SymPy/NumPy, or the
           Planner → Solver → Reviewer → Teacher agents using an LLM.
        4. **You learn**: every answer comes with steps you can follow.
        """
    )
