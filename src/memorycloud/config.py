# src/memorycloud/config.py
# MemoryCloud™ — Configuration Loader (fixed for Pydantic v2.9+)
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="MC_")

    DB_PATH: str = "data/memorycloud.db"
    KEY_PATH: str = "keys/mc.key"
    DATA_DIR: str = "data"
    LOG_DIR: str = "logs"
    DEBUG: bool = True

@lru_cache()
def get_settings() -> Settings:
    """Return cached environment settings."""
    return Settings()

settings = get_settings()
