"""matrix multiplication teaching tool using PySide6 GUI framework.
@author: Nikolay Yevik
"""

import sys


from PySide6.QtCore import Qt, QSize, qVersion
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

# matrix A and matrix B multiplication"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Learn Matrix Multiplication")

        button = QPushButton("Multiply Matrices")
        button.clicked.connect(self.multiply_matrices)
        button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        button.setMinimumSize(160, 36)
        button.setMaximumWidth(220)

        central = QWidget()

        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addStretch()

        button_row = QHBoxLayout()
        button_row.addWidget(button)
        button_row.addStretch()
        layout.addLayout(button_row)

        self.setCentralWidget(central)
        self.setMinimumSize(640, 420)
        self.resize(self.initial_window_size())
        self.center_on_screen()

    def initial_window_size(self):
        screen = QApplication.primaryScreen()
        available = screen.availableGeometry()

        width = min(1100, max(640, int(available.width() * 0.65)))
        height = min(800, max(420, int(available.height() * 0.65)))

        return QSize(width, height)

    def center_on_screen(self):
        screen = QApplication.primaryScreen()
        available = screen.availableGeometry()
        frame = self.frameGeometry()
        frame.moveCenter(available.center())
        self.move(frame.topLeft())

    def multiply_matrices(self):
        A = [[1, 2], [3, 4]]
        B = [[5, 6], [7, 8]]

        C = self.mat_mul(A, B)
        matrix_print(C, "C")

        C2 = self.my_mat_mul(A, B)
        matrix_print(C2, "C2")

    def mat_mul(self, A, B):
        result = [[0, 0], [0, 0]]
        matrix_print(result, "result before multiplication")
        for i in range(len(A)):
            for j in range(len(B[0])):
                for k in range(len(B)):
                    result[i][j] += A[i][k] * B[k][j]
        return result

    def my_mat_mul(self,  A, B):
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
# End Class


def matrix_print(matrix, name):
    print ("Matrix name:", name)
    for row in matrix:
        print(row)
    #print(matrix)


def my_mat_mul(A, B):
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
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
