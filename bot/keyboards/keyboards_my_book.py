from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.http_appointment import get_booking_appointment_by_tg_id

from .collback_factory import DeleteEditCallbackFactory


async def get_cards_appoiment(tg_id):
    cards = []
    error = None

    booking_appoiments_list = await get_booking_appointment_by_tg_id(tg_id)
    if booking_appoiments_list:
        for appointment in booking_appoiments_list:
            builder = InlineKeyboardBuilder()
            cards.append(
                f"Вы записаны на {appointment.date} "
                + f"{appointment.start_time} - {appointment.end_time}"
            )
            builder.button(
                text="перенести",
                callback_data=DeleteEditCallbackFactory(
                    action="edit", appointment_id=appointment.id
                ).pack(),
            )
            builder.button(
                text="отменить",
                callback_data=DeleteEditCallbackFactory(
                    action="delete", appointment_id=appointment.id
                ).pack(),
            )
            cards.append(builder.as_markup())
    elif booking_appoiments_list is None:
        error = "error"

    return cards, error
