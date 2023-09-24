from pydantic_settings import SettingsConfigDict

from utils.settings.base import BaseSettings


class ServiceSettings(BaseSettings):
    """Настройки сервисов."""

    model_config = SettingsConfigDict(env_prefix="service_")

    # Хост обновления.
    updater_host: str
    # Пустой GUID.
    empty_guid: str
    # Время ожидания ответа от хоста обновления.
    timeout: float = 60
