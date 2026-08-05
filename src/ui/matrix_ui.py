import streamlit as st

from src.calculator.matrix import *

def show():

    st.header("Matrix Mathematics")

    operation = st.selectbox(
        "Operation",
        [
            "Addition",
            "Subtraction",
            "Multiplication",
            "Transpose",
            "Determinant",
            "Inverse",
            "Rank",
            "Eigen Values",
            "Scalar Multiplication",
            "Identity Matrix",
            "Zero Matrix",
        ],
    )

    if operation in [
        "Addition",
        "Subtraction",
        "Multiplication",
    ]:

        matrix1 = st.text_area(
            "Matrix A",
            "1 2\n3 4"
        )

        matrix2 = st.text_area(
            "Matrix B",
            "5 6\n7 8"
        )

    elif operation in [
        "Transpose",
        "Determinant",
        "Inverse",
        "Rank",
        "Eigen Values",
        "Scalar Multiplication",
    ]:

        matrix1 = st.text_area(
            "Matrix",
            "1 2\n3 4"
        )

    elif operation == "Identity Matrix":

        size = st.number_input(
            "Size",
            min_value=1,
            value=3,
        )

    elif operation == "Zero Matrix":

        rows = st.number_input(
            "Rows",
            min_value=1,
            value=3,
        )

        cols = st.number_input(
            "Columns",
            min_value=1,
            value=3,
        )

    if operation == "Scalar Multiplication":
        scalar = st.number_input(
            "Scalar",
            value=2.0,
        )

    if st.button("Calculate"):

        if operation == "Addition":

            result = matrix_add(
                create_matrix(matrix1),
                create_matrix(matrix2),
            )

        elif operation == "Subtraction":

            result = matrix_subtract(
                create_matrix(matrix1),
                create_matrix(matrix2),
            )

        elif operation == "Multiplication":

            result = matrix_multiply(
                create_matrix(matrix1),
                create_matrix(matrix2),
            )

        elif operation == "Transpose":

            result = matrix_transpose(
                create_matrix(matrix1)
            )

        elif operation == "Determinant":

            result = matrix_determinant(
                create_matrix(matrix1)
            )

        elif operation == "Inverse":

            result = matrix_inverse(
                create_matrix(matrix1)
            )

        elif operation == "Rank":

            result = matrix_rank(
                create_matrix(matrix1)
            )

        elif operation == "Eigen Values":

            values, vectors = matrix_eigen(
                create_matrix(matrix1)
            )

            st.write("Eigen Values")
            st.write(values)

            st.write("Eigen Vectors")
            st.write(vectors)

            return

        elif operation == "Scalar Multiplication":

            result = scalar_multiply(
                create_matrix(matrix1),
                scalar,
            )

        elif operation == "Identity Matrix":

            result = identity_matrix(size)

        else:

            result = zero_matrix(
                rows,
                cols,
            )

        st.write(result)