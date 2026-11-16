# services/intent_detector.py

class IntentDetector:
    """Визначення наміру користувача"""

    INTENTS = {
        "dtc_code": ["p0", "p1", "c0", "b0", "u0", "код", "помилка"],
        "symptom": ["не горить", "не працює", "стук", "шум", "вібрація"],
        "how_to": ["як", "як перевірити", "як зробити", "як підключити"],
        "price": ["ціна", "вартість", "скільки", "коштує"],
        "booking": ["записатися", "записати", "приїхати", "час"],
    }

    def detect(self, text: str) -> str:
        text_lower = text.lower()
        for intent, keywords in self.INTENTS.items():
            if any(kw in text_lower for kw in keywords):
                return intent
        return "general"