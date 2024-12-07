from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

from src.activity_widget import ActivityWidget
from src.goals_widget import GoalsWidget
from src.progress_widget import ProgressWidget


class DashboardWidget(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Навигационное меню
        nav_layout = QHBoxLayout()

        goals_button = QPushButton("Цели")
        goals_button.clicked.connect(self.show_goals)
        nav_layout.addWidget(goals_button)

        progress_button = QPushButton("Прогресс")
        progress_button.clicked.connect(self.show_progress)
        nav_layout.addWidget(progress_button)

        activity_button = QPushButton("Добавить активность")
        activity_button.clicked.connect(self.show_add_activity)
        nav_layout.addWidget(activity_button)

        logout_button = QPushButton("Выйти")
        logout_button.clicked.connect(self.logout)
        nav_layout.addWidget(logout_button)

        layout.addLayout(nav_layout)

        # Приветствие пользователя
        welcome_label = QLabel(f"Добро пожаловать, {self.user_data['name']}!")
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(welcome_label)

        # Информация о пользователе
        user_info_label = QLabel(f"ID пользователя: {self.user_data['id']}")
        layout.addWidget(user_info_label)

        self.setLayout(layout)

    def show_add_activity(self):
        self.parent().setCentralWidget(ActivityWidget(self.user_data['id']))

    def show_goals(self):
        self.parent().setCentralWidget(GoalsWidget(self.user_data['id']))

    def show_progress(self):
        self.parent().setCentralWidget(ProgressWidget(self.user_data['id']))

    def logout(self):
        from login_widget import LoginWidget
        self.parent().setCentralWidget(LoginWidget())