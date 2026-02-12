import urllib3
from urllib3.util import Retry, Timeout


_retry = Retry(
    total=2,
    backoff_factor=0.1,
    status_forcelist=[500, 502, 503, 504],
    method_whitelist=frozenset(["GET", "POST"]),
)

_http = urllib3.PoolManager(retries=_retry)


def http_request(method: str, url: str):
    timeout = Timeout(connect=1.0, read=2.0)

    try:
        response = _http.request(method=method, url=url, timeout=timeout)
        body = response.data.decode("utf-8", errors="replace")
        return {
            "ok": True,
            "status": response.status,
            "body_snippet": body[:120],
        }
    except Exception as exc:
        return {
            "ok": False,
            "status": None,
            "body_snippet": "",
            "error": str(exc),
        }
