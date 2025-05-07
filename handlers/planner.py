from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from services.llm import generate_study_plan
from services.pdf import save_plan_to_pdf
from services.txt import save_plan_to_txt
from services.db import save_user_plan

router = Router()


class PlanFormat(StatesGroup):
    """State machine for selecting the format of the study plan."""
    waiting_for_format = State()
    waiting_for_topic = State()
    waiting_for_next_action = State()

    def __str__(self):
        return "PlanFormat FSM"


@router.message(Command("plan"))
async def cmd_plan(message: types.Message, state: FSMContext):
    await state.set_state(PlanFormat.waiting_for_format)
    await message.answer(
        "В каком формате хочешь получить план?\nВыбери: ",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="📄 pdf", callback_data="format_pdf")],
                [types.InlineKeyboardButton(text="📄 txt", callback_data="format_txt")]
            ]
        )
    )


@router.callback_query(F.data.startswith("format_"))
async def process_format(callback: types.CallbackQuery, state: FSMContext):
    selected_format = callback.data.split("_")[1]
    await state.update_data(selected_format=selected_format)
    await state.set_state(PlanFormat.waiting_for_topic)
    await callback.message.edit_text("Теперь отправь тему для учебного плана 📚")
    await callback.answer()


@router.message(PlanFormat.waiting_for_topic)
async def handle_topic(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    selected_format = user_data.get("selected_format")
    topic = message.text.strip()

    plan = await generate_study_plan(topic)
    save_user_plan(message.from_user.id, plan)

    if selected_format == "pdf":
        pdf_path = save_plan_to_pdf(plan, message.from_user.id)
        await message.answer_document(document=types.FSInputFile(pdf_path),
                                      caption="📘 Твой учебный план в PDF")
    else:
        # Using the txt module instead of inline text conversion
        txt_path = save_plan_to_txt(plan, message.from_user.id)
        await message.answer_document(
            document=types.FSInputFile(txt_path),
            caption="📄 Твой учебный план в TXT")

    await state.set_state(PlanFormat.waiting_for_next_action)
    await message.answer(
        "Что ещё ты хотел бы сделать?",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="🔄 Создать новый план",
                                            callback_data="new_plan")],
                [types.InlineKeyboardButton(text="👋 Ничего, хорошего дня!",
                                            callback_data="goodbye")]
            ]
        )
    )


@router.callback_query(PlanFormat.waiting_for_next_action, F.data == "new_plan")
async def handle_new_plan(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text("Создаем новый план!")
    await cmd_plan(callback.message, state)


@router.callback_query(PlanFormat.waiting_for_next_action, F.data == "goodbye")
async def handle_goodbye(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text("Хорошего дня! 👋 Буду рад помочь снова, когда понадобится.")
    await state.clear()
