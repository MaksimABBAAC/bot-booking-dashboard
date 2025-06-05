from aiogram import Router
from aiogram.types import CallbackQuery
from dispatcher.comands import cmd_my_appoiments

from keyboards.keyboards_master import DateCallbackFactory, MastersCallbackFactory, TimeCallbackFactory, data_message_for_description_master, get_keyboard_time_appointment, DeleteEditCallbackFactory
from utils.http_appoiment import book_appointment, delete_book_appointment


router = Router()

@router.callback_query(MastersCallbackFactory.filter())
async def callbacks_master(
    callback: CallbackQuery,
    callback_data: MastersCallbackFactory
):
    description, keyboard = await data_message_for_description_master(callback_data.master_id)
    await callback.message.answer(description + "\n выберете дату", reply_markup= keyboard)

@router.callback_query(DateCallbackFactory.filter())
async def callbacks_master(
    callback: CallbackQuery,
    callback_data: DateCallbackFactory
):
    keyboard = await get_keyboard_time_appointment(
        callback_data.master_id, 
        callback_data.date
        )
    await callback.message.answer("Выберете время\n", reply_markup= keyboard)

@router.callback_query(TimeCallbackFactory.filter())
async def callbacks_master(
    callback: CallbackQuery, 
    callback_data: TimeCallbackFactory):
    try:
        result = await book_appointment(
            tg_id=callback.from_user.id,
            appointment_id=callback_data.appointment_id
        )
        
        if "error" in result:
            await callback.message.answer(f"❌ Ошибка бронирования:")
        else:
            await callback.message.answer("✅ Запись успешно забронирована!")
    except:
        await callback.message.answer("❌ Произошла ошибка при бронировании")


@router.callback_query(DeleteEditCallbackFactory.filter())
async def delete_book(
    callback: CallbackQuery,
    callback_data: DeleteEditCallbackFactory
):
    if callback_data.action == 'delete':
        try:
            result = await delete_book_appointment(
                tg_id = callback.from_user.id,
                appointment_id = callback_data.appointment_id
            )

            if "error" in result:
                await callback.message.answer(f"❌ Ошибка в отмене бронирования:")
            else:
                await callback.message.answer("✅ Бронирование успешно отменено!")
        except:
            await callback.message.answer("❌ Произошла ошибка при отмене бронирования")