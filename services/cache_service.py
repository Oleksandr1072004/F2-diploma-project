# services/cache_service.py

import hashlib
from typing import Optional


class ResponseCache:
    """Кеш відповідей AI"""

    def __init__(self, ttl: int = 3600):
        self.cache = {}
        self.ttl = ttl

    def get(self, question: str) -> Optional[str]:
        key = hashlib.md5(question.lower().encode()).hexdigest()
        return self.cache.get(key)

    def set(self, question: str, answer: str):
        key = hashlib.md5(question.lower().encode()).hexdigest()
        self.cache[key] = answer