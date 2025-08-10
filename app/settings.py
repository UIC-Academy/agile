import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__name__).resolve().parent / ".env")


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours
ADMIN_REMEMBER_ME_EXPIRE_MINUTES = 10080  # 7 days
REFRESH_TOKEN_EXPIRE_MINUTES = 43200  # 30 days

MEDIA_DIR = "media"
MEDIA_URL = "/media"
MEDIA_PATH = Path(MEDIA_DIR)
MEDIA_PATH.mkdir(exist_ok=True, parents=True)

STATIC_DIR = "static"
STATIC_URL = "/static"
STATIC_PATH = Path(STATIC_DIR)
STATIC_PATH.mkdir(exist_ok=True, parents=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Celery settings
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
EMAIL_ADDRESS = "ekzosfera94@gmail.com"
EMAIL_PASSWORD = "rkcf svpv oldj nkrw"
SMTP_PORT = 587
SMTP_SERVER = "smtp.gmail.com"

FRONTEND_URL = "http://127.0.0.1:8000"

REDIS_URL = "redis://localhost:6379"
