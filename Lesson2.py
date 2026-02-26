# Code 1
# import sys
#
# from PyQt6.QtWidgets import QApplication, QWidget
#
# app = QApplication(sys.argv)
#
# window = QWidget()
# window.setWindowTitle("Наше первое приложение")
# window.resize(400, 300)
# window.show()
#
# sys.exit(app.exec())x

# Code 2
# import sys
# from PyQt6.QtWidgets import (
#     QApplication,
#     QWidget,
#     QVBoxLayout,
#     QLabel,
#     QPushButton,
#     QLineEdit
# )
#
# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle("Приложение с декомпзицией")
#         self.resize(400, 200)
#
#         self.setup_ui()
#         self.setup_signals()
#
#     def setup_ui(self):
#         self.layout = QVBoxLayout()
#
#         self.label = QLabel(self)
#         self.input = QLineEdit()
#         self.button = QPushButton("OK")
#
#         self.layout.addWidget(self.label)
#         self.layout.addWidget(self.input)
#         self.layout.addWidget(self.button)
#
#         self.setLayout(self.layout)
#
#     def setup_signals(self):
#         self.button.clicked.connect(self.on_click)
#
#     def on_click(self):
#         text = self.input.text()
#         self.label.setText(text)
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())

# Code 3
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox
)

class CalculatorWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Калькулятор")
        self.resize(350, 200)

        self.setup_ui()
        self.setup_signals()

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.input_layout = QHBoxLayout()

        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("Первое число")
        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("Второе число")

        self.result_label = QLabel("Результат:")

        self.button = QPushButton("Сложить")

        self.input_layout.addWidget(self.input1)
        self.input_layout.addWidget(self.input2)

        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addWidget(self.button)
        self.main_layout.addWidget(self.result_label)

        self.setLayout(self.main_layout)

    def setup_signals(self):
        self.button.clicked.connect(self.calculate)

    def calculate(self):
        try:
            num1 = float(self.input1.text())
            num2 = float(self.input2.text())

            result = num1 + num2
            self.result_label.setText(f"Результат: {result}")

        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректные числа!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorWindow()
    window.show()
    sys.exit(app.exec())