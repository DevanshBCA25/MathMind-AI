import streamlit as st

from src.ui.basic_ui import show as basic_ui
from src.ui.scientific_ui import show as scientific_ui
from src.ui.symbolic_ui import show as symbolic_ui
from src.ui.matrix_ui import show as matrix_ui
from src.ui.graph_ui import show as graph_ui
from src.ui.statistics_ui import show as statistics_ui
from src.ui.linear_algebra_ui import show as linear_algebra_ui
from src.ui.history_ui import show as history_ui
from src.ui.vision_ui import show as vision_ui
from src.ui.ocr_ui import show as ocr_ui
from src.ui.ai_chat_ui import show as ai_chat_ui
from src.ui.rag_ui import show as rag_ui
from src.ui.agents_ui import show as agents_ui
from src.ui.agentic_math_ui import (
    show as agentic_math_ui,
)
from src.ui.unified_ai_ui import (
    show as unified_ai_ui,
)
from src.ui.rag_agent_ui import show as rag_agent_ui
from src.ui.unified_solver_ui import show as unified_solver_ui
from src.ui.provider_health_ui import (
    show as provider_health_ui
)
from src.ui.analytics_ui import (
    show as analytics_ui,
)


st.set_page_config(
    page_title="MathMind AI",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 MathMind AI")
st.caption("AI Powered Mathematical Reasoning Platform")

module = st.sidebar.radio(
    "Navigation",
    [
        "Basic Calculator",
        "Scientific Calculator",
        "Symbolic Mathematics",
        "Matrix Mathematics",
        "Graph Visualization",
        "Statistics & Data Analysis",
        "Advanced Linear Algebra",
        "History",
        "Computer Vision",
        "OCR",
        "AI Chat",
        "RAG Assistant",
        "AI Agents",
        "Agentic Math Solver",
        "Unified AI Solver",
        "RAG + Agent Assistant",
        "LLM Provider Health",
        "Analytics",
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

elif module == "Statistics & Data Analysis":
    statistics_ui()

elif module == "Advanced Linear Algebra":
    linear_algebra_ui()

elif module == "History":
    history_ui()

elif module == "Computer Vision":
    vision_ui()

elif module == "OCR":
    ocr_ui()

elif module == "AI Chat":
    ai_chat_ui()

elif module == "RAG Assistant":
    rag_ui()

elif module == "AI Agents":
    agents_ui()

elif module == "Agentic Math Solver":
    agentic_math_ui()

elif module == "Unified AI Solver":
    unified_ai_ui()

elif module == "RAG + Agent Assistant":
    rag_agent_ui()

elif module == "LLM Provider Health":
    provider_health_ui()

elif module == "Analytics":
    analytics_ui()
