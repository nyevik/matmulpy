"""matrix multiplication"""

import sys

from PySide6.QtCore import qVersion
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton,QWidget

# matrix A and matrix B multiplication"""

A = [[1, 2], [3, 4]]

B = [[5, 6], [7, 8]]

def matrix_print(matrix, name):
    print ("Matrix name:", name)
    for row in matrix:
        print(row)
    #print(matrix)

def mat_mul(A, B):
    result = [[0, 0], [0, 0]]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result


def my_mat_myl(A, B):
    C = [[0, 0], [0, 0]]
    C[0][0] = A[0][0] * B[0][0] + A[0][1] * B[1][0]
    print("C[0][0]=", C[0][0])
    C[0][1] = A[0][0] * B[0][1] + A[0][1] * B[1][1]
    print("C[0][1]=", C[0][1])
    C[1][0] = A[1][0] * B[0][0] + A[1][1] * B[1][0]
    print("C[1][0]=", C[1][0])
    C[1][1] = A[1][0] * B[0][1] + A[1][1] * B[1][1]
    print("C[1][1]=", C[1][1])
    return C


def main():
    print(sys.executable)
    print("Qt version:", qVersion())

    C = mat_mul(A, B)
    matrix_print(C, "C")

    C2 = my_mat_myl(A, B)
    matrix_print(C2, "C2")


if __name__ == "__main__":
    main()
