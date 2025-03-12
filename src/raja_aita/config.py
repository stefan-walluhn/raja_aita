from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ra_")

    tinydb_path: Path | None = None
    cleanup_username: str
    cleanup_password: str


@lru_cache
def get_settings() -> Settings:
    return Settings()
