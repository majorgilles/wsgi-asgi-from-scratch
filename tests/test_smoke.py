from pathlib import Path

import runtime_lab
from runtime_lab.server import build_response


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


def test_build_response_includes_status_headers_and_body() -> None:
    response = build_response()

    assert response.startswith(b"HTTP/1.1 200 OK\r\n")
    assert b"Content-Type: text/plain\r\n" in response
    assert b"Content-Length: 12\r\n" in response
    assert response.endswith(b"\r\n\r\nHello world!")
