"""
Shared UI helpers: page header, global styling and the
sidebar LLM provider selector used by every AI page.
"""

from pathlib import Path

import streamlit as st

from src.config.settings import DEFAULT_PROVIDER, has_api_key


STYLE_FILE = (
    Path(__file__).resolve().parents[2]
    / "assets"
    / "style.css"
)

PROVIDERS = [
    "Gemini",
    "Groq",
    "OpenAI",
    "Ollama",
]

PROVIDER_KEY = "llm_provider"


def apply_style():

    if STYLE_FILE.exists():

        st.markdown(
            f"<style>{STYLE_FILE.read_text()}</style>",
            unsafe_allow_html=True,
        )


def page_header(icon, title, subtitle=""):

    st.markdown(
        f"""
        <div class="mm-page-header">
            <span class="mm-page-icon">{icon}</span>
            <div>
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _provider_label(provider):

    if provider == "Ollama":
        return "Ollama (local only)"

    if has_api_key(provider):
        return f"{provider} ✓"

    return f"{provider} (no API key)"


def provider_selector():
    """
    Sidebar selector shared by all AI pages.
    Providers with an API key are listed first.
    """

    ordered = sorted(
        PROVIDERS,
        key=lambda p: (
            p == "Ollama",
            not has_api_key(p),
            p != DEFAULT_PROVIDER,
        ),
    )

    if st.session_state.get(PROVIDER_KEY) not in ordered:
        st.session_state[PROVIDER_KEY] = ordered[0]

    st.sidebar.selectbox(
        "🤖 AI model provider",
        ordered,
        key=PROVIDER_KEY,
        format_func=_provider_label,
    )


def current_provider():

    return st.session_state.get(
        PROVIDER_KEY,
        DEFAULT_PROVIDER,
    )
