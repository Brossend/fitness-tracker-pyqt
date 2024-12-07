from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

from src.state.state_session import state_session
from src.widget.widget_activity import ActivityWidget
from src.widget.widget_analytics import AnalyticsWidget
from src.widget.widget_goals import GoalsWidget
from src.widget.widget_profile import ProfileWidget
from src.widget.widget_progress import ProgressWidget


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

        profile_button = QPushButton("Мой профиль")
        profile_button.clicked.connect(self.show_profile)
        layout.addWidget(profile_button)

        goals_button = QPushButton("Цели")
        goals_button.clicked.connect(self.show_goals)
        layout.addWidget(goals_button)

        progress_button = QPushButton("Прогресс")
        progress_button.clicked.connect(self.show_progress)
        layout.addWidget(progress_button)

        analytics_button = QPushButton("Аналитика")
        analytics_button.clicked.connect(self.show_analytics)
        layout.addWidget(analytics_button)

        activity_button = QPushButton("Добавить активность")
        activity_button.clicked.connect(self.show_add_activity)
        layout.addWidget(activity_button)

        logout_button = QPushButton("Выйти")
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button)

        self.setLayout(layout)

    def show_add_activity(self):
        self.parent().setCentralWidget(ActivityWidget())

    def show_goals(self):
        self.parent().setCentralWidget(GoalsWidget())

    def show_progress(self):
        self.parent().setCentralWidget(ProgressWidget())

    def show_analytics(self):
        self.parent().setCentralWidget(AnalyticsWidget())

    def show_profile(self):
        self.parent().setCentralWidget(ProfileWidget())

    def logout(self):
        from src.widget.widget_login import LoginWidget
        self.parent().setCentralWidget(LoginWidget())
        state_session.clear_user()