import subprocess

from flask import Blueprint, current_app, jsonify, request

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/ping", methods=["GET"])
def admin_ping():
    host = request.args.get("host", "127.0.0.1")

    # Intentionally vulnerable: untrusted input in shell command.
    command = f"ping -c 1 {host}"

    try:
        output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
        return jsonify(
            {
                "ok": True,
                "host": host,
                "command": command,
                "output": output,
                "service": current_app.config.get("SERVICE_NAME"),
            }
        )
    except subprocess.CalledProcessError as exc:
        return (
            jsonify(
                {
                    "ok": False,
                    "host": host,
                    "command": command,
                    "output": exc.output,
                    "service": current_app.config.get("SERVICE_NAME"),
                }
            ),
            500,
        )
