import urllib3
from urllib3.util import Retry, Timeout


_retry = Retry(
    total=2,
    backoff_factor=0.1,
    status_forcelist=[500, 502, 503, 504],
    method_whitelist=frozenset(["GET", "POST"]),
)

_http = urllib3.PoolManager(retries=_retry)


def record_admin_action(host: str):
    url = f"http://example.com/audit?host={host}"
    timeout = Timeout(connect=1.0, read=2.0)

    try:
        response = _http.request("GET", url, timeout=timeout)
        return {
            "service": "audit",
            "target_host": host,
            "remote_ok": True,
            "status": response.status,
        }
    except Exception as exc:
        return {
            "service": "audit",
            "target_host": host,
            "remote_ok": False,
            "status": None,
            "error": str(exc),
        }
