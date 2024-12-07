import sqlite3
from datetime import datetime, timedelta
import os

# Определяем путь к текущему файлу
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Абсолютный путь к базе данных
DB_PATH = os.path.join(BASE_DIR, '../../database/fitness_tracker.db')


def seed_database():
    # Подключение к базе данных
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Добавление тестового пользователя
    cursor.execute(
        """
        INSERT INTO Users (name, email, password)
        VALUES (?, ?, ?)
        """,
        ("Тестовый Пользователь", "test@example.com", "password123")
    )
    user_id = cursor.lastrowid

    # Добавление тестовых целей
    cursor.executemany(
        """
        INSERT INTO Goals (user_id, goal_name, target_value, current_value, deadline)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (user_id, "Похудение", 5, 0, "2024-12-31"),
            (user_id, "Пройти 10,000 шагов за день", 10000, 5000, "2024-12-31")
        ]
    )

    # Добавление данных активности
    start_date = datetime.now() - timedelta(days=7)
    for i in range(7):
        date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        steps = 5000 + i * 500
        calories = 200 + i * 20
        cursor.execute(
            """
            INSERT INTO ActivityLog (user_id, activity_date, steps, calories_burned)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, date, steps, calories)
        )

    conn.commit()
    conn.close()
    print("Тестовые данные добавлены!")


if __name__ == "__main__":
    seed_database()
