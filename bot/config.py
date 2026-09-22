import os
from pathlib import Path
from dotenv import load_dotenv

# Завантажуємо .env файл
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Інформація про сервіс
SERVICE_INFO = {
    "name": "AutoSpark Pro",
    "city": "Чернівці",
    "address": "вул. Олександра Маланчука, 49",
    "phone": "+380 95 212 02 35",
    "email": "autospark.ua@gmail.com",
    "working_hours": "Пн-Сб: 9:00 - 19:00, Нд: вихідний",
    "latitude": 48.2734,  # Координати для карти
    "longitude": 25.9345,
}

# База даних (опційно)
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "autoservice"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
}

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

# Параметри
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 500))
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.3))

# Налаштування бота
BOT_NAME = "AutoSpark Bot"
BOT_DESCRIPTION = "Віртуальний консультант автосервісу"