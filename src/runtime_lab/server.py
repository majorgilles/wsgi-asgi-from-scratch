import socket
import io
import sys
from runtime_lab.app import Environ, Headers, app

HOST = "127.0.0.1"
PORT = 8000


def build_environ(request_line: str) -> Environ:
    method, path, protocol = request_line.split()

    return {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "SERVER_PROTOCOL": protocol,
        "wsgi.version": (1, 0),
        "wsgi.url_scheme": "http",
        "wsgi.multithread": False,
        "wsgi.multiprocess": False,
        "wsgi.run_once": False,
        "wsgi.input": io.BytesIO(),  # No request body in this simple server
        "wsgi.errors": sys.stderr,
    }


def build_response(status: str, headers: Headers, body: bytes) -> bytes:
    response_headers = headers + [
        ("Content-Length", str(len(body))),
        ("Connection", "close"),
    ]

    header_bytes = b"".join(
        f"{name}: {value}\r\n".encode("ascii") for name, value in response_headers
    )

    return f"HTTP/1.1 {status}\r\n".encode("ascii") + header_bytes + b"\r\n" + body


def handle_client(
    client_socket: socket.socket, client_address: tuple[str, int]
) -> None:
    raw_request = client_socket.recv(4096)

    request_text = raw_request.decode("iso-8859-1")
    request_line = request_text.splitlines()[0] if request_text else ""

    print(f"{client_address} - {request_line}", flush=True)

    captured_status = ""
    captured_headers: Headers = []

    def start_response(status: str, headers: Headers) -> None:
        # This callback runs inside app(), but handle_client() needs these
        # values after app() returns. nonlocal makes the assignments below
        # update the variables above instead of creating new local variables.
        nonlocal captured_status, captured_headers
        captured_status = status
        captured_headers = headers

    environ = build_environ(request_line)
    body_chunks = app(environ, start_response)
    body = b"".join(body_chunks)

    client_socket.sendall(build_response(captured_status, captured_headers, body))


def serve_forever() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f"Listening on http://{HOST}:{PORT}", flush=True)

        try:
            while True:
                print("Waiting for a client connection...", flush=True)
                client_socket, client_address = server_socket.accept()

                with client_socket:
                    handle_client(client_socket, client_address)
        except KeyboardInterrupt:
            print("\nShutting down server", flush=True)


def main() -> int:
    serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
