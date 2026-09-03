import streamlit as st

from src.agents.agent_graph import MathMindAgentGraph


def initialize_agent():
    """
    Create the Agent Graph once and keep it
    inside Streamlit session state.
    """

    if "mathmind_agent_graph" not in st.session_state:

        st.session_state.mathmind_agent_graph = (
            MathMindAgentGraph()
        )

    return st.session_state.mathmind_agent_graph


def initialize_agent_history():

    if "agentic_math_history" not in st.session_state:

        st.session_state.agentic_math_history = []


def display_agent_result(result):
    """
    Display the result returned by the Agent Graph.
    """

    if not result:
        st.warning("No result returned by Agent Graph.")
        return

    st.markdown("## 🤖 Agentic Solution")

    # --------------------------------------------------
    # FINAL ANSWER
    # --------------------------------------------------

    final_answer = (
        result.get("final_answer")
        or result.get("answer")
        or result.get("response")
        or ""
    )

    if final_answer:

        st.success("### ✅ Final Answer")

        st.markdown(final_answer)

    # --------------------------------------------------
    # PLANNER
    # --------------------------------------------------

    planner_result = result.get("planner")

    if planner_result:

        with st.expander(
            "🧠 Planner — Problem Analysis",
            expanded=False,
        ):

            if isinstance(
                planner_result,
                dict,
            ):

                st.json(
                    planner_result
                )

            else:

                st.write(
                    planner_result
                )

    # --------------------------------------------------
    # SOLVER
    # --------------------------------------------------

    solver_result = result.get("solver")

    if solver_result:

        with st.expander(
            "🧮 Solver — Mathematical Solution",
            expanded=False,
        ):

            if isinstance(
                solver_result,
                dict,
            ):

                st.json(
                    solver_result
                )

            else:

                st.write(
                    solver_result
                )

    # --------------------------------------------------
    # REVIEWER
    # --------------------------------------------------

    reviewer_result = result.get("reviewer")

    if reviewer_result:

        with st.expander(
            "🔍 Reviewer — Solution Verification",
            expanded=False,
        ):

            if isinstance(
                reviewer_result,
                dict,
            ):

                st.json(
                    reviewer_result
                )

            else:

                st.write(
                    reviewer_result
                )

    # --------------------------------------------------
    # TEACHER
    # --------------------------------------------------

    teacher_result = result.get("teacher")

    if teacher_result:

        with st.expander(
            "👨‍🏫 Teacher — Explanation",
            expanded=False,
        ):

            if isinstance(
                teacher_result,
                dict,
            ):

                st.json(
                    teacher_result
                )

            else:

                st.write(
                    teacher_result
                )

    # --------------------------------------------------
    # RAW AGENT STATE
    # --------------------------------------------------

    with st.expander(
        "🔧 Raw Agent Graph Result",
        expanded=False,
    ):

        st.json(result)


def show():

    initialize_agent_history()

    st.title(
        "🤖 Agentic Math Solver"
    )

    st.caption(
        "Planner → Solver → Reviewer → Teacher"
    )

    st.markdown(
        """
        Enter a mathematical problem and let the
        MathMind-AI agent system analyze, solve,
        review and explain it.
        """
    )

    # --------------------------------------------------
    # INITIALIZE AGENT
    # --------------------------------------------------

    try:

        agent_graph = initialize_agent()

    except Exception as error:

        st.error(
            "❌ Agent Graph initialization failed."
        )

        st.exception(error)

        return

    # --------------------------------------------------
    # EXAMPLE QUESTIONS
    # --------------------------------------------------

    st.markdown(
        "### 💡 Example Problems"
    )

    examples = [
        "Solve 2x + 5 = 15",
        "Find the area of a rectangle with length 12 cm and width 5 cm.",
        "Find the derivative of x^2 + 3x + 2.",
        "Find the discriminant of 2x² + 5x + 3.",
    ]

    selected_example = st.selectbox(
        "Choose an example",
        [
            "Custom Question"
        ] + examples,
        key="agent_example",
    )

    if selected_example != "Custom Question":

        question = selected_example

    else:

        question = st.text_area(
            "Enter your mathematical question",
            height=120,
            placeholder=(
                "Example: Solve x² + 5x + 6 = 0"
            ),
            key="agent_question",
        )

    # --------------------------------------------------
    # SOLVE BUTTON
    # --------------------------------------------------

    if st.button(
        "🚀 Solve with AI Agents",
        type="primary",
        use_container_width=True,
    ):

        if not question or not question.strip():

            st.warning(
                "Please enter a mathematical question."
            )

            return

        question = question.strip()

        # Save user question
        st.session_state.agentic_math_history.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.spinner(
            "🤖 Agents are working..."
        ):

            try:

                # --------------------------------------------------
                # CALL AGENT GRAPH
                # --------------------------------------------------

                result = agent_graph.run(
                    question
                )

                # --------------------------------------------------
                # SAVE RESULT
                # --------------------------------------------------

                st.session_state.agentic_math_history.append(
                    {
                        "role": "assistant",
                        "content": result,
                    }
                )

                # --------------------------------------------------
                # DISPLAY
                # --------------------------------------------------

                display_agent_result(
                    result
                )

            except Exception as error:

                error_text = str(error)

                # API problems are intentionally not
                # handled specially here. They can be
                # fixed later.

                st.error(
                    "❌ Agent execution failed."
                )

                st.exception(error)

                if (
                    "api"
                    in error_text.lower()
                    or "key"
                    in error_text.lower()
                    or "quota"
                    in error_text.lower()
                    or "authentication"
                    in error_text.lower()
                ):

                    st.info(
                        "ℹ️ This appears to be a "
                        "provider/API configuration issue. "
                        "The Agentic UI itself is configured."
                    )

    # --------------------------------------------------
    # HISTORY
    # --------------------------------------------------

    st.divider()

    st.markdown(
        "### 🕘 Agent History"
    )

    history = (
        st.session_state.agentic_math_history
    )

    if not history:

        st.info(
            "No agent questions yet."
        )

    else:

        for index, item in enumerate(
            history,
            start=1,
        ):

            role = item.get(
                "role",
                "unknown",
            )

            content = item.get(
                "content",
                "",
            )

            with st.expander(
                f"{index}. {role.upper()}"
            ):

                if isinstance(
                    content,
                    dict,
                ):

                    st.json(content)

                else:

                    st.write(content)

    # --------------------------------------------------
    # CLEAR HISTORY
    # --------------------------------------------------

    if st.button(
        "🗑️ Clear Agent History",
        use_container_width=True,
    ):

        st.session_state.agentic_math_history = []

        st.rerun()