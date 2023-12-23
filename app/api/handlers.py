from typing import TYPE_CHECKING

from fastapi import status
from fastapi.responses import JSONResponse


if TYPE_CHECKING:
    from fastapi import FastAPI, Request


def add_all(app: "FastAPI") -> None:
    """Добавить обработчики ошибок к приложению."""
    app.add_exception_handler(Exception, _error_handler)


async def _error_handler(_request: "Request", exception: "Exception") -> "JSONResponse":
    """Обработчик неизвестных ошибок."""
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": str(exception)})
