import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.dispatcher.collback_query import router  # импортируйте ваш router и функции, если нужно

@pytest.mark.asyncio
@patch("bot.dispatcher.collback_query.data_message_for_description_master", new_callable=AsyncMock)
async def test_callbacks_master_masters(mock_data_message_for_description_master):
    mock_data_message_for_description_master.return_value = ("Описание мастера", "keyboard")

    mock_callback = MagicMock()
    mock_callback.message = MagicMock()
    mock_callback.message.answer = AsyncMock()
    mock_callback.from_user = MagicMock()
    mock_callback.from_user.id = 123

    mock_callback_data = MagicMock()
    mock_callback_data.master_id = 1


    from bot.dispatcher.collback_query import callbacks_master
    await callbacks_master(mock_callback, mock_callback_data)


    mock_data_message_for_description_master.assert_awaited_once()
    mock_callback.message.answer.assert_awaited_once_with("Описание мастера\n выберете дату", reply_markup="keyboard")


@pytest.mark.asyncio
@patch("bot.dispatcher.collback_query.get_keyboard_time_appointment", new_callable=AsyncMock)
async def test_callbacks_master_date(mock_get_keyboard_time_appointment):
    mock_get_keyboard_time_appointment.return_value = "keyboard"

    mock_callback = MagicMock()
    mock_callback.message = MagicMock()
    mock_callback.message.answer = AsyncMock()
    mock_callback.from_user = MagicMock()
    mock_callback.from_user.id = 123  # или другой id

    mock_callback_data = MagicMock()
    mock_callback_data.master_id = 1
    mock_callback_data.date = "2024-06-01"

    from bot.dispatcher.collback_query import callbacks_date
    await callbacks_date(mock_callback, mock_callback_data)

    mock_get_keyboard_time_appointment.assert_awaited_once_with(1, "2024-06-01")
    mock_callback.message.answer.assert_awaited_once_with("Выберете время\n", reply_markup="keyboard")


@pytest.mark.asyncio
@patch("bot.dispatcher.collback_query.book_appointment", new_callable=AsyncMock)
@patch("bot.dispatcher.collback_query.delete_book_appointment", new_callable=AsyncMock)
async def test_callbacks_master_time_success(mock_delete_book_appointment, mock_book_appointment):
    mock_book_appointment.return_value = {}
    mock_delete_book_appointment.return_value = {}

    mock_callback = MagicMock()
    mock_callback.message = MagicMock()
    mock_callback.message.answer = AsyncMock()
    mock_callback.from_user = MagicMock()
    mock_callback.from_user.id = 123  # или другой id

    mock_callback_data = MagicMock()
    mock_callback_data.appointment_id = 10

    mock_state = AsyncMock(spec=FSMContext)
    mock_state.get_data = AsyncMock(return_value={})
    mock_state.clear = AsyncMock()

    from bot.dispatcher.collback_query import callbacks_time
    await callbacks_time(mock_callback, mock_callback_data, mock_state)

    mock_book_appointment.assert_awaited_once_with(tg_id=123, appointment_id=10)
    mock_callback.message.answer.assert_awaited_once_with("✅ Запись успешно забронированна!")
    mock_state.get_data.assert_awaited_once()
    mock_state.clear.assert_not_awaited()  # т.к. old_appointment_id нет


@pytest.mark.asyncio
@patch("bot.dispatcher.collback_query.book_appointment", new_callable=AsyncMock)
@patch("bot.dispatcher.collback_query.delete_book_appointment", new_callable=AsyncMock)
async def test_callbacks_master_time_with_old_appointment(mock_delete_book_appointment, mock_book_appointment):
    mock_book_appointment.return_value = {}
    mock_delete_book_appointment.return_value = {}

    mock_callback = MagicMock()
    mock_callback.message = MagicMock()
    mock_callback.message.answer = AsyncMock()
    mock_callback.from_user = MagicMock()
    mock_callback.from_user
    mock_callback.from_user.id = 123

    mock_callback_data = MagicMock()
    mock_callback_data.appointment_id = 10

    mock_state = AsyncMock(spec=FSMContext)
    mock_state.get_data = AsyncMock(return_value={"old_appointment_id": 5})
    mock_state.clear = AsyncMock()

    from bot.dispatcher.collback_query import callbacks_time
    await callbacks_time(mock_callback, mock_callback_data, mock_state)

    mock_delete_book_appointment.assert_awaited_once_with(tg_id=123,appointment_id=5)
    mock_book_appointment.assert_awaited_once_with(tg_id=123, appointment_id=10)
    mock_callback.message.answer.assert_awaited_once_with("✅ Запись успешно перенесена!\n" "Новая запись создана, старая отменена.")
    mock_state.get_data.assert_awaited_once()
    mock_state.clear.assert_awaited_once()


@pytest.mark.asyncio
@patch("bot.dispatcher.collback_query.delete_book_appointment", new_callable=AsyncMock)
async def test_delete_book_delete_action_success(mock_delete_book_appointment):
    mock_delete_book_appointment.return_value = {}

    mock_callback = MagicMock()
    mock_callback.message = MagicMock()
    mock_callback.message.answer = AsyncMock()
    mock_callback.from_user = MagicMock()
    mock_callback.from_user.id = 123

    mock_callback_data = MagicMock()
    mock_callback_data.appointment_id = 10
    mock_callback_data.action = 'delete'
    mock_state = AsyncMock(spec=FSMContext)

    from bot.dispatcher.collback_query import delete_edit_book
    await delete_edit_book(mock_callback, mock_callback_data,mock_state)

    mock_delete_book_appointment.assert_awaited_once_with(tg_id=123,appointment_id=10)
    mock_callback.message.answer.assert_awaited_once_with("✅ Бронирование успешно отменено!")
