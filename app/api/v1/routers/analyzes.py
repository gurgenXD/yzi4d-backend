from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.api.templates import TEMPLATES
from app.container import CONTAINER


TAG = "analyzes"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("", response_class=HTMLResponse)
async def get_analyzes(request: Request) -> "HTMLResponse":
    """Получить анализы."""
    adapter = CONTAINER.analyzes_adapter()
    analyzes = await adapter.get_all(for_main=False)

    return TEMPLATES.TemplateResponse(  # type: ignore
        "analyzes.html", {"request": request, "analyzes": analyzes}
    )


@router.get("/{id}", response_class=HTMLResponse)
async def get_analysis(request: Request, id: int) -> "HTMLResponse":
    """Получить анализ."""
    adapter = CONTAINER.analyzes_adapter()
    analysis = await adapter.get(id=id)

    return TEMPLATES.TemplateResponse(  # type: ignore
        "analysis.html", {"request": request, "analysis": analysis}
    )
