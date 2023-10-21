from pydantic_settings import SettingsConfigDict

from utils.settings.base import BaseSettings


class ServerSettings(BaseSettings):
    """Настройки сервера."""

    model_config = SettingsConfigDict(env_prefix="server_")

    # Путь до ASGI в формате "<module>:<attribute>".
    app: str = "app.api.factory:create_app"
    # Рассматривать "app" как фабрику.
    factory: bool = True
    # Количество воркеров сервера.
    workers: int = 1
    # Флаг запуска сервера в режиме разработки.
    reload: bool = False
    # Уровень логирования.
    log_level: str = "info"
    # Тип event loop`а.
    loop: str = "auto"
    # Host приложения.
    host: str
    # Port приложения.
    port: int
    # Trusted IPs.
    forwarded_allow_ips: list[str] = ["*"]
