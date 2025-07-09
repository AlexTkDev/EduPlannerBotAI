from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types.message import Message

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
    await message.answer("Send the topic for your study plan 📚")


@router.message(PlanFormat.waiting_for_topic)
async def handle_topic(message: types.Message, state: FSMContext):
    if not message or not message.text:
        await message.answer("Error: could not get message text.")
        return
    topic = message.text.strip()

    # Send waiting message
    waiting_message = await message.answer(
        "⏳ Please wait a moment. Generating your study plan...")

    # Send "typing" action to show the bot is working
    if message.bot and message.chat and message.chat.id:
        await message.bot.send_chat_action(message.chat.id, "typing")

    # Generate plan
    plan = await generate_study_plan(topic)
    save_user_plan(message.from_user.id if message.from_user else 0, plan)
    await state.update_data(plan=plan)

    # Delete waiting message
    await waiting_message.delete()

    # Send plan to chat
    plan_text = "\n".join(plan)
    if len(plan_text) > 4000:
        plan_text = plan_text[:4000] + "...\n(The plan is too long, the full version will \
             be in the file)"

    await message.answer(f"📚 Your study plan:\n\n{plan_text}")

    # Ask for format
    await state.set_state(PlanFormat.waiting_for_format)
    await message.answer(
        "In which format do you want to save the plan?",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="📄 pdf", callback_data="format_pdf"
                    ),
                    types.InlineKeyboardButton(
                        text="📄 txt", callback_data="format_txt"
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        text="🔄 Skip", callback_data="format_skip"
                    )
                ],
            ]
        ),
    )


@router.callback_query(PlanFormat.waiting_for_format, F.data.startswith("format_"))
async def process_format(callback: types.CallbackQuery, state: FSMContext):
    selected_format = callback.data.split("_")[1] if callback.data else ""
    await callback.answer()
    user_data = await state.get_data()
    plan = user_data.get("plan", [])
    if not plan:
        if isinstance(callback.message, Message):
            await callback.message.answer("Plan not found. Try creating a new one.")
        return
    if selected_format == "pdf":
        pdf_path = save_plan_to_pdf(plan, callback.from_user.id if callback.from_user else 0)
        if isinstance(callback.message, Message):
            await callback.message.answer_document(
                document=types.FSInputFile(pdf_path),
                caption="📘 Your study plan in PDF"
            )
    else:
        txt_path = await save_plan_to_txt(
            plan, callback.from_user.id if callback.from_user else 0)
        if isinstance(callback.message, Message):
            await callback.message.answer_document(
                document=types.FSInputFile(txt_path),
                caption=(
                    "📚 Your saved study plan"
                ),
            )
    if isinstance(callback.message, Message):
        await show_next_actions(callback.message, state)


async def show_next_actions(message: types.Message, state: FSMContext):
    if not isinstance(message, Message):
        return
    await state.set_state(PlanFormat.waiting_for_next_action)
    await message.answer(
        "What else would you like to do?",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="⏰ Schedule reminders",
                                            callback_data="schedule_reminders")],
                [types.InlineKeyboardButton(text="🔄 Create a new plan",
                                            callback_data="new_plan")],
                [types.InlineKeyboardButton(text="👋 Nothing, have a nice day!",
                                            callback_data="goodbye")]
            ]
        )
    )


@router.callback_query(PlanFormat.waiting_for_next_action, F.data == "schedule_reminders")
async def handle_reminders(callback: types.CallbackQuery, state: FSMContext):
    from services.reminders import schedule_reminders  # pylint: disable=import-outside-toplevel
    await callback.answer()
    user_id = callback.from_user.id if callback.from_user else 0
    user_data = await state.get_data()
    plan = user_data.get("plan", [])
    if not plan:
        if isinstance(callback.message, Message):
            await callback.message.answer("Plan not found. Try creating a new one.")
        return
    # Start reminder scheduling
    message = await callback.message.answer("⏳ Scheduling reminders...") if isinstance(
        callback.message, Message
        ) else None
    # Run async reminder scheduling task
    if callback.bot is None:
        if isinstance(callback.message, Message):
            await callback.message.answer("Internal error: bot instance is not available.")
        return
    reminders_count = await schedule_reminders(user_id, plan, callback.bot)
    # Update message after scheduling completion
    if isinstance(message, Message):
        await message.edit_text(
            f"✅ {reminders_count} reminders scheduled for your study plan"
        )


@router.callback_query(PlanFormat.waiting_for_next_action, F.data == "new_plan")
async def handle_new_plan(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    if isinstance(callback.message, Message):
        await callback.message.edit_text("Creating a new plan!")
        await cmd_plan(callback.message, state)


@router.callback_query(PlanFormat.waiting_for_next_action, F.data == "goodbye")
async def handle_goodbye(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    if isinstance(callback.message, Message):
        await callback.message.edit_text("Have a nice day! 👋 I'll be happy to help \
             again when you need it.")
    await state.clear()


@router.message(Command("myplans"))
async def cmd_my_plans(message: types.Message):
    if not isinstance(message, Message):
        return
    user_id = message.from_user.id if message.from_user else 0
    plan = get_user_plan(user_id)
    if not plan:
        await message.answer(
            "You don't have any saved study plans yet. Use /plan to create a new one.")
        return
    plan_text = "\n".join(plan)
    if len(plan_text) > 4000:
        txt_path = await save_plan_to_txt(plan, user_id)
        await message.answer_document(document=types.FSInputFile(txt_path),
                                      caption="📚 Your saved study plan")
    else:
        await message.answer(
            f"📚 Your saved study plan:\n\n{plan_text}"
        )
