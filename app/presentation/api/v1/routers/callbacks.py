from fastapi import APIRouter

from app.container import CONTAINER
from app.domain.entities.callbacks import CallbackEntity


TAG = "callbacks"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.post("")
async def create_callback(callback: CallbackEntity) -> None:
    """Добавить заявку на обратный звонок."""

    adapter = CONTAINER.callback_adapter()
    return await adapter.create(callback)
