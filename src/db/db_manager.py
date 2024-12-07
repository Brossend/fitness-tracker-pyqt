import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '../../database/fitness_tracker.db')

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

            return self.authenticate_user(name, password)
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

    def update_password(self, user_id, new_password):
        self.cursor.execute(
            """
            UPDATE Users
            SET password = ?
            WHERE id = ?;
            """,
            (new_password, user_id)
        )
        self.connection.commit()

    def delete_user(self, user_id):
        self.cursor.execute(
            """
            DELETE FROM Users
            WHERE id = ?;
            """,
            (user_id,)
        )
        self.connection.commit()

    def update_user_details(self, user_id, new_name, new_email):
        self.cursor.execute(
            """
            UPDATE Users
            SET name = ?, email = ?
            WHERE id = ?;
            """,
            (new_name, new_email, user_id)
        )
        self.connection.commit()

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

    def get_goal_id(self, user_id, goal_name):
        self.cursor.execute(
            """
            SELECT id FROM Goals
            WHERE user_id = ? AND goal_name = ?;
            """,
            (user_id, goal_name)
        )
        result = self.cursor.fetchone()
        return result[0] if result else None

    def update_goal(self, goal_id, new_name, new_target_value):
        self.cursor.execute(
            """
            UPDATE Goals
            SET goal_name = ?, target_value = ?
            WHERE id = ?;
            """,
            (new_name, new_target_value, goal_id)
        )
        self.connection.commit()

    def delete_goal(self, goal_id):
        self.cursor.execute(
            """
            DELETE FROM Goals
            WHERE id = ?;
            """,
            (goal_id,)
        )
        self.connection.commit()

    def get_progress(self, user_id):
        self.cursor.execute(
            """
            SELECT activity_date, steps, calories_burned
            FROM ActivityLog
            WHERE user_id = ?
            ORDER BY activity_date ASC
            """,
            (user_id,)
        )
        rows = self.cursor.fetchall()
        return [
            {"date": row[0], "steps": row[1], "calories": row[2]}
            for row in rows
        ]

    def get_activities(self, user_id):
        self.cursor.execute(
            """
            SELECT id, activity_date, steps, calories_burned
            FROM ActivityLog
            WHERE user_id = ?
            ORDER BY activity_date DESC;
            """,
            (user_id,)
        )
        rows = self.cursor.fetchall()
        return [
            {"id": row[0], "date": row[1], "steps": row[2], "calories": row[3]}
            for row in rows
        ]

    def get_activity_id(self, user_id, date):
        self.cursor.execute(
            """
            SELECT id FROM ActivityLog
            WHERE user_id = ? AND activity_date = ?;
            """,
            (user_id, date)
        )
        result = self.cursor.fetchone()
        return result[0] if result else None

    def update_activity(self, activity_id, new_date, new_steps, new_calories):
        self.cursor.execute(
            """
            UPDATE ActivityLog
            SET activity_date = ?, steps = ?, calories_burned = ?
            WHERE id = ?;
            """,
            (new_date, new_steps, new_calories, activity_id)
        )
        self.connection.commit()

    def delete_activity(self, activity_id):
        self.cursor.execute(
            """
            DELETE FROM ActivityLog
            WHERE id = ?;
            """,
            (activity_id,)
        )
        self.connection.commit()

    def add_activity(self, user_id, date, steps, calories):
        self.cursor.execute(
            """
            INSERT INTO ActivityLog (user_id, activity_date, steps, calories_burned)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, date, steps, calories)
        )
        self.connection.commit()

    def close(self):
        self.connection.close()

    def get_analytics(self, user_id):
        self.cursor.execute(
            """
            SELECT AVG(steps), AVG(calories_burned)
            FROM ActivityLog
            WHERE user_id = ? AND activity_date >= DATE('now', '-7 days')
            """,
            (user_id,)
        )
        avg_steps, avg_calories = self.cursor.fetchone()

        self.cursor.execute(
            """
            SELECT activity_date, steps
            FROM ActivityLog
            WHERE user_id = ?
            ORDER BY steps DESC
            LIMIT 1
            """,
            (user_id,)
        )
        best_day = self.cursor.fetchone()

        return {
            "avg_steps": int(avg_steps) if avg_steps else 0,
            "avg_calories": int(avg_calories) if avg_calories else 0,
            "best_day": {"date": best_day[0], "steps": best_day[1]} if best_day else {"date": "-", "steps": 0}
        }
