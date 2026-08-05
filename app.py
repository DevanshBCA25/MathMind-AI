import streamlit as st

from src.ui.basic_ui import show as basic_ui
from src.ui.scientific_ui import show as scientific_ui
from src.ui.symbolic_ui import show as symbolic_ui
from src.ui.matrix_ui import show as matrix_ui
from src.ui.graph_ui import show as graph_ui

st.set_page_config(
    page_title="MathMind AI",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 MathMind AI")
st.markdown("### AI Powered Mathematics Platform")

st.sidebar.title("📚 Navigation")

module = st.sidebar.radio(
    "Choose Module",
    [
        "Basic Calculator",
        "Scientific Calculator",
        "Symbolic Mathematics",
        "Matrix Mathematics",
        "Graph Visualization",
    ],
)

if module == "Basic Calculator":
    basic_ui()

elif module == "Scientific Calculator":
    scientific_ui()

elif module == "Symbolic Mathematics":
    symbolic_ui()

elif module == "Matrix Mathematics":
    matrix_ui()

elif module == "Graph Visualization":
    graph_ui()