from pydantic import BaseSettings as PydanticBaseSettings

_ENV_FILE = ".env"
_ENV_FILE_ENCODING = "utf-8"


class BaseSettings(PydanticBaseSettings):
    """Базовый класс настроек."""

    class Config:
        """Статические настройки."""

        env_file = _ENV_FILE
        env_file_encoding = _ENV_FILE_ENCODING
