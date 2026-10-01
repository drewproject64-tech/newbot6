"""Render-compatible entry point for SB24.

This shim keeps the project compatible with Render services configured
with the conventional `python bot.py` start command.
"""

import asyncio

from app.main import main


if __name__ == "__main__":
    asyncio.run(main())
