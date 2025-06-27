import pytest
import asyncio
from services.reminders import schedule_reminders

@pytest.mark.asyncio
async def test_schedule_reminders():
    user_id = 1
    plan = ["Task 1", "Task 2", "Task 3", ""]  # The last empty one should not be counted
    count = await schedule_reminders(user_id, plan)
    assert count == 3 