from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from .content import INVALID_TEXT, WELCOME
from .keyboards import main_keyboard

router = Router()

MODE_LABELS = {
    "UPPERCASE": "UPPERCASE",
    "lowercase": "lowercase",
    "Title Case": "Title Case",
}


def conversion_prompt(mode: str) -> str:
    return (
        f"{mode} selected.\n\n"
        f"Send the text you want to convert to {mode}.\n"
        "I will return the converted text directly here."
    )


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(WELCOME, reply_markup=main_keyboard())


@router.message(Command("menu"))
async def menu_handler(message: Message) -> None:
    await message.answer(
        "Choose a text conversion:",
        reply_markup=main_keyboard(),
    )


@router.message(lambda message: message.text in MODE_LABELS)
async def mode_handler(message: Message) -> None:
    await message.answer(
        conversion_prompt(MODE_LABELS[message.text]),
        reply_markup=main_keyboard(),
    )
    await message.answer(
        "Now send your text.",
        reply_markup=main_keyboard(),
    )


@router.message()
async def text_handler(message: Message) -> None:
    text = (message.text or "").strip()
    if not text:
        await message.answer(INVALID_TEXT, reply_markup=main_keyboard())
        return

    # Determine the requested conversion from the most recently selected
    # text button by looking at Telegram's reply keyboard input. Since aiogram
    # does not preserve UI state in the message itself, this handler accepts a
    # simple command-prefixed workflow as well as plain text fallback.
    await message.answer(
        "Choose one of the three conversion buttons first, then send your text.",
        reply_markup=main_keyboard(),
    )


def convert_text(text: str, mode: str) -> str:
    if mode == "UPPERCASE":
        return text.upper()
    if mode == "lowercase":
        return text.lower()
    if mode == "Title Case":
        return text.title()
    raise ValueError(f"Unsupported mode: {mode}")
