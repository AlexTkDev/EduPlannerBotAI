from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from services.llm import generate_study_plan
from services.pdf import save_plan_to_pdf
from services.txt import save_plan_to_txt
from services.db import save_user_plan, get_user_plan

router = Router()


class PlanFormat(StatesGroup):
    """State machine for selecting the format of the study plan."""
    waiting_for_topic = State()
    waiting_for_format = State()
    waiting_for_next_action = State()

    def __str__(self):
        return "PlanFormat FSM"


@router.message(Command("plan"))
async def cmd_plan(message: types.Message, state: FSMContext):
    await state.set_state(PlanFormat.waiting_for_topic)
    await message.answer("Отправь тему для учебного плана 📚")


@router.message(PlanFormat.waiting_for_topic)
async def handle_topic(message: types.Message, state: FSMContext):
    topic = message.text.strip()

    # Send "typing" action to show the bot is working
    await message.bot.send_chat_action(message.chat.id, "typing")

    # Generate plan
    plan = await generate_study_plan(topic)
    save_user_plan(message.from_user.id, plan)
    await state.update_data(plan=plan)

    # Send plan to chat
    plan_text = "\n".join(plan)
    if len(plan_text) > 4000:
        plan_text = plan_text[:4000] + "...\n(план слишком длинный, полная версия будет в файле)"

    await message.answer(f"📚 Твой учебный план:\n\n{plan_text}")

    # Ask for format
    await state.set_state(PlanFormat.waiting_for_format)
    await message.answer(
        "В каком формате хочешь сохранить план?",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="📄 pdf", callback_data="format_pdf"),
                 types.InlineKeyboardButton(text="📄 txt", callback_data="format_txt")],
                [types.InlineKeyboardButton(text="🔄 Пропустить", callback_data="format_skip")]
            ]
        )
    )


@router.callback_query(PlanFormat.waiting_for_format, F.data.startswith("format_"))
async def process_format(callback: types.CallbackQuery, state: FSMContext):
    selected_format = callback.data.split("_")[1]
    await callback.answer()

    if selected_format == "skip":
        await show_next_actions(callback.message, state)
        return

    user_data = await state.get_data()
    plan = user_data.get("plan", [])

    if not plan:
        await callback.message.answer("План не найден. Попробуйте создать новый.")
        return

    if selected_format == "pdf":
        pdf_path = save_plan_to_pdf(plan, callback.from_user.id)
        await callback.message.answer_document(
            document=types.FSInputFile(pdf_path),
            caption="📘 Твой учебный план в PDF"
        )
    else:
        txt_path = save_plan_to_txt(plan, callback.from_user.id)
        await callback.message.answer_document(
            document=types.FSInputFile(txt_path),
            caption="📄 Твой учебный план в TXT"
        )

    await show_next_actions(callback.message, state)


async def show_next_actions(message: types.Message, state: FSMContext):
    await state.set_state(PlanFormat.waiting_for_next_action)
    await message.answer(
        "Что ещё ты хотел бы сделать?",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="⏰ Запланировать напоминания",
                                            callback_data="schedule_reminders")],
                [types.InlineKeyboardButton(text="🔄 Создать новый план",
                                            callback_data="new_plan")],
                [types.InlineKeyboardButton(text="👋 Ничего, хорошего дня!",
                                            callback_data="goodbye")]
            ]
        )
    )


@router.callback_query(PlanFormat.waiting_for_next_action, F.data == "schedule_reminders")
async def handle_reminders(callback: types.CallbackQuery, state: FSMContext):
    from services.reminders import schedule_reminders  # pylint: disable=import-outside-toplevel

    await callback.answer()
    user_id = callback.from_user.id

    # Get plan from state
    user_data = await state.get_data()
    plan = user_data.get("plan", [])

    if not plan:
        await callback.message.answer("План не найден. Попробуйте создать новый.")
        return

    # Start reminder scheduling
    message = await callback.message.answer("⏳ Планирую напоминания...")

    # Run async reminder scheduling task
    reminders_count = await schedule_reminders(user_id, plan)

    # Update message after scheduling completion
    await message.edit_text(
        f"✅ Запланировано {reminders_count} напоминаний для твоего учебного плана"
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


@router.message(Command("myplans"))
async def cmd_my_plans(message: types.Message):
    user_id = message.from_user.id
    plan = get_user_plan(user_id)

    if not plan:
        await message.answer(
            "У тебя пока нет сохранённых учебных планов. Используй /plan чтобы создать новый.")
        return

    plan_text = "\n".join(plan)
    if len(plan_text) > 4000:
        txt_path = save_plan_to_txt(plan, user_id)
        await message.answer_document(document=types.FSInputFile(txt_path),
                                      caption="📚 Твой сохранённый учебный план")
    else:
        await message.answer(f"📚 Твой сохранённый учебный план:\n\n{plan_text}")
