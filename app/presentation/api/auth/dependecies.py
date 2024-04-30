from typing import Annotated

from fastapi import Depends, Path, Response
from fastapi.security import APIKeyCookie, HTTPBasicCredentials, HTTPBasic
from jose import jwt

from app.container import CONTAINER


def get_http_basic() -> HTTPBasic:
    """Получить схему безопасности для HTTPBasic."""
    return HTTPBasic()


def get_api_key_cookie() -> APIKeyCookie:
    """Получить схему безопасности для APIKeyCookie."""
    return APIKeyCookie(name="accessToken")


async def get_user_id(credentials: Annotated[HTTPBasicCredentials, Depends(get_http_basic())]) -> str:
    """Получить id пользователя."""
    adapter = CONTAINER.patients_adapter()
    return await adapter.get_patient_id(credentials.username, credentials.password)


def get_token(response: Response, id_: str = Path(alias="id"), token: str = Depends(get_api_key_cookie())) -> str:
    """Получить токен."""
    security = CONTAINER.auth_security()
    settings = CONTAINER.auth_settings()

    try:
        security.validate_token(id_, token)
    except jwt.JWTError:
        response.delete_cookie("accessToken", domain=settings.domain)
        raise

    return token
