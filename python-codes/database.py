
import sqlite3
from datetime import datetime

DATABASE_NAME = "typeflow.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wpm REAL NOT NULL,
                raw_wpm REAL DEFAULT 0,
                accuracy REAL NOT NULL,
                mistakes INTEGER DEFAULT 0,
                correct_chars INTEGER DEFAULT 0,
                total_chars INTEGER DEFAULT 0,
                duration INTEGER DEFAULT 0,
                difficulty TEXT DEFAULT 'Easy',
                mode TEXT DEFAULT 'Timed',
                date TEXT NOT NULL
            )
        """)

        # Add newer columns if an older TypeFlow database is used.
        existing_columns = {
            row[1]
            for row in connection.execute(
                "PRAGMA table_info(test_results)"
            ).fetchall()
        }

        additions = {
            "raw_wpm": "REAL DEFAULT 0",
            "correct_chars": "INTEGER DEFAULT 0",
            "total_chars": "INTEGER DEFAULT 0",
            "duration": "INTEGER DEFAULT 0",
            "difficulty": "TEXT DEFAULT 'Easy'",
            "mode": "TEXT DEFAULT 'Timed'"
        }

        for column, definition in additions.items():
            if column not in existing_columns:
                connection.execute(
                    f"ALTER TABLE test_results ADD COLUMN {column} {definition}"
                )


def save_result(
    wpm,
    accuracy,
    mistakes,
    duration=0,
    difficulty="Easy",
    mode="Timed",
    raw_wpm=0,
    correct_chars=0,
    total_chars=0
):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO test_results (
                wpm, raw_wpm, accuracy, mistakes,
                correct_chars, total_chars, duration,
                difficulty, mode, date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            wpm,
            raw_wpm,
            accuracy,
            mistakes,
            correct_chars,
            total_chars,
            duration,
            difficulty,
            mode,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))


def get_history(limit=None):
    with get_connection() as connection:
        if limit is None:
            rows = connection.execute("""
                SELECT id, wpm, accuracy, mistakes, date,
                       raw_wpm, correct_chars, total_chars,
                       duration, difficulty, mode
                FROM test_results
                ORDER BY id DESC
            """).fetchall()
        else:
            rows = connection.execute("""
                SELECT id, wpm, accuracy, mistakes, date,
                       raw_wpm, correct_chars, total_chars,
                       duration, difficulty, mode
                FROM test_results
                ORDER BY id DESC
                LIMIT ?
            """, (limit,)).fetchall()

    return [
        {
            "id": row[0],
            "wpm": row[1],
            "accuracy": row[2],
            "mistakes": row[3],
            "date": row[4],
            "raw_wpm": row[5],
            "correct_chars": row[6],
            "total_chars": row[7],
            "duration": row[8],
            "difficulty": row[9],
            "mode": row[10]
        }
        for row in rows
    ]


def get_personal_best():
    with get_connection() as connection:
        row = connection.execute(
            "SELECT MAX(wpm) FROM test_results"
        ).fetchone()

    return row[0] or 0


def get_total_tests():
    with get_connection() as connection:
        row = connection.execute(
            "SELECT COUNT(*) FROM test_results"
        ).fetchone()

    return row[0]


def get_average_wpm():
    with get_connection() as connection:
        row = connection.execute(
            "SELECT AVG(wpm) FROM test_results"
        ).fetchone()

    return row[0] or 0


def get_average_accuracy():
    with get_connection() as connection:
        row = connection.execute(
            "SELECT AVG(accuracy) FROM test_results"
        ).fetchone()

    return row[0] or 0


def get_total_mistakes():
    with get_connection() as connection:
        row = connection.execute(
            "SELECT SUM(mistakes) FROM test_results"
        ).fetchone()

    return row[0] or 0


def get_recent_average_wpm(count=5):
    history = get_history(limit=count)

    if not history:
        return 0

    return sum(item["wpm"] for item in history) / len(history)


def get_progress_data():
    history = get_history(limit=20)
    history.reverse()

    return {
        "labels": [
            item["date"][5:16] for item in history
        ],
        "wpm": [
            item["wpm"] for item in history
        ],
        "accuracy": [
            item["accuracy"] for item in history
        ]
    }
