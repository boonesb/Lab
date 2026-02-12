import sqlite3
from datetime import datetime

from .config import DB_PATH


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    cur.execute("SELECT COUNT(*) AS total FROM users")
    count = cur.fetchone()["total"]

    if count == 0:
        now = datetime.utcnow().isoformat()
        seed_users = [
            ("admin", "adminpass", "admin", now),
            ("user", "userpass", "user", now),
        ]
        cur.executemany(
            "INSERT INTO users (username, password, role, created_at) VALUES (?, ?, ?, ?)",
            seed_users,
        )

    conn.commit()
    conn.close()
