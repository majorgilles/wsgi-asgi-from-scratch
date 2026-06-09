from collections.abc import Callable, Iterable
import io
from typing import cast, TypeAlias

Environ: TypeAlias = dict[str, object]
Headers: TypeAlias = list[tuple[str, str]]
StartResponse: TypeAlias = Callable[[str, Headers], None]
ResponseBody: TypeAlias = Iterable[bytes]


def app(environ: Environ, start_response: StartResponse) -> ResponseBody:
    status: str = "200 OK"
    headers: Headers = [("Content-Type", "text/plain; charset=utf-8")]

    if environ.get("PATH_INFO") != "/echo":
        start_response(status, headers)
        return [b"Hello, WSGI"]

    body_stream: io.BytesIO = cast(io.BytesIO, environ["wsgi.input"])
    body_bytes: bytes = body_stream.read()
    body_text: str = body_bytes.decode("utf-8")

    response_text: str = "\n".join(
        [
            f"method={environ.get('REQUEST_METHOD', '')}",
            f"path={environ.get('PATH_INFO', '')}",
            f"query={environ.get('QUERY_STRING', '')}",
            f"host={environ.get('HTTP_HOST', '')}",
            f"body={body_text}",
        ]
    )

    start_response(status, headers)
    return [(response_text + "\n").encode("utf-8")]
