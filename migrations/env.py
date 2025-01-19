from __future__ import with_statement
import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from app.core.config import Settings
import sys
import pathlib

from app.db import Base

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from app.models import *  # necessarily to import something from file where your models are stored

settings = Settings()
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)


target_metadata = Base.metadata

db_url = str(settings.DATABASE_URL)


def run_migrations_offline():
    context.configure(
        url=db_url, target_metadata=target_metadata, literal_binds=True, compare_type=True, dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    connectable = create_async_engine(db_url, echo=True, future=True)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())