import streamlit as st

from src.calculator.symbolic import (
    simplify_expression,
    expand_expression,
    factor_expression,
    solve_equation,
    derivative,
    integration,
    calculate_limit,
)


def show():

    st.header("Symbolic Mathematics")

    operation = st.selectbox(
        "Choose Operation",
        [
            "Simplify",
            "Expand",
            "Factor",
            "Solve Equation",
            "Derivative",
            "Integration",
            "Limit",
        ],
        key="symbolic_operation",
    )

    expression = st.text_input(
        "Enter Expression",
        key="expression",
    )

    right_side = "0"

    if operation == "Solve Equation":
        right_side = st.text_input(
            "Right Side",
            value="0",
            key="right_side",
        )

    limit_value = 0

    if operation == "Limit":
        limit_value = st.number_input(
            "Limit Value",
            value=0,
            key="limit_value",
        )

    if st.button("Calculate", key="symbolic_button"):

        if operation == "Simplify":
            result = simplify_expression(expression)

        elif operation == "Expand":
            result = expand_expression(expression)

        elif operation == "Factor":
            result = factor_expression(expression)

        elif operation == "Solve Equation":
            result = solve_equation(expression, right_side)

        elif operation == "Derivative":
            result = derivative(expression)

        elif operation == "Integration":
            result = integration(expression)

        else:
            result = calculate_limit(expression, limit_value)

        st.success(f"Result : {result}")