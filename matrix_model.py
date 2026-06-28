""" Matrix model for handling matrix operations 
    author: Nikolay Yevik
"""

from random import randint

def make_matrix (rows, cols, fill =0):
    """Create a matrix with given number of rows and columns."""
    return [[fill for _ in range(cols)] for _ in range(rows)]

def resize_matrix(matrix, rows , cols, fill = 0):
   result = make_matrix(rows, cols, fill)
   for i in range(min(rows, len(matrix))):
       for j in range(min(cols, len(matrix[0]))):
           result[i][j] = matrix[i][j]
   return result

def random_matrix(rows, cols, low = -10, high = 10):
    """Create a matrix with given number of rows and columns filled with random integers."""
    return [[randint(low, high) for _ in range(cols)] for _ in range(rows)]

def  identity_like(rows, cols):
    """Create an identity matrix with given number of rows and columns."""
    return [[1 if i == j else 0 for j in range(cols)] for i in range(rows)]

def multiply(a,b) :
    rows = len(a)
    shared = len(b)
    cols = len(b[0]) if b else 0
    return [
        [sum(a[i][k] * b[k][j] for k in range(shared)) for j in range(cols)]
        for i in range(rows)
    ]

def dot_terms(a, b, row, col):
    return [(k, a[row][k], b[k][col], a[row][k] * b[k][col]) for k in range(len(b))]

