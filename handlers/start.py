from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from handlers.language import LANGUAGES  # import language options
from handlers.planner import send_translated
from services.llm import translate_text
from services.db import get_user_language

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    await send_translated(
        message,
        "👋 Hi! I am a bot for creating study plans.\nUse the /plan command to start creating a study plan."
    )
    # Immediately prompt for language selection
    user_id = message.from_user.id if message.from_user else 0
    user_lang = get_user_language(user_id) or "en"
    # Do not translate language selection buttons so the filter works correctly
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=lang_name)] for lang_name in LANGUAGES.values()
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    prompt = await translate_text("Choose your language / Выберите язык:", user_lang)
    await send_translated(message, prompt)
    await message.answer(prompt, reply_markup=keyboard)
    await state.set_state("waiting_for_language")
