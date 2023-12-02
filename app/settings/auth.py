from datetime import timedelta

from pydantic_settings import SettingsConfigDict

from utils.settings.base import BaseSettings


class AuthSettings(BaseSettings):
    """Настройки авторизации."""

    model_config = SettingsConfigDict(env_prefix="auth_")

    # Секретный ключ.
    secret_key: str
    # Имя пользователя.
    username: str
    # Пароль от пользователя.
    password: str
    # Время жизни токена.
    lifetime: timedelta = timedelta(days=7)
