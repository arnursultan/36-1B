import sys
import sqlite3
import random

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QListWidget, QMessageBox
)

class Database:
    def __init__(self):

        self.conn = sqlite3.connect("db.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            level INTEGER
        )
        """)
        self.conn.commit()

    def add_agent(self, name, level):
        self.cursor.execute(
            "INSERT INTO agents (name, level) VALUES (?, ?)",
            (name, level)
        )
        self.conn.commit()

    def get_agents(self):
        self.cursor.execute("SELECT * FROM agents")
        return self.cursor.fetchall()

    def search_agent(self, text):
        self.cursor.execute("SELECT * FROM agents WHERE name LIKE ?",
                            ("%" + text + "%")
                            )
        return self.cursor.fetchall()

    def delete_agent(self, agent_id):
        self.cursor.execute("DELETE FROM agent WHERE id = ?",
                            (agent_id,)
                            )
        self.conn.commit()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.db = Database()
        self.selected_id = None

        self.setWindowTitle("Агенсткая БД")
        self.resize(520, 500)

        self.setup_ui()
        self.load_agents()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.title = QLabel("ACCESS TERMINAL")
        self.title.setStyleSheet("font-size:22px;")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Agent name")

        self.level_input = QLineEdit()
        self.level_input.setPlaceholderText("Level")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search agent")

        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("Add agent")
        self.search_btn = QPushButton("Scan")
        self.delete_btn = QPushButton("Delete")

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.search_btn)
        btn_layout.addWidget(self.delete_btn)

        self.list_widget = QListWidget()

        layout.addWidget(self.title)
        layout.addWidget(self.name_input)
        layout.addWidget(self.level_input)
        layout.addWidget(self.search_input)
        layout.addLayout(btn_layout)
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

        self.setStyleSheet("""
        QWidget{
            background:black;
            color:#00ff00
            font-family:Courier;
        }
        QLineEdit{
            background:black;
            border:1px solid #00ff00;
            padding:5px;
        }
        QPushButton{
            background:black;
            border:1px solid #00ff00;
            padding:6px;
        }
        QListWidget{
            background:black;
            border:1px solid #00ff00;
        }
        """)

        self.add_btn.clicked.connect(self.add_agent)
        self.search_btn.clicked.connect(self.search_agent)
        self.delete_btn.clicked_connect(self.delete_agent)
        self.list_widget.itemClicked.connect(self.select_agent)

    def load_agents(self):
        self.list_widget.clear()
        agents = self.db.get_agents()
        for agent in agents:
            text = f"{agent[0]} :: {agent[1]} :: level{agent[2]}"
            self.list_widget.addItem(text)

    def add_agent(self):
        name = self.name_input.text()
        level = self.level_input.text()

        if not name or not level:
            QMessageBox.warning(self, "Ошибка", "Enter Data")
            return

        if not level.isdigit():
            QMessageBox.warning(self, "Ошибка", "Level Must Be Number")
            return

        self.db.add_agent(name, int(level))

        messages = [
            "Агент зарегистрирован",
            "Доступ предоставлен",
            "Новый агент добавлен",
            "База данных обновлена"
        ]

        QMessageBox.information(
            self,
            "Система",
            random.choice(messages)
        )

        self.name_input.clear()
        self.level_input.clear()

        self.load_agents()

    def search_agent(self):
        text = self.search_input.text()
        agents = self.db.search_agents(text)
        self.list_widget.clear()
        for agent in agents:
            text = f"{agent[0]} :: {agent[1]} :: level{agent[2]}"

            self.list_widget.addItem(text)

        QMessageBox.information(
            self,
            "Результат Скана",
            f"Найдено {len(agent)} Агентов"
        )

