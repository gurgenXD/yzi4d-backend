import asyncio
import platform
from logging.config import fileConfig

from alembic import context
from sqlalchemy.future.engine import Connection

from app.infrastructure.adapters.storage.db import engine
from app.infrastructure.adapters.storage.db.base_model import BaseModel
from app.infrastructure.adapters.storage.models import *  # noqa: F403
from app.infrastructure.settings.db import DatabaseSettings


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = BaseModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# ... etc.


def do_run_migrations(connection: Connection) -> None:
    """Запустить миграции."""
    settings = DatabaseSettings()

    context.configure(connection=connection, target_metadata=target_metadata)
    connection.dialect.default_schema_name = settings.schema_

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    settings = DatabaseSettings()

    async with engine.get_async(settings).begin() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    message = "Unsupported operation. Online mode is available only."
    raise RuntimeError(message)

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(run_migrations_online())
