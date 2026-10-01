from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    bot_token: str
    bot_name: str
    bot_username: str

    @classmethod
    def from_env(cls) -> "Settings":
        token = os.getenv("BOT_TOKEN", "").strip()
        if not token:
            raise RuntimeError("BOT_TOKEN environment variable is required.")

        return cls(
            bot_token=token,
            bot_name=os.getenv("BOT_NAME", "SB24").strip() or "SB24",
            bot_username=os.getenv("BOT_USERNAME", "@SBWordFlipBot").strip() or "@SBWordFlipBot",
        )
