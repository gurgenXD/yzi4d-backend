from fastapi import APIRouter
from fastapi.responses import RedirectResponse


TAG = "updates"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("")
async def update_data() -> "RedirectResponse":
    """Обновить данные."""
    return RedirectResponse(url="/admin/update/list")
