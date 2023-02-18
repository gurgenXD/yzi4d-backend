from utils.settings.base import BaseSettings


class ServiceSettings(BaseSettings):
    """Настройки сервисов."""

    # Хост 1C.
    host_1c: str

    class Config:
        env_prefix = "service_"
