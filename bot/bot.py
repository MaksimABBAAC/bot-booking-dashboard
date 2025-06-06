import asyncio
import logging
from aiogram import Bot, Dispatcher, types

from config import settings
from dispatcher import comands, collback_query


logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.TOKEN)
dp = Dispatcher()

dp.include_router(comands.router)
dp.include_router(collback_query.router)

async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="start", description="Начать работу"),
        types.BotCommand(command="my_book", description="Мои записи")
    ]
    await bot.set_my_commands(commands)

async def main():
    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
