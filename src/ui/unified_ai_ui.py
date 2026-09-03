import streamlit as st

from src.agents.agent_rag_integration import (
    AgentRAGIntegration,
)

from src.rag.config import (
    VECTOR_DB_DIR,
)

from src.rag.vector_store import (
    VectorDatabase,
)

from src.rag.pipeline import (
    RAGPipeline,
)

from src.rag.memory import (
    ConversationMemory,
)


# ============================================================
# SESSION STATE
# ============================================================

def initialize_session_state():

    if "unified_integration" not in st.session_state:

        st.session_state.unified_integration = None

    if "unified_history" not in st.session_state:

        st.session_state.unified_history = []

    if "unified_rag_ready" not in st.session_state:

        st.session_state.unified_rag_ready = False


# ============================================================
# LOAD RAG PIPELINE
# ============================================================

def load_rag_pipeline(
    provider: str,
    retrieval_method: str,
    top_k: int,
):

    try:

        vector_db_manager = VectorDatabase()

        if not vector_db_manager.exists(
            VECTOR_DB_DIR
        ):

            return None

        vector_db = vector_db_manager.load(
            str(VECTOR_DB_DIR)
        )

        memory = ConversationMemory(
            max_messages=10
        )

        pipeline = RAGPipeline(
            vector_db=vector_db,
            provider=provider,
            retrieval_method=retrieval_method,
            top_k=top_k,
            memory=memory,
        )

        return pipeline

    except Exception as error:

        st.warning(
            f"RAG database could not be loaded: {error}"
        )

        return None


# ============================================================
# INITIALIZE INTEGRATION
# ============================================================

def initialize_integration(
    provider: str,
    retrieval_method: str,
    top_k: int,
):

    rag_pipeline = load_rag_pipeline(
        provider=provider,
        retrieval_method=retrieval_method,
        top_k=top_k,
    )

    integration = AgentRAGIntegration(
        rag_pipeline=rag_pipeline,
    )

    st.session_state.unified_integration = (
        integration
    )

    st.session_state.unified_rag_ready = (
        rag_pipeline is not None
    )

    return integration


# ============================================================
# DISPLAY SOURCES
# ============================================================

def display_sources(
    sources,
):

    if not sources:

        return

    st.markdown(
        "### 📚 Retrieved Sources"
    )

    for index, source in enumerate(
        sources,
        start=1,
    ):

        source_name = source.get(
            "source",
            "Unknown",
        )

        page = source.get(
            "page",
            None,
        )

        if page is not None:

            try:

                page_display = int(page) + 1

            except (
                TypeError,
                ValueError,
            ):

                page_display = page

            title = (
                f"📄 {source_name} — "
                f"Page {page_display}"
            )

        else:

            title = (
                f"📄 {source_name}"
            )

        with st.expander(
            f"{index}. {title}"
        ):

            st.write(
                source.get(
                    "content",
                    "",
                )
            )

            if "score" in source:

                st.caption(
                    f"Similarity Score: "
                    f"{source['score']}"
                )


# ============================================================
# DISPLAY AGENT DETAILS
# ============================================================

def display_agent_details(
    result,
):

    planner = result.get(
        "planner"
    )

    solver = result.get(
        "solver"
    )

    reviewer = result.get(
        "reviewer"
    )

    teacher = result.get(
        "teacher"
    )

    if planner:

        with st.expander(
            "🧠 Planner",
            expanded=False,
        ):

            if isinstance(
                planner,
                dict,
            ):

                st.json(
                    planner
                )

            else:

                st.write(
                    planner
                )

    if solver:

        with st.expander(
            "🧮 Solver",
            expanded=False,
        ):

            if isinstance(
                solver,
                dict,
            ):

                st.json(
                    solver
                )

            else:

                st.write(
                    solver
                )

    if reviewer:

        with st.expander(
            "🔍 Reviewer",
            expanded=False,
        ):

            if isinstance(
                reviewer,
                dict,
            ):

                st.json(
                    reviewer
                )

            else:

                st.write(
                    reviewer
                )

    if teacher:

        with st.expander(
            "👨‍🏫 Teacher",
            expanded=False,
        ):

            if isinstance(
                teacher,
                dict,
            ):

                st.json(
                    teacher
                )

            else:

                st.write(
                    teacher
                )


