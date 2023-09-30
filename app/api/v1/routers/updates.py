from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.responses import RedirectResponse
from app.services.updater.types import UpdaterDataType

from app.container import CONTAINER


TAG = "updates"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("", include_in_schema=False)
async def update_data(request: Request, tasks: BackgroundTasks) -> "RedirectResponse":
    """Обновить данные."""
    updater = CONTAINER.repo_updater_service()
    tasks.add_task(updater.update, data_type=UpdaterDataType.MAIN)

    return RedirectResponse(url=request.url_for("admin:list", identity="update"))
