import streamlit as st

from src.core.unified_solver import UnifiedSolver


def show():
    """
    MathMind AI Unified Solver UI

    Automatically routes questions to:
        Calculator
        Symbolic Mathematics
        RAG
        Multi-Agent System
    """

    st.title("🧠 MathMind AI — Unified Solver")

    st.caption(
        "One intelligent interface for mathematical reasoning"
    )

    st.markdown(
        """
        ### 🚀 How it works

        Enter any mathematical question.

        MathMind AI automatically determines the
        appropriate solving module:

        **Question → Classifier → Solver → Answer**
        """
    )

    st.divider()

    # ==========================================================
    # SETTINGS
    # ==========================================================

    col1, col2 = st.columns(2)

    with col1:

        provider = st.selectbox(
            "🤖 LLM Provider",
            [
                "Gemini",
                "OpenAI",
                "Groq",
                "Ollama",
            ],
            key="unified_provider",
        )

    with col2:

        force_module = st.selectbox(
            "⚙️ Solver Mode",
            [
                "Automatic",
                "Calculator",
                "Symbolic",
                "RAG",
                "Agent",
            ],
            key="unified_mode",
        )

    st.divider()

    # ==========================================================
    # QUESTION
    # ==========================================================

    question = st.text_area(
        "📝 Enter your question",
        placeholder=(
            "Examples:\n"
            "• 25 + 35\n"
            "• Solve x² + 5x + 6 = 0\n"
            "• Differentiate x³ + 2x\n"
            "• Explain why the quadratic formula works\n"
            "• According to the uploaded document, what is..."
        ),
        height=180,
        key="unified_question",
    )

    col1, col2 = st.columns(2)

    with col1:

        solve_button = st.button(
            "🚀 Solve",
            use_container_width=True,
            type="primary",
        )

    with col2:

        clear_button = st.button(
            "🗑️ Clear",
            use_container_width=True,
        )

    if clear_button:

        st.session_state[
            "unified_question"
        ] = ""

        st.rerun()

    if not solve_button:

        return

    if not question.strip():

        st.warning(
            "Please enter a question first."
        )

        return

    # ==========================================================
    # SOLVER
    # ==========================================================

    try:

        with st.spinner(
            "🧠 MathMind AI is solving..."
        ):

            solver = UnifiedSolver(
                provider=provider
            )

            selected_module = None

            if force_module != "Automatic":

                selected_module = (
                    force_module.lower()
                )

            result = solver.solve(
                question=question,
                force_module=selected_module,
            )

        st.divider()

        # ======================================================
        # STATUS
        # ======================================================

        status = result.get(
            "status",
            "UNKNOWN",
        )

        module = result.get(
            "module",
            "unknown",
        )

        if status == "SUCCESS":

            st.success(
                "✅ Successfully solved."
            )

        elif status in (
            "API_ERROR",
            "UNAVAILABLE",
        ):

            st.warning(
                "⚠️ Solver completed with a "
                "provider/API limitation."
            )

        else:

            st.info(
                f"Solver status: {status}"
            )

        # ======================================================
        # ROUTING INFORMATION
        # ======================================================

        st.markdown(
            "### 🔀 Solver Routing"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Detected Module",
                str(module).upper(),
            )

        with col2:

            st.metric(
                "Provider",
                provider,
            )

        with col3:

            st.metric(
                "Status",
                status,
            )

        st.divider()

        # ======================================================
        # FINAL ANSWER
        # ======================================================

        st.markdown(
            "### 💡 Answer"
        )

        answer = result.get(
            "answer",
            "",
        )

        if answer:

            st.markdown(
                str(answer)
            )

        else:

            st.warning(
                result.get(
                    "result",
                    {}
                ).get(
                    "message",
                    "No answer was generated.",
                )
            )

        # ======================================================
        # MODULE DETAILS
        # ======================================================

        raw_result = result.get(
            "result",
            {},
        )

        if isinstance(
            raw_result,
            dict,
        ):

            # ------------------------------
            # AGENT DETAILS
            # ------------------------------

            if module == "agent":

                st.divider()

                st.markdown(
                    "### 🤖 Multi-Agent Workflow"
                )

                plan = raw_result.get(
                    "plan"
                )

                solution = raw_result.get(
                    "solution"
                )

                review = raw_result.get(
                    "review"
                )

                explanation = raw_result.get(
                    "explanation"
                )

                if plan:

                    with st.expander(
                        "🧠 Planner",
                        expanded=False,
                    ):

                        st.write(plan)

                if solution:

                    with st.expander(
                        "🧮 Solver",
                        expanded=False,
                    ):

                        st.write(solution)

                if review:

                    with st.expander(
                        "🔍 Reviewer",
                        expanded=False,
                    ):

                        st.write(review)

                if explanation:

                    with st.expander(
                        "👨‍🏫 Teacher",
                        expanded=True,
                    ):

                        st.write(
                            explanation
                        )

            # ------------------------------
            # RAG DETAILS
            # ------------------------------

            if module == "rag":

                st.divider()

                st.markdown(
                    "### 📚 RAG Information"
                )

                sources = raw_result.get(
                    "sources",
                    [],
                )

                if sources:

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

                        content = source.get(
                            "content",
                            "",
                        )

                        with st.expander(
                            f"📄 Source {index}: "
                            f"{source_name}"
                        ):

                            if page is not None:

                                st.write(
                                    f"Page: {page}"
                                )

                            st.write(
                                content
                            )

                else:

                    st.info(
                        "No source information available."
                    )

        # ======================================================
        # RAW OUTPUT
        # ======================================================

        with st.expander(
            "🔧 Raw Unified Solver Output"
        ):

            st.json(result)

    except Exception as error:

        st.error(
            "❌ Unified Solver execution failed."
        )

        st.exception(error)