"""Optimized uvicorn entrypoint for ChronosMamba backend.

Uses uvloop for the event loop and httptools for HTTP parsing
to minimize latency on Linux deployments.
"""

import platform
import sys

import uvicorn


def main() -> None:
    """Start the uvicorn server with optimized settings."""
    # uvloop and httptools are only supported on Linux/macOS
    is_unix = platform.system() != "Windows"

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        loop="uvloop" if is_unix else "asyncio",
        http="httptools" if is_unix else "auto",
        workers=1,
        log_level="info",
        access_log=True,
    )


if __name__ == "__main__":
    main()
