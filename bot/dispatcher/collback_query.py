from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.keyboards_master import DateCallbackFactory, MastersCallbackFactory, TimeCallbackFactory, data_message_for_description_master, get_keyboard_time_appointment, DeleteEditCallbackFactory, get_keyboards_masters
from bot.utils.http_appointment import book_appointment, delete_book_appointment


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
    callback_data: TimeCallbackFactory,
    state: FSMContext
    ):
    try:
        result = await book_appointment(
            tg_id=callback.from_user.id,
            appointment_id=callback_data.appointment_id
        )
        
        if "error" in result:
            await callback.message.answer(f"❌ Ошибка бронирования:")

        state_data = await state.get_data()
        if 'old_appointment_id' in state_data:
            delete_result = await delete_book_appointment(
                tg_id=callback.from_user.id,
                appointment_id=state_data['old_appointment_id']
            )

            if "error" in delete_result:
                await callback.message.answer(
                    "✅ Новая запись создана, но не удалось отменить старую!\n"
                    f"Ошибка: {delete_result['error']}"
                )
            else:
                await callback.message.answer(
                    "✅ Запись успешно перенесена!\n"
                    "Новая запись создана, старая отменена."
                )
            await state.clear()
        else: 
            await callback.message.answer("✅ Запись успешно забронированна!")
    except:
        await callback.message.answer("❌ Произошла ошибка при бронировании")


@router.callback_query(DeleteEditCallbackFactory.filter())
async def delete_book(
    callback: CallbackQuery,
    callback_data: DeleteEditCallbackFactory,
    state: FSMContext
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
    elif callback_data.action == 'edit':
        await state.update_data(
            old_appointment_id=callback_data.appointment_id
        )
        await callback.message.answer(f"Перенос бронирование состоит из двух этапов\n" +
                                        "1. Бронирование новой записи\n"+
                                        "2. Отмена старой записи\n"+
                                        "Сейчас вам будет предложено забронировать новую запись")
        keyboard = await get_keyboards_masters();
        await callback.message.answer("Выберете мастера из списка", reply_markup= keyboard)