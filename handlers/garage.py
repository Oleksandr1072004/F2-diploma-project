# handlers/garage.py
from aiogram.dispatcher import router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot.database.connection import db


@router.message(Command("my_car"))
async def my_car(message: Message):
    """Особистий гараж клієнта"""
    user_id = message.from_user.id

    # Перевіряємо чи є авто в базі
    cars = await db.get_user_cars(user_id)

    if not cars:
        text = (
            "🚗 <b>Ваш гараж порожній</b>\n\n"
            "Додайте свій автомобіль, щоб:\n"
            "• Отримувати персоналізовані поради\n"
            "• Швидше записуватися на сервіс\n"
            "• Отримувати нагадування про ТО\n"
            "• Мати історію обслуговування\n\n"
            "Бажаєте додати авто?"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="➕ Додати авто", callback_data="add_car")],
        ])
    else:
        text = "🚗 <b>Ваші автомобілі:</b>\n\n"
        for car in cars:
            text += f"• {car['brand']} {car['model']} ({car['year']})\n"
            text += f"  VIN: {car['vin']}\n"
            text += f"  Останнє ТО: {car['last_service']}\n\n"

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="➕ Додати авто", callback_data="add_car")],
            [InlineKeyboardButton(text="📅 Записати на ТО", callback_data="book_service")],
        ])

    await message.answer(text, reply_markup=keyboard)