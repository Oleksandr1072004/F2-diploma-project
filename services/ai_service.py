import logging
from typing import List, Dict
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from config import GEMINI_API_KEY, GEMINI_MODEL, MAX_TOKENS, TEMPERATURE

logger = logging.getLogger(__name__)


class AIService:
    """AI-сервіс для AutoSpark Bot на базі Google Gemini"""

    SYSTEM_PROMPT = """Ти — спеціалізований ШІ-помічник автосервісу AutoSpark у Чернівцях.

ТВОЯ СПЕЦІАЛІЗАЦІЯ:
1. Автоелектрика та електроніка автомобілів
2. Діагностика (OBD-II, DTC коди, датчики, проводка)
3. Ремонт та відновлення оптики (фари, лінзи, LED, ксенон)
4. Встановлення сигналізацій та охоронних систем
5. Монтаж мультимедійних систем
6. Прошивка блоків (ECU, TCU, SRS, BODY, ODO)
7. Реєстрація ключів та іммобілайзерів
8. USA > EU конвертація
9. Retrofit (встановлення додаткових опцій)
10. Шумо-віброізоляція

СТРОГІ ПРАВИЛА:
1. Відповідай ТІЛЬКИ на питання, пов'язані з:
   - Автоелектрикою та електронікою авто
   - Діагностикою (коди помилок, датчики, проводка)
   - Оптикою (фари, лінзи, LED, ксенон, полірування)
   - Сигналізаціями та охоронними системами
   - Мультимедіа та прошивками
   - Ключами та іммобілайзерами
   - Конвертацією USA > EU
   - Retrofit та додатковими опціями

2. Якщо питання НЕ стосується цих тем (кулінарія, політика, ремонт двигуна, ходова, кузовний ремонт) — ввічливо відмов:
   "Я — бот-автоелектрик AutoSpark. Я не можу допомогти з цим питанням. 
   Задайте питання по проводці, датчиках, оптиці або діагностиці."

3. Відповідай КОРОТКО, професійно, доступною мовою.

4. Якщо це діагностика — підкажи, які параметри або ланцюги перевірити:
   - "перевір масу"
   - "прозвони ланцюг мультиметром"
   - "перевір напругу на роз'ємі"
   - "заміряй опір датчика"

5. Для кодів помилок (P0301, C1234, B0028, U0100):
   - Розшифруй код
   - Вкажи систему (двигун, шасі, кузов, мережа)
   - Дай рекомендації щодо перевірки
   - Вкажи серйозність

6. Для оптики:
   - Поясни причини (помутніння, запотівання, несправність LED)
   - Дай поради щодо ремонту
   - Вкажи вартість (орієнтовно)

7. Якщо не впевнений — рекомендуй звернутися до майстра:
   "Для точної діагностики рекомендуємо записатися на прийом:
    📍 вул. Олександра Маланчука, 49, Чернівці"

8. НІКОЛИ не вигадуй технічні дані, яких не знаєш.
9. Використовуй професійну термінологію, але пояснюй просто.
10. Відповідай українською мовою (або мовою запитання).

ПРИКЛАДИ ПРАВИЛЬНИХ ВІДПОВІДЕЙ:

Питання: "Що означає код P0301?"
Відповідь: "🔧 P0301 — пропуски запалювання в 1-му циліндрі.
Система: Двигун (Powertrain)
Серйозність: Висока
Що перевірити:
• Свічку запалювання 1-го циліндра
• Котушку запалювання
• Форсунку
• Компресію в циліндрі
• Проводку до форсунки та котушки
Рекомендація: Замініть свічку, перевірте іскру. Якщо не допомогло — діагностика."

Питання: "Як приготувати борщ?"
Відповідь: "Я — бот-автоелектрик AutoSpark. Я не можу допомогти з цим питанням. 
Задайте питання по проводці, датчиках, оптиці або діагностиці."
"""

    def __init__(self):
        if not GEMINI_API_KEY:
            logger.warning("⚠️ GEMINI_API_KEY не встановлено!")

        # Налаштування Gemini
        genai.configure(api_key=GEMINI_API_KEY)

        # Налаштування безпеки (щоб не блокував відповіді)
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        # Параметри генерації
        self.generation_config = {
            "temperature": TEMPERATURE,
            "max_output_tokens": MAX_TOKENS,
            "top_p": 0.95,
            "top_k": 40,
        }

        # Ініціалізація моделі з системною інструкцією
        self.model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=self.SYSTEM_PROMPT,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
        )

        # Історія чатів (user_id -> chat session)
        self.chat_sessions: Dict[int, any] = {}

    async def get_answer(
            self,
            user_id: int,
            question: str,
            save_history: bool = True
    ) -> str:
        """Отримання відповіді від Gemini"""
        try:
            # Отримуємо або створюємо чат-сесію
            if save_history:
                if user_id not in self.chat_sessions:
                    self.chat_sessions[user_id] = self.model.start_chat(history=[])
                chat = self.chat_sessions[user_id]
            else:
                chat = self.model.start_chat(history=[])

            # Відправляємо запит
            response = await chat.send_message_async(question)

            # Перевіряємо чи є відповідь
            if not response.text:
                return (
                    "🤔 Не вдалося отримати відповідь. Спробуйте перефразувати.\n\n"
                    "📞 Або зателефонуйте: +380 95 212 02 35"
                )

            return response.text

        except Exception as e:
            logger.error(f"Помилка Gemini: {e}")
            error_msg = str(e).lower()

            if "quota" in error_msg or "rate" in error_msg or "429" in error_msg:
                return (
                    "⏳ Забагато запитів. Зачекайте хвилинку і спробуйте ще раз.\n\n"
                    "📞 Або зателефонуйте: +380 95 212 02 35"
                )
            elif "api key" in error_msg or "401" in error_msg or "403" in error_msg:
                return (
                    "🔑 Помилка авторизації AI. Зверніться до адміністратора.\n\n"
                    "📞 Або зателефонуйте: +380 95 212 02 35"
                )
            elif "timeout" in error_msg:
                return (
                    "⏱ Перевищено час очікування. Спробуйте ще раз.\n\n"
                    "📞 Або зателефонуйте: +380 95 212 02 35"
                )
            else:
                return (
                    f"❌ Вибачте, сталася помилка. Спробуйте пізніше.\n\n"
                    f"📞 Або зателефонуйте: +380 95 212 02 35"
                )

    def clear_history(self, user_id: int):
        """Очищення історії діалогу"""
        if user_id in self.chat_sessions:
            del self.chat_sessions[user_id]
            logger.info(f"Історію для user_id={user_id} очищено")

    async def is_auto_related(self, question: str) -> bool:
        """Швидка перевірка, чи питання стосується автотематики"""
        keywords = [
            "проводка", "датчик", "реле", "запобіжник", "маса", "плюс", "мінус",
            "напруга", "струм", "опір", "мультиметр", "осцилограф",
            "генератор", "стартер", "акумулятор", "батарея",
            "помилка", "код", "dtc", "obd", "діагностика", "сканер",
            "p0", "p1", "c0", "b0", "u0", "check engine", "чек",
            "фара", "оптика", "лінза", "led", "ксенон", "біксенон",
            "полірування", "світло", "ближнє", "дальнє", "габарит",
            "поворотник", "стоп", "протитуманка", "immobilazer",
            "сигналізація", "охорона", "автозапуск", "брелок", "імобілайзер", "іммобілайзер",
            "магнітола", "мультимедіа", "carplay", "android auto", "екран",
            "прошивка", "ecu", "tcu", "srs", "body", "odo", "чіп-тюнінг",
            "ключ", "чип", "транспондер", "smart key",
            "retrofit", "usa", "eu", "конвертація", "шумоізоляція",
            "авто", "автомобіль", "машина", "автосервіс",
        ]

        question_lower = question.lower()
        return any(keyword in question_lower for keyword in keywords)