from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.container import CONTAINER
from app.presentation.api.auth.schemas import TokenSchema


TAG = "auth"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.post("/token", responses={status.HTTP_403_FORBIDDEN: {"description": "Forbidden."}})
async def generate_token(credentials: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenSchema:
    """Сгенерировать токен пользователя."""
    adapter = CONTAINER.patients_adapter()
    security = CONTAINER.auth_security()

    patient_id = await adapter.get_patient_id(credentials.username, credentials.password)
    patient = await adapter.get_info(patient_id)

    return security.generate_token(patient)
