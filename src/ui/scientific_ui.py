import streamlit as st

from src.ui.common import page_header
from src.utils.helpers import save_operation

from src.calculator.scientific import (
    power,
    square_root,
    sine,
    cosine,
    tangent,
)


def show():

    page_header(
        "🔬",
        "Scientific Calculator",
        "Powers, roots and trigonometry (degrees)",
    )

    num1 = st.number_input("Enter First Number", value=0.0, key="sci_num1")
    num2 = st.number_input("Enter Second Number", value=0.0, key="sci_num2")

    operation = st.selectbox(
        "Choose Operation",
        [
            "Power",
            "Square Root",
            "Sin",
            "Cos",
            "Tan",
        ],
        key="sci_operation",
    )

    if st.button("Calculate", key="sci_button", type="primary"):

        try:

            if operation == "Power":
                result = power(num1, num2)

            elif operation == "Square Root":
                result = square_root(num1)

            elif operation == "Sin":
                result = sine(num1)

            elif operation == "Cos":
                result = cosine(num1)

            else:
                result = tangent(num1)

            st.success(f"Result : {result}")

            save_operation(
                module="Scientific Calculator",
                operation=operation,
                input_data=f"{num1}, {num2}",
                result=result,
            )

        except Exception as error:

            st.error(f"Error: {error}")
