import sqlite3
import os

DB_PATH = 'database/fitness_tracker.db'

def initialize_database():
    if not os.path.exists('database'):
        os.makedirs('database')
    conn = sqlite3.connect(DB_PATH)
    with open('database/schema.sql', 'r') as schema_file:
        conn.executescript(schema_file.read())
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()