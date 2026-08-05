import numpy as np


def create_matrix(matrix_text):
    rows = matrix_text.strip().split("\n")
    matrix = [list(map(float, row.split())) for row in rows]
    return np.array(matrix)


def matrix_add(a, b):
    return np.add(a, b)


def matrix_subtract(a, b):
    return np.subtract(a, b)


def matrix_multiply(a, b):
    return np.matmul(a, b)


def matrix_transpose(a):
    return np.transpose(a)


def matrix_determinant(a):
    return np.linalg.det(a)


def matrix_inverse(a):
    return np.linalg.inv(a)


def matrix_rank(a):
    return np.linalg.matrix_rank(a)


def matrix_eigen(a):
    values, vectors = np.linalg.eig(a)
    return values, vectors


def scalar_multiply(a, scalar):
    return scalar * a


def identity_matrix(size):
    return np.identity(size)


def zero_matrix(rows, cols):
    return np.zeros((rows, cols))