# ============================================================
# DISPLAY RESULT
# ============================================================

def display_result(
    result,
):

    if not result:

        st.warning(
            "No result returned."
        )

        return

    status = result.get(
        "status",
        "UNKNOWN",
    )

    mode = result.get(
        "mode",
        "unknown",
    )

    if status == "ERROR":

        st.error(
            "❌ Processing failed."
        )

        error = result.get(
            "error",
            "",
        )

        if error:

            error_text = str(
                error
            )

            if any(
                keyword in error_text.lower()
                for keyword in [
                    "api",
                    "key",
                    "quota",
                    "authentication",
                    "401",
                    "403",
                ]
            ):

                st.info(
                    "ℹ️ This appears to be a "
                    "provider/API configuration issue. "
                    "We can fix the API configuration later."
                )

            else:

                st.exception(
                    Exception(
                        error_text
                    )
                )

        return

    st.success(
        f"✅ Completed using {mode.upper()} mode"
    )

    # --------------------------------------------------------
    # ANSWER
    # --------------------------------------------------------

    answer = (
        result.get("answer")
        or result.get("final_answer")
        or result.get("response")
        or ""
    )

    if answer:

        st.markdown(
            "## 📝 Answer"
        )

        st.markdown(
            str(answer)
        )

    # --------------------------------------------------------
    # AGENT DETAILS
    # --------------------------------------------------------

    if mode == "agent":

        display_agent_details(
            result
        )

    # --------------------------------------------------------
    # RAG SOURCES
    # --------------------------------------------------------

    sources = result.get(
        "sources",
        [],
    )

    if sources:

        display_sources(
            sources
        )

    # --------------------------------------------------------
    # RAW RESULT
    # --------------------------------------------------------

    with st.expander(
        "🔧 Raw Result",
        expanded=False,
    ):

        st.json(
            result
        )


# ============================================================
# HISTORY
# ============================================================

def display_history():

    history = (
        st.session_state.unified_history
    )

    if not history:

        return

    st.divider()

    st.markdown(
        "### 🕘 Conversation History"
    )

    for index, item in enumerate(
        history,
        start=1,
    ):

        role = item.get(
            "role",
            "unknown",
        )

        question = item.get(
            "question",
            "",
        )

        mode = item.get(
            "mode",
            "",
        )

        with st.expander(
            f"{index}. "
            f"{role.upper()} "
            f"| {mode.upper()}"
        ):

            st.write(
                "**Question:**"
            )

            st.write(
                question
            )

            answer = item.get(
                "answer",
                "",
            )

            if answer:

                st.write(
                    "**Answer:**"
                )

                st.write(
                    answer
                )


# ============================================================
# MAIN UI
# ============================================================

