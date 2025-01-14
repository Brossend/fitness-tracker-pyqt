from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDateEdit, QTableWidgetItem, QInputDialog,
    QTableWidget, QFileDialog
)
from PyQt5.QtCore import QDate

from src.db.db_manager import DatabaseManager
from src.state.state_session import state_session


class ActivityWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.calories_input = ''
        self.steps_input = ''
        self.date_input = ''
        self.user_data = state_session.get_user()
        self.db_manager = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

        # Заголовок
        layout.addWidget(QLabel("Добавить активность"))

        # Таблица для отображения активности
        self.activities_table = QTableWidget()
        self.activities_table.setColumnCount(3)
        self.activities_table.setHorizontalHeaderLabels(["Дата", "Шаги", "Калории"])
        layout.addWidget(self.activities_table)

        # Поле для ввода даты
        layout.addWidget(QLabel("Дата:"))
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        layout.addWidget(self.date_input)

        # Поле для ввода шагов
        layout.addWidget(QLabel("Шаги:"))
        self.steps_input = QLineEdit()
        self.steps_input.setPlaceholderText("Введите количество шагов")
        layout.addWidget(self.steps_input)

        # Поле для ввода калорий
        layout.addWidget(QLabel("Калории:"))
        self.calories_input = QLineEdit()
        self.calories_input.setPlaceholderText("Введите количество сожженных калорий")
        layout.addWidget(self.calories_input)

        # Кнопка добавления активности
        add_button = QPushButton("Добавить активность")
        add_button.clicked.connect(self.add_activity)
        layout.addWidget(add_button)

        # Кнопка загрузки активности из файла
        load_button = QPushButton("Загрузить активности из файла")
        load_button.clicked.connect(self.load_activities_from_file)
        layout.addWidget(load_button)

        # Кнопка редактирования активности
        edit_button = QPushButton("Редактировать активность")
        edit_button.clicked.connect(self.edit_activity)
        layout.addWidget(edit_button)

        # Кнопка удаления активности
        delete_button = QPushButton("Удалить активность")
        delete_button.clicked.connect(self.delete_activity)
        layout.addWidget(delete_button)

        self.setLayout(layout)
        self.load_activities()  # Загружаем данные активности

    def load_activities(self):
        self.activities_table.setRowCount(0)  # Очистка таблицы
        activities = self.db_manager.get_activities(self.user_data['id'])
        for row, activity in enumerate(activities):
            self.activities_table.insertRow(row)
            self.activities_table.setItem(row, 0, QTableWidgetItem(activity["date"]))
            self.activities_table.setItem(row, 1, QTableWidgetItem(str(activity["steps"])))
            self.activities_table.setItem(row, 2, QTableWidgetItem(str(activity["calories"])))

    def load_activities_from_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Text Files (*.txt);;All Files (*)")
        if not file_name:
            return

        try:
            with open(file_name, 'r') as file:
                for line in file:
                    date, steps, calories = line.strip().split(
                        ",")  # Предположим, что файл в формате "дата, шаги, калории"
                    self.db_manager.add_activity(self.user_data['id'], date, int(steps), float(calories))
            QMessageBox.information(self, "Успех", "Активности успешно загружены из файла.")
            self.load_activities()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить файл: {e}")

    def edit_activity(self):
        selected_row = self.activities_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для редактирования.")
            return

        date_item = self.activities_table.item(selected_row, 0)
        steps_item = self.activities_table.item(selected_row, 1)
        calories_item = self.activities_table.item(selected_row, 2)

        # Запрашиваем новые значения
        new_date, ok_date = QInputDialog.getText(self, "Редактирование активности", "Введите новую дату:",
                                                 QLineEdit.Normal, date_item.text())
        new_steps, ok_steps = QInputDialog.getInt(self, "Редактирование активности", "Введите новое количество шагов:",
                                                  value=int(steps_item.text()))
        new_calories, ok_calories = QInputDialog.getDouble(self, "Редактирование активности",
                                                           "Введите новое количество калорий:",
                                                           value=float(calories_item.text()))

        if ok_date and ok_steps and ok_calories:
            activity_id = self.db_manager.get_activity_id(self.user_data['id'], date_item.text())
            if activity_id:
                self.db_manager.update_activity(activity_id, new_date, new_steps, new_calories)
                QMessageBox.information(self, "Успех", "Активность обновлена успешно!")
                self.load_activities()

    def delete_activity(self):
        selected_row = self.activities_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления.")
            return

        date_item = self.activities_table.item(selected_row, 0)

        confirm = QMessageBox.question(self, "Удаление активности",
                                       f"Вы уверены, что хотите удалить запись за '{date_item.text()}'?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            activity_id = self.db_manager.get_activity_id(self.user_data['id'], date_item.text())
            if activity_id:
                self.db_manager.delete_activity(activity_id)
                QMessageBox.information(self, "Успех", "Активность удалена успешно!")
                self.load_activities()

    def add_activity(self):
        date = self.date_input.date().toString("yyyy-MM-dd")
        steps = self.steps_input.text()
        calories = self.calories_input.text()

        if not steps or not calories:
            QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения.")
            return

        try:
            steps = int(steps)
            calories = float(calories)
            self.db_manager.add_activity(self.user_data['id'], date, steps, calories)
            QMessageBox.information(self, "Успех", "Активность добавлена успешно!")
            self.steps_input.clear()
            self.calories_input.clear()
            self.load_activities()
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Шаги и калории должны быть числовыми значениями.")

    def closeEvent(self, event):
        self.db_manager.close()

    def go_back(self):
        from src.widget.widget_dashboard import DashboardWidget
        self.parent().setCentralWidget(DashboardWidget({"id": self.user_data['id'], "name": self.user_data['name']}))