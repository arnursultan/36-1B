import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QListWidget,
    QMessageBox,
)

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("students.database")
        self.cursor = self.conn.cursor()

        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
        """)
        self.conn.commit()

    def add_student(self, name, age):
        self.cursor.execute(
            "INSERT INTO students(name, age) VALUES(?,?)",
            (name, age)
        )
        self.conn.commit()

    def get_students(self):
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    def delete_student(self, student_id):
        self.cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )
        self.conn.commit()

    def update_student(self, student_id, name, age):
        self.cursor.execute(
            "UPDATE students SET name = ?, age = ? WHERE id = ?",
            (name, age, student_id)
        )
        self.conn.commit()