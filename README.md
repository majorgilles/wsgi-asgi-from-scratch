# WSGI to ASGI From Scratch

A source-backed, code-first tutorial project for Python backend developers who know web frameworks but want to understand the runtime internals underneath them.

We build one tiny educational web runtime through 30–60 minute learning milestones:

1. Raw HTTP over sockets
2. WSGI from scratch
3. WSGI request lifecycle
4. Middleware and tiny routing
5. Threaded WSGI concurrency
6. Gunicorn-style worker mental models
7. Asyncio event loop fundamentals
8. Bare ASGI applications
9. A tiny ASGI HTTP server
10. Streaming and backpressure concepts
11. ASGI lifespan
12. Sync/async interop with thread pools
13. Production mapping: Flask, Django, FastAPI, Starlette, Gunicorn, Uvicorn, Hypercorn
14. Capstone failure lab

This is not a production web server. It is a spec-aware educational mini-server designed to make the contracts explicit.

## Learning goals

By the end, you should understand:

- What a WSGI server owes a WSGI app
- Why WSGI is synchronous
- How threads and processes add concurrency around sync apps
- Why ASGI exists
- How ASGI uses `scope`, `receive`, and `send`
- What an asyncio event loop does and does not do
- Why blocking code still matters in async systems
- How Starlette/FastAPI/Django bridge sync and async code
- How Gunicorn, Uvicorn, and Hypercorn map to these concepts

## Codebase model

The project uses one evolving codebase. The runnable implementation lives in [`src/runtime_lab`](src/runtime_lab), and helper scripts live in [`scripts`](scripts). There is no `chapters/` directory and no copied per-milestone server files.

If you use `uv`, start the shared runtime server with:

```bash
uv run runtime-lab
```

Keep that terminal open. From another terminal, send one HTTP request to the server with:

```bash
curl -i http://127.0.0.1:8000/
```

If you are not using `uv`, install the package in editable mode once and then run the same console script:

```bash
python -m pip install -e .
runtime-lab
```

Each learning milestone is a small diff to the shared runtime package, helper scripts when useful, and this README when explanation is needed.

## WSGI environ notes

A WSGI server passes an `environ` dictionary to the app. Some values are simple request facts, such as `REQUEST_METHOD`, `PATH_INFO`, and `SERVER_PROTOCOL`.

Two WSGI keys are stream-like objects instead of plain strings:

- `wsgi.input` is where the app reads request body bytes. For the current GET-only milestone, an empty `io.BytesIO(b"")` is enough; later POST/body support can put real request bytes there.
- `wsgi.errors` is where the app writes error or debug text. For this tiny server, `sys.stderr` is a good minimal value.

In plain language: `wsgi.input` is for incoming body data, and `wsgi.errors` is for outgoing diagnostic messages.

## HTTP request parsing notes

A socket gives the server raw request bytes. After decoding those bytes, the server treats the request as three educational pieces:

```text
GET /echo?name=ada HTTP/1.1\r\n
Host: 127.0.0.1:8000\r\n
User-Agent: curl/8.0\r\n
\r\n
hello=world
```

The request line is the first line. It contains the HTTP method, the request target, and the protocol version:

```text
GET /echo?name=ada HTTP/1.1
```

For WSGI, the request target is split at `?`:

```text
/echo?name=ada
  -> PATH_INFO: /echo
  -> QUERY_STRING: name=ada
```

If there is no `?`, the whole target is `PATH_INFO` and `QUERY_STRING` is an empty string.

Headers are the lines after the request line and before the blank line. Most header names become WSGI `HTTP_*` keys by uppercasing the name and replacing `-` with `_`:

```text
Host: 127.0.0.1:8000
  -> HTTP_HOST: 127.0.0.1:8000

User-Agent: curl/8.0
  -> HTTP_USER_AGENT: curl/8.0
```

`Content-Type` and `Content-Length` are special WSGI/CGI names, so they do not get the `HTTP_` prefix:

```text
Content-Type: text/plain
  -> CONTENT_TYPE: text/plain

Content-Length: 11
  -> CONTENT_LENGTH: 11
```

The blank line, written as `\r\n\r\n` in HTTP bytes, separates the request head from the request body. The request head means the request line plus headers. The body is the optional bytes after the blank line; POST support will place those bytes in `wsgi.input`.

The end result is that the WSGI app does not need to know about sockets or raw HTTP text. It reads request facts from `environ` keys such as `REQUEST_METHOD`, `PATH_INFO`, `QUERY_STRING`, `HTTP_HOST`, and eventually `wsgi.input`.

## WSGI call flow

```text
curl
  -> socket server accepts connection
  -> recv() reads HTTP request bytes
  -> build_environ() creates WSGI environ
  -> app(environ, start_response)
  -> start_response captures status and headers
  -> app returns body bytes
  -> build_response() creates HTTP response bytes
  -> sendall() writes response to client
```

## Milestone format

Each milestone should keep the same codebase evolving:

- Small code diff to `src/runtime_lab/`
- Matching manual validation command or helper script when useful
- Short README note when the mental model changes
- One flow trace or diagram when it clarifies the runtime path
- One exercise idea when useful
- Source links
- “What we simplified” note

## Suggested repo structure

```text
.
├── README.md
├── pyproject.toml
├── src/
│   └── runtime_lab/
│       ├── __init__.py
│       ├── __main__.py          # python -m runtime_lab
│       └── server.py            # single evolving runtime
└── scripts/
```

## Backbone sources

- Ruslan Spivak, *Let’s Build a Web Server*
  - https://ruslanspivak.com/lsbaws-part1/
  - https://ruslanspivak.com/lsbaws-part2/
  - https://ruslanspivak.com/lsbaws-part3/
- PEP 3333 / WSGI: https://peps.python.org/pep-3333/
- Python `wsgiref`: https://docs.python.org/3/library/wsgiref.html
- Python `asyncio` conceptual overview: https://docs.python.org/3/howto/a-conceptual-overview-of-asyncio.html
- Python event loop docs: https://docs.python.org/3/library/asyncio-eventloop.html
- Python tasks / `to_thread`: https://docs.python.org/3/library/asyncio-task.html
- ASGI specification: https://asgi.readthedocs.io/en/latest/specs/main.html
- ASGI HTTP/WebSocket format: https://asgi.readthedocs.io/en/latest/specs/www.html
- ASGI lifespan spec: https://asgi.readthedocs.io/en/latest/specs/lifespan.html
- Uvicorn ASGI concepts: https://uvicorn.dev/concepts/asgi/
- Gunicorn design docs: https://gunicorn.org/design/
- Starlette thread pool docs: https://www.starlette.io/threadpool/
- Django async support: https://docs.djangoproject.com/en/dev/topics/async/
- asgiref README: https://github.com/django/asgiref/blob/main/README.rst

## Simplification policy

Every milestone should explicitly say what is being simplified.

Examples:

- HTTP parser is incomplete
- No TLS
- No keep-alive initially
- No production-grade error handling
- No HTTP/2
- No true backpressure implementation until later milestones
- WebSocket support may be conceptual unless explicitly implemented
- Thread/process behavior is educational, not a full Gunicorn clone

## Validation

Most milestones should include at least one manual validation example, such as:

```bash
uv run runtime-lab
curl -i http://127.0.0.1:8000/
python scripts/load_slow.py
```

## Non-goals

- Building a production web server
- Replacing Gunicorn/Uvicorn/Hypercorn
- Full HTTP compliance
- Full ASGI compliance
- Framework feature completeness
