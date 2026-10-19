# database/ai_logs.py
from bot.database.connection import db


async def log_ai_question(user_id: int, question: str, answer: str,
                          intent: str, response_time: float):
    """Логування AI-запитів"""
    async with db.pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO ai_logs 
            (user_id, question, answer, intent, response_time, created_at)
            VALUES ($1, $2, $3, $4, $5, NOW())
            """,
            user_id, question, answer, intent, response_time
        )