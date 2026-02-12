from lab_app.http_client import http_request


def record_admin_action(host: str):
    url = f"http://example.com/audit?host={host}"
    result = http_request("GET", url)
    return {
        "service": "audit",
        "target_host": host,
        "remote_ok": result["ok"],
        "status": result["status"],
    }
