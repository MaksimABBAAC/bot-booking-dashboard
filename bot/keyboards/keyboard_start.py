from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def get_keyboard_start() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text='/my_book')],
        [KeyboardButton(text='/booking')]
    ]
    return ReplyKeyboardMarkup(keyboard=kb)
