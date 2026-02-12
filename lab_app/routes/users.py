import sqlite3
from datetime import datetime

from flask import Blueprint, jsonify, request

from ..db import get_connection
from ..services import lookup_user_signal

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["GET"])
def get_users():
    name = request.args.get("name", "")

    try:
        lookup_user_signal(name)
    except Exception:
        pass

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


@users_bp.route("/create-user", methods=["POST"])
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
