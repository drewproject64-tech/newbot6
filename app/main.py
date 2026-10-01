from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError

from .content import ABOUT, DESCRIPTION
from .handlers import router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


async def configure_bot_profile(bot: Bot, settings) -> None:
    """Configure supported Telegram profile fields without blocking startup."""
    profile_updates = (
        ("name", bot.set_my_name(name=settings.bot_name, language_code="en")),
        ("description", bot.set_my_description(description=DESCRIPTION, language_code="en")),
        ("short description", bot.set_my_short_description(short_description=ABOUT, language_code="en")),
    )

    for label, request in profile_updates:
        try:
            await request
            logger.info("Updated bot %s.", label)
        except TelegramAPIError:
            logger.exception("Could not update bot %s; continuing.", label)


async def main() -> None:
    from .config import Settings

    settings = Settings.from_env()
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher()
    dispatcher.include_router(router)

    await configure_bot_profile(bot, settings)

    logger.info("Starting %s (%s)", settings.bot_name, settings.bot_username)
    try:
        await dispatcher.start_polling(
            bot,
            allowed_updates=dispatcher.resolve_used_update_types(),
        )
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
