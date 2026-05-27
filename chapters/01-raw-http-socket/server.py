from __future__ import annotations

import socket

HOST = "127.0.0.1"
PORT = 8000
RESPONSE_BODY = b"Hello from a raw socket HTTP server!\n"


def build_response() -> bytes:
    headers = [
        b"HTTP/1.1 200 OK",
        b"Content-Type: text/plain; charset=utf-8",
        f"Content-Length: {len(RESPONSE_BODY)}".encode("ascii"),
        b"Connection: close",
    ]
    return b"\r\n".join(headers) + b"\r\n\r\n" + RESPONSE_BODY


def request_line_from(raw_request: bytes) -> str:
    first_line = raw_request.splitlines()[0] if raw_request else b""
    return first_line.decode("iso-8859-1", errors="replace")


def serve_forever(host: str = HOST, port: int = PORT) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen()

        print(f"Serving on http://{host}:{port}/", flush=True)
        print("Press Ctrl+C to stop.", flush=True)

        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                raw_request = client_socket.recv(4096)
                print(f"{client_address}: {request_line_from(raw_request)}", flush=True)
                client_socket.sendall(build_response())


if __name__ == "__main__":
    serve_forever()
