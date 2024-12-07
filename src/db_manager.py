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

    def get_goals(self, user_id):
        self.cursor.execute(
            """
            SELECT goal_name, current_value, target_value
            FROM Goals
            WHERE user_id = ?
            """,
            (user_id,)
        )
        rows = self.cursor.fetchall()
        return [
            {"goal_name": row[0], "current_value": row[1], "target_value": row[2]}
            for row in rows
        ]

    def add_goal(self, user_id, goal_name, target_value):
        self.cursor.execute(
            """
            INSERT INTO Goals (user_id, goal_name, target_value)
            VALUES (?, ?, ?)
            """,
            (user_id, goal_name, target_value)
        )
        self.connection.commit()

    def close(self):
        self.connection.close()
