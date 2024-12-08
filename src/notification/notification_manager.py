from datetime import datetime
from PyQt5.QtWidgets import QMessageBox


def show_notification(title, message):
    QMessageBox.information(None, title, message)

class NotificationManager:
    def __init__(self, db_manager, user_id):
        self.db_manager = db_manager
        self.user_id = user_id

    def check_activity_reminder(self):
        today = datetime.now().strftime('%Y-%m-%d')
        activity = self.db_manager.get_activity_for_date(self.user_id, today)
        if not activity:
            show_notification("Напоминание", "Вы ещё не добавили активность за сегодня!")

    def check_goal_deadlines(self):
        upcoming_goals = self.db_manager.get_upcoming_goals(self.user_id)
        if upcoming_goals:
            for goal in upcoming_goals:
                show_notification(
                    "Дедлайн цели",
                    f"Цель '{goal['goal_name']}' должна быть выполнена к {goal['deadline']}. Успейте достигнуть её!"
                )
