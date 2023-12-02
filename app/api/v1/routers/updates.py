from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.responses import RedirectResponse

from app.container import CONTAINER
from app.services.updater.types import UpdaterDataType


TAG = "updates"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/data", include_in_schema=False)
async def update_data(request: Request, tasks: BackgroundTasks) -> "RedirectResponse":
    """Обновить данные."""
    updater = CONTAINER.repo_updater_service()
    tasks.add_task(updater.update, data_type=UpdaterDataType.MAIN)

    return RedirectResponse(url=request.url_for("admin:list", identity="update"))


@router.get("/images", include_in_schema=False)
async def update_images(request: Request, tasks: BackgroundTasks) -> "RedirectResponse":
    """Обновить фотографии."""
    updater = CONTAINER.repo_updater_service()
    tasks.add_task(updater.update, data_type=UpdaterDataType.IMAGES)

    return RedirectResponse(url=request.url_for("admin:list", identity="update"))
