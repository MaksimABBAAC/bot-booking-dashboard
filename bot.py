import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config import settings
from keyboards.keyboards_master import DateCallbackFactory, MastersCallbackFactory, TimeCallbackFactory, data_message_for_description_master, get_keyboard_time_appointment, get_keyboards_masters
from utils import book_appointment

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.TOKEN)

dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = await get_keyboards_masters()
    await message.answer("Hello message", reply_markup= keyboard)

async def main():
    await dp.start_polling(bot)

@dp.callback_query(MastersCallbackFactory.filter())
async def callbacks_master(
    callback: types.CallbackQuery,
    callback_data: MastersCallbackFactory
):
    description, keyboard = await data_message_for_description_master(callback_data.master_id)
    await callback.message.answer("Hello message\n" + description, reply_markup= keyboard)

@dp.callback_query(DateCallbackFactory.filter())
async def callbacks_master(
    callback: types.CallbackQuery,
    callback_data: DateCallbackFactory
):
    keyboard = await get_keyboard_time_appointment(
        callback_data.master_id, 
        callback_data.date
        )
    await callback.message.answer("Hello message\n", reply_markup= keyboard)

@dp.callback_query(TimeCallbackFactory.filter())
async def callbacks_master(callback: types.CallbackQuery, callback_data: TimeCallbackFactory):
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
    

if __name__ == "__main__":
    asyncio.run(main())
