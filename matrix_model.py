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