import streamlit as st

from src.calculator.scientific import (
    power,
    square_root,
    sine,
    cosine,
    tangent,
)


def show():

    st.header("Scientific Calculator")

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

    if st.button("Calculate", key="sci_button"):

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