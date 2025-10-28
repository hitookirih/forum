from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "forum.db.sqlite3"

class Settings(BaseSettings):
    db_url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    db_echo: bool = False
    # db_echo: bool = True

settings = Settings()
