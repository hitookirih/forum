from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "forum.db.sqlite3"


class DbSettings(BaseSettings):
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    echo: bool = False


class Settings(BaseSettings):

    db: DbSettings = DbSettings()
    # db_echo: bool = True

settings = Settings()
