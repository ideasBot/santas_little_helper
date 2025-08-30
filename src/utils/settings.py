from src.models.providers import ModelProvider
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    default_premium_model_provider: ModelProvider = ModelProvider.GOOGLE
    default_premium_model_id: str = "gemini-2.5-pro"
    default_model_provider: ModelProvider = ModelProvider.GOOGLE
    default_model_id: str = "gemini-2.5-flash"
    default_lite_model_provider: ModelProvider = ModelProvider.GOOGLE
    default_lite_model_id: str = "gemini-2.5-flash-lite"

    google_api_key: str = None  # Get a free API Key from https://aistudio.google.com


settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump())
