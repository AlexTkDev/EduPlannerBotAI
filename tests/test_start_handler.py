import pytest
from handlers.start import start_handler

class DummyBot:
    """Dummy bot for testing purposes."""
    def __init__(self):
        self.last_message = None
    async def send_message(self, chat_id, text):
        self.last_message = (chat_id, text)
        return None

class DummyMessage:
    """Dummy message for testing purposes."""
    def __init__(self):
        self.text = "/start"
        self.chat = type("Chat", (), {"id": 1})()
        self.from_user = type("User", (), {"id": 1})()
        self.answer_text = None
        self.all_answers = []
    async def answer(self, text, *_args, **_kwargs):
        self.answer_text = text
        self.all_answers.append(text)
        return text

class DummyState:
    """Dummy state for testing purposes."""
    async def set_state(self, *_args, **_kwargs):
        pass
    async def clear(self):
        pass

@pytest.mark.asyncio
async def test_start_handler():
    message = DummyMessage()
    state = DummyState()
    await start_handler(message, state)
    assert any("bot for creating study plans" in msg for msg in message.all_answers) 