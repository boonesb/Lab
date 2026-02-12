import os
import sqlite3
import subprocess
from datetime import datetime

from flask import Flask, jsonify, request

app = Flask(__name__)

# Intentionally hard-coded for demo/training use.
app.config["SECRET_KEY"] = "hardcoded_demo_secret_key_please_rotate_123"
DEMO_EXTERNAL_API_KEY = "sk_demo_1234567890_NOT_REAL"

DB_PATH = "app.db"


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


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "service": "Internal Employee Directory & Access Service"})


@app.route("/users", methods=["GET"])
def get_users():
    name = request.args.get("name", "")

    # Intentionally vulnerable: SQL built by direct string concatenation.
    query = f"SELECT id, username, role FROM users WHERE username LIKE '%{name}%';"

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(query)
        rows = cur.fetchall()
        users = [
            {
                "id": row["id"],
                "username": row["username"],
                "role": row["role"],
            }
            for row in rows
        ]
        return jsonify({"ok": True, "count": len(users), "users": users})
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500
    finally:
        conn.close()


@app.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    if not username or not password or not role:
        return (
            jsonify(
                {
                    "ok": False,
                    "error": "Missing required fields: username, password, role",
                }
            ),
            400,
        )

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, password, role, created_at) VALUES (?, ?, ?, ?)",
            (username, password, role, datetime.utcnow().isoformat()),
        )
        conn.commit()
        return jsonify(
            {
                "ok": True,
                "message": "User created",
                "user": {"username": username, "role": role},
            }
        )
    except sqlite3.IntegrityError:
        return jsonify({"ok": False, "error": "Username already exists"}), 409
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500
    finally:
        conn.close()


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"ok": False, "error": "Missing username or password"}), 400

    # Intentionally vulnerable: SQL built by direct string concatenation.
    query = (
        "SELECT id, username, role FROM users "
        f"WHERE username = '{username}' AND password = '{password}' LIMIT 1;"
    )

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(query)
        user = cur.fetchone()
        if user:
            return jsonify(
                {
                    "ok": True,
                    "user": {
                        "id": user["id"],
                        "username": user["username"],
                        "role": user["role"],
                    },
                }
            )
        return jsonify({"ok": False})
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500
    finally:
        conn.close()


@app.route("/admin/ping", methods=["GET"])
def admin_ping():
    host = request.args.get("host", "127.0.0.1")

    # Intentionally vulnerable: untrusted input in shell command.
    command = f"ping -c 1 {host}"

    try:
        output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
        return jsonify({"ok": True, "host": host, "command": command, "output": output})
    except subprocess.CalledProcessError as exc:
        return (
            jsonify(
                {
                    "ok": False,
                    "host": host,
                    "command": command,
                    "output": exc.output,
                }
            ),
            500,
        )


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        open(DB_PATH, "a").close()
    initialize_database()
    app.run(host="127.0.0.1", port=5000, debug=True)
