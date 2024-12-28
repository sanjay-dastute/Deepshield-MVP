from functools import lru_cache
from app.core.config import Settings

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
