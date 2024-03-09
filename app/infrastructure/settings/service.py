from pydantic_settings import SettingsConfigDict

from utils.settings.base import BaseSettings


class ServiceSettings(BaseSettings):
    """Настройки сервисов."""

    model_config = SettingsConfigDict(env_prefix="service_")

    # Хост источника.
    source_host: str
    # Пользователь источника.
    source_username: str
    # Пароль от пользователя источника.
    source_password: str
    # Время ожидания ответа от источника.
    updater_timeout: float = 60
    # Время ожидания ответа от хоста с информацией о пациентах.
    patients_timeout: float = 5

    # Пустой GUID.
    empty_guid: str
