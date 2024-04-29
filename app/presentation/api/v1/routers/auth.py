from typing import Annotated

from fastapi import APIRouter, Depends, status, Response

from app.container import CONTAINER
from app.presentation.api.auth.schemas import AuthSchema
from app.presentation.api.auth.dependecies import get_user_id, get_token


TAG = "auth"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.post("/token", responses={status.HTTP_403_FORBIDDEN: {"description": "Forbidden."}})
async def set_auth_cookie(response: Response, user_id: Annotated[str, Depends(get_user_id)]) -> AuthSchema:
    """Проставить cookie аутентификации."""
    adapter = CONTAINER.patients_adapter()
    security = CONTAINER.auth_security()

    patient = await adapter.get_info(user_id)
    token = security.generate_token(patient)

    response.set_cookie("accessToken", token.access_token, expires=token.expires_in, httponly=True)

    return AuthSchema(user_id=token.user_id)


@router.delete("/token/{id}", responses={status.HTTP_403_FORBIDDEN: {"description": "Forbidden."}})
async def remove_auth_cookie(response: Response, _token: Annotated[str, Depends(get_token)]) -> None:
    """Удалить cookie аутентификации."""
    response.delete_cookie("accessToken", httponly=True)
    return
