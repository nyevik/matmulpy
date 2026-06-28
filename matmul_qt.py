"""Matrix multiplication teaching tool using PySide6."""

import sys

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from matrix_model import multiply, resize_matrix


INITIAL_A = [[1, 2], [3, 4]]
INITIAL_B = [[5, 6], [7, 8]]
DIMENSIONS = (1, 2, 3, 4)
THEORY_NOTES = {
    "Big picture": (
        "A matrix is a rectangular grid of numbers. Matrix multiplication combines "
        "each row of A with each column of B to make one number in C."
    ),
    "Size rule": (
        "A x B is allowed when the columns of A match the rows of B. If A is "
        "m x n and B is n x p, the result C is m x p."
    ),
    "Dot product": (
        "A dot product means multiply matching numbers, then add them. Example: "
        "[1, 2] dot [5, 7] = 1*5 + 2*7 = 19."
    ),
    "One result cell": (
        "Each cell C[row, col] comes from one row of A and one column of B. "
        "That row and column are paired up with a dot product."
    ),
    "Order matters": (
        "Usually A x B is not the same as B x A. Sometimes both work but give "
        "different answers; sometimes only one order is possible."
    ),
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.m = 2
        self.n = 2
        self.p = 2
        self.a = [row[:] for row in INITIAL_A]
        self.b = [row[:] for row in INITIAL_B]
        self.c = multiply(self.a, self.b)

        self.setWindowTitle("Learn Matrix Multiplication Interactively")

        self.m_combo = self._dimension_combo(self.m)
        self.n_combo = self._dimension_combo(self.n)
        self.p_combo = self._dimension_combo(self.p)
        self.concept_combo = QComboBox()
        self.concept_combo.addItems(list(THEORY_NOTES))
        self.concept_explanation = QLabel()
        self.concept_explanation.setWordWrap(True)
        self.concept_explanation.setMinimumHeight(54)
        self.concept_explanation.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.a_table = QTableWidget()
        self.b_table = QTableWidget()
        self.c_table = QTableWidget()

        self.a_group = self._matrix_group("Matrix A", self.a_table)
        self.b_group = self._matrix_group("Matrix B", self.b_table)
        self.c_group = self._matrix_group("Matrix C", self.c_table)
        self.status_label = QLabel()

        central = QWidget()
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(20, 20, 20, 20)
        root_layout.setSpacing(16)
        root_layout.addWidget(self._theory_panel())
        root_layout.addLayout(self._dimension_controls())
        root_layout.addLayout(self._matrix_layout())
        root_layout.addWidget(self.status_label)
        root_layout.addStretch()

        self.setCentralWidget(central)
        self.setMinimumSize(760, 480)
        self.resize(self.initial_window_size())
        self.center_on_screen()

        self._connect_signals()
        self.update_theory_note()
        self.refresh_tables()

    def _dimension_combo(self, value):
        combo = QComboBox()
        combo.addItems([str(number) for number in DIMENSIONS])
        combo.setCurrentText(str(value))
        combo.setFixedWidth(72)
        return combo

    def _dimension_controls(self):
        layout = QHBoxLayout()
        layout.setSpacing(10)
        layout.addWidget(QLabel("m rows of A"))
        layout.addWidget(self.m_combo)
        layout.addWidget(QLabel("n columns of A / rows of B"))
        layout.addWidget(self.n_combo)
        layout.addWidget(QLabel("p columns of B"))
        layout.addWidget(self.p_combo)
        layout.addStretch()
        return layout

    def _theory_panel(self):
        group = QGroupBox("Matrix multiplication reference")
        group.setStyleSheet(
            "QGroupBox { font-weight: 600; }"
            "QLabel { color: #1f2937; }"
        )

        layout = QHBoxLayout(group)
        layout.setSpacing(12)

        label = QLabel("Concept")
        label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(label)
        layout.addWidget(self.concept_combo)
        layout.addWidget(self.concept_explanation, stretch=1)
        return group

    def _matrix_layout(self):
        layout = QHBoxLayout()
        layout.setSpacing(18)
        layout.addWidget(self.a_group)
        layout.addWidget(self._operator_label("x"))
        layout.addWidget(self.b_group)
        layout.addWidget(self._operator_label("="))
        layout.addWidget(self.c_group)
        layout.addStretch()
        return layout

    def _matrix_group(self, title, table):
        group = QGroupBox(title)
        layout = QVBoxLayout(group)
        layout.addWidget(table)
        self._prepare_table(table)
        return group

    def _operator_label(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 24px; font-weight: 600;")
        return label

    def _prepare_table(self, table):
        table.setAlternatingRowColors(True)
        table.setShowGrid(True)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        table.verticalHeader().setDefaultSectionSize(34)
        table.horizontalHeader().setDefaultSectionSize(66)
        table.horizontalHeader().setMinimumSectionSize(58)
        table.verticalHeader().setMinimumSectionSize(30)
        table.setMinimumHeight(160)
        table.setMinimumWidth(180)

    def _connect_signals(self):
        self.m_combo.currentTextChanged.connect(self.update_dimensions)
        self.n_combo.currentTextChanged.connect(self.update_dimensions)
        self.p_combo.currentTextChanged.connect(self.update_dimensions)
        self.concept_combo.currentTextChanged.connect(self.update_theory_note)
        self.a_table.itemChanged.connect(self.recompute)
        self.b_table.itemChanged.connect(self.recompute)

    def initial_window_size(self):
        screen = QApplication.primaryScreen()
        available = screen.availableGeometry()

        width = min(1200, max(760, int(available.width() * 0.70)))
        height = min(820, max(480, int(available.height() * 0.70)))

        return QSize(width, height)

    def center_on_screen(self):
        screen = QApplication.primaryScreen()
        available = screen.availableGeometry()
        frame = self.frameGeometry()
        frame.moveCenter(available.center())
        self.move(frame.topLeft())

    def update_theory_note(self, concept=None):
        if concept is None:
            concept = self.concept_combo.currentText()
        self.concept_explanation.setText(THEORY_NOTES[concept])

    def update_dimensions(self):
        self.m = int(self.m_combo.currentText())
        self.n = int(self.n_combo.currentText())
        self.p = int(self.p_combo.currentText())

        self.a = resize_matrix(self.a, self.m, self.n)
        self.b = resize_matrix(self.b, self.n, self.p)
        self.c = multiply(self.a, self.b)
        self.refresh_tables()

    def refresh_tables(self):
        self.a_group.setTitle(f"Matrix A ({self.m} x {self.n})")
        self.b_group.setTitle(f"Matrix B ({self.n} x {self.p})")
        self.c_group.setTitle(f"Matrix C ({self.m} x {self.p})")

        self.configure_table(self.a_table, self.m, self.n, editable=True)
        self.configure_table(self.b_table, self.n, self.p, editable=True)
        self.configure_table(self.c_table, self.m, self.p, editable=False)

        self.load_matrix(self.a_table, self.a)
        self.load_matrix(self.b_table, self.b)
        self.load_matrix(self.c_table, self.c)
        self.status_label.setText("C updates when you edit A or B.")

    def configure_table(self, table, rows, cols, editable):
        table.blockSignals(True)
        table.setRowCount(rows)
        table.setColumnCount(cols)
        table.setHorizontalHeaderLabels(str(col + 1) for col in range(cols))
        table.setVerticalHeaderLabels(str(row + 1) for row in range(rows))

        for row in range(rows):
            for col in range(cols):
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                if not editable:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    item.setBackground(Qt.GlobalColor.lightGray)
                table.setItem(row, col, item)

        table.blockSignals(False)

    def load_matrix(self, table, matrix):
        table.blockSignals(True)
        for row, values in enumerate(matrix):
            for col, value in enumerate(values):
                table.item(row, col).setText(self._format_number(value))
        table.blockSignals(False)

    def read_matrix(self, table):
        values = []
        for row in range(table.rowCount()):
            matrix_row = []
            for col in range(table.columnCount()):
                matrix_row.append(self._read_number(table, row, col))
            values.append(matrix_row)
        return values

    def recompute(self):
        try:
            self.a = self.read_matrix(self.a_table)
            self.b = self.read_matrix(self.b_table)
            self.c = multiply(self.a, self.b)
        except ValueError as error:
            self.status_label.setText(str(error))
            return

        self.load_matrix(self.c_table, self.c)
        self.status_label.setText("C = A x B")

    def _read_number(self, table, row, col):
        item = table.item(row, col)
        text = item.text().strip() if item else ""
        if not text:
            raise ValueError(f"Cell ({row + 1}, {col + 1}) is empty")

        try:
            value = float(text)
        except ValueError as error:
            raise ValueError(f"Cell ({row + 1}, {col + 1}) is not a number") from error

        return int(value) if value.is_integer() else value

    def _format_number(self, value):
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
