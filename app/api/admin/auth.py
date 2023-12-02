from datetime import datetime, timezone
from typing import TYPE_CHECKING

from fastapi.requests import Request
from jose import JWTError, jwt
from sqladmin.authentication import AuthenticationBackend


if TYPE_CHECKING:
    from app.settings.auth import AuthSettings


class AdminAuth(AuthenticationBackend):
    """Реализация аутентификации."""

    def __init__(self, settings: "AuthSettings") -> None:
        """Инициализация."""
        self._settings = settings

        super().__init__(secret_key=self._settings.secret_key)

    async def login(self, request: Request) -> bool:
        """Вход."""
        form = await request.form()
        username, password = form["username"], form["password"]

        if self._settings.username != username or self._settings.password != password:
            return False

        token = jwt.encode({"exp": datetime.now(tz=timezone.utc) + self._settings.lifetime}, self._settings.secret_key)

        request.session.update({"token": token})
        return True

    async def logout(self, request: Request) -> bool:
        """Выход."""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """Аутентификация."""
        if not (token := request.session.get("token")):
            return False

        try:
            claims = jwt.decode(token, self._settings.secret_key)
        except JWTError:
            return False

        if datetime.now(tz=timezone.utc) > datetime.fromtimestamp(claims.get("exp"), tz=timezone.utc):
            return False

        return True
