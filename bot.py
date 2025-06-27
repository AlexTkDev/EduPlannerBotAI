import logging
import asyncio
import os
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from config import TOKEN
from handlers import start, planner

# Create necessary directories
os.makedirs("plans", exist_ok=True)
os.makedirs("fonts", exist_ok=True)

# Проверка наличия токенов
if not TOKEN:
    print("[ERROR] BOT_TOKEN is not set in environment variables.", file=sys.stderr)
    sys.exit(1)

# Настройка логирования
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE = os.getenv("LOG_FILE")

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        *( [logging.FileHandler(LOG_FILE)] if LOG_FILE else [] )
    ]
)
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
