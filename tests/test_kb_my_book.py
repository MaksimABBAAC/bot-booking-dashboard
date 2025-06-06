import pytest
from unittest.mock import patch, AsyncMock
from aiogram.types import InlineKeyboardMarkup
from bot.keyboards.keyboards_my_book import get_cards_appoiment

@pytest.mark.asyncio
async def test_get_cards_appoiment_with_bookings():
    tg_id = 12345
    mock_appointments = [
        type("Appointment", (), {
            "id": 1,
            "date": "2023-10-01",
            "start_time": "10:00",
            "end_time": "11:00"
        })(),
        type("Appointment", (), {
            "id": 2,
            "date": "2023-10-02",
            "start_time": "12:00",
            "end_time": "13:00"
        })(),
    ]

    with patch("bot.keyboards.keyboards_my_book.get_booking_appointment_by_tg_id", new=AsyncMock(return_value=mock_appointments)):
        cards, error = await get_cards_appoiment(tg_id)

    print(cards)

    assert len(cards) == 4
    assert cards[0] == 'Вы записаны на 2023-10-01 10:00 - 11:00'
    assert isinstance(cards[1], InlineKeyboardMarkup)
    assert len(cards[1].inline_keyboard) == 1
    assert cards[2] == 'Вы записаны на 2023-10-02 12:00 - 13:00'
    assert isinstance(cards[3], InlineKeyboardMarkup)
    assert len(cards[3].inline_keyboard) == 1
    assert error is None

@pytest.mark.asyncio
async def test_get_cards_appoiment_no_bookings():
    tg_id = 12345

    with patch("bot.keyboards.keyboards_my_book.get_booking_appointment_by_tg_id", new=AsyncMock(return_value=[])):
        cards, error = await get_cards_appoiment(tg_id)

    assert cards == []
    assert error is None

@pytest.mark.asyncio
async def test_get_cards_appoiment_error():
    tg_id = 12345

    with patch("bot.keyboards.keyboards_my_book.get_booking_appointment_by_tg_id", new=AsyncMock(return_value=None)):
        cards, error = await get_cards_appoiment(tg_id)

    assert cards == []
    assert error == 'error'
