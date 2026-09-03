import streamlit as st

from src.agents.rag_agent_graph import RAGAgentGraph


SUPPORTED_PROVIDERS = [
    "Gemini",
    "OpenAI",
    "Groq",
    "Ollama",
]

SUPPORTED_RETRIEVAL = [
    "similarity",
    "mmr",
]


def _display_value(value):
    """Safely display dictionaries, lists and strings."""

    if value is None:
        return

    if isinstance(value, dict):
        st.json(value)

    elif isinstance(value, list):
        st.write(value)

    else:
        st.markdown(str(value))


def _display_sources(sources):
    """Display retrieved document sources."""

    if not sources:
        st.info("No sources returned.")
        return

    st.markdown("### 📖 Retrieved Sources")

    for index, source in enumerate(sources, start=1):

        if isinstance(source, dict):

            source_name = source.get(
                "source",
                "Unknown Source",
            )

            page = source.get(
                "page",
                None,
            )

            content = source.get(
                "content",
                "",
            )

            if page is not None:
                page_label = f"Page {int(page) + 1}"
            else:
                page_label = "Page unavailable"

        else:

            source_name = f"Source {index}"
            page_label = "Page unavailable"
            content = str(source)

        with st.expander(
            f"📄 {index}. {source_name} — {page_label}"
        ):

            st.write(content)


def _display_agent_result(result):
    """Display complete multi-agent workflow."""

    # ==========================================================
    # STATUS
    # ==========================================================

    status = result.get(
        "status",
        "UNKNOWN",
    )

    if status == "SUCCESS":

        st.success(
            "✅ RAG + Multi-Agent workflow completed successfully."
        )

    elif status in (
        "API_ERROR",
        "AGENT_ERROR",
    ):

        st.warning(
            "⚠️ Retrieval and workflow executed, "
            "but the selected LLM provider needs attention."
        )

    elif status == "NO_CONTEXT":

        st.warning(
            "⚠️ No relevant context was found "
            "in the uploaded documents."
        )

    else:

        st.warning(
            f"Workflow status: {status}"
        )

    st.divider()

    # ==========================================================
    # STEP 1 — RETRIEVAL
    # ==========================================================

    retrieval = result.get(
        "retrieval",
        {},
    )

    with st.expander(
        "📚 Step 1 — RAG Retrieval",
        expanded=True,
    ):

        if isinstance(retrieval, dict):

            st.write(
                "**Retrieval Status:**",
                retrieval.get(
                    "status",
                    "UNKNOWN",
                ),
            )

            documents = retrieval.get(
                "documents",
                [],
            )

            st.write(
                f"**Retrieved Documents:** {len(documents)}"
            )

        else:

            _display_value(retrieval)

    # ==========================================================
    # STEP 2 — CONTEXT
    # ==========================================================

    context = result.get(
        "context",
        "",
    )

    if context:

        with st.expander(
            "📄 Step 2 — Retrieved Context",
            expanded=False,
        ):

            st.text(
                str(context)
            )

    # ==========================================================
    # SOURCES
    # ==========================================================

    sources = result.get(
        "sources",
        [],
    )

    if sources:

        with st.expander(
            "📖 Retrieved Sources",
            expanded=False,
        ):

            _display_sources(
                sources
            )

    # ==========================================================
    # AGENTS
    # ==========================================================

    agents = result.get(
        "agents",
        {},
    )

    if agents:

        # ------------------------------------------------------
        # PLANNER
        # ------------------------------------------------------

        plan = agents.get(
            "plan",
            "",
        )

        with st.expander(
            "🧠 Step 3 — Planner",
            expanded=True,
        ):

            if plan:
                _display_value(plan)
            else:
                st.info(
                    "Planner did not return a result."
                )

        # ------------------------------------------------------
        # SOLVER
        # ------------------------------------------------------

        solver = agents.get(
            "solver",
            "",
        )

        solution = agents.get(
            "solution",
            "",
        )

        with st.expander(
            "🧮 Step 4 — Solver",
            expanded=True,
        ):

            if solver:
                _display_value(solver)

            if solution:

                st.markdown(
                    "### Solution"
                )

                st.markdown(
                    str(solution)
                )

            if not solver and not solution:

                st.info(
                    "Solver did not return a solution."
                )

        # ------------------------------------------------------
        # REVIEWER
        # ------------------------------------------------------

        review = agents.get(
            "review",
            "",
        )

        with st.expander(
            "🔍 Step 5 — Reviewer",
            expanded=True,
        ):

            if review:
                _display_value(review)

            else:

                st.info(
                    "Reviewer did not return a result."
                )

        # ------------------------------------------------------
        # TEACHER
        # ------------------------------------------------------

        teacher = agents.get(
            "teacher",
            "",
        )

        explanation = agents.get(
            "explanation",
            "",
        )

        with st.expander(
            "👨‍🏫 Step 6 — Teacher",
            expanded=True,
        ):

            if explanation:

                st.info(
                    str(explanation)
                )

            elif teacher:

                _display_value(
                    teacher
                )

            else:

                st.info(
                    "Teacher did not return an explanation."
                )

    # ==========================================================
    # FINAL ANSWER
    # ==========================================================

    final_answer = result.get(
        "final_answer",
        "",
    )

    explanation = result.get(
        "explanation",
        "",
    )

    if not final_answer and explanation:
        final_answer = explanation

    if final_answer:

        st.divider()

        st.markdown(
            "## 🎯 Final Answer"
        )

        st.success(
            str(final_answer)
        )

    # ==========================================================
    # WORKFLOW MESSAGE
    # ==========================================================

    message = result.get(
        "message",
        "",
    )

    if message:

        with st.expander(
            "⚠️ Workflow Details",
            expanded=False,
        ):

            st.code(
                str(message)
            )

    # ==========================================================
    # RAW OUTPUT
    # ==========================================================

    with st.expander(
        "🔧 Raw Integrated Output",
        expanded=False,
    ):

        st.json(
            result
        )


