from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.container import CONTAINER


def get_oauth2_password_bearer() -> OAuth2PasswordBearer:
    """Получить схему безопасности для OAuth2PasswordBearer."""
    return OAuth2PasswordBearer(tokenUrl="auth/token")


def get_token(token: str = Depends(get_oauth2_password_bearer())) -> str:
    """Получить токен."""
    security = CONTAINER.auth_security()
    security.validate_token(token)

    return token
