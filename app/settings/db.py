from datetime import timedelta

from utils.settings.base import BaseSettings


class DatabaseSettings(BaseSettings):
    """Настройки подключения к базе данных."""

    # Тип БД.
    type_: str = "postgresql"
    # Асинхронный драйвер подключения к БД.
    async_driver: str = "asyncpg"
    # Драйвер подключения к БД.
    driver: str = "psycopg2"
    # Пользователь БД.
    user: str
    # Пароль пользователя БД.
    password: str
    # Хост БД.
    host: str
    # Порт БД.
    port: int
    # Имя БД.
    name: str
    # Схема БД.
    schema_: str

    # Минимальное количество подключений к БД.
    pool_size: int = 1
    # Максимальное количество подключений к БД.
    max_overflow: int = 1
    # Время простоя подключения к БД.
    pool_timeout: int = 5

    @property
    def async_url(self) -> str:
        """Ссылка для ассинхронного подключения к БД."""
        schema = f"{self.type_}+{self.async_driver}"
        return f"{schema}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    @property
    def url(self) -> str:
        """Ссылка для подключения к БД."""
        schema = f"{self.type_}+{self.driver}"
        return f"{schema}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    class Config:
        env_prefix = "db_"
