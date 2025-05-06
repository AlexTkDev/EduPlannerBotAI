from aiogram import Router, types

router = Router()


@router.message(lambda msg: msg.text and msg.text.lower() in {"/start", "start"})
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот для создания учебных планов. Напиши, что хочешь изучить.")
