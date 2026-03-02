# import sys
# from PyQt6.QtWidgets import (
#     QApplication,
#     QWidget,
#     QVBoxLayout,
#     QLabel,
#     QPushButton,
#     QMessageBox,
#     QLineEdit
# )
#
# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle("Работа с виджетами")
#         self.resize(400, 250)
#
#         self.setup_ui()
#         self.setup_signals()
#
#     def setup_ui(self):
#         self.main_layout = QVBoxLayout()
#
#         self.title_label = QLabel("Добавление пользователя")
#
#         self.name_input = QLineEdit()
#         self.name_input.setPlaceholderText("Введите имя")
#
#         self.age_input = QLineEdit()
#         self.age_input.setPlaceholderText("Введите возраст")
#
#         self.add_button = QPushButton("Добавить")
#
#         self.result_label = QLabel("")
#
#         self.main_layout.addWidget(self.title_label)
#         self.main_layout.addWidget(self.name_input)
#         self.main_layout.addWidget(self.age_input)
#         self.main_layout.addWidget(self.add_button)
#         self.main_layout.addWidget(self.result_label)
#
#         self.setLayout(self.main_layout)
#
#     def setup_signals(self):
#         self.add_button.clicked.connect(self.add_user)
#
#     def add_user(self):
#         name = self.name_input.text()
#         age = self.age_input.text()
#
#         if not name or not age:
#             QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
#             return
#
#         if not age.isdigit():
#             QMessageBox.warning(self, "Ошибка", "Возраст должен быть числом!")
#             return
#
#         self.result_label.setText(f"Пользователь {name}, {age} лет добавлен!")
#
#         self.name_input.clear()
#         self.age_input.clear()
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())

import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QListWidget
)
from PyQt6.QtGui import QIntValidator


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Список пользователей")
        self.resize(400, 300)

        self.setup_ui()
        self.setup_signals()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        self.title_label = QLabel("Добавление пользователя")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите имя")

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Введите возраст")
        self.age_input.setValidator(QIntValidator(1, 120))

        self.add_button = QPushButton("Добавить")

        self.user_list = QListWidget()

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.age_input)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.user_list)

        self.setLayout(self.layout)

    def setup_signals(self):
        self.name_input.returnPressed.connect(self.focus_age)

        self.age_input.returnPressed.connect(self.add_user)

        self.add_button.clicked.connect(self.add_user)

    def focus_age(self):
        self.age_input.setFocus()

    def add_user(self):
        name = self.name_input.text().strip()
        age = self.age_input.text().strip()

        if not name or not age:
            return

        user_text = f"{name}, {age} лет"
        self.user_list.addItem(user_text)

        self.name_input.clear()
        self.age_input.clear()
        self.name_input.setFocus()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())