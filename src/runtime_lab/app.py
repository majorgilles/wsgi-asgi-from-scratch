from collections.abc import Callable, Iterable
from typing import TypeAlias

Environ: TypeAlias = dict[str, object]
Headers: TypeAlias = list[tuple[str, str]]
StartResponse: TypeAlias = Callable[[str, Headers], None]
ResponseBody: TypeAlias = Iterable[bytes]


def app(environ: Environ, start_response: StartResponse) -> ResponseBody:
    status: str = "200 OK"
    headers: Headers = [("Content-Type", "text/plain")]
    start_response(status, headers)

    return [b"Hello, WSGI"]
