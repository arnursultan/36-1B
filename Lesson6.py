import sys
import sqlite3
import random

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QListWidget, QMessageBox
)

class Database:

    def __init__(self):
        self.conn = sqlite3.connect("agents.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            level INTEGER
        )
        """)

        self.conn.commit()

    def add_agent(self, name, level):
        self.cursor.execute(
            "INSERT INTO agents(name, level) VALUES (?,?)",
            (name, level)
        )
        self.conn.commit()

    def get_agents(self):
        self.cursor.execute("SELECT * FROM agents")
        return self.cursor.fetchall()

    def search_agent(self, text):
        self.cursor.execute(
            "SELECT * FROM agents WHERE name LIKE ?",
            ("%" + text + "%",)
        )
        return self.cursor.fetchall()

    def delete_agent(self, agent_id):
        self.cursor.execute(
            "DELETE FROM agents WHERE id=?",
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

        self.title = QLabel("ТЕРМИНАЛ ДОСТУПА")
        self.title.setStyleSheet("font-size:22px;")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Имя агента")

        self.level_input = QLineEdit()
        self.level_input.setPlaceholderText("Уровень")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск агента")

        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("ДОБАВИТЬ")
        self.search_btn = QPushButton("ПОИСК")
        self.delete_btn = QPushButton("УДАЛИТЬ")

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
            color:#00ff00;
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
        self.delete_btn.clicked.connect(self.delete_agent)
        self.list_widget.itemClicked.connect(self.select_agent)

    def load_agents(self):

        self.list_widget.clear()

        agents = self.db.get_agents()

        for agent in agents:
            text = f"{agent[0]} :: {agent[1]} :: уровень {agent[2]}"
            self.list_widget.addItem(text)

    def add_agent(self):

        name = self.name_input.text()
        level = self.level_input.text()

        if not name or not level:
            QMessageBox.warning(self, "ОШИБКА", "ВВЕДИТЕ ДАННЫЕ")
            return

        if not level.isdigit():
            QMessageBox.warning(self, "ОШИБКА", "УРОВЕНЬ ДОЛЖЕН БЫТЬ ЧИСЛОМ")
            return

        self.db.add_agent(name, int(level))

        messages = [
            "Агент зарегистрирован",
            "Доступ разрешён",
            "Новый агент добавлен",
            "База данных обновлена"
        ]

        QMessageBox.information(
            self,
            "СИСТЕМА",
            random.choice(messages)
        )

        self.name_input.clear()
        self.level_input.clear()

        self.load_agents()

    def search_agent(self):

        text = self.search_input.text()

        agents = self.db.search_agent(text)

        self.list_widget.clear()

        for agent in agents:
            text = f"{agent[0]} :: {agent[1]} :: уровень {agent[2]}"
            self.list_widget.addItem(text)

        QMessageBox.information(
            self,
            "РЕЗУЛЬТАТ СКАНИРОВАНИЯ",
            f"НАЙДЕНО АГЕНТОВ: {len(agents)}"
        )

    def select_agent(self, item):

        data = item.text().split(" :: ")
        self.selected_id = int(data[0])

    def delete_agent(self):

        if self.selected_id is None:

            QMessageBox.warning(
                self,
                "СИСТЕМА",
                "ВЫБЕРИТЕ АГЕНТА"
            )
            return

        confirm = QMessageBox.question(
            self,
            "СИСТЕМА",
            "УДАЛИТЬ АГЕНТА?"
        )

        if confirm == QMessageBox.StandardButton.Yes:

            self.db.delete_agent(self.selected_id)

            phrases = [
                "Агент удалён",
                "Запись уничтожена",
                "Цель устранена",
                "База данных очищена"
            ]

            QMessageBox.information(
                self,
                "СИСТЕМА",
                random.choice(phrases)
            )

            self.selected_id = None

            self.load_agents()


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())
