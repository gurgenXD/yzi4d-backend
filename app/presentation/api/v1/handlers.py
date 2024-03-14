from typing import TYPE_CHECKING

from fastapi import status
from fastapi.responses import JSONResponse

from app.domain.services.exceptions import CredentialsError, InvalidTokenError, NotFoundError


if TYPE_CHECKING:
    from fastapi import FastAPI, Request


def add_all(app: "FastAPI") -> None:
    """Добавить обработчики ошибок к приложению."""
    app.add_exception_handler(NotFoundError, _not_found_error_handler)
    app.add_exception_handler(CredentialsError, _forbidden_error_handler)
    app.add_exception_handler(InvalidTokenError, _unauthorized_error_handler)


async def _not_found_error_handler(_request: "Request", _exception: "Exception") -> "JSONResponse":
    """Обработчик ошибок 404."""
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Object not found."})


async def _forbidden_error_handler(_request: "Request", _exception: "Exception") -> "JSONResponse":
    """Обработчик ошибок 403."""
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "Forbidden."})


async def _unauthorized_error_handler(_request: "Request", _exception: "Exception") -> "JSONResponse":
    """Обработчик ошибок 401."""
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Unauthorized."})
