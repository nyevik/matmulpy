"""Matrix operations used by the PySide6 teaching GUI."""

from random import randint


def make_matrix(rows, cols, fill=0):
    """Create a matrix with given number of rows and columns."""
    return [[fill for _ in range(cols)] for _ in range(rows)]


def resize_matrix(matrix, rows, cols, fill=0):
    """Resize a matrix while preserving existing values where possible."""
    result = make_matrix(rows, cols, fill)
    for i in range(min(rows, len(matrix))):
        for j in range(min(cols, len(matrix[i]))):
            result[i][j] = matrix[i][j]
    return result


def random_matrix(rows, cols, low=-5, high=5):
    """Create a matrix with given number of rows and columns filled with random integers."""
    return [[randint(low, high) for _ in range(cols)] for _ in range(rows)]


def identity_like(rows, cols):
    """Create an identity-style matrix for rectangular shapes."""
    return [[1 if i == j else 0 for j in range(cols)] for i in range(rows)]


def multiply(a, b):
    """Return the matrix product a * b."""
    if not a or not b:
        return []

    shared = len(a[0])
    if shared != len(b):
        raise ValueError("Matrix dimensions do not align for multiplication")

    rows = len(a)
    cols = len(b[0])
    return [
        [sum(a[i][k] * b[k][j] for k in range(shared)) for j in range(cols)]
        for i in range(rows)
    ]


def dot_terms(a, b, row, col):
    """Return the terms used to compute one output cell."""
    return [(k, a[row][k], b[k][col], a[row][k] * b[k][col]) for k in range(len(b))]
