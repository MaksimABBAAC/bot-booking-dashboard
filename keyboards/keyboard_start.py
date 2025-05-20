from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def get_keyboard_time_appointment() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text='/my_book')],
        [KeyboardButton(text='/booking')]
    ]
    return ReplyKeyboardMarkup(keyboard=kb)
