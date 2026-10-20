"""Typed application settings loaded from the local environment."""

from functools import lru_cache
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration for the local API process."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "AgentEval Lab API"
    app_env: Literal["local", "test", "production"] = "local"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    database_url: SecretStr = SecretStr(
        "postgresql+asyncpg://agenteval:local_dev_password@127.0.0.1:55432/agenteval"
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance for application construction."""

    return Settings()
