import asyncpg
from typing import Optional

from bot.config import DB_CONFIG


class Database:
    """Клас для роботи з PostgreSQL"""

    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        """Створення пулу підключень"""
        self.pool = await asyncpg.create_pool(**DB_CONFIG)
        print("✅ Підключено до PostgreSQL")

    async def disconnect(self):
        """Закриття пулу"""
        if self.pool:
            await self.pool.close()
            print("❌ Відключено від PostgreSQL")

    async def add_client(self, telegram_id: int, name: str, phone: str = None):
        """Додавання клієнта"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO clients (telegram_id, name, phone)
                VALUES ($1, $2, $3)
                ON CONFLICT (telegram_id) DO UPDATE
                SET name = $2, phone = $3
                """,
                telegram_id, name, phone
            )

    async def get_client_history(self, telegram_id: int):
        """Отримання історії клієнта"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT d.date, d.ecu_type, d.dtc_codes, c.brand, c.model
                FROM diagnostics d
                JOIN cars c ON d.car_id = c.id
                JOIN clients cl ON c.client_id = cl.id
                WHERE cl.telegram_id = $1
                ORDER BY d.date DESC
                LIMIT 10
                """,
                telegram_id
            )
            return rows


# Глобальний екземпляр
db = Database()