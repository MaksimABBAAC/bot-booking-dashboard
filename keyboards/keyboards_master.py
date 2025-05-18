from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils import get_Masters

async def get_Kmasters():
    masters = await get_Masters()
    builder = InlineKeyboardBuilder()
    if masters:
        for master in masters:
            builder.button(
                text = f"{master.name} {master.name} {master.patronymic}.\n {master.specialty}",
                callback_data = f"master_{master.id}"
                )
        return builder.as_markup()
    else:
        return builder.row(types.InlineKeyboardButton(text = "Сейчас сервис для записи недоступен"))
    