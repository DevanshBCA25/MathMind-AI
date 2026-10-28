import numpy as np
import plotly.graph_objects as go
import streamlit as st
from sympy import diff, latex

from src.ui.common import page_header
from src.calculator.graph import evaluate
from src.calculator.symbolic import main_variable, parse_math


def build_figure(expressions, x_min, x_max, show_derivative):

    x_values = np.linspace(x_min, x_max, 800)

    fig = go.Figure()

    for text in expressions:

        fig.add_trace(go.Scatter(
            x=x_values,
            y=evaluate(text, x_values),
            mode="lines",
            name=f"y = {text}",
            connectgaps=False,
        ))

        if show_derivative:

            expr = parse_math(text)
            slope = str(diff(expr, main_variable(expr)))

            fig.add_trace(go.Scatter(
                x=x_values,
                y=evaluate(slope, x_values),
                mode="lines",
                name=f"y' = {slope}",
                line={"dash": "dash"},
            ))

    fig.update_layout(
        height=520,
        margin={"l": 10, "r": 10, "t": 30, "b": 10},
        legend={"orientation": "h", "y": -0.15},
        hovermode="x unified",
        xaxis={"zeroline": True, "zerolinewidth": 2, "title": "x"},
        yaxis={"zeroline": True, "zerolinewidth": 2, "title": "y"},
    )

    return fig


def show():

    page_header(
        "📈",
        "Graph Plotter",
        "Plot functions of x. Use ^ for powers, e.g. x^2 - 3x",
    )

    text = st.text_area(
        "Functions (one per line)",
        "x^2/4 - 3\n3sin(x)\n1/x",
        height=110,
    )

    col1, col2 = st.columns([3, 1])

    with col1:

        x_min, x_max = st.slider(
            "x range",
            min_value=-50.0,
            max_value=50.0,
            value=(-10.0, 10.0),
            step=0.5,
        )

    with col2:

        show_derivative = st.toggle("Show derivative")

    expressions = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not expressions:
        st.info("Enter at least one function.")
        return

    if x_min >= x_max:
        st.warning("Choose a range where the start is less than the end.")
        return

    try:

        st.latex(
            r",\quad ".join(
                f"y = {latex(parse_math(e))}" for e in expressions
            )
        )

        st.plotly_chart(
            build_figure(expressions, x_min, x_max, show_derivative),
            width="stretch",
        )

    except Exception as error:

        st.error(f"Could not plot: {error}")
