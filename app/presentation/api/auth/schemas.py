from datetime import datetime

from pydantic import BaseModel


class TokenSchema(BaseModel):
    """Схема токена."""

    access_token: str
    expires_in: datetime
