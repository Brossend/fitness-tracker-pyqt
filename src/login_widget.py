from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from db_manager import DatabaseManager
from src.dashboard_widget import DashboardWidget


class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.password_input = ''
        self.email_input = ''
        self.db_manager = DatabaseManager()  # Инициализация менеджера базы данных
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Поле для email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Введите вашу почту")
        layout.addWidget(QLabel("Электронная почта:"))
        layout.addWidget(self.email_input)

        # Поле для пароля
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Введите ваш пароль")
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)

        # Кнопка входа
        login_button = QPushButton("Войти")
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def handle_login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения.")
            return

        user = self.db_manager.authenticate_user(email, password)
        if user:
            QMessageBox.information(self, "Успех", f"Добро пожаловать, {user['name']}!")
            self.parent().setCentralWidget(DashboardWidget(user))  # Переход на личный кабинет
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный email или пароль.")

    def closeEvent(self, event):
        self.db_manager.close()  # Закрытие соединения с базой данных
