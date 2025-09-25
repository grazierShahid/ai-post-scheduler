import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv

# Load environment variables from .env file early so imported modules pick them up
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, text
from alembic import context
from app.models.base_model import Base

# Add all your model imports here

from app.models.api import Api
from app.models.image import Image
from app.models.post import Post, PostAnalysis, AiInsight
from app.models.product import Product
from app.models.social_platform import SocialPlatform

from logging.config import fileConfig
from app.database.session import DATABASE_URL


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "affpilot")
db_user = os.getenv("DB_USER", "affpilot")
db_password = os.getenv("DB_PASSWORD", "affpilot")
db_url = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Prefer the application's DATABASE_URL when available so Alembic uses the
# exact same connection string as the application. Otherwise fall back to
# constructing a URL that matches the application's default (MySQL via pymysql).
if DATABASE_URL:
    url = config.set_main_option("sqlalchemy.url", DATABASE_URL)
else:
    # load the database URL from the environment variable
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME", "affpilot")
    db_user = os.getenv("DB_USER", "affpilot")
    db_password = os.getenv("DB_PASSWORD", "affpilot")
    db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    url = config.set_main_option("sqlalchemy.url", db_url)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()