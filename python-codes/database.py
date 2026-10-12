import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).with_name("typing_test.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():
    """Create the test history table if it does not already exist."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_date TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                duration INTEGER NOT NULL,
                wpm REAL NOT NULL,
                raw_wpm REAL NOT NULL,
                accuracy REAL NOT NULL,
                correct_chars INTEGER NOT NULL,
                incorrect_chars INTEGER NOT NULL,
                typed_chars INTEGER NOT NULL
            )
        """)


def save_result(result):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO test_results (
                test_date, difficulty, duration, wpm, raw_wpm,
                accuracy, correct_chars, incorrect_chars, typed_chars
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            result["difficulty"],
            result["duration"],
            result["wpm"],
            result["raw_wpm"],
            result["accuracy"],
            result["correct_chars"],
            result["incorrect_chars"],
            result["typed_chars"]
        ))


def get_history(limit=100):
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT id, test_date, difficulty, duration, wpm, accuracy,
                   incorrect_chars
            FROM test_results
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()
    return rows


def get_statistics():
    with get_connection() as connection:
        row = connection.execute("""
            SELECT COUNT(*), COALESCE(MAX(wpm), 0),
                   COALESCE(AVG(wpm), 0), COALESCE(AVG(accuracy), 0)
            FROM test_results
        """).fetchone()
    return {
        "total_tests": row[0],
        "personal_best": round(row[1], 1),
        "average_wpm": round(row[2], 1),
        "average_accuracy": round(row[3], 1)
    }


def get_recent_progress(limit=10):
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT test_date, wpm, accuracy
            FROM (
                SELECT id, test_date, wpm, accuracy
                FROM test_results
                ORDER BY id DESC
                LIMIT ?
            )
            ORDER BY id ASC
        """, (limit,)).fetchall()
    return rows


def clear_history():
    with get_connection() as connection:
        connection.execute("DELETE FROM test_results")
