from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError

from .config import Settings
from .content import ABOUT, BOT_NAME, BOT_USERNAME, DESCRIPTION
from .handlers import router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


async def configure_bot_profile(bot: Bot, settings: Settings) -> None:
    """Configure profile fields supported by Telegram Bot API."""
    try:
        await bot.set_my_name(
            name=settings.bot_name,
            language_code="en",
        )
        await bot.set_my_description(
            description=DESCRIPTION,
            language_code="en",
        )
        await bot.set_my_short_description(
            short_description=ABOUT,
            language_code="en",
        )
        logger.info(
            "Telegram profile configured for %s (%s)",
            settings.bot_name,
            settings.bot_username,
        )
    except TelegramAPIError:
        logger.exception(
            "Could not update one or more Telegram profile fields. "
            "The bot will continue running."
        )


async def main() -> None:
    settings = Settings.from_env()

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(router)

    await configure_bot_profile(bot, settings)

    logger.info("Starting %s %s", BOT_NAME, BOT_USERNAME)
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
