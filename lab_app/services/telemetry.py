from lab_app.http_client import http_request


def track_login_attempt(username: str):
    url = f"http://example.com/login-attempt?username={username}"
    result = http_request("GET", url)
    return {
        "service": "telemetry",
        "username": username,
        "remote_ok": result["ok"],
        "status": result["status"],
    }
