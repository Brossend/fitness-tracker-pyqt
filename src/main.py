import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QVBoxLayout, QLabel

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

        program_menu = menu_bar.addMenu("Программа")
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about_dialog)
        program_menu.addAction(about_action)

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        program_menu.addAction(exit_action)

        user_menu = menu_bar.addMenu("Авторизация")

        login_action = QAction("Войти", self)
        login_action.triggered.connect(self.show_login)
        user_menu.addAction(login_action)

        register_action = QAction("Регистрация", self)
        register_action.triggered.connect(self.show_registration)
        user_menu.addAction(register_action)

        # Центральный виджет
        central_widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Добро пожаловать в Fitness Tracker!")
        label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(label)

        # Добавление изображения
        image_label = QLabel(self)
        pixmap = QPixmap("../assets/images/gigachad.png")
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

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

    def show_about_dialog(self):
        QMessageBox.about(self, "О программе", "Fitness Tracker v1.0\nРазработано Лямцевым Иваном и Мирясовым Сергеем, ИСТ-213.")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
