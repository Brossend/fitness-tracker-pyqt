from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)


class RegistrationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Поле для имени
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите ваше имя")
        layout.addWidget(QLabel("Имя:"))
        layout.addWidget(self.name_input)

        # Поле для электронной почты
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

        # Кнопка регистрации
        register_button = QPushButton("Зарегистрироваться")
        register_button.clicked.connect(self.handle_registration)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def handle_registration(self):
        # Получение введенных данных
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        if not name or not email or not password:
            QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения.")
            return

        print(f"Name: {name}, Email: {email}, Password: {password}")
        QMessageBox.information(self, "Успех", "Регистрация прошла успешно!")
