from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from bot.keyboards.main_keyboard import get_main_keyboard
from bot.keyboards.inline_keyboards import get_start_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обробка команди /start"""
    user_name = message.from_user.first_name

    welcome_text = (
        f"👋 <b>Вітаю, {user_name}!</b>\n\n"
        f"Я — віртуальний консультант автосервісу <b>AutoSpark</b>.\n\n"
        f"🔧 <b>Ми знаходимось у Чернівцях:</b>\n"
        f"📍 вул. Олександра Маланчука, 49\n\n"
        f"Я можу:\n"
        f"✅ Розповісти про наші послуги\n"
        f"✅ Розшифрувати коди помилок\n"
        f"✅ Порадити вирішення проблем\n"
        f"✅ Показати як нас знайти\n"
        f"✅ Записати на сервіс\n\n"
        f"Оберіть тему нижче або просто напишіть своє питання!"
    )

    await message.answer(welcome_text, reply_markup=get_start_keyboard())
    await message.answer(
        "Використовуйте кнопки нижче для навігації:",
        reply_markup=get_main_keyboard()
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обробка команди /help"""
    help_text = (
        "❓ <b>Допомога</b>\n\n"
        "<b>Доступні команди:</b>\n"
        "/start - Почати роботу\n"
        "/help - Показати допомогу\n"
        "/services - Список послуг\n"
        "/prices - Ціни\n"
        "/contacts - Контакти та адреса\n"
        "/location - Як нас знайти\n"
        "/booking - Записатися на сервіс\n\n"
        "<b>Або просто напишіть:</b>\n"
        "• Назву послуги (наприклад, \"діагностика\")\n"
        "• Код помилки (наприклад, \"P0301\")\n"
        "• Своє питання\n\n"
        "<i>Я постараюсь допомогти!</i>"
    )
    await message.answer(help_text)