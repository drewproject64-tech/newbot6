from __future__ import annotations

from html import escape

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from .content import INVALID_TEXT, WELCOME
from .keyboards import main_keyboard

router = Router()


class ConversionState(StatesGroup):
    mode = State()


MODE_LABELS = {
    "UPPERCASE": "UPPERCASE",
    "lowercase": "lowercase",
    "Title Case": "Title Case",
}


def convert_text(text: str, mode: str) -> str:
    if mode == "UPPERCASE":
        return text.upper()
    if mode == "lowercase":
        return text.lower()
    if mode == "Title Case":
        return text.title()
    raise ValueError(f"Unsupported mode: {mode}")


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(WELCOME, reply_markup=main_keyboard())


@router.message(Command("menu"))
async def menu_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Choose a text conversion:",
        reply_markup=main_keyboard(),
    )


@router.message(F.text.in_(MODE_LABELS.keys()))
async def mode_handler(message: Message, state: FSMContext) -> None:
    mode = MODE_LABELS[message.text]
    await state.set_state(ConversionState.mode)
    await state.update_data(mode=mode)
    await message.answer(
        f"<b>{escape(mode)}</b> selected.\n\n"
        f"Send the text you want to convert to {escape(mode)}.",
        reply_markup=main_keyboard(),
    )


@router.message(ConversionState.mode, F.text)
async def conversion_handler(message: Message, state: FSMContext) -> None:
    source = message.text or ""
    if not source.strip():
        await message.answer(INVALID_TEXT, reply_markup=main_keyboard())
        return

    data = await state.get_data()
    mode = data.get("mode")
    if mode not in MODE_LABELS:
        await state.clear()
        await message.answer(
            "Please choose one of the three conversion buttons first.",
            reply_markup=main_keyboard(),
        )
        return

    try:
        result = convert_text(source, mode)
    except (TypeError, ValueError):
        await state.clear()
        await message.answer(
            "I couldn't convert that text. Please choose a conversion and try again.",
            reply_markup=main_keyboard(),
        )
        return

    await message.answer(
        f"<b>{escape(mode)} result</b>\n\n{escape(result)}",
        reply_markup=main_keyboard(),
    )
    await state.clear()


@router.message()
async def invalid_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        INVALID_TEXT if (message.text or "").strip() == "" else
        "Choose one of the three conversion buttons, then send your text.",
        reply_markup=main_keyboard(),
    )
