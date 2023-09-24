from pydantic_settings import SettingsConfigDict

from utils.settings.base import BaseSettings


class ServiceSettings(BaseSettings):
    """Настройки сервисов."""

    model_config = SettingsConfigDict(env_prefix="service_")

    # Хост 1C.
    host_1c: str
