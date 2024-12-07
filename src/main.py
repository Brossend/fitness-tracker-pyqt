import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox

from PyQt5.QtWidgets import QMenuBar, QAction

from src.state.state_session import state_session
from src.widget.widget_login import LoginWidget
from src.widget.widget_registration import RegistrationWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fitness Tracker")
        self.setGeometry(100, 100, 800, 600)

        # Меню
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Меню "Файл"
        file_menu = menu_bar.addMenu("Файл")
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Меню "Пользователь"
        user_menu = menu_bar.addMenu("Пользователь")

        login_action = QAction("Войти", self)
        login_action.triggered.connect(self.show_login)
        user_menu.addAction(login_action)

        register_action = QAction("Регистрация", self)
        register_action.triggered.connect(self.show_registration)
        user_menu.addAction(register_action)

        # Центральный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

    def show_registration(self):
        if state_session.get_user():
            QMessageBox.warning(self, "Ошибка", "Вы уже вошли в систему.")
        else:
            registration_widget = RegistrationWidget()
            self.setCentralWidget(registration_widget)

    def show_login(self):
        if state_session.get_user():
            QMessageBox.warning(self, "Ошибка", "Вы уже вошли в систему.")
        else:
            login_widget = LoginWidget()
            self.setCentralWidget(login_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
