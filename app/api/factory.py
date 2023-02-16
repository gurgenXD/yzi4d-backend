from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import admin, handlers
from app.api.routers import (analyzes, index, news, offices, pages, promotions,
                             services, specialists)
from utils.constants import MEDIA_DIR, STATIC_DIR

STATIC_PREFIX = "/static"
MEDIA_PREFIX = "/media"


def create_app() -> "FastAPI":
    """Создать приложение FastAPI."""
    app = FastAPI(docs_url=None, redoc_url=None)

    # Добавление обработчиков ошибок.
    handlers.add_all(app)

    # Подключение админ-панели.
    admin.create_app(app)

    static_files = StaticFiles(directory=STATIC_DIR)
    app.mount(STATIC_PREFIX, static_files, name="static")
    media_files = StaticFiles(directory=MEDIA_DIR)
    app.mount(MEDIA_PREFIX, media_files, name="media")

    # Подключение подприложений.
    app.include_router(index.router)
    app.include_router(specialists.router)
    app.include_router(analyzes.router)
    app.include_router(offices.router)
    app.include_router(news.router)
    app.include_router(pages.router)
    app.include_router(promotions.router)
    app.include_router(services.router)

    return app
