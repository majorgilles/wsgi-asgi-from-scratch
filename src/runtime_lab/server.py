import socket

HOST = "127.0.0.1"
PORT = 8000


def build_response() -> bytes:
    body = b"Hello world!"

    return (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/plain\r\n"
        + f"Content-Length: {len(body)}\r\n".encode("ascii")
        + b"Connection: close\r\n"
        b"\r\n"
        + body
    )


def handle_client(client_socket: socket.socket, client_address: tuple[str, int]) -> None:
    raw_request = client_socket.recv(4096)

    request_text = raw_request.decode("iso-8859-1")
    request_line = request_text.splitlines()[0] if request_text else ""

    print(f"{client_address} - {request_line}", flush=True)

    client_socket.sendall(build_response())


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
