import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

from PyQt5.QtWidgets import QMenuBar, QAction, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fitness Tracker")
        self.setGeometry(100, 100, 800, 600)

        # Установка меню
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Файл
        file_menu = menu_bar.addMenu("Файл")
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Справка
        help_menu = menu_bar.addMenu("Справка")
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

        # Центральный виджет
        central_widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Добро пожаловать в Fitness Tracker!")
        label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(label)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_about_dialog(self):
        QMessageBox.about(self, "О программе", "Fitness Tracker v1.0\nРазработано с использованием PyQt5.")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
