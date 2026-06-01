from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./award_finder.db"
    cache_ttl_minutes: int = 60
    cors_origins: str = "http://localhost:5173"
    http_timeout_seconds: int = 20
    use_mock_fallback: bool = True
    log_level: str = "INFO"

    @property
    def cors_origin_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
