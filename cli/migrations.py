import subprocess
import sys

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
    try:
        subprocess.check_call(
            f'alembic -c {ALEMBIC_CONFIG_FILE} revision --autogenerate -m "{message}"', shell=True
        )
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)


@migrations.command()
@click.option("--revision", default="head", type=str)
def up(revision: str) -> None:
    """Обновить до заданной версии."""
    _validate_revision(revision)

    try:
        subprocess.check_call(f"alembic -c {ALEMBIC_CONFIG_FILE} upgrade {revision}", shell=True)
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)


@migrations.command()
@click.option("--revision", default="-1")
def down(revision: str) -> None:
    """Откатить до заданной версии."""
    _validate_revision(revision)

    try:
        subprocess.check_call(f"alembic -c {ALEMBIC_CONFIG_FILE} downgrade {revision}", shell=True)
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)


def _validate_revision(revision: str) -> None:
    """Validate revision name.

    :param revision: Revision name.
    """
    message = f"Invalid revision: '{revision}'. Revision must be one word without any spaces."
    if " " in revision.strip():
        raise click.BadArgumentUsage(message)
