from collections import namedtuple
from datetime import date, time
import pytest
from unittest.mock import AsyncMock, patch
from aiogram import types

from bot.utils.model import Availabl_appointment


Master = namedtuple("Master", ["id", "name", "patronymic", "specialty"])


@pytest.mark.asyncio
async def test_get_keyboards_masters_with_masters():
    master = Master(id=1, name="Иван", patronymic="Иванович", specialty="Парикмахер")
    
    with patch("bot.keyboards.keyboards_master.get_masters_list", new=AsyncMock(return_value=[master])):
        with patch("bot.keyboards.collbackFactory.MastersCallbackFactory") as mock_factory:
            mock_factory.return_value.pack.return_value = "callback_data"

            from bot.keyboards.keyboards_master import get_keyboards_masters
            markup = await get_keyboards_masters()
    
    print(markup)
    assert isinstance(markup, types.InlineKeyboardMarkup)
    buttons = [btn for row in markup.inline_keyboard for btn in row]
    assert any("Иван Иванович" in btn.text for btn in buttons)


@pytest.mark.asyncio
async def test_get_keyboard_date_appointment_with_dates():
    class DummyAppointment:
        def __init__(self, date):
            self.date = date

    import datetime
    master = AsyncMock()
    master.id = 1
    dates = [datetime.date(2024, 6, 1), datetime.date(2024, 6, 2)]
    appointments = [DummyAppointment(d) for d in dates]

    with patch("bot.keyboards.collbackFactory.DateCallbackFactory") as mock_factory:
        mock_factory.from_date_obj.side_effect = lambda master_id, date_obj: AsyncMock(pack=lambda: f"cb_{date_obj}")
        from bot.keyboards.keyboards_master import get_keyboard_date_appointment
        markup = await get_keyboard_date_appointment(appointments, master)

    assert isinstance(markup, types.InlineKeyboardMarkup)
    buttons_texts = [btn.text for row in markup.inline_keyboard for btn in row]
    for d in dates:
        assert d.strftime("%Y-%m-%d") in buttons_texts


@pytest.mark.asyncio
async def test_get_keyboard_date_appointment_no_data():
    from bot.keyboards.keyboards_master import get_keyboard_date_appointment
    markup = await get_keyboard_date_appointment([], None)
    assert isinstance(markup, types.InlineKeyboardMarkup)
    buttons_texts = [btn.text for row in markup.inline_keyboard for btn in row]
    assert any("Сейчас сервис для записи недоступен" in text for text in buttons_texts)


@pytest.mark.asyncio
async def test_get_keyboard_time_appointment_with_appointments():
    appointments = [
        Availabl_appointment(id=1, master=1, date=date(2024, 6, 1), start_time=time(10, 0), end_time=time(11, 0), is_available=True),
        Availabl_appointment(id=2, master=1, date=date(2024, 6, 1), start_time=time(11, 0), end_time=time(12, 0), is_available=True),
    ]

    with patch("bot.keyboards.keyboards_master.get_available_appointment_by_master_id", new=AsyncMock(return_value=appointments)):
        with patch("bot.keyboards.collbackFactory.TimeCallbackFactory") as mock_factory:
            mock_factory.side_effect = lambda appointment_id: AsyncMock(pack=lambda: f"cb_{appointment_id}")
            from bot.keyboards.keyboards_master import get_keyboard_time_appointment
            markup = await get_keyboard_time_appointment(1, "2024-06-01")
    print(markup)
    assert isinstance(markup, types.InlineKeyboardMarkup)
    buttons_texts = [btn.text for row in markup.inline_keyboard for btn in row]
    for appt in appointments:
        expected_text = f"{appt.start_time} - {appt.end_time}"
        assert expected_text in buttons_texts

@pytest.mark.asyncio
async def test_get_keyboard_time_appointment_no_appointments():
    with patch("bot.keyboards.keyboards_master.get_available_appointment_by_master_id", new=AsyncMock(return_value=[])):
        from bot.keyboards.keyboards_master import get_keyboard_time_appointment
        markup = await get_keyboard_time_appointment(1, "2024-06-01")
    assert isinstance(markup, types.InlineKeyboardMarkup)
    buttons_texts = [btn.text for row in markup.inline_keyboard for btn in row]
    assert any("Сейчас сервис для записи недоступен" in text for text in buttons_texts)
