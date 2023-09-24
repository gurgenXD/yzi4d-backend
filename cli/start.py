import click
import uvicorn

from app.settings.server import ServerSettings


@click.group()
def start() -> None:
    """Запустить сервис."""


@start.command()
def api() -> None:
    """Сервис API."""
    uvicorn.run(**ServerSettings().dict())
