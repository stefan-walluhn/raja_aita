from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ra_")

    tinydb_path: Path | None = None
    cleanup_username: str
    cleanup_password: str
