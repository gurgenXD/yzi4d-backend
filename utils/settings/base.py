from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import SettingsConfigDict


_ENV_FILE = ".env"
_ENV_FILE_ENCODING = "utf-8"


class BaseSettings(PydanticBaseSettings):
    """Базовый класс настроек."""

    model_config = SettingsConfigDict(env_file=_ENV_FILE, env_file_encoding=_ENV_FILE_ENCODING)
