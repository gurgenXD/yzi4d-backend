import click
import uvicorn

from app.infrastructure.settings.server import ServerSettings


@click.group()
def start() -> None:
    """Запустить сервис."""


@start.command()
def api() -> None:
    """Сервис API."""
    uvicorn.run(**ServerSettings().model_dump())
