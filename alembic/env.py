from logging.config import fileConfig
import os
import sys

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from dotenv import load_dotenv

# Project root ko Python path mein add karo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# .env load karo
load_dotenv()

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env")

# Alembic Config object
config = context.config

# .env ka DATABASE_URL use karo
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# IMPORTANT:
# Apne models import karo taake SQLAlchemy unko metadata mein register kare.
from app.core.database import Base

# Yahan apne saare models import karo
from app.models.user import User
from app.models.genre_categories import GENRE
from app.models.genre_categories import GENRE_CATEGORIES
from app.models.label import Label
from app.models.packs import Pack
from app.models.songs import SONGS

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()