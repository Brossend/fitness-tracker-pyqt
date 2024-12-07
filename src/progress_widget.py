from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from db_manager import DatabaseManager


class ProgressWidget(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.db_manager = DatabaseManager()
        self.init_ui()
        self.load_progress()

    def init_ui(self):
        layout = QVBoxLayout()

        # Заголовок
        layout.addWidget(QLabel("Ваш прогресс"))

        # Таблица для статистики
        self.progress_table = QTableWidget()
        self.progress_table.setColumnCount(3)
        self.progress_table.setHorizontalHeaderLabels(["Дата", "Шаги", "Калории"])
        layout.addWidget(self.progress_table)

        # График
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def load_progress(self):
        self.progress_table.setRowCount(0)  # Очистка таблицы
        progress_data = self.db_manager.get_progress(self.user_id)

        # Заполнение таблицы
        for row, entry in enumerate(progress_data):
            self.progress_table.insertRow(row)
            self.progress_table.setItem(row, 0, QTableWidgetItem(entry["date"]))
            self.progress_table.setItem(row, 1, QTableWidgetItem(str(entry["steps"])))
            self.progress_table.setItem(row, 2, QTableWidgetItem(str(entry["calories"])))

        # Построение графика
        self.plot_progress(progress_data)

    def plot_progress(self, progress_data):
        dates = [entry["date"] for entry in progress_data]
        steps = [entry["steps"] for entry in progress_data]

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(dates, steps, marker="o", label="Шаги")
        ax.set_title("Прогресс шагов")
        ax.set_xlabel("Дата")
        ax.set_ylabel("Шаги")
        ax.legend()
        self.canvas.draw()