from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)

from src.db.db_manager import DatabaseManager
from src.state.state_session import state_session


class GoalsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.goal_target_input = ''
        self.goal_name_input = ''
        self.goals_table = ''
        self.user_data = state_session.get_user()
        self.db_manager = DatabaseManager()
        self.init_ui()
        self.load_goals()

    def init_ui(self):
        layout = QVBoxLayout()

        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

        # Заголовок
        layout.addWidget(QLabel("Ваши цели"))

        # Таблица для отображения целей
        self.goals_table = QTableWidget()
        self.goals_table.setColumnCount(3)
        self.goals_table.setHorizontalHeaderLabels(["Цель", "Текущее значение", "Целевое значение"])
        layout.addWidget(self.goals_table)

        # Поля ввода для новой цели
        layout.addWidget(QLabel("Добавить новую цель"))
        self.goal_name_input = QLineEdit()
        self.goal_name_input.setPlaceholderText("Название цели")
        layout.addWidget(self.goal_name_input)

        self.goal_target_input = QLineEdit()
        self.goal_target_input.setPlaceholderText("Целевое значение")
        layout.addWidget(self.goal_target_input)

        # Кнопка добавления цели
        add_goal_button = QPushButton("Добавить цель")
        add_goal_button.clicked.connect(self.add_goal)
        layout.addWidget(add_goal_button)

        self.setLayout(layout)

    def load_goals(self):
        self.goals_table.setRowCount(0)  # Очистка таблицы
        goals = self.db_manager.get_goals(self.user_data['id'])
        for row, goal in enumerate(goals):
            self.goals_table.insertRow(row)
            self.goals_table.setItem(row, 0, QTableWidgetItem(goal["goal_name"]))
            self.goals_table.setItem(row, 1, QTableWidgetItem(str(goal["current_value"])))
            self.goals_table.setItem(row, 2, QTableWidgetItem(str(goal["target_value"])))

    def add_goal(self):
        goal_name = self.goal_name_input.text()
        target_value = self.goal_target_input.text()

        if not goal_name or not target_value:
            QMessageBox.warning(self, "Ошибка", "Название цели и целевое значение обязательны для заполнения.")
            return

        try:
            target_value = float(target_value)
            self.db_manager.add_goal(self.user_data['id'], goal_name, target_value)
            QMessageBox.information(self, "Успех", "Цель добавлена успешно!")
            self.goal_name_input.clear()
            self.goal_target_input.clear()
            self.load_goals()  # Обновление таблицы целей
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Целевое значение должно быть числом.")

    def go_back(self):
        from src.widget.widget_dashboard import DashboardWidget
        self.parent().setCentralWidget(DashboardWidget({"id": self.user_data['id'], "name": self.user_data['name']}))