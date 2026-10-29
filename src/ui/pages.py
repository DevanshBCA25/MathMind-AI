"""
Page registry for the app's navigation.

Every page imports its module only when opened, so heavy
libraries (torch, EasyOCR, FAISS) load only on the pages
that need them.
"""

import importlib

import streamlit as st


def _lazy(module_name):

    def render():
        importlib.import_module(
            f"src.ui.{module_name}"
        ).show()

    render.__name__ = module_name

    return render


def _page(module_name, title, icon, url_path, default=False):

    return st.Page(
        _lazy(module_name),
        title=title,
        icon=icon,
        url_path=url_path,
        default=default,
    )


HOME = _page("home_ui", "Home", "🏠", None, default=True)

ASK = _page("unified_solver_ui", "Ask MathMind", "🧠", "ask")
CHAT = _page("ai_chat_ui", "AI Tutor Chat", "💬", "chat")
DOCS = _page("rag_ui", "Document Q&A", "📚", "documents")
PRACTICE = _page("practice_ui", "Practice Mode", "🎯", "practice")

BASIC = _page("basic_ui", "Basic Calculator", "➕", "basic")
SCIENTIFIC = _page("scientific_ui", "Scientific Calculator", "🔬", "scientific")
SYMBOLIC = _page("symbolic_ui", "Algebra & Calculus", ":material/functions:", "symbolic")
GRAPH = _page("graph_ui", "Graph Plotter", "📈", "graph")
MATRIX = _page("matrix_ui", "Matrices", "🔢", "matrix")
LINEAR = _page("linear_algebra_ui", "Linear Algebra", "🧮", "linear-algebra")
STATS = _page("statistics_ui", "Statistics", "📊", "statistics")

OCR = _page("ocr_ui", "Scan & Solve (OCR)", "📷", "ocr")
VISION = _page("vision_ui", "Image Lab", "🖼️", "vision")

HISTORY = _page("history_ui", "My History", "📜", "history")
ANALYTICS = _page("analytics_ui", "Analytics", "📉", "analytics")
HEALTH = _page("provider_health_ui", "AI Provider Status", "🩺", "status")


NAVIGATION = {
    "": [HOME],
    "AI Solver": [ASK, CHAT, DOCS],
    "Learn": [PRACTICE],
    "Calculators": [BASIC, SCIENTIFIC, SYMBOLIC, GRAPH, MATRIX, LINEAR, STATS],
    "Vision": [OCR, VISION],
    "Insights": [HISTORY, ANALYTICS, HEALTH],
}
