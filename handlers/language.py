from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from services.db import set_user_language, get_user_language
from services.llm import translate_text
from handlers.planner import send_translated

router = Router()

LANGUAGES = {
    "en": "English",
    "ru": "Русский",
    "es": "Español",
}

@router.message(Command("language"))
async def choose_language(message: types.Message, state: FSMContext):
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

@router.message(F.text.in_(LANGUAGES.values()))
async def set_language(message: types.Message, state: FSMContext):
    lang_code = [k for k, v in LANGUAGES.items() if v == message.text][0]
    user_id = message.from_user.id if message.from_user else 0
    set_user_language(user_id, lang_code)
    lang_set_msg = await translate_text(f"Language set to {LANGUAGES[lang_code]}", lang_code)
    await send_translated(message, lang_set_msg)
    await message.answer(lang_set_msg, reply_markup=types.ReplyKeyboardRemove())
    await state.clear()
    # Send greeting and next-step instruction in the chosen language
    greeting = (
        "👋 Hi! I am a bot for creating study plans.\n"
        "Use the /plan command to start creating a study plan."
    )
    if lang_code != "en":
        greeting = await translate_text(greeting, lang_code)
    await send_translated(message, greeting) 