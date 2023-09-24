from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import admin, v1
from utils.constants import MEDIA_DIR, STATIC_DIR


def create_app() -> "FastAPI":
    """Создать приложение FastAPI."""
    app = FastAPI(title="Yzi4D", docs_url="/", redoc_url=None)

    # Подключение админ-панели.
    admin.create_app(app)

    # Подключение статики.
    static_files = StaticFiles(directory=STATIC_DIR)
    app.mount("/static", static_files, name="static")

    # Подключение медиа.
    media_files = StaticFiles(directory=MEDIA_DIR)
    app.mount("/media", media_files, name="media")

    # Подключение под-приложений.
    app.mount("/api/v1", v1.create_app(), name="api_v1")

    return app
