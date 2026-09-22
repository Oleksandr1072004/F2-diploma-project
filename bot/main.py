import asyncio
import logging
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN, GEMINI_API_KEY

# Імпорт роутерів
from handlers.start import router as start_router
from handlers.menu import router as menu_router
from handlers.diagnostics import router as diagnostics_router
from handlers.keys import router as keys_router
from handlers.contacts import router as contacts_router
from handlers.faq import router as faq_router
from handlers.ai_chat import router as ai_router  # НОВИЙ

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


async def main():
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN не знайдено!")
        return

    if not GEMINI_API_KEY:
        logger.warning("⚠️ GEMINI_API_KEY не знайдено! AI-режим буде недоступний.")

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Реєстрація роутерів (ВАЖЛИВО: ai_router — ОСТАННІЙ!)
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(diagnostics_router)
    dp.include_router(keys_router)
    dp.include_router(contacts_router)
    dp.include_router(ai_router)  # AI обробляє все, що не обробили інші
    dp.include_router(faq_router)  # FAQ — останній fallback

    logger.info("🤖 AutoSpark Bot запущено!")

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Помилка: {e}")
    finally:
        await bot.session.close()
        logger.info("👋 Бот зупинено!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Бот зупинено користувачем!")