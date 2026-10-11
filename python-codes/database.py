import sqlite3
from pathlib import Path
from datetime import datetime

DATABASE_FILE = Path(__file__).resolve().parent / "typing_history.db"


def get_connection():
    return sqlite3.connect(DATABASE_FILE)


def create_tables():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS typing_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wpm REAL NOT NULL,
                accuracy REAL NOT NULL,
                mistakes INTEGER NOT NULL,
                difficulty TEXT NOT NULL,
                duration INTEGER NOT NULL,
                date TEXT NOT NULL
            )
        """)


def save_result(wpm, accuracy, mistakes, difficulty, duration):
    test_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as connection:
        connection.execute("""
            INSERT INTO typing_results
            (wpm, accuracy, mistakes, difficulty, duration, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            round(wpm, 2),
            round(accuracy, 2),
            mistakes,
            difficulty,
            duration,
            test_date
        ))


def get_history(limit=50):
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT id, wpm, accuracy, mistakes, difficulty, duration, date
            FROM typing_results
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))

        return cursor.fetchall()


def get_personal_best():
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT wpm, accuracy, difficulty, date
            FROM typing_results
            ORDER BY wpm DESC
            LIMIT 1
        """)

        return cursor.fetchone()


def get_total_tests():
    with get_connection() as connection:
        cursor = connection.execute(
            "SELECT COUNT(*) FROM typing_results"
        )

        return cursor.fetchone()[0]


def get_average_wpm():
    with get_connection() as connection:
        cursor = connection.execute(
            "SELECT AVG(wpm) FROM typing_results"
        )

        result = cursor.fetchone()[0]
        return round(result, 2) if result is not None else 0


def clear_history():
    with get_connection() as connection:
        connection.execute("DELETE FROM typing_results")
