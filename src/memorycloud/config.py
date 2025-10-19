# src/memorycloud/config.py
# MemoryCloud™ — Configuration Loader (CI-stable / Final)
import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Deterministic environment configuration for MemoryCloud.
    Includes backward-compatible aliases for test and API imports:
      - db_path      → DB_PATH
      - audit_log    → LOG_DIR/audit.jsonl (settable)
      - app_name     → APP_NAME
      - indicator_required → HUD indicator enforcement flag
    """
    model_config = SettingsConfigDict(env_file=".env", env_prefix="MC_")

    # Core identifiers
    APP_NAME: str = "MemoryCloud"

    # Core paths
    DB_PATH: str = "data/memorycloud.db"
    KEY_PATH: str = "keys/mc.key"
    DATA_DIR: str = "data"
    LOG_DIR: str = "logs"
    DEBUG: bool = True

    # HUD / indicator settings
    INDICATOR_REQUIRED: bool = True

    # Derived / legacy aliases
    @property
    def db_path(self) -> str:
        return self.DB_PATH

    # make audit_log both readable and writable for tests
    @property
    def audit_log(self) -> str:
        return getattr(self, "_audit_log", os.path.join(self.LOG_DIR, "audit.jsonl"))

    @audit_log.setter
    def audit_log(self, value: str) -> None:
        self._audit_log = value

    @property
    def app_name(self) -> str:
        return self.APP_NAME

    @property
    def indicator_required(self) -> bool:
        """Alias for INDICATOR_REQUIRED (used in HUD tests)."""
        return self.INDICATOR_REQUIRED

@lru_cache()
def get_settings() -> Settings:
    """Return cached settings singleton."""
    return Settings()

settings = get_settings()
