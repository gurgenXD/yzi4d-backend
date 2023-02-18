from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import RedirectResponse

from app.container import CONTAINER


TAG = "updates"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("")
async def update_data(tasks: BackgroundTasks) -> "RedirectResponse":
    """Обновить данные."""
    updater = CONTAINER.repo_updater_service()
    tasks.add_task(updater.update)

    return RedirectResponse(url="/admin/updater/list")
