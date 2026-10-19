from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_start_keyboard() -> InlineKeyboardMarkup:
    """Клавіатура для стартового повідомлення"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔍 Діагностика", callback_data="service_diag"),
            InlineKeyboardButton(text="🔑 Ключі", callback_data="service_keys"),
        ],
        [
            InlineKeyboardButton(text="💡 Оптика", callback_data="service_optics"),
            InlineKeyboardButton(text="⚡ Прошивка", callback_data="service_firmware"),
        ],
        [
            InlineKeyboardButton(text="🛡 Сигналізація", callback_data="service_alarm"),
        ],
        [
            InlineKeyboardButton(text="📍 Як нас знайти", callback_data="show_location"),
        ],
        [
            InlineKeyboardButton(
                text="📞 Записатися на сервіс",
                url="https://t.me/vasili_84"
            ),
        ],
    ])
    return keyboard


def get_services_keyboard() -> InlineKeyboardMarkup:
    """Клавіатура з послугами"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔍 Діагностика", callback_data="service_diag"),
            InlineKeyboardButton(text="🛡 Сигналізація", callback_data="service_alarm"),
        ],
        [
            InlineKeyboardButton(text="💡 Оптика", callback_data="service_optics"),
            InlineKeyboardButton(text="🔧 Retrofit", callback_data="service_retrofit"),
        ],
        [
            InlineKeyboardButton(text="🔑 Ключі", callback_data="service_keys"),
            InlineKeyboardButton(text="⚡ Прошивка", callback_data="service_firmware"),
        ],
        [
            InlineKeyboardButton(
                text="🇺🇸 USA > EU конвертація",
                callback_data="service_usa_eu"
            ),
        ],
        [
            InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main"),
        ],
    ])
    return keyboard


def get_diagnostics_keyboard() -> InlineKeyboardMarkup:
    """Клавіатура для діагностики"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📅 Записатися", callback_data="diag_book"),
            InlineKeyboardButton(text="💰 Ціни", callback_data="show_prices"),
        ],
        [
            InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main"),
        ],
    ])
    return keyboard


def get_keys_keyboard() -> InlineKeyboardMarkup:
    """Клавіатура для ключів"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📋 Типи ключів", callback_data="key_types"),
        ],
        [
            InlineKeyboardButton(text="📅 Записатися", callback_data="key_booking"),
        ],
        [
            InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main"),
        ],
    ])
    return keyboard