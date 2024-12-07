from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)

from src.db_manager import DatabaseManager


class RegistrationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.email_input = ''
        self.password_input = ''
        self.name_input = ''
        self.db_manager = DatabaseManager()  # Инициализация менеджера базы данных
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите ваше имя")
        layout.addWidget(QLabel("Имя:"))
        layout.addWidget(self.name_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Введите вашу почту")
        layout.addWidget(QLabel("Электронная почта:"))
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Введите ваш пароль")
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)

        register_button = QPushButton("Зарегистрироваться")
        register_button.clicked.connect(self.handle_registration)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def handle_registration(self):
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        if not name or not email or not password:
            QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения.")
            return

        success = self.db_manager.add_user(name, email, password)
        if success:
            QMessageBox.information(self, "Успех", "Регистрация прошла успешно!")
            self.name_input.clear()
            self.email_input.clear()
            self.password_input.clear()
        else:
            QMessageBox.warning(self, "Ошибка", "Пользователь с таким email уже существует.")

    def closeEvent(self, event):
        self.db_manager.close()  # Закрытие соединения с базой данных
