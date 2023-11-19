from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api import admin, v1, middlewares
from utils.constants import MEDIA_DIR
from app.settings.api import ApiSettings


def create_app() -> "FastAPI":
    """Создать приложение FastAPI."""
    settings = ApiSettings()
    app = FastAPI(title=settings.title, docs_url="/", redoc_url=None)

    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
    )
    app.add_middleware(middlewares.DelayMiddleware, delay=settings.delay)

    # Подключение админ-панели.
    admin.create_app(app)

    # Подключение медиа.
    media_files = StaticFiles(directory=MEDIA_DIR)
    app.mount("/media", media_files, name="media")

    # Подключение под-приложений.
    app.mount("/api/v1", v1.create_app(), name="api_v1")

    return app
