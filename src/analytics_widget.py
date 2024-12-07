from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from db_manager import DatabaseManager


class AnalyticsWidget(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.db_manager = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

        layout.addWidget(QLabel("Аналитика активности"))

        # Получение данных аналитики
        analytics = self.db_manager.get_analytics(self.user_id)

        # Средние значения
        layout.addWidget(QLabel(f"Среднее количество шагов за неделю: {analytics['avg_steps']}"))
        layout.addWidget(QLabel(f"Среднее количество калорий за неделю: {analytics['avg_calories']}"))

        # Лучший день
        best_day = analytics["best_day"]
        layout.addWidget(QLabel(f"Лучший день: {best_day['date']} - {best_day['steps']} шагов"))

        self.setLayout(layout)

    def go_back(self):
        from dashboard_widget import DashboardWidget
        self.parent().setCentralWidget(DashboardWidget({"id": self.user_id, "name": "Пользователь"}))