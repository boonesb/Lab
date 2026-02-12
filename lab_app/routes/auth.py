from flask import Blueprint, jsonify, request

from ..db import get_connection

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
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
