from collections import namedtuple
from datetime import date, time
from unittest.mock import AsyncMock, patch

import pytest
from aiogram import types

from bot.keyboards.keyboards_master import (get_keyboard_date_appointment,
                                            get_keyboard_time_appointment,
                                            get_keyboards_masters)
from bot.utils.model import AvailablAppointment

Master = namedtuple("Master", ["id", "name", "patronymic", "specialty"])


@pytest.mark.asyncio
async def test_get_keyboards_masters_with_masters():
    master = Master(id=1, name="Иван", patronymic="Иванович", specialty="Парикмахер")

    with patch(
        "bot.keyboards.keyboards_master.get_masters_list",
        new=AsyncMock(return_value=[master]),
    ):
        with patch(
            "bot.keyboards.collback_factory.MastersCallbackFactory"
        ) as mock_factory:
            mock_factory.return_value.pack.return_value = "callback_data"

            markup = await get_keyboards_masters()

    print(markup)
    assert isinstance(markup, types.InlineKeyboardMarkup)
    buttons = [btn for row in markup.inline_keyboard for btn in row]
    assert any("Иван Иванович" in btn.text for btn in buttons)


@pytest.mark.asyncio
async def test_get_keyboard_date_appointment_with_dates():
    Appointment = namedtuple("Appointment", ["date"])
    master = AsyncMock()
    master.id = 1
    dates = [date(2024, 6, 1), date(2024, 6, 2)]
    appointments = [Appointment(d) for d in dates]

    with patch("bot.keyboards.collback_factory.DateCallbackFactory") as mock_factory:
        mock_factory.from_date_obj.side_effect = lambda master_id, date_obj: AsyncMock(
            pack=lambda: f"cb_{date_obj}"
        )

        markup = await get_keyboard_date_appointment(appointments, master)

    assert isinstance(markup, types.InlineKeyboardMarkup)
    buttons_texts = [btn.text for row in markup.inline_keyboard for btn in row]
    for d in dates:
        assert d.strftime("%Y-%m-%d") in buttons_texts


@pytest.mark.asyncio
async def test_get_keyboard_date_appointment_no_data():
    markup = await get_keyboard_date_appointment([], None)
    assert isinstance(markup, types.InlineKeyboardMarkup)
    buttons_texts = [btn.text for row in markup.inline_keyboard for btn in row]
    assert any("Сейчас сервис для записи недоступен" in text for text in buttons_texts)


@pytest.mark.asyncio
async def test_get_keyboard_time_appointment_with_appointments():
    appointments = [
        AvailablAppointment(
            id=1,
            master=1,
            date=date(2024, 6, 1),
            start_time=time(10, 0),
            end_time=time(11, 0),
            is_available=True,
        ),
        AvailablAppointment(
            id=2,
            master=1,
            date=date(2024, 6, 1),
            start_time=time(11, 0),
            end_time=time(12, 0),
            is_available=True,
        ),
    ]

    with patch(
        "bot.keyboards.keyboards_master.get_available_appointment_by_master_id",
        new=AsyncMock(return_value=appointments),
    ):
        with patch(
            "bot.keyboards.collback_factory.TimeCallbackFactory"
        ) as mock_factory:
            mock_factory.side_effect = lambda appointment_id: AsyncMock(
                pack=lambda: f"cb_{appointment_id}"
            )
            markup = await get_keyboard_time_appointment(1, "2024-06-01")
    assert isinstance(markup, types.InlineKeyboardMarkup)
    buttons_texts = [btn.text for row in markup.inline_keyboard for btn in row]
    for appt in appointments:
        expected_text = f"{appt.start_time} - {appt.end_time}"
        assert expected_text in buttons_texts


@pytest.mark.asyncio
async def test_get_keyboard_time_appointment_no_appointments():
    with patch(
        "bot.keyboards.keyboards_master.get_available_appointment_by_master_id",
        new=AsyncMock(return_value=[]),
    ):

        markup = await get_keyboard_time_appointment(1, "2024-06-01")
    assert isinstance(markup, types.InlineKeyboardMarkup)
    buttons_texts = [btn.text for row in markup.inline_keyboard for btn in row]
    assert any("Сейчас сервис для записи недоступен" in text for text in buttons_texts)
