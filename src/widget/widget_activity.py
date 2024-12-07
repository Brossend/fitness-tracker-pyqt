from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDateEdit
)
from PyQt5.QtCore import QDate

from src.db.db_manager import DatabaseManager
from src.state.state_session import state_session


class ActivityWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.calories_input = ''
        self.steps_input = ''
        self.date_input = ''
        self.user_data = state_session.get_user()
        self.db_manager = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

        # Заголовок
        layout.addWidget(QLabel("Добавить активность"))

        # Поле для ввода даты
        layout.addWidget(QLabel("Дата:"))
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        layout.addWidget(self.date_input)

        # Поле для ввода шагов
        layout.addWidget(QLabel("Шаги:"))
        self.steps_input = QLineEdit()
        self.steps_input.setPlaceholderText("Введите количество шагов")
        layout.addWidget(self.steps_input)

        # Поле для ввода калорий
        layout.addWidget(QLabel("Калории:"))
        self.calories_input = QLineEdit()
        self.calories_input.setPlaceholderText("Введите количество сожженных калорий")
        layout.addWidget(self.calories_input)

        # Кнопка добавления
        add_button = QPushButton("Добавить активность")
        add_button.clicked.connect(self.add_activity)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def add_activity(self):
        date = self.date_input.date().toString("yyyy-MM-dd")
        steps = self.steps_input.text()
        calories = self.calories_input.text()

        if not steps or not calories:
            QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения.")
            return

        try:
            steps = int(steps)
            calories = float(calories)
            self.db_manager.add_activity(self.user_data['id'], date, steps, calories)
            QMessageBox.information(self, "Успех", "Активность добавлена успешно!")
            self.steps_input.clear()
            self.calories_input.clear()
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Шаги и калории должны быть числовыми значениями.")

    def closeEvent(self, event):
        self.db_manager.close()

    def go_back(self):
        from src.widget.widget_dashboard import DashboardWidget
        self.parent().setCentralWidget(DashboardWidget({"id": self.user_data['id'], "name": self.user_data['name']}))