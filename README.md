# WSGI to ASGI From Scratch

A source-backed, code-first tutorial project for Python backend developers who know web frameworks but want to understand the runtime internals underneath them.

We build a tiny educational web runtime in 30–60 minute chapters:

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

## Chapter format

Each chapter is a 30–60 minute runnable package. Start from the reusable [chapter template](chapters/CHAPTER_TEMPLATE.md):

- Small code diff
- Short explanation
- One flow trace or diagram
- One exercise
- Source links
- “What we simplified” note

## Suggested repo structure

```text
.
├── README.md
├── pyproject.toml
├── chapters/
│   ├── 00-scaffold/
│   ├── 01-raw-http-socket/
│   ├── 02-wsgi-callable/
│   ├── 03-wsgi-request-lifecycle/
│   ├── 04-wsgi-middleware-routing/
│   ├── 05-wsgi-threading/
│   ├── 06-gunicorn-worker-models/
│   ├── 07-asyncio-event-loop/
│   ├── 08-bare-asgi-app/
│   ├── 09-tiny-asgi-server/
│   ├── 10-asgi-streaming/
│   ├── 11-asgi-lifespan/
│   ├── 12-sync-async-interop/
│   ├── 13-production-map/
│   └── 14-capstone-failure-lab/
├── src/
│   └── runtime_lab/
├── tests/
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

Every chapter should explicitly say what is being simplified.

Examples:

- HTTP parser is incomplete
- No TLS
- No keep-alive initially
- No production-grade error handling
- No HTTP/2
- No true backpressure implementation until later chapters
- WebSocket support may be conceptual unless explicitly implemented
- Thread/process behavior is educational, not a full Gunicorn clone

## Validation

Most chapters should include at least one of:

```bash
python chapters/<chapter>/server.py
curl -i http://127.0.0.1:8000/
python -m pytest -q
python scripts/load_slow.py
```

## Non-goals

- Building a production web server
- Replacing Gunicorn/Uvicorn/Hypercorn
- Full HTTP compliance
- Full ASGI compliance
- Framework feature completeness
