from fastapi import FastAPI

from app.api.v1 import handlers
from app.api.v1.routers import (
    analyzes,
    news,
    offices,
    pages,
    promotions,
    services,
    specialists,
    updates,
)


def create_app() -> "FastAPI":
    """Создать приложение FastAPI."""
    app = FastAPI(title="Yzi4D API", docs_url="/", version="0.1.0")

    # Добавление обработчиков ошибок.
    handlers.add_all(app)

    # Подключение под-приложений.
    app.include_router(specialists.router)
    app.include_router(analyzes.router)
    app.include_router(offices.router)
    app.include_router(news.router)
    app.include_router(pages.router)
    app.include_router(promotions.router)
    app.include_router(services.router)
    app.include_router(updates.router)

    return app