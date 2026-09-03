import streamlit as st

from src.llm.router import LLMRouter
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


router = LLMRouter()


def show():

    st.title("🤖 AI Chat")

    initialize_chat()

    provider = st.selectbox(
        "Select Model",
        [
            "OpenAI",
            "Gemini",
            "Groq",
            "Ollama",
        ],
    )

    for message in get_messages():

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    prompt = st.chat_input(
        "Ask anything..."
    )

    if prompt:

        add_message("user", prompt)

        with st.chat_message("user"):

            st.markdown(prompt)

        try:

            response = router.ask(
                provider,
                prompt,
            )

            response = format_response(response)

            add_message(
                "assistant",
                response,
            )

            with st.chat_message(
                "assistant"
            ):

                st.markdown(response)

            save_operation(
                module="AI Chat",
                operation=provider,
                input_data=prompt,
                result="Success",
            )

        except Exception as e:

            log_error(str(e))

            st.error(e)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button("🗑 Clear Chat"):

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
        )