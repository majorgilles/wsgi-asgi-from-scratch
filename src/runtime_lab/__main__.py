"""Command-line entrypoint for ``python -m runtime_lab``."""

from .server import main

if __name__ == "__main__":
    raise SystemExit(main())
