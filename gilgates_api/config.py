# -*- coding: utf-8 -*-
"""Application configuration.
Most configuration is set via environment variables.
For local development, use a .env file to set
environment variables.
"""
import secrets
from pathlib import Path
from environs import Env
from gilgates_api.helpers.config_helpers import get_project_metadata


env = Env()
env.read_env()
default_password = "pqqrLJBCh9HPFBorJ8MbeSHe5C7i7nLwYBSBdXas2gQ8"

ROOT_DIR = Path(__file__).parent.parent
metadata = get_project_metadata(str(ROOT_DIR))

ENV: str = env.str("ENV", default="development")


if ENV == "production":
    DATABASE_URL = env.str(
        "DATABASE_URL",
        "postgresql://doadmin:AVNS_QtPqJ0r8kRGu1XJdwXU@gilgates-api-do-user-11151596-0.b.db.ondigitalocean.com:25060/defaultdb?sslmode=require",
    )
else:
    DATABASE_URL = "sqlite:///db.sqlite3"
    SQLALCHEMY_ENGINE_OPTIONS = {"connect_args": {"check_same_thread": False}}

DEBUG = env.bool("DEBUG", default=False)

SECRET_KEY = env.str("SECRET_KEY", secrets.token_urlsafe(32))
REFRESH_SECRET_KEY = env.str("REFRESH_SECRET_KEY", secrets.token_urlsafe(32))
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
MOCK_AUTH = env.bool("MOCK_AUTH", False)
BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = DEBUG
SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER = env.str("UPLOAD_FOLDER", default=f"{ROOT_DIR}/data")
ALLOWED_EXTENSIONS = {"docx", "pdf", "png", "jpg", "jpeg"}
VERSION = metadata["version"]

CELERY_CONFIG = {
    "broker_url": "redis://localhost:6379",
    "result_backend": "redis://localhost:6379",
}

AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_REGION = "sa-east-1"
CHARSET = "UTF-8"

POSTMARK_API_TOKEN = env.str("POSTMARK_API_TOKEN", "")
