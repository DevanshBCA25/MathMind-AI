import streamlit as st

from src.ui.common import page_header
from src.utils.helpers import save_operation
from src.calculator.basic import add, subtract, multiply, divide


def show():

    page_header(
        "➕",
        "Basic Calculator",
        "Add, subtract, multiply and divide",
    )

    num1 = st.number_input("Enter First Number", value=0.0, key="basic_num1")
    num2 = st.number_input("Enter Second Number", value=0.0, key="basic_num2")

    operation = st.selectbox(
        "Choose Operation",
        [
            "Addition",
            "Subtraction",
            "Multiplication",
            "Division",
        ],
        key="basic_operation",
    )

    if st.button("Calculate", key="basic_button", type="primary"):

        try:

            if operation == "Addition":
                result = add(num1, num2)

            elif operation == "Subtraction":
                result = subtract(num1, num2)

            elif operation == "Multiplication":
                result = multiply(num1, num2)

            else:
                result = divide(num1, num2)

            st.success(f"Result : {result}")

            save_operation(
                module="Basic Calculator",
                operation=operation,
                input_data=f"{num1}, {num2}",
                result=result,
            )

        except Exception as error:

            st.error(f"Error: {error}")
