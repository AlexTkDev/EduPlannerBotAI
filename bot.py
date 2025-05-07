import logging
import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from config import TOKEN
from handlers import start, planner

# Создаем необходимые директории
os.makedirs("plans", exist_ok=True)
os.makedirs("fonts", exist_ok=True)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# Register handlers
dp.include_router(start.router)
dp.include_router(planner.router)

if __name__ == "__main__":
    async def main():
        try:
            logger.info("Starting bot...")
            await dp.start_polling(bot)
        except (KeyboardInterrupt, SystemExit):
            logger.info("Bot stopped!")
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Error starting bot: %s", e)


    asyncio.run(main())
