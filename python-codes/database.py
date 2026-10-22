import sqlite3
from datetime import date
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "typeflow.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wpm REAL NOT NULL,
                accuracy REAL NOT NULL,
                mistakes INTEGER NOT NULL,
                duration INTEGER NOT NULL,
                difficulty TEXT NOT NULL,
                characters INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)

        conn.execute("""
            INSERT OR IGNORE INTO settings (key, value)
            VALUES ('daily_goal', '3')
        """)


def save_result(wpm, accuracy, mistakes, duration,
                difficulty, characters):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO results
            (wpm, accuracy, mistakes, duration,
             difficulty, characters, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            round(wpm, 2),
            round(accuracy, 2),
            mistakes,
            duration,
            difficulty,
            characters,
            date.today().isoformat()
        ))


def get_results(search=""):
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row

        if search.strip():
            return [
                dict(row) for row in conn.execute("""
                    SELECT * FROM results
                    WHERE difficulty LIKE ?
                       OR created_at LIKE ?
                    ORDER BY id DESC
                """, (
                    f"%{search.strip()}%",
                    f"%{search.strip()}%"
                )).fetchall()
            ]

        return [
            dict(row) for row in conn.execute("""
                SELECT * FROM results
                ORDER BY id DESC
            """).fetchall()
        ]


def get_setting(key, default=""):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT value FROM settings WHERE key = ?",
            (key,)
        ).fetchone()

    return row[0] if row else default


def set_setting(key, value):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO settings (key, value)
            VALUES (?, ?)
            ON CONFLICT(key)
            DO UPDATE SET value = excluded.value
        """, (key, str(value)))


def get_today_count():
    with get_connection() as conn:
        row = conn.execute("""
            SELECT COUNT(*) FROM results
            WHERE created_at = ?
        """, (date.today().isoformat(),)).fetchone()

    return row[0]


def delete_result(result_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM results WHERE id = ?",
            (result_id,)
        )


def clear_results():
    with get_connection() as conn:
        conn.execute("DELETE FROM results")
