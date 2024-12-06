CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE Goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    goal_name TEXT NOT NULL,
    target_value REAL NOT NULL,
    current_value REAL DEFAULT 0,
    deadline DATE,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TABLE Workouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    workout_type TEXT NOT NULL,
    duration INTEGER,
    calories_burned REAL,
    date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);