def show():
    """
    RAG + Multi-Agent Streamlit UI.

    Workflow:

        Question
            ↓
        RAG Retrieval
            ↓
        Context
            ↓
        Planner
            ↓
        Solver
            ↓
        Reviewer
            ↓
        Teacher
            ↓
        Final Answer
    """

    st.title(
        "🧠📚 MathMind AI — RAG + Multi-Agent Assistant"
    )

    st.caption(
        "Document-Aware Multi-Agent Mathematical Reasoning"
    )

    st.markdown(
        """
        ### 🔄 Complete Workflow

        **Question → RAG → Planner → Solver → Reviewer → Teacher → Final Answer**

        The agents use information retrieved from your
        uploaded mathematical documents.
        """
    )

    st.divider()

    # ==========================================================
    # GET RAG PIPELINE
    # ==========================================================

    pipeline = st.session_state.get(
        "rag_pipeline"
    )

    if pipeline is None:

        st.warning(
            "⚠️ RAG pipeline is not loaded."
        )

        st.info(
            "Go to the RAG Assistant module and "
            "Build/Rebuild or Load the vector database first."
        )

        return

    # ==========================================================
    # SETTINGS
    # ==========================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        provider = st.selectbox(
            "🤖 LLM Provider",
            SUPPORTED_PROVIDERS,
            key="rag_agent_provider",
        )

    with col2:

        retrieval_method = st.selectbox(
            "🔎 Retrieval Method",
            SUPPORTED_RETRIEVAL,
            key="rag_agent_retrieval",
        )

    with col3:

        top_k = st.slider(
            "📚 Top-K",
            min_value=1,
            max_value=10,
            value=4,
            key="rag_agent_top_k",
        )

    st.divider()

    # ==========================================================
    # QUESTION
    # ==========================================================

    question = st.text_area(
        "📝 Enter your mathematical question",
        placeholder=(
            "Example:\n"
            "According to the uploaded document, "
            "solve the worked example and explain why "
            "the answer is correct."
        ),
        height=160,
        key="rag_agent_question",
    )

    col1, col2 = st.columns(2)

    with col1:

        run_button = st.button(
            "🚀 Run RAG + Agents",
            use_container_width=True,
            type="primary",
        )

    with col2:

        clear_button = st.button(
            "🗑 Clear",
            use_container_width=True,
        )

    # ==========================================================
    # CLEAR
    # ==========================================================

    if clear_button:

        st.session_state.pop(
            "rag_agent_question",
            None,
        )

        st.session_state.pop(
            "rag_agent_result",
            None,
        )

        st.rerun()

    if not run_button:
        return

    if not question.strip():

        st.warning(
            "Please enter a mathematical question."
        )

        return

    # ==========================================================
    # SYNC PIPELINE SETTINGS
    # ==========================================================

    try:

        pipeline.change_provider(
            provider
        )

        pipeline.change_retrieval_method(
            retrieval_method
        )

        pipeline.change_top_k(
            top_k
        )

    except AttributeError:

        # Compatibility with older pipeline versions.

        pipeline.provider = provider
        pipeline.retrieval_method = retrieval_method
        pipeline.top_k = int(top_k)

    # ==========================================================
    # CREATE RAG AGENT GRAPH
    # ==========================================================

    try:

        with st.spinner(
            "📚 Retrieving documents and running AI agents..."
        ):

            # IMPORTANT:
            # vector_db MUST be passed.
            # Your previous error came from this constructor.

            integrated_graph = RAGAgentGraph(
                vector_db=pipeline.vector_db,
                rag_pipeline=pipeline,
                provider=provider,
                retrieval_method=retrieval_method,
                top_k=top_k,
            )

            # Optional setters for compatibility.

            if hasattr(
                integrated_graph,
                "set_provider",
            ):

                integrated_graph.set_provider(
                    provider
                )

            if hasattr(
                integrated_graph,
                "set_retrieval_method",
            ):

                integrated_graph.set_retrieval_method(
                    retrieval_method
                )

            if hasattr(
                integrated_graph,
                "set_top_k",
            ):

                integrated_graph.set_top_k(
                    top_k
                )

            result = integrated_graph.run(
                question
            )

        st.session_state[
            "rag_agent_result"
        ] = result

    except Exception as error:

        st.error(
            "❌ RAG + Agent integration failed."
        )

        st.exception(
            error
        )

        return

    # ==========================================================
    # DISPLAY RESULT
    # ==========================================================

    _display_agent_result(
        result
    )