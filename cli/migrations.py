import alembic.config
import click

from utils.constants import BASE_DIR


ALEMBIC_CONFIG_FILE = BASE_DIR / "migrations" / "alembic.ini"


@click.group()
def migrations() -> None:
    """Миграции базы данных."""


@migrations.command()
@click.argument("message", type=str)
def make(message: str) -> None:
    """Создать миграцию."""
    alembic_args = ["-c", str(ALEMBIC_CONFIG_FILE), "revision", "--autogenerate", "--message", message]
    alembic.config.main(argv=alembic_args)


@migrations.command()
@click.option("--revision", default="head", type=str)
def up(revision: str) -> None:
    """Обновить до заданной версии."""
    alembic_args = ["-c", str(ALEMBIC_CONFIG_FILE), "upgrade", revision.strip()]
    alembic.config.main(argv=alembic_args)


@migrations.command()
@click.option("--revision", default="-1")
def down(revision: str) -> None:
    """Откатить до заданной версии."""
    alembic_args = ["-c", str(ALEMBIC_CONFIG_FILE), "downgrade", revision.strip()]
    alembic.config.main(argv=alembic_args)
