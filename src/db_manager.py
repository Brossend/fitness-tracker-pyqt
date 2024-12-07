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

    def authenticate_user(self, email, password):
        self.cursor.execute(
            """
            SELECT id, name FROM Users WHERE email = ? AND password = ?
            """,
            (email, password)
        )
        user = self.cursor.fetchone()
        if user:
            return {"id": user[0], "name": user[1]}
        return None

    def close(self):
        self.connection.close()
