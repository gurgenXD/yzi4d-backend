from pydantic_settings import SettingsConfigDict

from utils.settings.base import BaseSettings


class ApiSettings(BaseSettings):
    """Настройки API."""

    model_config = SettingsConfigDict(env_prefix="api_")

    # Название.
    title: str = "Yzi4D"
    # Задержка ответа.
    delay: float = 0.0

    # CORS.
    allow_origins: list[str] = ["*"]
