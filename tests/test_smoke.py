import io
import sys
from pathlib import Path

import runtime_lab
from runtime_lab.app import app
from runtime_lab.server import build_environ, build_response


def test_runtime_lab_package_imports() -> None:
    assert runtime_lab.__version__ == "0.1.0"


def test_expected_project_scaffold_exists() -> None:
    root = Path(__file__).resolve().parents[1]

    assert (root / "README.md").is_file()
    assert (root / "pyproject.toml").is_file()
    assert not (root / "chapters").exists()
    assert (root / "src" / "runtime_lab").is_dir()
    assert (root / "src" / "runtime_lab" / "server.py").is_file()
    assert (root / "tests").is_dir()
    assert (root / "scripts").is_dir()


def test_runtime_code_lives_under_src_package() -> None:
    root = Path(__file__).resolve().parents[1]

    assert (root / "src" / "runtime_lab" / "server.py").is_file()
    assert not (root / "server.py").exists()


def test_build_environ_extracts_request_line_parts() -> None:
    environ = build_environ("GET /hello HTTP/1.1")

    assert environ["REQUEST_METHOD"] == "GET"
    assert environ["PATH_INFO"] == "/hello"
    assert environ["SERVER_PROTOCOL"] == "HTTP/1.1"
    assert environ["wsgi.version"] == (1, 0)
    assert environ["wsgi.url_scheme"] == "http"
    assert environ["wsgi.multithread"] is False
    assert environ["wsgi.multiprocess"] is False
    assert environ["wsgi.run_once"] is False

    wsgi_input: object = environ["wsgi.input"]
    assert isinstance(wsgi_input, io.BytesIO)
    assert wsgi_input.read() == b""
    assert environ["wsgi.errors"] is sys.stderr


def test_build_response_includes_status_headers_and_body() -> None:
    response = build_response(
        "200 OK",
        [("Content-Type", "text/plain")],
        b"Hello, WSGI",
    )

    assert response.startswith(b"HTTP/1.1 200 OK\r\n")
    assert b"Content-Type: text/plain\r\n" in response
    assert b"Content-Length: 11\r\n" in response
    assert response.endswith(b"\r\n\r\nHello, WSGI")


def test_wsgi_app_sets_status_headers_and_body() -> None:
    captured_status = ""
    captured_headers: list[tuple[str, str]] = []

    def start_response(status: str, headers: list[tuple[str, str]]) -> None:
        # The fake callback is nested inside this test. nonlocal lets it update
        # the outer variables so the assertions can inspect what the app sent.
        nonlocal captured_status, captured_headers
        captured_status = status
        captured_headers = headers

    body = list(app({}, start_response))

    assert captured_status == "200 OK"
    assert captured_headers == [("Content-Type", "text/plain")]
    assert body == [b"Hello, WSGI"]
