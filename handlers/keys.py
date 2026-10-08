from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from bot.keyboards.inline_keyboards import get_keys_keyboard

router = Router()


@router.message(Command("keys"))
async def cmd_keys(message: Message):
    """Команда /keys"""
    text = (
        "🔑 <b>Реєстрація ключів</b>\n\n"
        "Ми виконуємо:\n"
        "• Реєстрацію нових ключів\n"
        "• Дублювання чіпів\n"
        "• Програмування брелоків\n"
        "• Ремонт ключів\n\n"
        "<b>Типи ключів:</b>\n"
        "• Транспондерні (ID48, ID46, 4D, 8A)\n"
        "• Смарт-ключі\n"
        "• Дистанційні брелоки\n\n"
        "<b>Вартість:</b> від 800 грн\n"
        "<b>Час:</b> 30-90 хвилин"
    )
    await message.answer(text, reply_markup=get_keys_keyboard())


@router.callback_query(F.data == "key_types")
async def process_key_types(callback: CallbackQuery):
    """Інформація про типи ключів"""
    text = (
        "📋 <b>Типи ключів та чипів</b>\n\n"
        "1️⃣ <b>Транспондерні:</b>\n"
        "• ID48 - VAG група\n"
        "• ID46 - більшість азіатських авто\n"
        "• 4D - Toyota, Lexus\n"
        "• 8A - деякі європейські\n\n"
        "2️⃣ <b>Смарт-ключі:</b>\n"
        "• Proximity (безключовий доступ)\n"
        "• Start/Stop система\n\n"
        "3️⃣ <b>Дистанційні:</b>\n"
        "• Звичайні брелоки\n"
        "• З автозапуском\n\n"
        "<i>Не впевнені який у вас ключ? Напишіть марку авто!</i>"
    )
    await callback.message.answer(text)
    await callback.answer()