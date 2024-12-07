from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

from src.db.db_manager import DatabaseManager
from src.state.state_session import state_session


class ProfileWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.password_input = ''
        self.email_input = ''
        self.name_input = ''
        self.user_data = state_session.get_user()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

        # Заголовок
        layout.addWidget(QLabel("Профиль пользователя"))

        # Имя пользователя
        self.name_input = QLineEdit()
        self.name_input.setText(self.user_data['name'])
        layout.addWidget(QLabel("Имя"))
        layout.addWidget(self.name_input)

        # Email
        self.email_input = QLineEdit()
        self.email_input.setText(self.user_data['email'])
        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.email_input)

        # Кнопка для изменения данных
        update_button = QPushButton("Обновить данные")
        update_button.clicked.connect(self.update_profile)
        layout.addWidget(update_button)

        # Пароль
        self.password_input = QLineEdit()
        self.password_input.setText(self.user_data['password'])
        layout.addWidget(QLabel("Пароль"))
        layout.addWidget(self.password_input)

        # Кнопка для смены пароля
        change_password_button = QPushButton("Изменить пароль")
        change_password_button.clicked.connect(self.change_password)
        layout.addWidget(change_password_button)

        # Кнопка для удаления аккаунта
        delete_account_button = QPushButton("Удалить аккаунт")
        delete_account_button.clicked.connect(self.delete_account)
        layout.addWidget(delete_account_button)

        self.setLayout(layout)

    def update_profile(self):
        new_name = self.name_input.text()
        new_email = self.email_input.text()

        if not new_name or not new_email:
            QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения.")
            return

        # Обновляем данные пользователя в user_session и в базе данных
        user_data = state_session.get_user()
        user_data['name'] = new_name
        user_data['email'] = new_email
        state_session.set_user(user_data)

        self.db_manager.update_user_details(user_data['id'], new_name, new_email)

        QMessageBox.information(self, "Успех", "Данные обновлены успешно!")

    def change_password(self):
        # Логика для изменения пароля
        new_password = self.password_input.text()

        if not new_password:
            QMessageBox.warning(self, "Ошибка", "Поле пароля пустое.")
            return

        user_data = state_session.get_user()
        user_data['password'] = new_password
        self.db_manager.update_password(user_data['id'], new_password)

        QMessageBox.information(self, "Успех", "Пароль успешно изменен!")

    def delete_account(self):
        from src.widget.widget_login import LoginWidget
        self.db_manager.delete_user(self.user_data['id'])
        state_session.clear_user()
        QMessageBox.information(self, "Удаление", "Ваш аккаунт был удален.")
        self.parent().setCentralWidget(LoginWidget())

    def go_back(self):
        from src.widget.widget_dashboard import DashboardWidget
        self.parent().setCentralWidget(DashboardWidget({"id": self.user_data['id'], "name": self.user_data['name']}))