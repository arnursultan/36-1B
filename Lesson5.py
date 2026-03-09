import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QListWidget,
    QMessageBox
)


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("students.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
        """)
        self.conn.commit()

    def add_student(self, name, age):
        self.cursor.execute(
            "INSERT INTO students(name, age) VALUES (?, ?)",
            (name, age)
        )
        self.conn.commit()

    def get_students(self):
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    def delete_student(self, student_id):
        self.cursor.execute(
            "DELETE FROM students WHERE id=?",
            (student_id,)
        )
        self.conn.commit()

    def update_student(self, student_id, name, age):
        self.cursor.execute(
            "UPDATE students SET name=?, age=? WHERE id=?",
            (name, age, student_id)
        )
        self.conn.commit()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.db = Database()
        self.selected_id = None

        self.setWindowTitle("Student Manager")
        self.resize(500, 400)

        self.setup_ui()
        self.load_students()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Имя")

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Возраст")

        self.students_list = QListWidget()
        self.students_list.itemClicked.connect(self.select_student)

        buttons_layout = QHBoxLayout()

        self.add_btn = QPushButton("Добавить")
        self.update_btn = QPushButton("Обновить")
        self.delete_btn = QPushButton("Удалить")

        buttons_layout.addWidget(self.add_btn)
        buttons_layout.addWidget(self.update_btn)
        buttons_layout.addWidget(self.delete_btn)

        layout.addWidget(QLabel("Имя"))
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Возраст"))
        layout.addWidget(self.age_input)

        layout.addLayout(buttons_layout)
        layout.addWidget(self.students_list)

        self.setLayout(layout)

        self.add_btn.clicked.connect(self.add_student)
        self.update_btn.clicked.connect(self.update_student)
        self.delete_btn.clicked.connect(self.delete_student)

    def load_students(self):
        self.students_list.clear()

        students = self.db.get_students()

        for student in students:
            text = f"{student[0]} | {student[1]} | {student[2]}"
            self.students_list.addItem(text)

    def validate_input(self):
        name = self.name_input.text().strip()
        age = self.age_input.text().strip()

        if not name or not age:
            QMessageBox.warning(self, "Ошибка", "Введите данные")
            return None, None

        if not age.isdigit():
            QMessageBox.warning(self, "Ошибка", "Возраст должен быть числом")
            return None, None

        return name, int(age)

    def add_student(self):
        name, age = self.validate_input()

        if name is None:
            return

        self.db.add_student(name, age)
        self.clear_inputs()
        self.load_students()

    def select_student(self, item):
        data = item.text().split(" | ")

        self.selected_id = int(data[0])

        self.name_input.setText(data[1])
        self.age_input.setText(data[2])

    def update_student(self):
        if self.selected_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите студента")
            return


        name, age = self.validate_input()

        if name is None:
            return

        self.db.update_student(self.selected_id, name, age)

        self.clear_inputs()
        self.load_students()

    def delete_student(self):
        if self.selected_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите студента")
            return

        confirm = QMessageBox.question(
            self,
            "Подтверждение",
            "Удалить студента?"
        )

        if confirm == QMessageBox.StandardButton.Yes:
            self.db.delete_student(self.selected_id)

            self.clear_inputs()
            self.load_students()

    def clear_inputs(self):
        self.name_input.clear()
        self.age_input.clear()
        self.selected_id = None


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())
