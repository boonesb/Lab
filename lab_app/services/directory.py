import urllib3
from urllib3.util import Retry, Timeout


_retry = Retry(
    total=2,
    backoff_factor=0.1,
    status_forcelist=[500, 502, 503, 504],
    method_whitelist=frozenset(["GET", "POST"]),
)

_http = urllib3.PoolManager(retries=_retry)


def lookup_user_signal(name: str):
    url = f"http://example.com/?user={name}"
    timeout = Timeout(connect=1.0, read=2.0)

    try:
        response = _http.request("GET", url, timeout=timeout)
        return {
            "service": "directory",
            "queried_name": name,
            "remote_ok": True,
            "status": response.status,
        }
    except Exception as exc:
        return {
            "service": "directory",
            "queried_name": name,
            "remote_ok": False,
            "status": None,
            "error": str(exc),
        }
