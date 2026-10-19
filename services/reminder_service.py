# services/reminder_service.py

import asyncio
from datetime import datetime, timedelta


class ReminderService:
    """Сервіс нагадувань"""

    def __init__(self, bot):
        self.bot = bot
        self.reminders = []

    async def check_reminders(self):
        """Перевірка нагадувань кожну годину"""
        while True:
            current_time = datetime.now()

            for reminder in self.reminders:
                if reminder['time'] <= current_time:
                    await self.send_reminder(reminder)
                    self.reminders.remove(reminder)

            await asyncio.sleep(3600)  # Перевірка кожну годину

    async def send_reminder(self, reminder):
        """Відправка нагадування"""
        text = (
            f"⏰ <b>Нагадування!</b>\n\n"
            f"Час провести {reminder['service_name']} для вашого "
            f"{reminder['car_brand']} {reminder['car_model']}.\n\n"
            f"📅 Заплановано: {reminder['planned_date']}\n"
            f"📞 Зателефонуйте: +380 95 212 02 35"
        )
        await self.bot.send_message(reminder['user_id'], text)