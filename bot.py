import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from config import TOKEN
from handlers import start, planner

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# Register handlers
dp.include_router(start.router)
dp.include_router(planner.router)

if __name__ == "__main__":
    import asyncio


    async def main():
        await dp.start_polling(bot)


    asyncio.run(main())
