from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ChatAction

from services.ai_service import AIService

router = Router()
ai_service = AIService()


@router.message(Command("ai"))
async def cmd_ai(message: Message):
    """Команда /ai — активація AI-режиму"""
    text = (
        "🤖 <b>AI-режим AutoSpark активовано!</b>\n\n"
        "Тепер я відповідаю на питання як справжній автоелектрик:\n"
        "• Коди помилок (OBD-II)\n"
        "• Симптоми несправностей\n"
        "• Терміни автоелектрики\n"
        "• Діагностика проводки\n"
        "• Ремонт оптики\n"
        "• Сигналізації та мультимедіа\n\n"
        "Просто напишіть своє питання! 👇\n\n"
        "<i>Наприклад: \"Що означає код P0301?\" або "
        "\"Не горить ближнє світло\"</i>"
    )
    await message.answer(text)


@router.message(Command("clear"))
async def cmd_clear(message: Message):
    """Очищення історії діалогу"""
    ai_service.clear_history(message.from_user.id)
    await message.answer(
        "🧹 Історію діалогу очищено!\n\n"
        "Тепер я не пам'ятаю попередні питання."
    )


@router.message(F.text == "🤖 AI-помічник")
async def text_ai_helper(message: Message):
    """Обробка кнопки 'AI-помічник'"""
    await cmd_ai(message)


@router.message(F.text)
async def handle_ai_question(message: Message):
    """AI-відповідь на будь-яке питання (fallback)"""
    question = message.text.strip()

    if len(question) < 3:
        return

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING
    )

    answer = await ai_service.get_answer(
        user_id=message.from_user.id,
        question=question
    )

    await message.answer(answer)


@router.callback_query(F.data == "ai_help")
async def process_ai_help(callback: CallbackQuery):
    """Допомога по AI-режиму"""
    text = (
        "🤖 <b>Як користуватися AI-помічником:</b>\n\n"
        "<b>Приклади питань:</b>\n"
        "• \"Що означає код P0301?\"\n"
        "• \"Не горить ближнє світло\"\n"
        "• \"Як перевірити датчик колінвала?\"\n"
        "• \"Чому запотівають фари?\"\n"
        "• \"Як підключити сигналізацію?\"\n"
        "• \"Що таке іммобілайзер?\"\n\n"
        "<b>Команди:</b>\n"
        "/ai — активувати AI-режим\n"
        "/clear — очистити історію діалогу\n"
        "/help — загальна допомога\n\n"
        "<i>Я відповідаю тільки на питання про автоелектрику та оптику!</i>"
    )
    await callback.message.answer(text)
    await callback.answer()