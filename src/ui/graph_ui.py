import streamlit as st

from src.calculator.graph import (
    plot_function,
    plot_multiple,
)


def show():

    st.header("📈 Graph Visualization")

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

        if st.button("Plot"):

            fig = plot_function(expression)

            st.pyplot(fig)

    else:

        expression = st.text_area(
            "Functions",
            "x\nx**2\nsin(x)",
        )

        if st.button("Plot"):

            expressions = expression.split("\n")

            fig = plot_multiple(expressions)

            st.pyplot(fig)