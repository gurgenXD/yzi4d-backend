from typing import Annotated

from fastapi import APIRouter, Depends, status, Response, Path

from app.container import CONTAINER
from app.presentation.api.auth.schemas import AuthSchema
from app.presentation.api.auth.dependecies import get_user_id, get_token
from app.domain.entities.patients import ChangePasswordEntity, GeneratePasswordEntity

TAG = "auth"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.post("/token", responses={status.HTTP_403_FORBIDDEN: {"description": "Forbidden."}})
async def set_auth_cookie(response: Response, user_id: Annotated[str, Depends(get_user_id)]) -> AuthSchema:
    """Проставить cookie аутентификации."""
    adapter = CONTAINER.patients_adapter()
    security = CONTAINER.auth_security()
    settings = CONTAINER.auth_settings()

    patient = await adapter.get_info(user_id)
    token = security.generate_token(patient)

    response.set_cookie(
        "accessToken", token.access_token, expires=token.expires_in, httponly=True, domain=settings.domain
    )

    return AuthSchema(user_id=token.user_id)


@router.delete("/token/{id}", responses={status.HTTP_403_FORBIDDEN: {"description": "Forbidden."}})
async def remove_auth_cookie(response: Response, _token: Annotated[str, Depends(get_token)]) -> None:
    """Удалить cookie аутентификации."""
    settings = CONTAINER.auth_settings()

    response.delete_cookie("accessToken", httponly=True, domain=settings.domain)
    return


@router.post("/change-password/{id}")
async def change_password(
    credentials: ChangePasswordEntity, _token: Annotated[str, Depends(get_token)], id_: str = Path(alias="id")
) -> None:
    """Сменить пароль."""
    adapter = CONTAINER.patients_adapter()
    return await adapter.change_password(id_, credentials.current_password, credentials.new_password)


@router.post("/generate-password")
async def generate_password(credentials: GeneratePasswordEntity) -> None:
    """Сгенерировать пароль."""
    adapter = CONTAINER.patients_adapter()
    return await adapter.generate_password(credentials.username)
