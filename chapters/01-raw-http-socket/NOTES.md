# Notes: Raw HTTP over sockets

These are the discoveries from building the server by hand.

## Mental model

A socket is one endpoint of a network conversation.

For this chapter, the server has two kinds of sockets:

```text
server socket
  waits at 127.0.0.1:8000 for new clients

client connection socket
  represents one accepted client conversation
```

The server socket is like a front desk. The client connection socket is like the private conversation after the front desk picks up.

## Address choice

We use:

```python
HOST = "127.0.0.1"
PORT = 8000
```

`127.0.0.1` means this same computer using IPv4.

`localhost` can often work, but it is a hostname that must be resolved to an address. Depending on the machine, it may resolve to IPv4 (`127.0.0.1`) or IPv6 (`::1`). Since this chapter uses `socket.AF_INET`, which means IPv4, `127.0.0.1` is the more explicit match.

## Creating the socket

```python
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

Read this as:

```text
Create a TCP socket that uses IPv4 addresses.
```

- `AF_INET` means IPv4.
- `SOCK_STREAM` means TCP: a reliable stream of bytes.

## Binding

```python
server_socket.bind((HOST, PORT))
```

`bind()` gives the socket an address.

The address is the pair:

```python
("127.0.0.1", 8000)
```

The host says which machine/interface to use. The port is the numbered doorway on that host.

## Listening

```python
server_socket.listen()
```

`listen()` tells the operating system to treat this bound socket as a server socket.

After this, the socket is ready to receive connection attempts, but it has not accepted a client yet.

## Accepting a connection

```python
client_socket, client_address = server_socket.accept()
```

`accept()` is a blocking call. That means the Python program pauses on this line until a client connects.

If the terminal prints something like this and then appears stuck:

```text
Listening on http://127.0.0.1:8000
```

that is expected. The server is waiting inside `accept()`.

A useful debugging trick is to print before and after a blocking call:

```python
print("Before accept()")
client_socket, client_address = server_socket.accept()
print("After accept()")
```

If `Before accept()` prints but `After accept()` does not, the server is still waiting for a client connection.

## Connection first, HTTP bytes second

A client like `curl` does two separate things:

```text
1. Open a TCP connection to 127.0.0.1:8000
2. Send HTTP request bytes through that connection
```

`accept()` handles step 1. It does not read the HTTP request.

The next operation, `recv()`, handles step 2:

```python
raw_request = client_socket.recv(4096)
```

`recv()` is also a blocking call. It waits for bytes from an already-connected client.

## Current flow

```text
Python program starts
  -> create IPv4/TCP socket
  -> bind it to 127.0.0.1:8000
  -> mark it as listening
  -> block at accept() until a client connects
  -> receive a new client_socket for that one conversation
```

## Key distinction

```text
accept() waits for a connection
recv() waits for data on that connection
```
