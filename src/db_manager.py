import sqlite3

DB_PATH = 'database/fitness_tracker.db'

class DatabaseManager:
    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()

    def add_user(self, name, email, password):
        try:
            self.cursor.execute(
                """
                INSERT INTO Users (name, email, password)
                VALUES (?, ?, ?)
                """,
                (name, email, password)
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def close(self):
        self.connection.close()
