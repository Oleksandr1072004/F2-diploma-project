from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, Location
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.config import SERVICE_INFO

router = Router()


@router.message(Command("contacts"))
async def cmd_contacts(message: Message):
    """Команда /contacts - контакти та адреса"""
    text = (
        "📞 <b>Наші контакти</b>\n\n"
        f"🏢 <b>{SERVICE_INFO['name']}</b>\n"
        f"📍 <b>Адреса:</b> {SERVICE_INFO['address']}\n"
        f"🏙 <b>Місто:</b> {SERVICE_INFO['city']}\n\n"
        f"📱 <b>Телефон:</b> {SERVICE_INFO['phone']}\n"
        f"📧 <b>Email:</b> {SERVICE_INFO['email']}\n"
        f"🕐 <b>Графік роботи:</b>\n{SERVICE_INFO['working_hours']}"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📍 Показати на карті",
                callback_data="show_location"
            )
        ],
        [
            InlineKeyboardButton(
                text="🗺 Відкрити в Google Maps",
                url=f"https://www.google.com/maps/search/{SERVICE_INFO['address']}, {SERVICE_INFO['city']}"
            )
        ],
        [
            InlineKeyboardButton(
                text="📞 Зателефонувати",
                callback_data="call_phone"
            )
        ],
    ])

    await message.answer(text, reply_markup=keyboard)


@router.message(Command("location"))
async def cmd_location(message: Message):
    """Команда /location - як нас знайти"""
    text = (
        "📍 <b>Як нас знайти</b>\n\n"
        f"Ми знаходимось за адресою:\n"
        f"<b>{SERVICE_INFO['city']}, {SERVICE_INFO['address']}</b>\n\n"
        "<b>Орієнтири:</b>\n"
        "• Поруч з автозаправкою\n"
        "• В'їзд з вулиці Маланчука\n"
        "• Є безкоштовна парковка\n\n"
        "<i>Натисніть кнопку нижче, щоб відкрити карту 👇</i>"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🗺 Відкрити Google Maps",
                url="https://www.google.com/maps/place/FGAuto/@48.2638244,25.9646303,973m/data=!3m2!1e3!4b1!4m6!3m5!1s0x473409cc34d64b6b:0x60399bfa2036ebe4!8m2!3d48.2638209!4d25.9672052!16s%2Fg%2F11ngjr44jx?entry=ttu&g_ep=EgoyMDI2MDkwOS4wIKXMDSoASAFQAw%3D%3D"
            )
        ],
        [
            InlineKeyboardButton(
                text="📍 Надіслати локацію",
                callback_data="send_location"
            )
        ],
    ])

    await message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data == "show_location")
async def process_show_location(callback: CallbackQuery):
    """Відправка локації"""
    await callback.message.answer_location(
        latitude=SERVICE_INFO['latitude'],
        longitude=SERVICE_INFO['longitude'],
    )
    await callback.answer()


@router.callback_query(F.data == "send_location")
async def process_send_location(callback: CallbackQuery):
    """Надсилання локації"""
    await callback.message.answer_location(
        latitude=48.26373,
        longitude=25.96719,
        title=SERVICE_INFO['name'],
        address=f"{SERVICE_INFO['city']}, {SERVICE_INFO['address']}",
        foursquare_id=""
    )
    await callback.answer()


@router.callback_query(F.data == "call_phone")
async def process_call(callback: CallbackQuery):
    """Показати номер телефону"""
    await callback.message.answer(
        f"📞 <b>Телефон для зв'язку:</b>\n\n"
        f"<code>{SERVICE_INFO['phone']}</code>\n\n"
        f"Натисніть на номер, щоб зателефонувати!"
    )
    await callback.answer()


@router.message(F.text == "📞 Контакти")
async def text_contacts(message: Message):
    """Обробка кнопки 'Контакти' з клавіатури"""
    await cmd_contacts(message)


@router.message(F.text == "📍 Адреса")
async def text_address(message: Message):
    """Обробка кнопки 'Адреса' з клавіатури"""
    await cmd_location(message)