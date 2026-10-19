from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Головна клавіатура бота"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🔍 Діагностика"),
                KeyboardButton(text="🔑 Ключі"),
            ],
            [
                KeyboardButton(text="💡 Оптика"),
                KeyboardButton(text="⚡ Прошивка"),
            ],
            [
                KeyboardButton(text="🛡 Сигналізація"),
                KeyboardButton(text="🔧 Retrofit"),
            ],
            [
                KeyboardButton(text="🇺🇸 USA > EU"),
                KeyboardButton(text="💰 Ціни"),
            ],
            [
                KeyboardButton(text="📞 Контакти"),
                KeyboardButton(text="📍 Адреса"),
            ],
        ],
        resize_keyboard=True,
        persistent=True,
    )
    return keyboard