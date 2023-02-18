from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.container import CONTAINER


TAG = "updates"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("")
async def update_data() -> "RedirectResponse":
    """Обновить данные."""
    updater = CONTAINER.repo_updater_service()
    await updater.update()
    return RedirectResponse(url="/admin/update/list")
