import os
from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()

class Settings(BaseSettings):
    """Central configuration for MemoryCloud demo."""
    app_name: str = Field("MemoryCloud", description="App display name")
    db_path: str = Field(default="data/memorycloud.db", description="SQLite database path")
    data_dir: str = Field(default="data", description="Local data directory")
    keys_dir: str = Field(default=".keys", description="Keypair directory")
    audit_log: str = Field(default="provenance/audit.jsonl", description="Provenance log path")
    retention_days: int = Field(default=7, description="Retention policy in days")
    indicator_required: bool = Field(default=True, description="Fail-closed capture gate")
    api_host: str = Field(default="127.0.0.1")
    api_port: int = Field(default=8000)
    env: str = Field(default="local")
    class Config:
        env_prefix = "MC_"

settings = Settings()
