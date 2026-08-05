import streamlit as st
from src.calculator.basic import add, subtract, multiply, divide


def show():

    st.header("Basic Calculator")

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

    if st.button("Calculate", key="basic_button"):

        if operation == "Addition":
            result = add(num1, num2)

        elif operation == "Subtraction":
            result = subtract(num1, num2)

        elif operation == "Multiplication":
            result = multiply(num1, num2)

        else:
            result = divide(num1, num2)

        st.success(f"Result : {result}")