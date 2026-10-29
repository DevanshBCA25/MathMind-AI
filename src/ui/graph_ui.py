import streamlit as st

from src.ui.common import page_header

from src.calculator.graph import (
    plot_function,
    plot_multiple,
)


def show():

    page_header(
        "📈",
        "Graph Plotter",
        "Plot functions of x. Use ^ for powers, e.g. x^2 - 3x",
    )

    option = st.selectbox(
        "Graph Type",
        [
            "Single Function",
            "Multiple Functions",
        ],
    )

    if option == "Single Function":

        expression = st.text_input(
            "Function",
            "x**2",
        )

        if st.button("Plot", type="primary"):

            try:

                fig = plot_function(expression)

                st.pyplot(fig)

            except Exception as error:

                st.error(f"Could not plot: {error}")

    else:

        expression = st.text_area(
            "Functions",
            "x\nx**2\nsin(x)",
        )

        if st.button("Plot", type="primary"):

            expressions = expression.split("\n")

            try:

                fig = plot_multiple(expressions)

                st.pyplot(fig)

            except Exception as error:

                st.error(f"Could not plot: {error}")