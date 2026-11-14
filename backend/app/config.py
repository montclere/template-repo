from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str = "sqlite:///./dev.db"
    cors_origins: str = "http://localhost:5173"
    ml_url: str = "http://localhost:8100"
    ml_timeout_seconds: float = 120


settings = Settings()
