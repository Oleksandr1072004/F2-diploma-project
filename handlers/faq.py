from aiogram import Router, F
from aiogram.types import Message
import re

from services.faq_service import FAQService
from services.dtc_decoder import DTCDecoder

router = Router()
faq_service = FAQService()
dtc_decoder = DTCDecoder()


# 1. DTC коди — P0301, C1234, B0028, U0100
@router.message(F.text.regexp(r'^[PpBbCcUu][0-9]{4}$'))
async def handle_dtc_code(message: Message):
    code = message.text.upper()
    decoded = dtc_decoder.decode(code)
    if decoded:
        response = dtc_decoder.format_for_telegram(decoded)
    else:
        response = (
            f"❌ <b>Код {code} не знайдено в базі.</b>\n\n"
            f"Перевірте правильність коду або зверніться до майстра."
        )
    await message.answer(response)


# 2. FAQ ключові слова
@router.message(F.text.lower().contains("діагностик"))
async def faq_diag(message: Message):
    answer = faq_service.search_answer("діагностика")
    await message.answer(answer["answer"])


@router.message(F.text.lower().contains("ключ"))
async def faq_keys(message: Message):
    answer = faq_service.search_answer("ключ")
    await message.answer(answer["answer"])


@router.message(F.text.lower().contains("прошивк"))
async def faq_firmware(message: Message):
    answer = faq_service.search_answer("прошивка")
    await message.answer(answer["answer"])


@router.message(F.text.lower().contains("оптик") | F.text.lower().contains("фар"))
async def faq_optics(message: Message):
    answer = faq_service.search_answer("оптика")
    await message.answer(answer["answer"])


@router.message(F.text.lower().contains("сигналізац"))
async def faq_alarm(message: Message):
    answer = faq_service.search_answer("сигналізація")
    await message.answer(answer["answer"])


@router.message(F.text.lower().contains("usa") | F.text.lower().contains("конвертац"))
async def faq_usa(message: Message):
    answer = faq_service.search_answer("usa")
    await message.answer(answer["answer"])


@router.message(F.text.lower().contains("retrofit") | F.text.lower().contains("ретрофіт"))
async def faq_retrofit(message: Message):
    answer = faq_service.search_answer("retrofit")
    await message.answer(answer["answer"])


# 3. Привітання
@router.message(F.text.lower().in_({"привіт", "добрий день", "вітаю", "hello", "hi"}))
async def handle_greeting(message: Message):
    await message.answer(
        "👋 Добрий день!\n\n"
        "Я допоможу вам з питаннями щодо:\n"
        "• Діагностики\n"
        "• Ремонту оптики\n"
        "• Реєстрації ключів\n"
        "• Прошивки блоків\n"
        "• Встановлення сигналізації\n\n"
        "Що вас цікавить? Або просто напишіть своє питання — "
        "я відповім як AI-помічник! 🤖"
    )


# 4. Локація
@router.message(F.text.lower().contains("де ви") | F.text.lower().contains("адрес"))
async def handle_location(message: Message):
    await message.answer(
        "📍 <b>Ми знаходимось у Чернівцях!</b>\n\n"
        "🏢 <b>Адреса:</b>\n"
        "вул. Олександра Маланчука, 49\n\n"
        "Використайте /location для детальної інформації."
    )


# 5. Ціни
@router.message(F.text.lower().in_({"ціна", "ціни", "вартість", "прайс"}))
async def handle_price(message: Message):
    await message.answer(
        "💰 <b>Орієнтовні ціни:</b>\n\n"
        "• Діагностика: від 500 грн\n"
        "• Реєстрація ключа: від 800 грн\n"
        "• Полірування фар: від 600 грн\n"
        "• Прошивка ECU: від 1500 грн\n"
        "• Сигналізація: від 3000 грн\n"
        "• USA > EU: від 2000 грн\n\n"
        "<i>Точна вартість залежить від марки авто та складності робіт.</i>"
    )