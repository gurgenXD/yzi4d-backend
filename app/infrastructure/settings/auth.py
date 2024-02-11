from datetime import timedelta

from pydantic_settings import SettingsConfigDict

from app.presentation.api.admin.permissions import PermissionType
from utils.settings.base import BaseSettings


class AuthSettings(BaseSettings):
    """Настройки авторизации."""

    model_config = SettingsConfigDict(env_prefix="auth_")

    # Секретный ключ.
    secret_key: str
    # Время жизни токена.
    lifetime: timedelta = timedelta(days=7)

    # Логин администратора.
    admin_username: str
    # Пароль администратора.
    admin_password: str

    # Логин маркетолога.
    marketer_username: str
    # Пароль маркетолога.
    marketer_password: str

    # Логин оператора.
    operator_username: str
    # Пароль оператора.
    operator_password: str

    @property
    def users(self) -> dict[str, str]:
        """Получить пользователей."""
        return {
            self.admin_username: self.admin_password,
            self.marketer_username: self.marketer_password,
            self.operator_username: self.operator_password,
        }

    @property
    def permissions(self) -> dict[str, list[str]]:
        """Получить права пользователей."""
        return {
            self.admin_username: [PermissionType.ADMIN.value],
            self.marketer_username: [PermissionType.MARKETER.value],
            self.operator_username: [PermissionType.OPERATOR.value],
        }
