import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QComboBox, QLineEdit, QLabel, QMessageBox
)
from Lesson8db_logic import get_products, get_categories, add_product


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD App")
        self.setGeometry(100, 100, 500, 300)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Цена", "Категория"])

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Название товара")

        self.input_price = QLineEdit()
        self.input_price.setPlaceholderText("Цена")

        self.combo = QComboBox()
        self.load_categories()

        self.btn_load = QPushButton("Загрузить данные")
        self.btn_load.clicked.connect(self.load_data)

        self.btn_add = QPushButton("Добавить")
        self.btn_add.clicked.connect(self.add_product)

        layout.addWidget(self.table)

        layout.addWidget(QLabel("Название"))
        layout.addWidget(self.input_name)

        layout.addWidget(QLabel("Цена"))
        layout.addWidget(self.input_price)

        layout.addWidget(QLabel("Категория"))
        layout.addWidget(self.combo)

        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_load)

        self.setLayout(layout)

    def load_categories(self):
        categories = get_categories()
        for cat in categories:
            self.combo.addItem(cat[1], cat[0])

    def load_data(self):
        data = get_products()
        self.table.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def add_product(self):
        name = self.input_name.text()
        price = self.input_price.text()
        category_id = self.combo.currentData()

        if not name or not price:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        if not price.isdigit():
            QMessageBox.warning(self, "Ошибка", "Цена должна быть числом")
            return
        add_product(name, int(price), category_id)

        QMessageBox.information(self, "Успех", "Товар добавлен")

        self.load_data()
        self.input_name.clear()
        self.input_price.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
