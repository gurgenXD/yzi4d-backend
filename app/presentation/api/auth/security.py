from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

from jose import jwt

from app.domain.services.exceptions import InvalidTokenError
from app.presentation.api.auth.schemas import TokenSchema


if TYPE_CHECKING:
    from app.infrastructure.settings.auth import AuthSettings


@dataclass
class AuthSecurity:
    """Сервис для работы с аутентификацией."""

    _settings: "AuthSettings"

    def generate_token(self, user_id: str) -> TokenSchema:
        """Сгенерировать токен."""
        expires_in = datetime.now(tz=UTC) + timedelta(minutes=1)
        claims = {"user_id": user_id, "exp": expires_in}

        return TokenSchema(access_token=jwt.encode(claims=claims, key=self._settings.secret_key), expires_in=expires_in)

    def validate_token(self, token: str) -> None:
        """Провалидировать токен."""
        try:
            decoded_claims = jwt.decode(token=token, key=self._settings.secret_key)

            if datetime.fromtimestamp(decoded_claims["exp"], tz=UTC) <= datetime.now(tz=UTC):
                raise jwt.ExpiredSignatureError("Token was expired.")
        except jwt.JWTError as exc:
            raise InvalidTokenError("Invalid token.") from exc
