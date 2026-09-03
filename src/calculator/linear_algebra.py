import numpy as np
from scipy.linalg import lu, qr, svd


def to_matrix(text):

    rows = text.strip().split("\n")

    matrix = []

    for row in rows:
        matrix.append([float(x) for x in row.split()])

    return np.array(matrix)


def matrix_rank(text):

    matrix = to_matrix(text)

    return np.linalg.matrix_rank(matrix)


def matrix_trace(text):

    matrix = to_matrix(text)

    return np.trace(matrix)


def matrix_determinant(text):

    matrix = to_matrix(text)

    return np.linalg.det(matrix)


def matrix_inverse(text):

    matrix = to_matrix(text)

    return np.linalg.inv(matrix)


def matrix_norm(text):

    matrix = to_matrix(text)

    return np.linalg.norm(matrix)


def matrix_condition(text):

    matrix = to_matrix(text)

    return np.linalg.cond(matrix)


def lu_decomposition(text):

    matrix = to_matrix(text)

    P, L, U = lu(matrix)

    return P, L, U


def qr_decomposition(text):

    matrix = to_matrix(text)

    Q, R = qr(matrix)

    return Q, R


def svd_decomposition(text):

    matrix = to_matrix(text)

    U, S, VT = svd(matrix)

    return U, S, VT


def eigen_values(text):

    matrix = to_matrix(text)

    values, vectors = np.linalg.eig(matrix)

    return values


def eigen_vectors(text):

    matrix = to_matrix(text)

    values, vectors = np.linalg.eig(matrix)

    return vectors


def symmetric(text):

    matrix = to_matrix(text)

    return np.allclose(matrix, matrix.T)


def orthogonal(text):

    matrix = to_matrix(text)

    identity = np.eye(matrix.shape[0])

    return np.allclose(matrix.T @ matrix, identity)


def positive_definite(text):

    matrix = to_matrix(text)

    try:
        np.linalg.cholesky(matrix)
        return True
    except:
        return False