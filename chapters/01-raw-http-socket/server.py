import socket

HOST = "127.0.0.1"
PORT = 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Bound to {HOST}:{PORT}")
print(f"Listening on http://{HOST}:{PORT}")

client_socket, client_address = server_socket.accept()
print(f"Accepted connection from {client_address}")
