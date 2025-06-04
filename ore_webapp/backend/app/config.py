import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR / "app.db"}')
SECRET_KEY = os.getenv('SECRET_KEY', 'change_this_secret')

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
