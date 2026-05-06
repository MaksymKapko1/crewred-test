from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ARTIC_BASE_URL: str = "https://api.artic.edu/api/v1"
    DATABASE_URL: str = "sqlite:///database.db"

settings = Settings()