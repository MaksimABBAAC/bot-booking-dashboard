from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.utils.http_appointment import (book_appointment,
                                        delete_book_appointment)

from ..keyboards.collback_factory import (DateCallbackFactory,
                                          DeleteEditCallbackFactory,
                                          MastersCallbackFactory,
                                          TimeCallbackFactory)
from ..keyboards.keyboards_master import (data_message_for_description_master,
                                          get_keyboard_time_appointment,
                                          get_keyboards_masters)

router = Router()


@router.callback_query(MastersCallbackFactory.filter())
async def callbacks_master(
    callback: CallbackQuery, callback_data: MastersCallbackFactory
):
    description, keyboard = await data_message_for_description_master(
        callback_data.master_id
    )
    await callback.message.answer(
        description + "\n выберете дату", reply_markup=keyboard
    )


@router.callback_query(DateCallbackFactory.filter())
async def callbacks_date(callback: CallbackQuery, callback_data: DateCallbackFactory):
    keyboard = await get_keyboard_time_appointment(
        callback_data.master_id, callback_data.date
    )
    await callback.message.answer("Выберете время\n", reply_markup=keyboard)


@router.callback_query(TimeCallbackFactory.filter())
async def callbacks_time(
    callback: CallbackQuery, callback_data: TimeCallbackFactory, state: FSMContext
):
    try:
        result = await book_appointment(
            tg_id=callback.from_user.id, appointment_id=callback_data.appointment_id
        )

        if "error" in result:
            await callback.message.answer("❌ Ошибка бронирования:")

        state_data = await state.get_data()
        if "old_appointment_id" in state_data:
            delete_result = await delete_book_appointment(
                tg_id=callback.from_user.id,
                appointment_id=state_data["old_appointment_id"],
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
    except Exception:
        await callback.message.answer("❌ Произошла ошибка при бронировании")


@router.callback_query(DeleteEditCallbackFactory.filter())
async def delete_edit_book(
    callback: CallbackQuery, callback_data: DeleteEditCallbackFactory, state: FSMContext
):
    if callback_data.action == "delete":
        try:
            result = await delete_book_appointment(
                tg_id=callback.from_user.id, appointment_id=callback_data.appointment_id
            )

            if "error" in result:
                await callback.message.answer("❌ Ошибка в отмене бронирования:")
            else:
                await callback.message.answer("✅ Бронирование успешно отменено!")
        except Exception:
            await callback.message.answer("❌ Произошла ошибка при отмене бронирования")
    elif callback_data.action == "edit":
        await state.update_data(old_appointment_id=callback_data.appointment_id)
        await callback.message.answer(
            """Перенос бронирование состоит из двух этапов
            1. Бронирование новой записи
            2. Отмена старой записи
            Сейчас вам будет предложено забронировать новую запись"""
        )
        keyboard = await get_keyboards_masters()
        await callback.message.answer(
            "Выберете мастера из списка", reply_markup=keyboard
        )
