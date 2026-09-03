import streamlit as st

from src.agents.agent_graph import MathMindAgentGraph


def show():
    """
    MathMind AI - Multi-Agent Assistant UI

    Workflow:
        Planner
          ↓
        Solver
          ↓
        Reviewer
          ↓
        Teacher
    """

    st.title("🤖 MathMind AI — Agent Assistant")

    st.caption(
        "Multi-Agent Mathematical Reasoning System"
    )

    st.markdown(
        """
        ### 🧠 How it works

        Your mathematical problem is processed through
        four specialized AI agents:

        **Planner → Solver → Reviewer → Teacher**

        - 🧠 Planner — analyzes the problem
        - 🧮 Solver — solves the problem
        - 🔍 Reviewer — checks the solution
        - 👨‍🏫 Teacher — explains the final result
        """
    )

    st.divider()

    # ==================================================
    # PROVIDER
    # ==================================================

    provider = st.selectbox(
        "🤖 Agent LLM Provider",
        [
            "Gemini",
            "OpenAI",
            "Groq",
            "Ollama",
        ],
        key="agent_provider",
    )

    st.caption(
        f"Selected provider: **{provider}**"
    )

    # ==================================================
    # QUESTION
    # ==================================================

    question = st.text_area(
        "📝 Enter your mathematical problem",
        placeholder=(
            "Example: Solve 2x² + 5x - 3 = 0 "
            "and explain the steps."
        ),
        height=150,
        key="agent_question",
    )

    # ==================================================
    # BUTTONS
    # ==================================================

    col1, col2 = st.columns(2)

    with col1:

        run_button = st.button(
            "🚀 Solve with AI Agents",
            use_container_width=True,
            type="primary",
        )

    with col2:

        clear_button = st.button(
            "🗑 Clear",
            use_container_width=True,
        )

    if clear_button:

        st.session_state.pop(
            "agent_question",
            None,
        )

        st.rerun()

    if not run_button:
        return

    if not question.strip():

        st.warning(
            "Please enter a mathematical problem first."
        )

        return

    # ==================================================
    # RUN AGENT GRAPH
    # ==================================================

    try:

        with st.spinner(
            "🤖 Planner → Solver → Reviewer → Teacher..."
        ):

            agent_graph = MathMindAgentGraph(
                provider=provider
            )

            result = agent_graph.run(
                question
            )

        # ==================================================
        # RESULT STATUS
        # ==================================================

        status = result.get(
            "status",
            "UNKNOWN",
        )

        if status == "SUCCESS":

            st.success(
                "✅ Agent workflow completed successfully."
            )

        elif status == "API_ERROR":

            st.warning(
                "⚠️ Agent workflow reached an LLM/API "
                "configuration issue. The non-LLM stages "
                "completed where possible."
            )

        else:

            st.warning(
                f"⚠️ Agent workflow status: {status}"
            )

        st.divider()

        # ==================================================
        # PLANNER
        # ==================================================

        planner_result = result.get(
            "plan",
            "",
        )

        if planner_result:

            with st.expander(
                "🧠 Planner — Problem Analysis",
                expanded=True,
            ):

                if isinstance(
                    planner_result,
                    dict,
                ):

                    st.json(
                        planner_result
                    )

                else:

                    st.markdown(
                        str(planner_result)
                    )

        # ==================================================
        # SOLVER
        # ==================================================

        solver_result = result.get(
            "solver",
            result.get(
                "solution",
                "",
            ),
        )

        if solver_result:

            with st.expander(
                "🧮 Solver — Solution",
                expanded=True,
            ):

                if isinstance(
                    solver_result,
                    dict,
                ):

                    st.json(
                        solver_result
                    )

                else:

                    st.markdown(
                        str(solver_result)
                    )

        # ==================================================
        # REVIEWER
        # ==================================================

        reviewer_result = result.get(
            "review",
            "",
        )

        if reviewer_result:

            with st.expander(
                "🔍 Reviewer — Verification",
                expanded=True,
            ):

                if isinstance(
                    reviewer_result,
                    dict,
                ):

                    st.json(
                        reviewer_result
                    )

                else:

                    st.markdown(
                        str(reviewer_result)
                    )

        # ==================================================
        # TEACHER
        # ==================================================

        teacher_result = result.get(
            "teacher",
            result.get(
                "explanation",
                "",
            ),
        )

        if teacher_result:

            st.markdown(
                "## 👨‍🏫 Teacher Explanation"
            )

            if isinstance(
                teacher_result,
                dict,
            ):

                explanation = (
                    teacher_result.get(
                        "explanation",
                        "",
                    )
                )

                if explanation:

                    st.info(
                        str(explanation)
                    )

                else:

                    st.json(
                        teacher_result
                    )

            else:

                st.info(
                    str(teacher_result)
                )

        # ==================================================
        # API ERROR INFORMATION
        # ==================================================

        if status == "API_ERROR":

            solver_data = result.get(
                "solver",
                {},
            )

            if isinstance(
                solver_data,
                dict,
            ):

                error_message = (
                    solver_data.get(
                        "error",
                        solver_data.get(
                            "message",
                            "",
                        ),
                    )
                )

                if error_message:

                    with st.expander(
                        "⚠️ API / Provider Details"
                    ):

                        st.code(
                            str(error_message)
                        )

        # ==================================================
        # RAW OUTPUT
        # ==================================================

        with st.expander(
            "🔧 Raw Agent Output"
        ):

            st.json(
                result
                if isinstance(
                    result,
                    dict,
                )
                else {
                    "result": str(result)
                }
            )

    except Exception as error:

        st.error(
            "❌ Agent execution failed."
        )

        st.exception(error)