from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from bot.dispatcher.comands import cmd_booking, cmd_my_appoiments, cmd_start


@pytest.mark.asyncio
@patch("bot.dispatcher.comands.get_keyboard_start", new_callable=AsyncMock)
async def test_cmd_start(mock_get_keyboard_start):
    mock_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="test")]])
    mock_get_keyboard_start.return_value = mock_keyboard

    mock_message = AsyncMock(spec=Message)
    mock_message.answer = AsyncMock()

    await cmd_start(mock_message)

    mock_get_keyboard_start.assert_awaited_once()
    mock_message.answer.assert_awaited_once()
    args, kwargs = mock_message.answer.call_args
    assert "Здраствуйте" in args[0]
    assert kwargs["reply_markup"] == mock_keyboard


@pytest.mark.asyncio
@patch("bot.dispatcher.comands.get_cards_appoiment", new_callable=AsyncMock)
async def test_cmd_my_appoiments_success(mock_get_cards_appoiment):
    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="btn")]])
    cards = ["Текст 1", keyboard, "Текст 2", keyboard]
    mock_get_cards_appoiment.return_value = (cards, None)

    mock_message = AsyncMock(spec=Message)
    mock_message.answer = AsyncMock()

    mock_message.from_user = MagicMock()
    mock_message.from_user.id = 123

    await cmd_my_appoiments(mock_message)

    mock_get_cards_appoiment.assert_awaited_once_with(123)
    assert mock_message.answer.await_count == 2
    call_args_0 = mock_message.answer.await_args_list[0][1]
    assert call_args_0["text"] == "Текст 1"
    assert call_args_0["reply_markup"] == keyboard
    call_args_1 = mock_message.answer.await_args_list[1][1]
    assert call_args_1["text"] == "Текст 2"
    assert call_args_1["reply_markup"] == keyboard


@pytest.mark.asyncio
@patch("bot.dispatcher.comands.get_cards_appoiment", new_callable=AsyncMock)
async def test_cmd_my_appoiments_error(mock_get_cards_appoiment):
    mock_get_cards_appoiment.return_value = (None, True)

    mock_message = AsyncMock(spec=Message)
    mock_message.answer = AsyncMock()

    mock_message.from_user = MagicMock()
    mock_message.from_user.id = 123

    await cmd_my_appoiments(mock_message)

    mock_get_cards_appoiment.assert_awaited_once_with(123)
    mock_message.answer.assert_awaited_once_with(text="Ошибка")


@pytest.mark.asyncio
@patch("bot.dispatcher.comands.get_cards_appoiment", new_callable=AsyncMock)
async def test_cmd_my_appoiments_no_cards(mock_get_cards_appoiment):
    mock_get_cards_appoiment.return_value = ([], None)

    mock_message = AsyncMock(spec=Message)
    mock_message.answer = AsyncMock()

    mock_message.from_user = MagicMock()
    mock_message.from_user.id = 123

    await cmd_my_appoiments(mock_message)

    mock_get_cards_appoiment.assert_awaited_once_with(123)
    mock_message.answer.assert_awaited_once_with(text="У вас нет записей")


@pytest.mark.asyncio
@patch("bot.dispatcher.comands.get_keyboards_masters", new_callable=AsyncMock)
async def test_cmd_booking(mock_get_keyboards_masters):
    mock_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="master1")]])
    mock_get_keyboards_masters.return_value = mock_keyboard

    mock_message = AsyncMock(spec=Message)
    mock_message.answer = AsyncMock()

    mock_message.from_user = MagicMock()
    mock_message.from_user.id = 123

    await cmd_booking(mock_message)

    mock_get_keyboards_masters.assert_awaited_once()
    mock_message.answer.assert_awaited_once_with(
        "Выберете мастера из списка", reply_markup=mock_keyboard
    )
