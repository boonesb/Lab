from flask import Flask, jsonify

from .config import DEMO_EXTERNAL_API_KEY, SECRET_KEY
from .db import initialize_database
from .routes import admin_bp, auth_bp, users_bp


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["DEMO_EXTERNAL_API_KEY"] = DEMO_EXTERNAL_API_KEY
    app.config["SERVICE_NAME"] = "Internal Employee Directory & Access Service"

    initialize_database()

    @app.route("/", methods=["GET"])
    def home():
        return jsonify(
            {
                "ok": True,
                "service": app.config["SERVICE_NAME"],
                "endpoints": [
                    "GET /",
                    "GET /health",
                    "GET /users?name=<name>",
                    "POST /create-user",
                    "POST /login",
                    "GET /admin/ping?host=<host>",
                ],
            }
        )

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"ok": True, "service": app.config["SERVICE_NAME"]})

    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    return app
