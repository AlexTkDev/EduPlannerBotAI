from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот для создания учебных планов.\n"
        "Используй команду /plan чтобы начать создание плана обучения.")
