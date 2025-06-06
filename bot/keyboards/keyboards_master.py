from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from ..keyboards.collbackFactory import DateCallbackFactory, DeleteEditCallbackFactory, MastersCallbackFactory, TimeCallbackFactory
from bot.utils.http_appointment import Availabl_appointment, get_available_appointment_by_master_id, get_booking_appointment_by_tg_id
from ..utils.http_master import get_master_by_id, get_masters_list


async def get_keyboards_masters() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    master_list = await get_masters_list()
    if master_list:
        for master in master_list:
            builder.row(types.InlineKeyboardButton(
                text = f"{master.name} {master.name} {master.patronymic}.\n{master.specialty}",
                callback_data = MastersCallbackFactory(master_id = master.id).pack()
                ))
    else:
        builder.row(types.InlineKeyboardButton(
            text = "Сейчас сервис для записи недоступен\n попробуйте позже",
            callback_data = "error"))
    return builder.as_markup()

async def data_message_for_description_master(master_id):
    available_appointment_list = await get_available_appointment_by_master_id(master_id)
    master = await get_master_by_id(master_id)
    keyboard_date_appointment = await get_keyboard_date_appointment(available_appointment_list, master)
    return master.description, keyboard_date_appointment



async def get_keyboard_date_appointment(
    available_appointment_list: list[Availabl_appointment], 
    master
) -> types.InlineKeyboardMarkup:
    
    builder = InlineKeyboardBuilder()
    
    if available_appointment_list and master:
        unique_dates = {appointment.date for appointment in available_appointment_list}
        
        for date_obj in sorted(unique_dates):
            builder.row(types.InlineKeyboardButton(
                text=date_obj.strftime("%Y-%m-%d"), 
                callback_data=DateCallbackFactory.from_date_obj(
                    master_id=master.id,
                    date_obj=date_obj
                ).pack()
            ))
    else:
        builder.row(types.InlineKeyboardButton(
            text="Сейчас сервис для записи недоступен\n попробуйте позже",
            callback_data="error"
        ))
    
    return builder.as_markup()



async def get_keyboard_time_appointment(master_id, date) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    available_appointment_list = await get_available_appointment_by_master_id(master_id, date)
    if available_appointment_list:
        for appointment in available_appointment_list:
                builder.row(types.InlineKeyboardButton(
                    text = f"{appointment.start_time} - {appointment.end_time}",
                    callback_data = TimeCallbackFactory(appointment_id = appointment.id).pack()
                    ))
    else:
        builder.row(types.InlineKeyboardButton(
            text = "Сейчас сервис для записи недоступен\n попробуйте позже",
            callback_data = "error"))
    return builder.as_markup()
