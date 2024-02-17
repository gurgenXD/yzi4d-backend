from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.infrastructure.settings.api import ApiSettings
from app.presentation.api import admin, handlers, middlewares, v1
from utils.constants import MEDIA_DIR


def create_app() -> "FastAPI":
    """Создать приложение FastAPI."""
    settings = ApiSettings()
    app = FastAPI(title=settings.title, docs_url="/", redoc_url=None)

    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
    )
    app.add_middleware(middlewares.DelayMiddleware, delay=settings.delay)

    # Подключение админ-панели.
    admin.create_app(app)

    # Подключение медиа.
    media_files = StaticFiles(directory=MEDIA_DIR)
    app.mount("/media", media_files, name="media")

    # Подключение под-приложений.
    app_v1 = v1.create_app()
    app.mount("/api/v1", app_v1, name="api_v1")
    # Добавление общих обработчиков ошибок.
    handlers.add_all(app_v1)

    return app
