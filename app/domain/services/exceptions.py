class NotFoundError(Exception):
    """Объект не найден."""


class CredentialsError(Exception):
    """Пользователь не аутентифицирован."""


class InvalidTokenError(Exception):
    """Невалидный токен."""
