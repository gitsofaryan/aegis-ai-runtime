from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Aegis AI Runtime"
    REDIS_URL: str = "redis://localhost:6379"
    DATABASE_URL: str = "postgresql+asyncpg://aegis_user:aegis_password@localhost:5432/aegis_db"
    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
