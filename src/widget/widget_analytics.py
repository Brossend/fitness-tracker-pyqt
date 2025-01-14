from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from src.db.db_manager import DatabaseManager
from src.state.state_session import state_session


class AnalyticsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.user_data = state_session.get_user()
        self.db_manager = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

        layout.addWidget(QLabel("Аналитика активности"))

        # Добавление изображения
        image_label = QLabel(self)
        pixmap = QPixmap("../assets/images/muscules.jpg")
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setFixedHeight(400)
        layout.addWidget(image_label)

        # Получение данных аналитики
        analytics = self.db_manager.get_analytics(self.user_data['id'])

        # Средние значения
        layout.addWidget(QLabel(f"Среднее количество шагов за неделю: {analytics['avg_steps']}"))
        layout.addWidget(QLabel(f"Среднее количество калорий за неделю: {analytics['avg_calories']}"))

        # Лучший день
        best_day = analytics["best_day"]
        layout.addWidget(QLabel(f"Лучший день: {best_day['date']} - {best_day['steps']} шагов"))

        self.setLayout(layout)

    def go_back(self):
        from src.widget.widget_dashboard import DashboardWidget
        self.parent().setCentralWidget(DashboardWidget({"id": self.user_data['id'], "name": self.user_data['name']}))