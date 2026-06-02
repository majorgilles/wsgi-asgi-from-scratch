# Chapter 01: Raw HTTP over sockets

## Goal

Build a minimal blocking HTTP server that shows the path from a client connection to request bytes and back to an HTTP response.

For the line-by-line learning notes, see [NOTES.md](NOTES.md).

## Runnable command

Start the server:

```bash
python chapters/01-raw-http-socket/server.py
```

From another terminal, send one request:

```bash
curl -i http://127.0.0.1:8000/
```

You should see a `200 OK` response in `curl`, and the server terminal should print the client address and request line.

## Stopping the server

The server runs in a `while True` loop, so the terminal running it belongs to the Python process until you stop it. After handling one request, seeing `Waiting for a client connection...` again means the server is working and waiting for the next client connection.

In a normal terminal, stop it with:

```text
Ctrl-C
```

In a Neovim `:terminal` split, make sure the terminal buffer is in input mode first:

```text
i
Ctrl-C
```

If the server still does not stop, kill the process listening on port `8000` from another terminal:

```bash
kill $(lsof -ti tcp:8000)
```

## Flow trace / diagram

```text
curl/browser
  -> connects to 127.0.0.1:8000
  -> Python server socket accepts the connection
  -> recv() reads raw HTTP request bytes
  -> server prints the request line and client address
  -> sendall() writes raw HTTP response bytes
  -> client displays the response
```

## Walkthrough

1. `socket.socket()` creates a network endpoint for the server process.
2. `bind()` attaches that socket to `127.0.0.1:8000`.
3. `listen()` marks it as a server socket that can wait for clients.
4. `accept()` blocks until one client connects, then returns a connection socket and client address.
5. `recv()` reads bytes from that client connection.
6. `sendall()` writes a complete HTTP response back to the client.

## Exercise

Change the response body based on the request path. For example, return one body for `/` and another body for `/hello`.

## Source links

- Ruslan Spivak, *Let's Build A Web Server. Part 1*: https://ruslanspivak.com/lsbaws-part1/
- Python `socket` docs: https://docs.python.org/3/library/socket.html

## What we simplified

- Parses only enough HTTP to see the request line.
- Handles one request at a time.
- Does not support TLS.
- Does not support keep-alive or connection reuse.
- Does not implement concurrency.
- Ignores malformed requests and most headers.
