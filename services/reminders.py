import asyncio
import logging

logger = logging.getLogger(__name__)


async def schedule_reminders(user_id: int, plan: list):
    """Schedule reminders for study plan steps"""
    logger.info("Scheduling reminders for user %s", user_id)

    for i, task in enumerate(plan, start=1):
        if task.strip():  # Skip empty lines in plan
            await asyncio.sleep(0.1)  # Simulate delay for scheduling
            logger.info("Reminder for %s: day %s — %s", user_id, i, task)

    return len([task for task in plan if task.strip()])  # Return number of reminders
