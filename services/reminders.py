import asyncio
import logging

logger = logging.getLogger(__name__)


async def schedule_reminders(user_id: int, plan: list):
    """Schedule reminders for study plan steps"""
    logger.info("Scheduling reminders for user %s", user_id)

    for i, task in enumerate(plan, start=1):
        if task.strip():  # Skip empty lines in plan
            await asyncio.sleep(0.1)  # Simulate delay for scheduling
            logger.info(f"Reminder for {user_id}: day {i} — {task}")

    return len([task for task in plan if task.strip()])  # Return number of reminders

    # Add handler for reminders in handlers/planner.py
    # Update handle_topic and add new callback_handler

    # In handle_topic method add:
    # Save plan in state for later use
    await state.update_data(plan=plan)


# Добавить новый callback handler для напоминаний:
@router.callback_query(PlanFormat.waiting_for_next_action, F.data == "schedule_reminders")
async def handle_reminders(callback: types.CallbackQuery, state: FSMContext):
    from services.reminders import schedule_reminders

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

    # Update keyboard in handle_topic, adding button for reminders:
    await message.answer(
        "Что ещё ты хотел бы сделать?",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="📊 Визуализировать план",
                                            callback_data="visualize_plan")],
                [types.InlineKeyboardButton(text="⏰ Запланировать напоминания",
                                            callback_data="schedule_reminders")],
                [types.InlineKeyboardButton(text="🔄 Создать новый план",
                                            callback_data="new_plan")],
                [types.InlineKeyboardButton(text="👋 Ничего, хорошего дня!",
                                            callback_data="goodbye")]
            ]
        )
    )