def show():

    initialize_session_state()

    st.title(
        "🧠 MathMind AI — Unified AI Solver"
    )

    st.caption(
        "Agentic Reasoning + Retrieval-Augmented Generation"
    )

    st.markdown(
        """
        Ask a mathematical question, solve it with
        the Agent system, or ask a question about
        your uploaded documents using RAG.
        """
    )

    # ========================================================
    # SETTINGS
    # ========================================================

    st.sidebar.markdown(
        "## ⚙️ Unified AI Settings"
    )

    mode = st.sidebar.selectbox(
        "Processing Mode",
        [
            "Auto",
            "Agent",
            "RAG",
        ],
        key="unified_mode",
    )

    provider = st.sidebar.selectbox(
        "LLM Provider",
        [
            "Gemini",
            "OpenAI",
            "Groq",
            "Ollama",
        ],
        key="unified_provider",
    )

    retrieval_method = st.sidebar.selectbox(
        "RAG Retrieval",
        [
            "similarity",
            "mmr",
        ],
        key="unified_retrieval",
    )

    top_k = st.sidebar.slider(
        "Top-K",
        min_value=1,
        max_value=10,
        value=4,
        key="unified_top_k",
    )

    # ========================================================
    # RAG STATUS
    # ========================================================

    if st.session_state.unified_rag_ready:

        st.sidebar.success(
            "🟢 RAG Database Ready"
        )

    else:

        st.sidebar.info(
            "⚪ RAG Database Not Loaded"
        )

    # ========================================================
    # INITIALIZE
    # ========================================================

    try:

        integration = (
            st.session_state.unified_integration
        )

        if integration is None:

            integration = initialize_integration(
                provider=provider,
                retrieval_method=retrieval_method,
                top_k=top_k,
            )

    except Exception as error:

        st.error(
            "Unified AI initialization failed."
        )

        st.exception(
            error
        )

        return

    # ========================================================
    # QUESTION
    # ========================================================

    st.markdown(
        "### 💬 Ask Your Question"
    )

    question = st.text_area(
        "Question",
        height=120,
        placeholder=(
            "Example:\n"
            "Solve x² + 5x + 6 = 0\n\n"
            "or\n\n"
            "According to the uploaded document, "
            "what is the area of the rectangle?"
        ),
        key="unified_question",
    )

    # ========================================================
    # EXAMPLES
    # ========================================================

    example = st.selectbox(
        "💡 Example Question",
        [
            "None",
            "Solve 2x + 5 = 15",
            "Find the derivative of x² + 3x",
            "Find the discriminant of 2x² + 5x + 3",
            "According to the uploaded document, "
            "what is the area of the rectangle?",
        ],
        key="unified_example",
    )

    if example != "None":

        question_to_process = example

    else:

        question_to_process = question

    # ========================================================
    # RUN
    # ========================================================

    if st.button(
        "🚀 Run MathMind AI",
        type="primary",
        use_container_width=True,
    ):

        if not question_to_process.strip():

            st.warning(
                "Please enter a question."
            )

            return

        # ----------------------------------------------------
        # Configure integration
        # ----------------------------------------------------

        integration = (
            st.session_state.unified_integration
        )

        if integration is None:

            integration = initialize_integration(
                provider=provider,
                retrieval_method=retrieval_method,
                top_k=top_k,
            )

        # ----------------------------------------------------
        # Refresh RAG provider/settings
        # ----------------------------------------------------

        if integration.rag_pipeline:

            integration.rag_pipeline.change_provider(
                provider
            )

            integration.rag_pipeline.change_retrieval_method(
                retrieval_method
            )

            integration.rag_pipeline.top_k = top_k

        # ----------------------------------------------------
        # Convert UI mode
        # ----------------------------------------------------

        if mode == "Auto":

            execution_mode = "auto"

        elif mode == "Agent":

            execution_mode = "agent"

        else:

            execution_mode = "rag"

        # ----------------------------------------------------
        # Execute
        # ----------------------------------------------------

        with st.spinner(
            "🤖 MathMind AI is thinking..."
        ):

            result = integration.run(
                question=question_to_process.strip(),
                mode=execution_mode,
            )

        # ----------------------------------------------------
        # History
        # ----------------------------------------------------

        answer = (
            result.get("answer")
            or result.get("final_answer")
            or result.get("response")
            or ""
        )

        st.session_state.unified_history.append(
            {
                "role": "user",
                "question": question_to_process.strip(),
                "answer": str(answer),
                "mode": result.get(
                    "mode",
                    execution_mode,
                ),
            }
        )

        # ----------------------------------------------------
        # Display
        # ----------------------------------------------------

        display_result(
            result
        )

    # ========================================================
    # HISTORY
    # ========================================================

    display_history()

    # ========================================================
    # CLEAR HISTORY
    # ========================================================

    if st.session_state.unified_history:

        st.divider()

        if st.button(
            "🗑️ Clear Unified AI History",
            use_container_width=True,
        ):

            st.session_state.unified_history = []

            st.rerun()


__all__ = [
    "show",
]