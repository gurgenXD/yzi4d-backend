from pydantic_settings import SettingsConfigDict

from utils.settings.base import BaseSettings


class ServiceSettings(BaseSettings):
    """Настройки сервисов."""

    model_config = SettingsConfigDict(env_prefix="service_")

    # Хост обновления.
    updater_host: str
    # Время ожидания ответа от хоста обновления.
    updater_timeout: float = 60
    # Пустой GUID.
    empty_guid: str

    # Хост личного кабинета.
    profile_host: str
    # Время ожидания ответа от хоста личного кабинета.
    profile_timeout: float = 5
