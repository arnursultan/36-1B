# CREATE - Создаёт таблицу
# INSERT - Добавляет данные
# SELECT - Получает данные
# UPDATE - Изменяет данные
# DELETE - Удаляет данные

import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QListWidget
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Работа с БД")
        self.resize(400, 400)

        self.init_db()
        self.setup_ui()
        self.load_students()

    def init_db(self):
        self.connection = sqlite3.connect("students.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER
        )
        """)

        self.connection.commit()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        self.name_label = QLabel("Имя")
        self.name_input = QLineEdit()

        self.age_label = QLabel("Возраст")
        self.age_input = QLineEdit()

        self.add_button = QPushButton("Добавить")

        self.students_list = QListWidget()

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.age_label)
        self.layout.addWidget(self.age_input)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.students_list)

        self.setLayout(self.layout)

        self.add_button.clicked.connect(self.add_student)

    def add_student(self):
        name = self.name_input.text()
        age = self.age_input.text()

        self.cursor.execute(
            "INSERT INTO students(name, age) VALUES(?, ?)",
            (name, age)
        )

        self.connection.commit()

        self.name_input.clear()
        self.age_input.clear()

        self.load_students()

    def load_students(self):
        self.students_list.clear()

        self.cursor.execute("SELECT * FROM students")
        students = self.cursor.fetchall()

        for student in students:
            text = f"{student[1]} - {student[2]}"
            self.students_list.addItem(text)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())