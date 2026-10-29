import streamlit as st

from src.ui.common import page_header
from src.utils.helpers import save_operation
from src.calculator.practice import LEVELS, TOPICS, check, generate


def _new_question(topic, level):

    st.session_state.practice_question = generate(topic, level)
    st.session_state.practice_feedback = None
    st.session_state.practice_answer = ""
    st.session_state.practice_hint = False


def show():

    page_header(
        "🎯",
        "Practice Mode",
        "Unlimited questions, checked instantly. No AI key needed.",
    )

    if "practice_score" not in st.session_state:
        st.session_state.practice_score = {"correct": 0, "attempted": 0}

    col1, col2 = st.columns(2)

    with col1:
        topic = st.selectbox("Topic", TOPICS, key="practice_topic")

    with col2:
        level = st.radio("Level", LEVELS, horizontal=True, key="practice_level")

    question = st.session_state.get("practice_question")

    if (
        question is None
        or question["topic"] != topic
        or st.session_state.get("practice_for") != (topic, level)
    ):
        _new_question(topic, level)
        st.session_state.practice_for = (topic, level)
        question = st.session_state.practice_question

    score = st.session_state.practice_score

    # Filled at the end, after this run's answer is counted.
    scoreboard = st.container()

    with st.container(border=True):

        st.markdown(f"**{question['prompt']}**")

        st.latex(question["latex"])

        with st.form("practice_form", clear_on_submit=False):

            answer = st.text_input(
                "Your answer",
                key="practice_answer",
                placeholder="e.g. 3x^2 + 2   or   x = 2, -3",
            )

            submitted = st.form_submit_button("Check answer", type="primary")

    if submitted:

        try:

            correct = check(question, answer)

            score["attempted"] += 1
            score["correct"] += int(correct)

            st.session_state.practice_feedback = correct

            save_operation(
                module="Practice",
                operation=topic,
                input_data=question["latex"],
                result="Correct" if correct else "Wrong",
            )

        except Exception as error:

            st.warning(f"Could not read your answer: {error}")

    feedback = st.session_state.get("practice_feedback")

    if feedback is True:
        st.success("✅ Correct! Well done.")

    elif feedback is False:
        st.error("❌ Not quite. The correct answer is:")
        st.latex(question["answer_latex"])

    col1, col2 = st.columns(2)

    with col1:

        if st.button("💡 Hint", width="stretch"):
            st.session_state.practice_hint = True

    with col2:

        st.button(
            "➡ Next question",
            width="stretch",
            on_click=_new_question,
            args=(topic, level),
        )

    if st.session_state.get("practice_hint"):
        st.info(question["hint"])

    c1, c2, c3 = scoreboard.columns(3)
    c1.metric("Correct", score["correct"])
    c2.metric("Attempted", score["attempted"])
    c3.metric(
        "Accuracy",
        f"{100 * score['correct'] // score['attempted']}%"
        if score["attempted"] else "–",
    )
