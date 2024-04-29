from datetime import datetime

from pydantic import BaseModel


class TokenSchema(BaseModel):
    """Схема токена."""

    access_token: str
    expires_in: datetime
    user_id: str


class AuthSchema(BaseModel):
    """Схема аутентификации."""

    user_id: str
