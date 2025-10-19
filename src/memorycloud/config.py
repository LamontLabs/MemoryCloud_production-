# src/memorycloud/config.py
# MemoryCloud™ — Configuration Loader (CI-verified / Pydantic v2.9+)
import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Deterministic environment configuration for MemoryCloud.
    Backward-compatible aliases for old test attributes:
      - db_path → DB_PATH
      - audit_log → LOG_DIR/audit.jsonl
    """
    model_config = SettingsConfigDict(env_file=".env", env_prefix="MC_")

    # Core paths
    DB_PATH: str = "data/memorycloud.db"
    KEY_PATH: str = "keys/mc.key"
    DATA_DIR: str = "data"
    LOG_DIR: str = "logs"
    DEBUG: bool = True

    # Derived / legacy aliases
    @property
    def db_path(self) -> str:
        return self.DB_PATH

    @property
    def audit_log(self) -> str:
        """Return the path for the default audit log JSONL file."""
        return os.path.join(self.LOG_DIR, "audit.jsonl")

@lru_cache()
def get_settings() -> Settings:
    """Return cached settings singleton."""
    return Settings()

settings = get_settings()
