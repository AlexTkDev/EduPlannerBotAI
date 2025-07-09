import pytest
from services.reminders import schedule_reminders

class DummyBot:
    """A dummy bot for testing schedule_reminders without real Telegram API calls."""
    async def send_message(self, user_id, text):
        pass

@pytest.mark.asyncio
async def test_schedule_reminders():
    user_id = 1
    plan = ["Task 1", "Task 2", "Task 3", ""]  # The last empty one should not be counted
    bot = DummyBot()
    count = await schedule_reminders(user_id, plan, bot)
    assert count == 3 