from fastapi import FastAPI

from app.presentation.api.v1 import handlers
from app.presentation.api.v1.routers import (
    auth,
    callbacks,
    consultations,
    contacts,
    documents,
    news,
    patients,
    promotions,
    services,
    specialists,
    specializations,
    updates,
    vacancies,
)


def create_app() -> "FastAPI":
    """Создать приложение FastAPI."""
    app = FastAPI(title="Yzi4D API", docs_url="/", version="1.0.0")

    # Добавление обработчиков ошибок.
    handlers.add_all(app)

    # Подключение под-приложений.
    app.include_router(specializations.router)
    app.include_router(specialists.router)
    app.include_router(services.router)
    app.include_router(contacts.router)
    app.include_router(news.router)
    app.include_router(updates.router)
    app.include_router(promotions.router)
    app.include_router(documents.router)
    app.include_router(vacancies.router)
    app.include_router(consultations.router)
    app.include_router(callbacks.router)
    app.include_router(patients.router)
    app.include_router(auth.router)

    return app
