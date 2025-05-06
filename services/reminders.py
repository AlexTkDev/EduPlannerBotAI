import asyncio

async def schedule_reminders(user_id: int, plan: list):
    # Emulate scheduling reminders
    for i, task in enumerate(plan, start=1):
        await asyncio.sleep(0.1)  # Imitate delay for scheduling
        print(f"Напоминание для {user_id}: день {i} — {task}")
