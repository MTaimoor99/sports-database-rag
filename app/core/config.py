# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    api_sports_key: str
    google_api_key: str
    api_sports_base_url: str = "https://v3.football.api-sports.io"
settings = Settings()