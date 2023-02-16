from typing import TYPE_CHECKING

from fastapi import status
from fastapi.responses import JSONResponse

from app.services.exceptions import NotFoundError


if TYPE_CHECKING:
    from fastapi import FastAPI, Request


def add_all(app: "FastAPI") -> None:
    """Добавить обработчики ошибок к приложению."""
    app.add_exception_handler(NotFoundError, _not_found_error_handler)


async def _not_found_error_handler(_request: "Request", _exception: "Exception") -> "JSONResponse":
    """Обработчик ошибок 404."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"message": "object not found."}
    )
