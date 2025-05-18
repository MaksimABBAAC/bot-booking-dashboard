import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config import settings
from keyboards.keyboards_master import get_Kmasters

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.TOKEN)

dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = await get_Kmasters()
    await message.answer("Hello message", reply_markup= keyboard)

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)




if __name__ == "__main__":
    asyncio.run(main())
