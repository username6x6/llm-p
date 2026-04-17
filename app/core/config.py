from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения, загружаемые из .env файла."""

    # Приложение
    app_name: str = "LLM-P"
    environment: str = "development"

    # Безопасность и JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # База данных
    sqlite_path: str = "./app.db"

    # OpenRouter
    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "openai/gpt-3.5-turbo"
    openrouter_referer: str = "http://localhost:8000"
    openrouter_title: str = "LLM-P"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()