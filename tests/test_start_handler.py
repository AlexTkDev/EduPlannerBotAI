import pytest
from aiogram.types import Message
from handlers.start import start_handler

class DummyBot:
    async def send_message(self, chat_id, text, **kwargs):
        self.last_message = (chat_id, text)
        return None

class DummyMessage:
    def __init__(self):
        self.text = "/start"
        self.chat = type("Chat", (), {"id": 1})()
        self.from_user = type("User", (), {"id": 1})()
        self.answer_text = None
    async def answer(self, text):
        self.answer_text = text
        return text

@pytest.mark.asyncio
async def test_start_handler():
    message = DummyMessage()
    await start_handler(message)
    assert message.answer_text is not None
    assert "bot for creating study plans" in message.answer_text 