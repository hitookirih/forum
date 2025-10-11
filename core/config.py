from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///./forum.db.sqlite3"
    db_echo: bool = False

settings = Settings()
