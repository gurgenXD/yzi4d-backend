import click
import uvicorn

from app.settings.uvicorn import UvicornSettings


@click.group()
def start() -> None:
    """Запустить сервис."""


@start.command()
def api() -> None:
    """Сервис API."""
    uvicorn.run(**UvicornSettings().dict())
