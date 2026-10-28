import streamlit as st

from src.ui.common import current_provider, page_header

from src.llm.router import LLMRouter
from src.llm.prompts import SYSTEM_PROMPT
from src.llm.chat_history import (
    initialize_chat,
    add_message,
    clear_chat,
    get_messages,
)

from src.llm.formatter import format_response

from src.utils.helpers import (
    save_operation,
    log_error,
)


# How many earlier messages are sent to the model as context.
CONTEXT_MESSAGES = 10

EXAMPLES = [
    "Explain the quadratic formula with an example",
    "What is the derivative of sin(x)·x²? Show steps",
    "Why is 0.999... equal to 1?",
]


@st.cache_resource
def get_router():

    return LLMRouter()


def build_prompt(messages):
    """
    Turn the conversation into one prompt so every provider
    sees the system prompt and the recent history.
    """

    lines = [SYSTEM_PROMPT.strip(), "", "Conversation so far:"]

    for message in messages[-CONTEXT_MESSAGES:]:

        speaker = (
            "Student"
            if message["role"] == "user"
            else "MathMind"
        )

        lines.append(f"{speaker}: {message['content']}")

    lines.append("")
    lines.append(
        "Reply to the student's last message as MathMind."
    )

    return "\n".join(lines)


def show():

    page_header(
        "💬",
        "AI Tutor Chat",
        "Ask anything, get step-by-step explanations",
    )

    initialize_chat()

    provider = current_provider()

    st.caption(
        f"Answering with **{provider}**. "
        "Change the model in the sidebar."
    )

    if not get_messages():

        st.markdown("**Try one of these:**")

        columns = st.columns(len(EXAMPLES))

        for column, example in zip(columns, EXAMPLES):

            if column.button(example, width="stretch"):

                st.session_state.chat_example = example

                st.rerun()

    for message in get_messages():

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    prompt = st.chat_input(
        "Ask a maths question..."
    ) or st.session_state.pop("chat_example", None)

    if prompt:

        add_message("user", prompt)

        with st.chat_message("user"):

            st.markdown(prompt)

        try:

            with st.chat_message("assistant"):

                with st.spinner("Thinking..."):

                    response = get_router().ask(
                        provider,
                        build_prompt(get_messages()),
                    )

                response = format_response(response)

                st.markdown(response)

            add_message(
                "assistant",
                response,
            )

            save_operation(
                module="AI Chat",
                operation=provider,
                input_data=prompt,
                result="Success",
            )

        except Exception as e:

            # Drop the unanswered question so it is not resent as context.
            get_messages().pop()

            log_error(str(e))

            st.error(e)

    if not get_messages():
        return

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button("🗑 Clear Chat", width="stretch"):

            clear_chat()

            st.rerun()

    with col2:

        chat = ""

        for item in get_messages():

            chat += (
                f"{item['role']}:\n"
                f"{item['content']}\n\n"
            )

        st.download_button(
            "⬇ Export Chat",
            data=chat,
            file_name="chat_history.txt",
            mime="text/plain",
            width="stretch",
        )
