from lab_app.http_client import http_request


def lookup_user_signal(name: str):
    url = f"http://example.com/?user={name}"
    result = http_request("GET", url)
    return {
        "service": "directory",
        "queried_name": name,
        "remote_ok": result["ok"],
        "status": result["status"],
    }
