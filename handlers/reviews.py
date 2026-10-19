# handlers/reviews.py
from aiogram import F
from aiogram.dispatcher import router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


@router.message(Command("review"))
async def leave_review(message: Message):
    """Залишити відгук"""
    text = (
        "⭐ <b>Залиште відгук про нашу роботу!</b>\n\n"
        "Оберіть оцінку:"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="😡 1", callback_data="rate_1"),
            InlineKeyboardButton(text="😕 2", callback_data="rate_2"),
            InlineKeyboardButton(text="😐 3", callback_data="rate_3"),
            InlineKeyboardButton(text="🙂 4", callback_data="rate_4"),
            InlineKeyboardButton(text="😍 5", callback_data="rate_5"),
        ],
    ])

    await message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("rate_"))
async def process_rating(callback: CallbackQuery):
    """Обробка оцінки"""
    rating = int(callback.data.split("_")[1])

    if rating >= 4:
        response = "Дякуємо за високу оцінку! 🎉"
    else:
        response = "Дякуємо за відгук! Ми станемо краще."

    await callback.message.answer(response)
    await callback.answer()