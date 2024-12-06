import sqlite3

def initialize_database():
    conn = sqlite3.connect('database/fitness_tracker.db')
    with open('database/schema.sql', 'r') as schema_file:
        conn.executescript(schema_file.read())
    conn.close()
    print("Database initialized successfully!")