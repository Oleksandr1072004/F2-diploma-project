import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from handlers.start import router as start_router
from handlers.menu import router as menu_router
from handlers.diagnostics import router as diagnostics_router
from handlers.keys import router as keys_router
from handlers.faq import router as faq_router

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


async def main():
    # Ініціалізація бота
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Реєстрація роутерів
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(diagnostics_router)
    dp.include_router(keys_router)
    dp.include_router(faq_router)

    # Запуск бота
    logger.info("Бот запущено!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
