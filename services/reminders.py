import asyncio
import logging
from aiogram import Bot

logger = logging.getLogger(__name__)


async def schedule_reminders(user_id: int, plan: list, bot: Bot):
    """Schedule reminders for study plan steps and send messages to the user"""
    logger.info("Scheduling reminders for user %s", user_id)

    count = 0
    for i, task in enumerate(plan, start=1):
        if task.strip():  # Skip empty lines in plan
            await asyncio.sleep(0.1)  # Simulate delay for scheduling
            reminder_text = f"⏰ Reminder {i}: {task}"
            try:
                await bot.send_message(user_id, reminder_text)
            except Exception as e:
                logger.error("Failed to send reminder to %s: %s", user_id, e)
            logger.info("Reminder for %s: day %s — %s", user_id, i, task)
            count += 1

    return count  # Return number of reminders
