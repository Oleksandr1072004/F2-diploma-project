from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from bot.services.faq_service import FAQService
from bot.keyboards.inline_keyboards import get_services_keyboard

router = Router()
faq_service = FAQService()

@router.message(Command("services"))
async def cmd_services(message: Message):
    """Показати всі послуги"""
    services_text = (
        "🔧 <b>Наші послуги</b>\n\n"
        "1️⃣ Діагностика та ремонт електроустаткування\n"
        "2️⃣ Монтаж охоронних систем\n"
        "3️⃣ Монтаж мультимедійних систем\n"
        "4️⃣ Шумо-віброізоляція\n"
        "5️⃣ Ремонт та відновлення оптики\n"
        "6️⃣ Прошивка мультимедії\n"
        "7️⃣ Реєстрація ключів\n"
        "8️⃣ Прошивка блоків ECU, TCU, SRS\n"
        "9️⃣ Монтаж та кодування опцій (retrofit)\n"
        "🔟 USA > EU конвертація\n\n"
        "<i>Оберіть послугу для детальної інформації</i>"
    )
    await message.answer(services_text, reply_markup=get_services_keyboard())

@router.callback_query(F.data == "menu_diag")
async def process_diag(callback: CallbackQuery):
    """Обробка кнопки 'Діагностика'"""
    answer = faq_service.search_answer("діагностика")
    if answer:
        await callback.message.answer(answer["answer"])
    await callback.answer()

@router.callback_query(F.data == "menu_keys")
async def process_keys(callback: CallbackQuery):
    """Обробка кнопки 'Ключі'"""
    answer = faq_service.search_answer("ключ")
    if answer:
        await callback.message.answer(answer["answer"])
    await callback.answer()

@router.callback_query(F.data == "menu_optics")
async def process_optics(callback: CallbackQuery):
    """Обробка кнопки 'Оптика'"""
    answer = faq_service.search_answer("оптика")
    if answer:
        await callback.message.answer(answer["answer"])
    await callback.answer()

@router.callback_query(F.data == "menu_firmware")
async def process_firmware(callback: CallbackQuery):
    """Обробка кнопки 'Прошивка'"""
    answer = faq_service.search_answer("прошивка")
    if answer:
        await callback.message.answer(answer["answer"])
    await callback.answer()

@router.callback_query(F.data == "menu_alarm")
async def process_alarm(callback: CallbackQuery):
    """Обробка кнопки 'Сигналізація'"""
    answer = faq_service.search_answer("сигналізація")
    if answer:
        await callback.message.answer(answer["answer"])
    await callback.answer()

@router.callback_query(F.data == "back_to_main")
async def process_back(callback: CallbackQuery):
    """Повернення в головне меню"""
    await callback.message.answer(
        "Повертаємось в головне меню:",
        reply_markup=get_services_keyboard()
    )
    await callback.answer()