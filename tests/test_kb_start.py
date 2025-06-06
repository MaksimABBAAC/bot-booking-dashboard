import pytest
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.keyboards.keyboard_start import get_keyboard_start


@pytest.mark.asyncio
async def test_get_keyboard_time_appointment():
    markup = await get_keyboard_start()

    assert isinstance(markup, ReplyKeyboardMarkup)
    assert len(markup.keyboard) == 2

    # Проверяем текст кнопок
    assert markup.keyboard[0][0].text == '/my_book'
    assert markup.keyboard[1][0].text == '/booking'
