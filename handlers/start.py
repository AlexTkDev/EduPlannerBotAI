from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Hi! I am a bot for creating study plans.\n"
        "Use the /plan command to start creating a study plan.")
