from datetime import datetime

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QInputDialog,
    QDateEdit, QFileDialog
)

from src.db.db_manager import DatabaseManager
from src.state.state_session import state_session


class GoalsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.goal_deadline_input = ''
        self.goal_target_input = ''
        self.goal_name_input = ''
        self.goals_table = ''
        self.user_data = state_session.get_user()
        self.db_manager = DatabaseManager()
        self.init_ui()
        self.load_goals()

    def init_ui(self):
        layout = QVBoxLayout()

        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

        # Заголовок
        layout.addWidget(QLabel("Ваши цели"))

        # Таблица для отображения целей
        self.goals_table = QTableWidget()
        self.goals_table.setColumnCount(4)
        self.goals_table.setHorizontalHeaderLabels(["Цель", "Текущее значение", "Целевое значение", "Дедлайн"])
        layout.addWidget(self.goals_table)

        # Поля ввода для новой цели
        layout.addWidget(QLabel("Добавить новую цель"))
        self.goal_name_input = QLineEdit()
        self.goal_name_input.setPlaceholderText("Название цели")
        layout.addWidget(self.goal_name_input)

        self.goal_target_input = QLineEdit()
        self.goal_target_input.setPlaceholderText("Целевое значение")
        layout.addWidget(self.goal_target_input)

        layout.addWidget(QLabel("Дедлайн:"))
        self.goal_deadline_input = QDateEdit()
        self.goal_deadline_input.setDate(QDate.currentDate())
        self.goal_deadline_input.setCalendarPopup(True)
        layout.addWidget(self.goal_deadline_input)

        # Кнопка добавления цели
        add_goal_button = QPushButton("Добавить цель")
        add_goal_button.clicked.connect(self.add_goal)
        layout.addWidget(add_goal_button)

        # Кнопка редактирования цели
        edit_goal_button = QPushButton("Редактировать цель")
        edit_goal_button.clicked.connect(self.edit_goal)
        layout.addWidget(edit_goal_button)

        # Кнопка удаления цели
        delete_goal_button = QPushButton("Удалить цель")
        delete_goal_button.clicked.connect(self.delete_goal)
        layout.addWidget(delete_goal_button)

        # Кнопка для скачивания целей в формате TXT
        download_button = QPushButton("Скачать данные целей")
        download_button.clicked.connect(self.download_goals_as_txt)
        layout.addWidget(download_button)

        # Кнопка загрузки целей из TXT
        load_button = QPushButton("Загрузить цели из файла")
        load_button.clicked.connect(self.load_goals_from_txt)
        layout.addWidget(load_button)

        self.setLayout(layout)

    def load_goals(self):
        self.goals_table.setRowCount(0)  # Очистка таблицы
        goals = self.db_manager.get_goals(self.user_data['id'])
        for row, goal in enumerate(goals):
            self.goals_table.insertRow(row)
            self.goals_table.setItem(row, 0, QTableWidgetItem(goal["goal_name"]))
            self.goals_table.setItem(row, 1, QTableWidgetItem(str(goal["current_value"])))
            self.goals_table.setItem(row, 2, QTableWidgetItem(str(goal["target_value"])))
            self.goals_table.setItem(row, 3, QTableWidgetItem(str(goal["deadline"])))

    def add_goal(self):
        goal_name = self.goal_name_input.text()
        target_value = self.goal_target_input.text()
        deadline_value = self.goal_deadline_input.text()

        if not goal_name or not target_value or not deadline_value:
            QMessageBox.warning(self, "Ошибка", "Название цели и целевое значение обязательны для заполнения.")
            return

        try:
            target_value = float(target_value)
            self.db_manager.add_goal(self.user_data['id'], goal_name, target_value, deadline_value)
            QMessageBox.information(self, "Успех", "Цель добавлена успешно!")
            self.goal_name_input.clear()
            self.goal_target_input.clear()
            self.load_goals()  # Обновление таблицы целей
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Целевое значение должно быть числом.")

    def edit_goal(self):
        selected_row = self.goals_table.currentRow()  # Получаем выбранную строку
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите цель для редактирования.")
            return

        goal_name_item = self.goals_table.item(selected_row, 0)
        target_value_item = self.goals_table.item(selected_row, 2)
        deadline_item = self.goals_table.item(selected_row, 3)

        # Запрашиваем новое значение
        new_goal_name, ok_name = QInputDialog.getText(self, "Редактирование цели", "Введите новое название:",
                                                      QLineEdit.Normal, goal_name_item.text())
        new_target_value, ok_value = QInputDialog.getDouble(self, "Редактирование цели",
                                                            "Введите новое целевое значение:",
                                                            value=float(target_value_item.text()))
        new_deadline, ok_deadline = QInputDialog.getText(self, "Редактирование цели",
        "Введите новый дедлайн (ГГГГ-ММ-ДД):",
                                                      QLineEdit.Normal, deadline_item.text())

        if ok_name and ok_value and ok_deadline:
            goal_id = self.db_manager.get_goal_id(self.user_data['id'], goal_name_item.text())
            if goal_id:
                try:
                    datetime.strptime(new_deadline, "%d.%m.%Y")
                    self.db_manager.update_goal(goal_id, new_goal_name, new_target_value, new_deadline)
                    QMessageBox.information(self, "Успех", "Цель обновлена успешно!")
                    self.load_goals()
                except ValueError:
                    self.db_manager.update_goal(goal_id, new_goal_name, new_target_value, deadline_item.text())
                    QMessageBox.warning(self, "Предупреждение", "Название и целевое значение сохранены. Дата не сохранена. Введите дату в формате ДД.ММ.ГГГГ.")
                    self.load_goals()

    def delete_goal(self):
        selected_row = self.goals_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите цель для удаления.")
            return

        goal_name_item = self.goals_table.item(selected_row, 0)

        confirm = QMessageBox.question(self, "Удаление цели",
                                       f"Вы уверены, что хотите удалить цель '{goal_name_item.text()}'?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            goal_id = self.db_manager.get_goal_id(self.user_data['id'], goal_name_item.text())
            if goal_id:
                self.db_manager.delete_goal(goal_id)
                QMessageBox.information(self, "Успех", "Цель удалена успешно!")
                self.load_goals()

    def load_goals_from_txt(self):
        # Открываем диалог для выбора файла
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть файл с целями", "", "Text Files (*.txt);;All Files (*)", options=options)
        if not file_path:
            return  # Если пользователь отменил выбор файла

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # Переменные для хранения данных о цели
            goal_name, current_value, target_value, deadline = '', '', '', ''

            # Чтение строк и извлечение данных
            for line in lines:
                line = line.strip()

                if line.startswith("Цель:"):
                    if goal_name:  # Если есть данные о предыдущей цели, добавляем в базу
                        self.db_manager.add_goal(self.user_data['id'], goal_name, float(target_value), deadline)
                    goal_name = line.split(":")[1].strip()
                elif line.startswith("Текущее значение:"):
                    current_value = line.split(":")[1].strip()
                elif line.startswith("Целевое значение:"):
                    target_value = line.split(":")[1].strip()
                elif line.startswith("Дедлайн:"):
                    deadline = line.split(":")[1].strip()

            # Добавляем последнюю цель
            if goal_name:
                self.db_manager.add_goal(self.user_data['id'], goal_name, float(target_value), deadline)

            # Обновление таблицы после загрузки
            self.load_goals()

            QMessageBox.information(self, "Успех", "Цели успешно загружены из файла!")

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке целей: {str(e)}")

    def download_goals_as_txt(self):
        # Получаем все цели пользователя из базы данных
        goals = self.db_manager.get_goals(self.user_data['id'])
        if not goals:
            QMessageBox.warning(self, "Ошибка", "У пользователя нет целей для скачивания.")
            return

        # Открываем диалог для выбора места сохранения
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить как", "", "Text Files (*.txt)", options=options)
        if not file_path:
            return  # Если пользователь отменил выбор файла

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                for goal in goals:
                    goal_name = goal["goal_name"]
                    current_value = goal["current_value"]
                    target_value = goal["target_value"]
                    deadline = goal["deadline"]
                    file.write(
                        f"Цель: {goal_name}\nТекущее значение: {current_value}\nЦелевое значение: {target_value}\nДедлайн: {deadline}\n\n")
            QMessageBox.information(self, "Успех", f"Цели успешно сохранены в файл!")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при сохранении файла: {str(e)}")

    def go_back(self):
        from src.widget.widget_dashboard import DashboardWidget
        self.parent().setCentralWidget(DashboardWidget({"id": self.user_data['id'], "name": self.user_data['name']}))