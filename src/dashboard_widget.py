from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from src.goals_widget import GoalsWidget


class DashboardWidget(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Приветствие пользователя
        welcome_label = QLabel(f"Добро пожаловать, {self.user_data['name']}!")
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(welcome_label)

        # Информация о пользователе
        user_info_label = QLabel(f"ID пользователя: {self.user_data['id']}")
        layout.addWidget(user_info_label)

        # Кнопки действий
        goals_button = QPushButton("Цели и задачи")
        goals_button.clicked.connect(self.show_goals)
        layout.addWidget(goals_button)

        progress_button = QPushButton("Прогресс")
        progress_button.clicked.connect(self.show_progress)
        layout.addWidget(progress_button)

        self.setLayout(layout)

    def show_goals(self):
        self.parent().setCentralWidget(GoalsWidget(self.user_data['id']))

    def show_progress(self):
        # Будет заменено на реальный функционал в будущем
        print("Переход на экран прогресса")
