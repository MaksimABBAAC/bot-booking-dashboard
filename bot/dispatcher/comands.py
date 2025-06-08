from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message

from ..keyboards.keyboard_start import get_keyboard_start
from ..keyboards.keyboards_master import get_keyboards_masters
from ..keyboards.keyboards_my_book import get_cards_appoiment

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    keyboard = await get_keyboard_start()
    await message.answer(
        "Здраствуйте!\n"
        + "это бот предназначен для записиси к мастеру\n"
        + "Нажмите команду my_book для просмотра ваши записей или "
        + "на booking чтобы записаться",
        reply_markup=keyboard,
    )


@router.message(Command("my_book"))
async def cmd_my_appoiments(message: Message):
    cards, error = await get_cards_appoiment(message.from_user.id)

    if error:
        await message.answer(text="Ошибка")
        return

    if not cards:
        await message.answer(text="У вас нет записей")
        return

    for i in range(0, len(cards), 2):
        text = cards[i]
        keyboard = cards[i + 1] if i + 1 < len(cards) else None
        await message.answer(text=text, reply_markup=keyboard)


@router.message(Command("booking"))
async def cmd_booking(message: Message):
    keyboard = await get_keyboards_masters()
    await message.answer("Выберете мастера из списка", reply_markup=keyboard)
