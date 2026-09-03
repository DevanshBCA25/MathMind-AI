import streamlit as st

from src.calculator.linear_algebra import *


def show():

    st.header("🧮 Advanced Linear Algebra")

    matrix = st.text_area(
        "Enter Matrix (space separated)",
        "1 2\n3 4",
        height=150,
    )

    operation = st.selectbox(
        "Choose Operation",
        [
            "Rank",
            "Trace",
            "Determinant",
            "Inverse",
            "Norm",
            "Condition Number",
            "LU Decomposition",
            "QR Decomposition",
            "SVD",
            "Eigen Values",
            "Eigen Vectors",
            "Symmetric Check",
            "Orthogonal Check",
            "Positive Definite Check",
        ],
    )

    if st.button("Compute"):

        try:

            if operation == "Rank":
                st.success(matrix_rank(matrix))

            elif operation == "Trace":
                st.success(matrix_trace(matrix))

            elif operation == "Determinant":
                st.success(matrix_determinant(matrix))

            elif operation == "Inverse":
                st.write(matrix_inverse(matrix))

            elif operation == "Norm":
                st.success(matrix_norm(matrix))

            elif operation == "Condition Number":
                st.success(matrix_condition(matrix))

            elif operation == "LU Decomposition":

                P, L, U = lu_decomposition(matrix)

                st.subheader("P Matrix")
                st.write(P)

                st.subheader("L Matrix")
                st.write(L)

                st.subheader("U Matrix")
                st.write(U)

            elif operation == "QR Decomposition":

                Q, R = qr_decomposition(matrix)

                st.subheader("Q Matrix")
                st.write(Q)

                st.subheader("R Matrix")
                st.write(R)

            elif operation == "SVD":

                U, S, VT = svd_decomposition(matrix)

                st.subheader("U Matrix")
                st.write(U)

                st.subheader("Singular Values")
                st.write(S)

                st.subheader("Vᵀ Matrix")
                st.write(VT)

            elif operation == "Eigen Values":
                st.write(eigen_values(matrix))

            elif operation == "Eigen Vectors":
                st.write(eigen_vectors(matrix))

            elif operation == "Symmetric Check":
                st.success(symmetric(matrix))

            elif operation == "Orthogonal Check":
                st.success(orthogonal(matrix))

            elif operation == "Positive Definite Check":
                st.success(positive_definite(matrix))

        except Exception as e:
            st.error(e)