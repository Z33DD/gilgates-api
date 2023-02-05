from functools import lru_cache
from pathlib import Path
import secrets
from typing import Any, Dict
from pydantic import BaseSettings, RedisDsn
from gilgates_api.helpers.config_helpers import get_project_metadata


ROOT_DIR = Path(__file__).parent.parent

metadata = get_project_metadata(str(ROOT_DIR))


class Settings(BaseSettings):
    app_name: str = "GilGates API"
    env: str = "development"
    version: str = metadata["version"]
    debug: bool = True

    database_url: str = "sqlite:///db.sqlite3"
    connect_args: Dict[str, Any] = {"check_same_thread": False}

    secret_key: str = secrets.token_urlsafe(32)
    refresh_secret_key: str = secrets.token_urlsafe(32)
    token_expiration: int = 30  # 30 minutes
    refresh_token_expiration: int = 60 * 2 * 7  # 7 days
    algorithm: str = "HS256"

    celery_broker_url: RedisDsn = RedisDsn(url="redis://localhost:6379", scheme="redis")
    celery_result_backend: RedisDsn = RedisDsn(
        url="redis://localhost:6379", scheme="redis"
    )

    postmark_api_token: str = ""

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


config = get_settings()
