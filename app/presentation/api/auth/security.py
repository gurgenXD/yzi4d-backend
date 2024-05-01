from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from jose import jwt

from app.presentation.api.auth.schemas import TokenSchema


if TYPE_CHECKING:
    from app.domain.entities.patients import PatientEntity
    from app.infrastructure.settings.auth import AuthSettings


@dataclass
class AuthSecurity:
    """Сервис для работы с аутентификацией."""

    _settings: "AuthSettings"

    def generate_token(self, patient: "PatientEntity") -> TokenSchema:
        """Сгенерировать токен."""
        expires_in = datetime.now(tz=UTC) + self._settings.lifetime
        claims = {
            "user_id": patient.id,
            "exp": expires_in,
            "members": [member.id for member in patient.members],
            "user_name": f"{patient.surname} {patient.name}",
        }

        return TokenSchema(
            access_token=jwt.encode(claims=claims, key=self._settings.secret_key),
            expires_in=expires_in - self._settings.lifetime_delta,
            user_id=patient.id,
        )

    def validate_token(self, user_id: str, token: str) -> None:
        """Провалидировать токен."""
        decoded_claims = jwt.decode(token=token, key=self._settings.secret_key)

        if user_id != decoded_claims["user_id"] and user_id not in decoded_claims["members"]:
            raise jwt.JWTClaimsError("Invalid user_id.")

        if datetime.fromtimestamp(decoded_claims["exp"], tz=UTC) <= datetime.now(tz=UTC):
            raise jwt.ExpiredSignatureError("Token was expired.")
