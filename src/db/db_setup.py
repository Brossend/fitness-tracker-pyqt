import sqlite3
import os

# Определяем путь к текущему файлу
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Абсолютный путь к базе данных
DB_PATH = os.path.join(BASE_DIR, '../../database/fitness_tracker.db')

# Абсолютный путь к файлу schema.sql
SCHEMA_PATH = os.path.join(BASE_DIR, '../../schema/schema.sql')

def initialize_database():
    # Создаем директорию для базы данных, если ее нет
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # Подключаемся к базе данных
    conn = sqlite3.connect(DB_PATH)

    # Выполняем скрипт инициализации схемы
    with open(SCHEMA_PATH, 'r') as schema_file:
        conn.executescript(schema_file.read())

    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()