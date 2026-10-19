from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import re

from bot.services.dtc_decoder import DTCDecoder
from bot.keyboards.inline_keyboards import get_diagnostics_keyboard

router = Router()
dtc_decoder = DTCDecoder()


@router.message(Command("diagnostics"))
async def cmd_diagnostics(message: Message):
    """Команда /diagnostics"""
    text = (
        "🔍 <b>Комп'ютерна діагностика</b>\n\n"
        "Ми виконуємо діагностику всіх електронних систем:\n"
        "• Двигун (ECU)\n"
        "• Коробка передач (TCU)\n"
        "• Подушки безпеки (SRS)\n"
        "• ABS/ESP\n"
        "• Клімат-контроль\n"
        "• Електрообладнання\n\n"
        "<b>Вартість:</b> від 500 грн\n"
        "<b>Час:</b> 30-60 хвилин\n\n"
        "<i>Напишіть код помилки (наприклад, P0301) для розшифровки!</i>"
    )
    await message.answer(text, reply_markup=get_diagnostics_keyboard())


@router.message(F.text.regexp(r'^[PBCU][0-9]{4}$'))
async def handle_dtc_code(message: Message):
    """Автоматична розшифровка DTC коду"""
    code = message.text.upper()
    decoded = dtc_decoder.decode(code)

    if decoded:
        response = dtc_decoder.format_for_telegram(decoded)
    else:
        response = (
            f"❌ <b>Код {code} не знайдено в базі.</b>\n\n"
            f"Перевірте правильність коду або "
            f"зверніться до майстра для консультації."
        )

    await message.answer(response)


@router.callback_query(F.data == "diag_book")
async def process_diag_booking(callback: CallbackQuery):
    """Запис на діагностику"""
    await callback.message.answer(
        "📅 <b>Запис на діагностику</b>\n\n"
        "Для запису зателефонуйте нам:\n"
        "📞 +380 95 212 02 35\n\n"
    )
    await callback.answer()