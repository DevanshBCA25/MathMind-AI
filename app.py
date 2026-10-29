import streamlit as st

import src.config.settings  # noqa: F401  (loads .env and Streamlit secrets)

from src.ui.common import apply_style, provider_selector
from src.ui.pages import NAVIGATION


st.set_page_config(
    page_title="MathMind AI",
    page_icon="🧠",
    layout="wide",
)

apply_style()

page = st.navigation(NAVIGATION, expanded=True)

with st.sidebar:

    st.markdown("### 🧠 MathMind AI")

    st.caption("AI-powered maths reasoning platform")

provider_selector()

page.run()
