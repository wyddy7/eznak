Directory structure:
└── EZNAK/
    ├── alembic.ini
    ├── docker-compose.yml
    ├── pyproject.toml
    ├── test_llm.py
    ├── test_media.py
    ├── test_random_llm.py
    ├── .env.example
    ├── alembic/
    │   ├── README
    │   ├── env.py
    │   ├── script.py.mako
    │   └── versions/
    │       ├── 001_init.py
    │       ├── 784ce0a789f1_add_datasets.py
    │       ├── 785_add_datasets_unique.py
    │       ├── 786_add_is_posting_channel.py
    │       ├── 787_add_dataset_source_channel_id.py
    │       └── 788_add_prompt_templates.py
    ├── assets/
    │   └── fonts/
    │       └── README.md
    ├── backend/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── api/
    │   │   ├── __init__.py
    │   │   ├── channels.py
    │   │   ├── deps.py
    │   │   ├── generation.py
    │   │   ├── posts.py
    │   │   └── prompt_templates.py
    │   ├── core/
    │   │   ├── __init__.py
    │   │   ├── config.py
    │   │   ├── config_loader.py
    │   │   ├── logging.py
    │   │   └── prompts.py
    │   ├── db/
    │   │   ├── __init__.py
    │   │   ├── models.py
    │   │   └── session.py
    │   ├── middleware/
    │   │   ├── __init__.py
    │   │   └── logging_middleware.py
    │   └── services/
    │       ├── __init__.py
    │       ├── llm_pipeline.py
    │       ├── media_gen.py
    │       └── scheduler.py
    ├── bot/
    │   ├── __init__.py
    │   └── bot.py
    ├── config/
    │   ├── media.yaml
    │   └── prompts.yaml
    ├── docs/
    │   ├── SUPABASE_DB.md
    │   └── tz/
    │       ├── epics logic todos.md
    │       ├── tehdolg.md
    │       ├── tz.md
    │       ├── инсайты.md
    │       └── archive/
    │           ├── обудмывание с ллмкой.md
    │           ├── отфильтрованные идеи ллмки с тз.md
    │           └── черновик идеи.md
    └── scripts/
        ├── create_bg.py
        ├── load_dataset_from_html.py
        ├── run_backend.py
        ├── seed.py
        └── seed_channel.py

================================================
FILE: alembic.ini
================================================
# A generic, single database configuration.

[alembic]
# path to migration scripts.
# this is typically a path given in POSIX (e.g. forward slashes)
# format, relative to the token %(here)s which refers to the location of this
# ini file
script_location = %(here)s/alembic

# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
# Uncomment the line below if you want the files to be prepended with date and time
# see https://alembic.sqlalchemy.org/en/latest/tutorial.html#editing-the-ini-file
# for all available tokens
# file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s
# Or organize into date-based subdirectories (requires recursive_version_locations = true)
# file_template = %%(year)d/%%(month).2d/%%(day).2d_%%(hour).2d%%(minute).2d_%%(second).2d_%%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.  for multiple paths, the path separator
# is defined by "path_separator" below.
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the tzdata library which can be installed by adding
# `alembic[tz]` to the pip requirements.
# string value is passed to ZoneInfo()
# leave blank for localtime
# timezone =

# max length of characters to apply to the "slug" field
# truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version location specification; This defaults
# to <script_location>/versions.  When using multiple version
# directories, initial revisions must be specified with --version-path.
# The path separator used here should be the separator specified by "path_separator"
# below.
# version_locations = %(here)s/bar:%(here)s/bat:%(here)s/alembic/versions

# path_separator; This indicates what character is used to split lists of file
# paths, including version_locations and prepend_sys_path within configparser
# files such as alembic.ini.
# The default rendered in new alembic.ini files is "os", which uses os.pathsep
# to provide os-dependent path splitting.
#
# Note that in order to support legacy alembic.ini files, this default does NOT
# take place if path_separator is not present in alembic.ini.  If this
# option is omitted entirely, fallback logic is as follows:
#
# 1. Parsing of the version_locations option falls back to using the legacy
#    "version_path_separator" key, which if absent then falls back to the legacy
#    behavior of splitting on spaces and/or commas.
# 2. Parsing of the prepend_sys_path option falls back to the legacy
#    behavior of splitting on spaces, commas, or colons.
#
# Valid values for path_separator are:
#
# path_separator = :
# path_separator = ;
# path_separator = space
# path_separator = newline
#
# Use os.pathsep. Default configuration used for new projects.
path_separator = os


# set to 'true' to search source files recursively
# in each "version_locations" directory
# new in Alembic version 1.10
# recursive_version_locations = false

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

# database URL.  This is consumed by the user-maintained env.py script only.
# other means of configuring database URLs may be customized within the env.py
# file.
sqlalchemy.url = postgresql+asyncpg://user:pass@localhost:5432/dbname


[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

# lint with attempts to fix using "ruff" - use the module runner, against the "ruff" module
# hooks = ruff
# ruff.type = module
# ruff.module = ruff
# ruff.options = check --fix REVISION_SCRIPT_FILENAME

# Alternatively, use the exec runner to execute a binary found on your PATH
# hooks = ruff
# ruff.type = exec
# ruff.executable = ruff
# ruff.options = check --fix REVISION_SCRIPT_FILENAME

# Logging configuration.  This is also consumed by the user-maintained
# env.py script only.
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARNING
handlers = console
qualname =

[logger_sqlalchemy]
level = WARNING
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S



================================================
FILE: docker-compose.yml
================================================
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: eznak
      POSTGRES_PASSWORD: eznak
      POSTGRES_DB: eznak
    ports:
      - "5432:5432"



================================================
FILE: pyproject.toml
================================================
[project]
name = "eznak"
version = "0.1.0"
description = "Автоматизированная система генерации и отложенного постинга для Telegram-каналов"
requires-python = ">=3.11"
dependencies = [
    "fastapi",
    "uvicorn",
    "python-dotenv",
    "sqlalchemy[asyncio]",
    "asyncpg",
    "alembic",
    "pydantic-ai",
    "aiogram",
    "structlog",
    "apscheduler",
    "pillow",
    "aiohttp",
    "pyyaml>=6.0.3",
]



================================================
FILE: test_llm.py
================================================
"""Тест LLM-пайплайна: генерация и ранжирование фраз."""

import asyncio
import json
import os
from uuid import uuid4

# Загружаем .env и настраиваем логирование (LOG_LEVEL из env)
from dotenv import load_dotenv

load_dotenv()

from backend.core.logging import configure_logging

configure_logging()


async def main() -> None:
    from backend.services.llm_pipeline import run_llm_pipeline

    channel_id = uuid4()
    mock_dataset = [
        "У тебя обязательно все получится!",
        "Разреши себе чувствовать и проживать все эмоции",
        "Перестань жертвовать собой ради других!",
        "Страх уходит во время движения!",
        "У тебя есть суперсила и это ты!",
    ]

    print("Запуск LLM-пайплайна...")
    print(f"channel_id: {channel_id}")
    print(f"OPENROUTER_API_KEY: {'***' + os.environ.get('OPENROUTER_API_KEY', '')[-4:] if os.environ.get('OPENROUTER_API_KEY') else 'НЕ ЗАДАН!'}")
    print()

    result = await run_llm_pipeline(channel_id=channel_id, dataset=mock_dataset)

    print("\n--- Результат (RankedPhrase) ---")
    output = [{"text": r.text, "score": r.score} for r in result]
    print(json.dumps(output, ensure_ascii=False, indent=2))
    print(f"\nВсего фраз: {len(result)}")


if __name__ == "__main__":
    asyncio.run(main())



================================================
FILE: test_media.py
================================================
"""Тестовый скрипт для проверки генерации картинок с текстом."""

from backend.services.media_gen import generate_post_image

TEST_TEXT = (
    "Это тестовая фраза для проверки генерации изображения. "
    "Текст должен переноситься на несколько строк и не вылезать за края картинки."
)

if __name__ == "__main__":
    photo_bytes = generate_post_image(TEST_TEXT)
    with open("output.jpg", "wb") as f:
        f.write(photo_bytes)
    print("Сохранено: output.jpg")



================================================
FILE: test_random_llm.py
================================================
#!/usr/bin/env python3
"""
Тест Шага 3: вариативность промптов (рандомизация датасета).
Вызывает LLM-пайплайн для канала из seed.
Проверяет: фразы из datasets, случайная выборка, валидный RankedPhrase.
Запуск: uv run python test_random_llm.py
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import select

from backend.db.models import Channel, Dataset
from backend.db.session import async_session_factory
from backend.services.llm_pipeline import run_llm_pipeline


async def main() -> None:
    async with async_session_factory() as session:
        # Берём первый канал с датасетом (из seed), иначе — любой канал
        result = await session.execute(
            select(Channel)
            .join(Dataset, Dataset.channel_id == Channel.id)
            .limit(1)
        )
        channel = result.scalar_one_or_none()
        if not channel:
            result = await session.execute(select(Channel).limit(1))
            channel = result.scalar_one_or_none()
        if not channel:
            print("ОШИБКА: Нет каналов в БД. Запусти scripts/seed.py")
            sys.exit(1)

        # Проверяем, есть ли датасет у канала
        ds_result = await session.execute(
            select(Dataset.text).where(Dataset.channel_id == channel.id)
        )
        db_phrases = [r for r in ds_result.scalars().all() if r and r.strip()]
        print(f"Канал: {channel.name} (id={channel.id})")
        print(f"Фраз в datasets: {len(db_phrases)}")
        if db_phrases:
            print("Примеры из БД:", db_phrases[:3])
        else:
            print("(будет fallback на default_dataset из YAML)")

        print("\n--- Запуск LLM-пайплайна ---")
        ranked = await run_llm_pipeline(channel_id=channel.id, session=session)

        print(f"\nРезультат: {len(ranked)} фраз (RankedPhrase)")
        for i, p in enumerate(ranked, 1):
            preview = p.text[:80] + "..." if len(p.text) > 80 else p.text
            print(f"  {i}. [{p.score}] {preview}")

        # Критерии успеха
        assert isinstance(ranked, list), "Должен вернуться список"
        for p in ranked:
            assert hasattr(p, "text") and hasattr(p, "score"), "Каждый элемент — RankedPhrase"
            assert 1 <= p.score <= 10, f"Скор должен быть 1-10, получено {p.score}"

        print("\n[OK] Шаг 3 завершен. Вариативность внедрена.")


if __name__ == "__main__":
    asyncio.run(main())



================================================
FILE: .env.example
================================================
# Telegram Bot
BOT_TOKEN=your_bot_token_here

# Доступ только для админов (список Telegram ID через запятую)
ADMIN_TELEGRAM_IDS=123456789,987654321

# Защита API бэкенда
BACKEND_API_KEY=your_secret_api_key_here

# URL бэкенда (для бота)
BACKEND_URL=http://localhost:8000

# База данных (Supabase PostgreSQL)
# Supabase: Settings → Database → Connection string → URI
# Формат: postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:5432/postgres
# Или Direct: postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres
DB_URL=postgresql+asyncpg://user:password@host:5432/dbname

# Логирование (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# LLM (OpenRouter)
OPENROUTER_API_KEY=your_openrouter_api_key_here
# Модель OpenRouter (например: anthropic/claude-sonnet-4, deepseek/deepseek-chat)
OPENROUTER_MODEL=deepseek/deepseek-chat



================================================
FILE: alembic/README
================================================
Generic single-database configuration with an async dbapi.


================================================
FILE: alembic/env.py
================================================
import asyncio
import os
from logging.config import fileConfig
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

from backend.db.models import Base

# Загрузка .env из корня проекта (рядом с alembic.ini)
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_env_path)

config = context.config

# DB_URL из .env — используем напрямую, без ConfigParser (избегаем проблем с % в пароле)
db_url = os.getenv("DB_URL")
if not db_url:
    raise RuntimeError(
        "DB_URL не задан. Создайте .env в корне проекта и укажите DB_URL "
        "(например из Supabase: Settings → Database → Connection string)"
    )
# Supabase даёт postgresql:// или postgres:// — для asyncpg нужен postgresql+asyncpg://
if db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Create engine from DB_URL directly (bypasses ConfigParser and % escaping)."""
    connectable = create_async_engine(db_url, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()



================================================
FILE: alembic/script.py.mako
================================================
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, Sequence[str], None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    """Upgrade schema."""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Downgrade schema."""
    ${downgrades if downgrades else "pass"}



================================================
FILE: alembic/versions/001_init.py
================================================
"""init

Revision ID: 001
Revises:
Create Date: 2025-03-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    poststatus = postgresql.ENUM("draft", "scheduled", "posted", "failed", name="poststatus", create_type=True)
    poststatus.create(op.get_bind(), checkfirst=True)

    # create_type=False — тип уже создан выше, иначе SQLAlchemy попытается создать его снова
    poststatus_col = postgresql.ENUM("draft", "scheduled", "posted", "failed", name="poststatus", create_type=False)

    op.create_table(
        "channels",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("telegram_id", sa.String(64), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "posts",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("channel_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", poststatus_col, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["channel_id"], ["channels.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("posts")
    op.drop_table("channels")
    poststatus = postgresql.ENUM("draft", "scheduled", "posted", "failed", name="poststatus")
    poststatus.drop(op.get_bind(), checkfirst=True)



================================================
FILE: alembic/versions/784ce0a789f1_add_datasets.py
================================================
"""add datasets

Revision ID: 784ce0a789f1
Revises: 001
Create Date: 2026-03-11 16:25:08.733390

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '784ce0a789f1'
down_revision: Union[str, Sequence[str], None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('datasets',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('channel_id', sa.UUID(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('datasets')
    # ### end Alembic commands ###



================================================
FILE: alembic/versions/785_add_datasets_unique.py
================================================
"""add unique constraint datasets channel_id text

Revision ID: 785
Revises: 784ce0a789f1
Create Date: 2026-03-11

"""
from typing import Sequence, Union

from alembic import op

revision: str = "785"
down_revision: Union[str, Sequence[str], None] = "784ce0a789f1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_datasets_channel_id_text",
        "datasets",
        ["channel_id", "text"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_datasets_channel_id_text",
        "datasets",
        type_="unique",
    )



================================================
FILE: alembic/versions/786_add_is_posting_channel.py
================================================
"""add is_posting_channel to channels

Revision ID: 786
Revises: 785
Create Date: 2026-03-11

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "786"
down_revision: Union[str, Sequence[str], None] = "785"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "channels",
        sa.Column("is_posting_channel", sa.Boolean(), nullable=False, server_default=sa.true()),
    )


def downgrade() -> None:
    op.drop_column("channels", "is_posting_channel")



================================================
FILE: alembic/versions/787_add_dataset_source_channel_id.py
================================================
"""add dataset_source_channel_id to channels

Revision ID: 787
Revises: 786
Create Date: 2026-03-11

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "787"
down_revision: Union[str, Sequence[str], None] = "786"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "channels",
        sa.Column(
            "dataset_source_channel_id",
            sa.UUID(),
            sa.ForeignKey("channels.id"),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("channels", "dataset_source_channel_id")



================================================
FILE: alembic/versions/788_add_prompt_templates.py
================================================
"""add prompt_templates table and prompt_template_id to channels

Revision ID: 788
Revises: 787
Create Date: 2026-03-11

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "788"
down_revision: Union[str, Sequence[str], None] = "787"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "prompt_templates",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("generator_system", sa.Text(), nullable=False),
        sa.Column("generator_user_template", sa.Text(), nullable=False),
        sa.Column("critic_system", sa.Text(), nullable=False),
        sa.Column("critic_user_template", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="uq_prompt_templates_name"),
    )
    op.add_column(
        "channels",
        sa.Column(
            "prompt_template_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("prompt_templates.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("channels", "prompt_template_id")
    op.drop_table("prompt_templates")



================================================
FILE: assets/fonts/README.md
================================================
# Шрифты для генерации картинок

Положи сюда `CormorantUnicase-Regular.ttf` или `CormorantUnicase-Regular.otf` для использования шрифта Cormorant Unicase.

Скачать: [Google Fonts](https://fonts.google.com/specimen/Cormorant+Unicase) или поиск по названию.



================================================
FILE: backend/__init__.py
================================================




================================================
FILE: backend/main.py
================================================
from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()

from backend.core.logging import configure_logging

configure_logging()

import structlog
from fastapi import FastAPI

from backend.api.channels import router as channels_router
from backend.api.generation import router as generation_router
from backend.api.posts import router as posts_router
from backend.api.prompt_templates import router as prompt_templates_router
from backend.middleware.logging_middleware import RequestLoggingMiddleware
from backend.services.scheduler import scheduler, setup_scheduler

log = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_scheduler()
    scheduler.start()
    log.info("scheduler_started")
    yield
    scheduler.shutdown(wait=True)


app = FastAPI(lifespan=lifespan)
app.add_middleware(RequestLoggingMiddleware)

app.include_router(channels_router, prefix="/api/v1")
app.include_router(generation_router, prefix="/api/v1")
app.include_router(posts_router, prefix="/api/v1")
app.include_router(prompt_templates_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"status": "ok"}



================================================
FILE: backend/api/__init__.py
================================================




================================================
FILE: backend/api/channels.py
================================================
"""Роутер каналов: datasets bulk insert."""

from uuid import UUID

import structlog
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.api.deps import get_api_key
from backend.db.models import Channel, Dataset
from backend.db.session import get_session

log = structlog.get_logger(__name__)
router = APIRouter(prefix="/channels", tags=["channels"])


@router.get("")
async def list_channels(
    posting_only: bool = False,
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Список каналов (id, name, telegram_id, prompt_template_id, prompt_template_name) — для выбора в боте.
    posting_only: если True — только каналы с is_posting_channel=True.
    """
    log.info("api.channels.list", posting_only=posting_only)
    query = (
        select(Channel)
        .options(selectinload(Channel.prompt_template))
        .order_by(Channel.name)
    )
    if posting_only:
        query = query.where(Channel.is_posting_channel.is_(True))
    result = await session.execute(query)
    channels = result.scalars().all()
    return {
        "channels": [
            {
                "id": str(c.id),
                "name": c.name,
                "telegram_id": c.telegram_id,
                "prompt_template_id": str(c.prompt_template_id) if c.prompt_template_id else None,
                "prompt_template_name": c.prompt_template.name if c.prompt_template else None,
            }
            for c in channels
        ]
    }


class ChannelPatchRequest(BaseModel):
    """Частичное обновление канала."""

    name: str | None = None
    prompt_template_id: UUID | None = Field(None, description="UUID шаблона промптов или null для fallback на YAML")


class BulkDatasetsRequest(BaseModel):
    phrases: list[str] = Field(..., min_length=1, description="Фразы для эталонного датасета")


@router.patch("/{channel_id}")
async def patch_channel(
    channel_id: UUID,
    body: ChannelPatchRequest,
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Обновление канала (name, prompt_template_id).
    """
    log.info("api.channels.patch", channel_id=str(channel_id))
    result = await session.execute(select(Channel).where(Channel.id == channel_id))
    channel = result.scalar_one_or_none()
    if not channel:
        raise HTTPException(status_code=404, detail="Канал не найден")
    updates = body.model_dump(exclude_unset=True)
    if "name" in updates:
        channel.name = updates["name"]
    if "prompt_template_id" in updates:
        pt_id = updates["prompt_template_id"]
        if pt_id:
            from backend.db.models import PromptTemplate

            tpl_result = await session.execute(
                select(PromptTemplate).where(PromptTemplate.id == pt_id)
            )
            if not tpl_result.scalar_one_or_none():
                raise HTTPException(status_code=404, detail="Шаблон промптов не найден")
        channel.prompt_template_id = pt_id
    await session.commit()
    return {"updated": True}


@router.post("/{channel_id}/datasets/bulk")
async def bulk_insert_datasets(
    channel_id: UUID,
    body: BulkDatasetsRequest,
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Bulk insert фраз в датасет канала.
    Одна фраза — одна строка в таблице datasets.
    """
    log.info("api.channels.datasets.bulk", channel_id=str(channel_id), count=len(body.phrases))
    result = await session.execute(select(Channel).where(Channel.id == channel_id))
    channel = result.scalar_one_or_none()
    if not channel:
        raise HTTPException(status_code=404, detail="Канал не найден")

    for text in body.phrases:
        dataset = Dataset(channel_id=channel_id, text=text.strip())
        session.add(dataset)

    log.info("api.channels.datasets.bulk.success", inserted=len(body.phrases))
    return {"inserted": len(body.phrases)}



================================================
FILE: backend/api/deps.py
================================================
"""Зависимости API: проверка API-ключа."""

import os

import structlog
from fastapi import HTTPException, Request

log = structlog.get_logger(__name__)
BACKEND_API_KEY = os.getenv("BACKEND_API_KEY", "")


async def get_api_key(request: Request) -> str:
    """
    Проверяет заголовок X-API-Key на совпадение с BACKEND_API_KEY из .env.
    Защищает все роуты от несанкционированного доступа.
    Возвращает 401 при отсутствии или неверном ключе.
    """
    if not BACKEND_API_KEY:
        log.error("api.auth.no_backend_key", reason="BACKEND_API_KEY не задан в .env")
        raise HTTPException(
            status_code=500,
            detail="BACKEND_API_KEY не настроен на сервере",
        )
    x_api_key = request.headers.get("X-API-Key")
    if not x_api_key or x_api_key != BACKEND_API_KEY:
        log.warning(
            "api.auth.unauthorized",
            path=request.url.path,
            has_key=bool(x_api_key),
            reason="Неверный или отсутствующий X-API-Key. Проверь BACKEND_API_KEY в .env бота.",
        )
        raise HTTPException(status_code=401, detail="Неверный или отсутствующий API-ключ")
    return x_api_key



================================================
FILE: backend/api/generation.py
================================================
"""Роутер генерации фраз через LLM."""

from uuid import UUID

import structlog
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps import get_api_key
from backend.db.models import Channel
from backend.db.session import get_session
from backend.services.llm_pipeline import run_llm_pipeline

log = structlog.get_logger(__name__)
router = APIRouter(prefix="/generate", tags=["generation"])


class GenerateRequest(BaseModel):
    channel_id: UUID = Field(..., description="UUID канала для генерации")


@router.post("")
async def generate_phrases(
    body: GenerateRequest,
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Генерирует фразы через LLM-пайплайн.
    Body строго {"channel_id": "uuid"}.
    """
    log.info("api.generate.request", channel_id=str(body.channel_id))
    result = await session.execute(select(Channel).where(Channel.id == body.channel_id))
    channel = result.scalar_one_or_none()
    if not channel:
        raise HTTPException(status_code=404, detail="Канал не найден")

    channel_id: UUID = channel.id
    log.info("api.generate.channel_found", channel_id=str(channel_id), channel_name=channel.name)
    try:
        ranked = await run_llm_pipeline(channel_id=channel_id, session=session)
    except Exception as e:
        log.exception("api.generate.llm_error", channel_id=str(channel_id), error=str(e))
        raise

    phrases = [p.text for p in ranked]
    if not phrases:
        log.warning(
            "api.generate.empty_phrases",
            channel_id=str(channel_id),
            reason="LLM вернул пустой список или ранжирование отфильтровало всё. Проверь OPENROUTER_API_KEY и промпты.",
        )
        return {"status": "ok", "channel_id": str(channel_id), "channel_name": channel.name, "phrases": []}

    log.info("api.generate.success", channel_id=str(channel_id), count=len(phrases))
    return {"status": "ok", "channel_id": str(channel_id), "channel_name": channel.name, "phrases": phrases}



================================================
FILE: backend/api/posts.py
================================================
"""Роутер постов: approve, schedule-batch, post-now."""

import random
from datetime import datetime, timedelta
from uuid import UUID

import aiohttp
import structlog
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from zoneinfo import ZoneInfo

from backend.api.deps import get_api_key
from backend.core.config import BOT_TOKEN
from backend.core.config_loader import get_media
from backend.db.models import Channel, Post, PostStatus
from backend.db.session import get_session

log = structlog.get_logger(__name__)
router = APIRouter(prefix="/posts", tags=["posts"])

MSK = ZoneInfo("Europe/Moscow")

# Слоты по МСК для suggested_time (часы дня)
DEFAULT_SLOT_HOURS = [9, 12, 15, 18, 21]
MAX_POSTS_PER_DAY = 2


def _generate_suggested_times(count: int) -> list[datetime]:
    """Генерирует слоты времени по МСК. Не более MAX_POSTS_PER_DAY постов в день."""
    now = datetime.now(MSK)
    start = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    hours_to_use = DEFAULT_SLOT_HOURS[:MAX_POSTS_PER_DAY]
    slots: list[datetime] = []
    for i in range(count):
        day_offset = i // MAX_POSTS_PER_DAY
        hour_idx = i % MAX_POSTS_PER_DAY
        day = start + timedelta(days=day_offset)
        hour = hours_to_use[hour_idx]
        slot = day.replace(hour=hour, minute=0, second=0, microsecond=0)
        slots.append(slot)
    return slots


# --- Schemas ---

class ApproveRequest(BaseModel):
    channel_id: UUID = Field(..., description="UUID канала")
    phrases: list[str] = Field(..., min_length=1, description="Финальные тексты постов")


class DraftPostResponse(BaseModel):
    id: UUID
    text: str
    channel_id: UUID
    channel_name: str
    suggested_time: str  # ISO8601 с таймзоной

    class Config:
        from_attributes = True


class ScheduleItem(BaseModel):
    post_id: UUID
    channel_id: UUID
    time: str  # ISO8601


class PostNowRequest(BaseModel):
    post_id: UUID = Field(..., description="UUID поста для немедленной публикации")


class ApproveOneRequest(BaseModel):
    channel_id: UUID = Field(..., description="UUID канала")
    text: str = Field(..., min_length=1, description="Текст поста")


class PatchPostRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Новый текст поста")


TELEGRAM_API = "https://api.telegram.org"


# --- Endpoints ---

@router.get("")
async def list_posts(
    status: PostStatus | None = Query(None, description="Фильтр по статусу"),
    channel_id: UUID | None = Query(None, description="Фильтр по каналу"),
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Список постов. Для бота: status=scheduled — ожидающие постинга, status=draft — черновики.
    """
    log.info("api.posts.list", status=status.value if status else "all", channel_id=str(channel_id) if channel_id else None)
    q = select(Post).options(selectinload(Post.channel))
    if status == PostStatus.draft:
        q = q.order_by(Post.created_at.asc())
    else:
        q = q.order_by(Post.scheduled_at.asc())
    if status is not None:
        q = q.where(Post.status == status)
    if channel_id is not None:
        q = q.where(Post.channel_id == channel_id)
    result = await session.execute(q)
    posts = result.scalars().all()
    log.info("api.posts.list.result", count=len(posts))
    full_text = status == PostStatus.scheduled or status == PostStatus.draft
    suggested_times = _generate_suggested_times(len(posts)) if status == PostStatus.draft and posts else []
    return {
        "posts": [
            {
                "id": str(p.id),
                "text": p.text if full_text else (p.text[:100] + "..." if len(p.text) > 100 else p.text),
                "channel_id": str(p.channel_id),
                "channel_name": p.channel.name if p.channel else None,
                "scheduled_at": p.scheduled_at.isoformat() if p.scheduled_at else None,
                "status": p.status.value,
                **({"suggested_time": suggested_times[i].isoformat()} if status == PostStatus.draft and i < len(suggested_times) else {}),
            }
            for i, p in enumerate(posts)
        ]
    }


@router.post("/{post_id}/cancel")
async def cancel_post(
    post_id: UUID,
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Отмена поста из расписания. Переводит status в draft, scheduled_at в None.
    """
    log.info("api.posts.cancel", post_id=str(post_id))
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    if post.status != PostStatus.scheduled:
        raise HTTPException(status_code=400, detail="Можно отменить только пост со статусом scheduled")
    post.status = PostStatus.draft
    post.scheduled_at = None
    await session.commit()
    log.info("api.posts.cancel.success", post_id=str(post_id))
    return {"status": "cancelled", "post_id": str(post_id)}


@router.post("/approve")
async def approve_posts(
    body: ApproveRequest,
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Создаёт посты для указанного канала со статусом draft.
    Возвращает draft_posts с id, text, channel_id, channel_name, suggested_time.
    """
    log.info("api.posts.approve", channel_id=str(body.channel_id), phrases_count=len(body.phrases))
    result = await session.execute(select(Channel).where(Channel.id == body.channel_id))
    channel = result.scalar_one_or_none()
    if not channel:
        raise HTTPException(status_code=404, detail="Канал не найден")

    channel_id = channel.id
    channel_name = channel.name
    suggested_times = _generate_suggested_times(len(body.phrases))

    draft_posts: list[dict] = []
    for i, text in enumerate(body.phrases):
        post = Post(
            channel_id=channel_id,
            text=text,
            status=PostStatus.draft,
            scheduled_at=None,
        )
        session.add(post)
        await session.flush()  # чтобы получить id

        slot = suggested_times[i]
        draft_posts.append({
            "id": post.id,
            "text": post.text,
            "channel_id": post.channel_id,
            "channel_name": channel_name,
            "suggested_time": slot.isoformat(),
        })

    log.info("api.posts.approve.success", draft_count=len(draft_posts))
    return {"draft_posts": draft_posts}


@router.post("/approve-one")
async def approve_one(
    body: ApproveOneRequest,
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Создаёт один пост со статусом draft.
    Возвращает id, text, channel_id, channel_name.
    """
    log.info("api.posts.approve_one", channel_id=str(body.channel_id))
    result = await session.execute(select(Channel).where(Channel.id == body.channel_id))
    channel = result.scalar_one_or_none()
    if not channel:
        raise HTTPException(status_code=404, detail="Канал не найден")
    post = Post(
        channel_id=channel.id,
        text=body.text,
        status=PostStatus.draft,
        scheduled_at=None,
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    log.info("api.posts.approve_one.success", post_id=str(post.id))
    return {
        "id": str(post.id),
        "text": post.text,
        "channel_id": str(post.channel_id),
        "channel_name": channel.name,
    }


@router.patch("/{post_id}")
async def patch_post(
    post_id: UUID,
    body: PatchPostRequest,
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Обновляет текст поста. Только для status=draft.
    """
    log.info("api.posts.patch", post_id=str(post_id))
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    if post.status != PostStatus.draft:
        raise HTTPException(status_code=400, detail="Можно редактировать только черновик")
    post.text = body.text
    await session.commit()
    log.info("api.posts.patch.success", post_id=str(post_id))
    return {"id": str(post.id), "text": post.text}


@router.post("/schedule-batch")
async def schedule_batch(
    body: list[ScheduleItem],
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Пакетное подтверждение расписания.
    Обновляет посты: scheduled_at и статус scheduled.
    Время в MSK (ISO8601).
    """
    log.info("api.posts.schedule_batch", items_count=len(body))
    for item in body:
        result = await session.execute(select(Post).where(Post.id == item.post_id))
        post = result.scalar_one_or_none()
        if not post:
            continue
        if post.channel_id != item.channel_id:
            continue

        dt = datetime.fromisoformat(item.time.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=MSK)
        post.scheduled_at = dt
        post.status = PostStatus.scheduled

    log.info("api.posts.schedule_batch.success", scheduled=len(body))
    return {"scheduled": len(body)}


@router.post("/post-now")
async def post_now(
    body: PostNowRequest,
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Немедленная публикация поста в канал.
    Находит пост, достаёт post.channel.telegram_id, отправляет туда
    (sendMessage или sendPhoto с вероятностью из config/media.yaml, 0.3).
    Меняет статус на posted.
    """
    log.info("api.posts.post_now", post_id=str(body.post_id))
    result = await session.execute(
        select(Post).options(selectinload(Post.channel)).where(Post.id == body.post_id)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    if not post.channel:
        raise HTTPException(status_code=500, detail="Канал поста не найден")

    if not BOT_TOKEN:
        raise HTTPException(status_code=503, detail="BOT_TOKEN не задан")

    target_channel_id = post.channel.telegram_id
    channel_name = post.channel.name

    image_prob = get_media().get("image_probability", 0.3)
    use_media = random.random() <= image_prob
    photo_bytes = None

    if use_media:
        try:
            from backend.services.media_gen import generate_post_image

            photo_bytes = generate_post_image(post.text)
        except Exception as e:
            log.warning("api.posts.post_now.media_gen_failed", post_id=str(post.id), error=str(e))
            use_media = False

    async with aiohttp.ClientSession() as http:
        if use_media and photo_bytes:
            url = f"{TELEGRAM_API}/bot{BOT_TOKEN}/sendPhoto"
            form = aiohttp.FormData()
            form.add_field("chat_id", target_channel_id)
            form.add_field("photo", photo_bytes, filename="post.jpg", content_type="image/jpeg")
            async with http.post(url, data=form) as resp:
                data = await resp.json()
                status_code = resp.status
        else:
            url = f"{TELEGRAM_API}/bot{BOT_TOKEN}/sendMessage"
            async with http.post(url, json={"chat_id": target_channel_id, "text": post.text}) as resp:
                data = await resp.json()
                status_code = resp.status

    if status_code != 200 or not data.get("ok"):
        desc = data.get("description", "unknown")
        log.error("api.posts.post_now.telegram_error", post_id=str(post.id), description=desc)
        raise HTTPException(status_code=502, detail=f"Telegram API: {desc}")

    post.status = PostStatus.posted
    await session.commit()

    log.info(
        "api.posts.post_now.success",
        post_id=str(post.id),
        channel_name=channel_name,
        has_media=use_media,
    )
    return {
        "status": "posted",
        "post_id": str(post.id),
        "channel_id": str(post.channel_id),
        "channel_name": channel_name,
        "has_media": use_media,
    }



================================================
FILE: backend/api/prompt_templates.py
================================================
"""Роутер шаблонов промптов."""

from uuid import UUID

import structlog
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps import get_api_key
from backend.db.models import PromptTemplate
from backend.db.session import get_session

log = structlog.get_logger(__name__)
router = APIRouter(prefix="/prompt-templates", tags=["prompt-templates"])


@router.get("")
async def list_prompt_templates(
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Список шаблонов промптов (id, name).
    """
    log.info("api.prompt_templates.list")
    result = await session.execute(select(PromptTemplate).order_by(PromptTemplate.name))
    templates = result.scalars().all()
    return {
        "prompt_templates": [
            {"id": str(t.id), "name": t.name}
            for t in templates
        ]
    }


@router.get("/{template_id}")
async def get_prompt_template(
    template_id: UUID,
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Детали шаблона: все 4 промпта.
    """
    log.info("api.prompt_templates.get", template_id=str(template_id))
    result = await session.execute(
        select(PromptTemplate).where(PromptTemplate.id == template_id)
    )
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="Шаблон не найден")
    return {
        "id": str(template.id),
        "name": template.name,
        "generator_system": template.generator_system,
        "generator_user_template": template.generator_user_template,
        "critic_system": template.critic_system,
        "critic_user_template": template.critic_user_template,
    }



================================================
FILE: backend/core/__init__.py
================================================
[Empty file]


================================================
FILE: backend/core/config.py
================================================
"""Конфигурация приложения из переменных окружения."""

import os

TARGET_CHANNEL_ID: str = os.getenv("TARGET_CHANNEL_ID", "")
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")



================================================
FILE: backend/core/config_loader.py
================================================
"""Загрузка конфигов из YAML (промпты, медиа)."""

from pathlib import Path

import yaml

# Корень проекта (родитель backend/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"


def _load_yaml(filename: str) -> dict:
    path = CONFIG_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Конфиг не найден: {path}")
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_prompts() -> dict:
    """Загружает config/prompts.yaml."""
    return _load_yaml("prompts.yaml")


def load_media() -> dict:
    """Загружает config/media.yaml."""
    return _load_yaml("media.yaml")


# Кэш при первом обращении
_prompts_cache: dict | None = None
_media_cache: dict | None = None


def get_prompts() -> dict:
    """Возвращает промпты (кэшировано)."""
    global _prompts_cache
    if _prompts_cache is None:
        _prompts_cache = load_prompts()
    return _prompts_cache


def get_media() -> dict:
    """Возвращает настройки медиа (кэшировано)."""
    global _media_cache
    if _media_cache is None:
        _media_cache = load_media()
    return _media_cache



================================================
FILE: backend/core/logging.py
================================================
"""Централизованная настройка structlog + stdlib. Уровень из LOG_LEVEL в env."""

import logging
import os
import sys

import structlog


def _get_log_level() -> int:
    """Уровень логирования из env. DEBUG, INFO, WARNING, ERROR."""
    name = os.environ.get("LOG_LEVEL", "INFO").upper()
    return getattr(logging, name, logging.INFO)


def configure_logging() -> None:
    """
    Настраивает structlog с stdlib как backend.
    Все логи (structlog + uvicorn) идут в один поток через logging.
    """
    level = _get_log_level()

    # Общие процессоры для structlog
    shared_processors = [
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # ProcessorFormatter для вывода structlog-событий
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.dev.ConsoleRenderer(
                colors=True,
                exception_formatter=structlog.dev.plain_traceback,
            ),
        ],
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)

    # uvicorn — пусть идёт через root
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        log = logging.getLogger(name)
        log.handlers.clear()
        log.propagate = True



================================================
FILE: backend/core/prompts.py
================================================
"""Промпты и датасет — загружаются из config/prompts.yaml."""

from backend.core.config_loader import get_prompts

_prompts = get_prompts()
_generator = _prompts.get("generator", {})
_critic = _prompts.get("critic", {})

DEFAULT_DATASET: list[str] = _prompts.get("default_dataset", [])
PROMPT_1_SYSTEM: str = _generator.get("system", "")
PROMPT_1_USER_TEMPLATE: str = _generator.get("user_template", "")
PROMPT_2_SYSTEM: str = _critic.get("system", "")
PROMPT_2_USER_TEMPLATE: str = _critic.get("user_template", "")



================================================
FILE: backend/db/__init__.py
================================================




================================================
FILE: backend/db/models.py
================================================
import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class PromptTemplate(Base):
    __tablename__ = "prompt_templates"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    generator_system: Mapped[str] = mapped_column(Text, nullable=False)
    generator_user_template: Mapped[str] = mapped_column(Text, nullable=False)
    critic_system: Mapped[str] = mapped_column(Text, nullable=False)
    critic_user_template: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class PostStatus(str, PyEnum):
    draft = "draft"
    scheduled = "scheduled"
    posted = "posted"
    failed = "failed"


class Channel(Base):
    __tablename__ = "channels"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    telegram_id: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_posting_channel: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    dataset_source_channel_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("channels.id"), nullable=True
    )
    prompt_template_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("prompt_templates.id", ondelete="SET NULL"),
        nullable=True,
    )

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="channel")
    prompt_template: Mapped["PromptTemplate | None"] = relationship(
        "PromptTemplate", lazy="selectin"
    )
    datasets: Mapped[list["Dataset"]] = relationship("Dataset", back_populates="channel")


class Dataset(Base):
    __tablename__ = "datasets"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    channel_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("channels.id"), nullable=False
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)

    channel: Mapped["Channel"] = relationship("Channel", back_populates="datasets")


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    channel_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("channels.id"), nullable=False
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[PostStatus] = mapped_column(
        Enum(PostStatus), nullable=False, default=PostStatus.draft
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )

    channel: Mapped["Channel"] = relationship("Channel", back_populates="posts")



================================================
FILE: backend/db/session.py
================================================
"""Асинхронная сессия БД для FastAPI."""

import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.db.models import Base

db_url = os.getenv("DB_URL")
if not db_url:
    raise RuntimeError("DB_URL не задан в .env")

if db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)

engine = create_async_engine(db_url, echo=False)
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_session() -> AsyncSession:
    """Dependency для FastAPI: выдаёт сессию БД."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise



================================================
FILE: backend/middleware/__init__.py
================================================
[Empty file]


================================================
FILE: backend/middleware/logging_middleware.py
================================================
"""Middleware для логирования запросов."""

import time

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

log = structlog.get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Логирует каждый запрос: method, path, status, duration_ms."""

    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        log.info(
            "request",
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=round(duration_ms, 1),
        )
        return response



================================================
FILE: backend/services/__init__.py
================================================
[Empty file]


================================================
FILE: backend/services/llm_pipeline.py
================================================
"""LLM-пайплайн: генерация 15 фраз -> ранжирование -> топ M фраз (Pydantic)."""

import os
import random
from datetime import datetime
from uuid import UUID
from zoneinfo import ZoneInfo

import structlog
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.core.config_loader import get_prompts
from backend.core.prompts import DEFAULT_DATASET
from backend.db.models import Channel, Dataset

log = structlog.get_logger(__name__)

MSK = ZoneInfo("Europe/Moscow")
MONTHS_RU = [
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря",
]
WEEKDAYS_RU = [
    "понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье",
]


def _format_today_msk() -> str:
    """Человекочитаемая дата для промпта: '12 марта 2026, среда'."""
    now = datetime.now(MSK)
    return f"{now.day} {MONTHS_RU[now.month - 1]} {now.year}, {WEEKDAYS_RU[now.weekday()]}"


def _get_sample_size() -> int:
    """Размер выборки из датасета (из config/prompts.yaml)."""
    return int(get_prompts().get("dataset_sample_size", 50))


# --- Pydantic-модели для structured output ---

class GeneratedPhrases(BaseModel):
    """Выход Prompt 1: 15 сгенерированных фраз."""

    phrases: list[str] = Field(description="Ровно 15 мотивационных фраз")


class RankedPhrase(BaseModel):
    """Одна фраза с оценкой."""

    text: str = Field(description="Текст фразы")
    score: int = Field(ge=1, le=10, description="Оценка от 1 до 10")


class LLMResponse(BaseModel):
    """Выход Prompt 2: отфильтрованные фразы со скором >= 7, макс. 7 шт."""

    approved_phrases: list[RankedPhrase] = Field(
        description="Лучшие фразы (скор >= 7), максимум 7"
    )


# --- Агенты pydantic-ai ---

def _get_openrouter_model() -> str:
    """Модель OpenRouter из env. Fallback: anthropic/claude-sonnet-4."""
    return os.environ.get("OPENROUTER_MODEL", "anthropic/claude-sonnet-4")


def _create_generator_agent(system_prompt: str) -> Agent[None, GeneratedPhrases]:
    """Агент для генерации 15 фраз."""
    return Agent(
        f"openrouter:{_get_openrouter_model()}",
        output_type=GeneratedPhrases,
        system_prompt=system_prompt,
    )


def _create_ranker_agent(system_prompt: str) -> Agent[None, LLMResponse]:
    """Агент для ранжирования и отбора фраз."""
    return Agent(
        f"openrouter:{_get_openrouter_model()}",
        output_type=LLMResponse,
        system_prompt=system_prompt,
    )


async def _get_prompts_for_channel(
    session: AsyncSession, channel_id: UUID
) -> tuple[str, str, str, str, str]:
    """
    Возвращает (gen_system, gen_user_template, critic_system, critic_user_template, prompt_source).
    prompt_source: имя шаблона или "yaml_fallback".
    """
    result = await session.execute(
        select(Channel)
        .options(selectinload(Channel.prompt_template))
        .where(Channel.id == channel_id)
    )
    channel = result.scalar_one_or_none()
    if channel and channel.prompt_template_id and channel.prompt_template:
        t = channel.prompt_template
        return (
            t.generator_system,
            t.generator_user_template,
            t.critic_system,
            t.critic_user_template,
            t.name,
        )
    prompts = get_prompts()
    gen = prompts.get("generator", {})
    crit = prompts.get("critic", {})
    return (
        gen.get("system", ""),
        gen.get("user_template", ""),
        crit.get("system", ""),
        crit.get("user_template", ""),
        "yaml_fallback",
    )


async def _fetch_dataset_for_channel(session: AsyncSession, channel_id: UUID) -> list[str]:
    """
    Загружает фразы из datasets.
    Если у канала задан dataset_source_channel_id — берёт датасет из того канала.
    Иначе — из своего channel_id.
    Если пусто — fallback на default_dataset из YAML.
    Случайная выборка (размер из config: dataset_sample_size) для вариативности.
    """
    channel_result = await session.execute(select(Channel).where(Channel.id == channel_id))
    channel = channel_result.scalar_one_or_none()
    effective_id = channel.dataset_source_channel_id if channel and channel.dataset_source_channel_id else channel_id

    result = await session.execute(
        select(Dataset.text).where(Dataset.channel_id == effective_id)
    )
    rows = result.scalars().all()
    phrases = [r for r in rows if r and r.strip()]

    if not phrases:
        log.info(
            "llm_pipeline_dataset_empty",
            channel_id=str(channel_id),
            source_channel_id=str(effective_id),
            fallback="default_dataset",
        )
        phrases = list(DEFAULT_DATASET)

    sample_count = min(_get_sample_size(), len(phrases))
    sampled = random.sample(phrases, sample_count)
    source = "datasets" if rows else "default_dataset"
    log.info(
        "llm_pipeline_dataset_loaded",
        channel_id=str(channel_id),
        source_channel_id=str(effective_id),
        total=len(phrases),
        sampled=sample_count,
        source=source,
    )
    return sampled


async def run_llm_pipeline(
    channel_id: UUID,
    session: AsyncSession | None = None,
    dataset: list[str] | None = None,
) -> list[RankedPhrase]:
    """
    Цепочка: Prompt 1 (15 фраз) -> Prompt 2 (ранжирование).
    Возвращает список RankedPhrase (макс. 7).
    dataset: если передан — используется как есть; иначе — запрос в БД + рандомизация (session обязателен).
    """
    if dataset is not None:
        phrases_data = dataset
        log.info("llm_pipeline_dataset_override", channel_id=str(channel_id), size=len(phrases_data))
    else:
        if session is None:
            raise ValueError("session обязателен, когда dataset не передан (нужен запрос в БД)")
        phrases_data = await _fetch_dataset_for_channel(session, channel_id)

    if session is not None:
        gen_system, gen_user_tpl, critic_system, critic_user_tpl, prompt_source = (
            await _get_prompts_for_channel(session, channel_id)
        )
    else:
        prompts = get_prompts()
        gen = prompts.get("generator", {})
        crit = prompts.get("critic", {})
        gen_system = gen.get("system", "")
        gen_user_tpl = gen.get("user_template", "")
        critic_system = crit.get("system", "")
        critic_user_tpl = crit.get("user_template", "")
        prompt_source = "yaml_fallback"

    log.info(
        "llm_pipeline_start",
        channel_id=str(channel_id),
        dataset_size=len(phrases_data),
        model=_get_openrouter_model(),
        prompt_source=prompt_source,
    )

    dataset_text = "\n".join(f"- {p}" for p in phrases_data)
    log.debug(
        "llm_pipeline_dataset",
        channel_id=str(channel_id),
        dataset=phrases_data,
        dataset_text=dataset_text,
    )

    # --- Шаг 1: Генерация 15 фраз ---
    gen_agent = _create_generator_agent(gen_system)
    user_prompt_1 = gen_user_tpl.format(dataset=dataset_text)
    user_prompt_1 += f"\n\nКонтекст: сегодня {_format_today_msk()}. Учитывай сезон при упоминании погоды и времени года."

    log.debug(
        "llm_pipeline_prompt1",
        channel_id=str(channel_id),
        system_prompt=gen_system,
        user_prompt=user_prompt_1,
    )

    result_1 = await gen_agent.run(user_prompt_1)
    generated = result_1.output

    if not generated.phrases:
        log.warning("llm_pipeline_empty_generation", channel_id=str(channel_id))
        return []

    # Берём до 15 фраз (модель может вернуть меньше)
    phrases_to_rank = generated.phrases[:15]
    log.info(
        "llm_pipeline_generated",
        channel_id=str(channel_id),
        count=len(phrases_to_rank),
    )
    log.debug(
        "llm_pipeline_generated_phrases",
        channel_id=str(channel_id),
        phrases=phrases_to_rank,
    )

    # --- Шаг 2: Ранжирование ---
    phrases_block = "\n".join(f"{i+1}. {p}" for i, p in enumerate(phrases_to_rank))
    user_prompt_2 = critic_user_tpl.format(phrases=phrases_block)

    log.debug(
        "llm_pipeline_prompt2",
        channel_id=str(channel_id),
        system_prompt=critic_system,
        user_prompt=user_prompt_2,
        input_phrases=phrases_to_rank,
    )

    rank_agent = _create_ranker_agent(critic_system)
    result_2 = await rank_agent.run(user_prompt_2)
    ranked = result_2.output

    approved = ranked.approved_phrases
    log.info(
        "llm_pipeline_ranked",
        channel_id=str(channel_id),
        approved_count=len(approved),
    )
    if not approved:
        log.warning(
            "llm_pipeline_empty_ranker",
            channel_id=str(channel_id),
            reason="Ранжировщик отфильтровал все фразы (скор < 7). Попробуй другой датасет или модель.",
        )
    log.debug(
        "llm_pipeline_ranked_output",
        channel_id=str(channel_id),
        approved_phrases=[{"text": p.text, "score": p.score} for p in approved],
    )

    return approved



================================================
FILE: backend/services/media_gen.py
================================================
"""Генерация картинок с текстом поста через Pillow."""

import io
import random
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from backend.core.config_loader import get_media

# Позиции загружаются из config/media.yaml


def _get_text_positions() -> list[tuple[float, float]]:
    media = get_media()
    positions = media.get("text_positions", [{"x": 0.5, "y": 0.5}])
    return [(p.get("x", 0.5), p.get("y", 0.5)) for p in positions]

TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "assets" / "templates"
FONTS_DIR = Path(__file__).resolve().parents[2] / "assets" / "fonts"
FONT_SIZE = 32  # 48 / 1.5
TEXT_COLOR = (255, 255, 255)
PADDING_RATIO = 0.85  # текст занимает до 85% ширины


def _get_font(size: int = FONT_SIZE) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Загружает Arial, fallback — Cormorant Unicase, затем дефолтный шрифт."""
    candidates = [
        "arial.ttf",
        "Arial.ttf",
        "C:/Windows/Fonts/arial.ttf",
        str(FONTS_DIR / "CormorantUnicase-Regular.ttf"),
        str(FONTS_DIR / "CormorantUnicase-Regular.otf"),
        "C:/Windows/Fonts/CormorantUnicase-Regular.ttf",
        "C:/Windows/Fonts/CormorantUnicase-Regular.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/msttcorefonts/arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _pick_background() -> Path:
    """Выбирает случайный фон из assets/templates/."""
    if not TEMPLATES_DIR.exists():
        raise FileNotFoundError(f"Папка шаблонов не найдена: {TEMPLATES_DIR}")
    exts = {".jpg", ".jpeg", ".png"}
    files = [f for f in TEMPLATES_DIR.iterdir() if f.suffix.lower() in exts]
    if not files:
        raise FileNotFoundError(
            f"Нет фонов в {TEMPLATES_DIR}. Добавьте bg.jpg или другой файл."
        )
    return random.choice(files)


def generate_post_image(
    text: str,
    position: tuple[float, float] | None = None,
) -> bytes:
    """
    Генерирует изображение с текстом поста на случайном фоне.

    Args:
        text: Текст поста.
        position: Позиция текста (x, y) — доли 0–1. Если None — случайная
            из config/media.yaml.

    Returns:
        Байты JPEG-изображения.
    """
    bg_path = _pick_background()
    img = Image.open(bg_path).convert("RGB")
    w, h = img.size

    text = text.lower()
    font_size = FONT_SIZE
    font = _get_font(font_size)
    max_chars = max(10, int(w * PADDING_RATIO / (font_size * 0.5)))
    lines = textwrap.wrap(text, width=max_chars)
    wrapped = "\n".join(lines)

    draw = ImageDraw.Draw(img)
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Уменьшаем шрифт, если текст не помещается
    while (text_w > w * PADDING_RATIO or text_h > h * PADDING_RATIO) and font_size > 12:
        font_size -= 4
        font = _get_font(font_size)
        max_chars = max(10, max_chars - 2)
        lines = textwrap.wrap(text, width=max_chars)
        wrapped = "\n".join(lines)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

    if position is None:
        positions = _get_text_positions()
        px, py = random.choice(positions) if positions else (0.5, 0.5)
    else:
        px, py = position
    xy = (int(w * px), int(h * py))

    draw.multiline_text(
        xy,
        wrapped,
        font=font,
        fill=TEXT_COLOR,
        align="center",
        anchor="mm",
    )

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()



================================================
FILE: backend/services/scheduler.py
================================================
"""APScheduler для автопостинга одобренных постов в Telegram."""

import asyncio
import random
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import aiohttp
import structlog
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

from backend.core.config import BOT_TOKEN
from backend.core.config_loader import get_media
from backend.db.models import Post, PostStatus
from backend.db.session import async_session_factory
from sqlalchemy.orm import selectinload

log = structlog.get_logger(__name__)
MSK = ZoneInfo("Europe/Moscow")

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

TELEGRAM_API = "https://api.telegram.org"


async def _publish_scheduled_posts() -> None:
    """
    Job: раз в минуту ищем посты со status=scheduled и scheduled_at <= now (UTC).
    Отправляем в post.channel.telegram_id, при успехе — status=posted.
    """
    if not BOT_TOKEN:
        log.warning("scheduler.skip", reason="BOT_TOKEN не задан")
        return

    now_utc = datetime.now(timezone.utc)

    async with async_session_factory() as session:
        try:
            result = await session.execute(
                select(Post)
                .options(selectinload(Post.channel))
                .where(Post.status == PostStatus.scheduled)
                .where(Post.scheduled_at <= now_utc)
                .order_by(Post.scheduled_at.asc())
            )
            posts = result.scalars().all()
        except Exception as e:
            log.error("scheduler.db_error", error=str(e), exc_info=True)
            return

        if not posts:
            return

        async with aiohttp.ClientSession() as http:
            for post in posts:
                try:
                    if not post.channel:
                        log.warning("scheduler.skip_post", post_id=str(post.id), reason="Канал не найден")
                        continue
                    if not getattr(post.channel, "is_posting_channel", True):
                        log.warning(
                            "scheduler.skip_post",
                            post_id=str(post.id),
                            reason="Канал dataset-only, постинг запрещён",
                        )
                        continue

                    target_channel_id = post.channel.telegram_id
                    image_prob = get_media().get("image_probability", 0.03)
                    use_media = random.random() <= image_prob
                    photo_bytes = None

                    if use_media:
                        try:
                            from backend.services.media_gen import generate_post_image

                            photo_bytes = generate_post_image(post.text)
                        except Exception as e:
                            log.warning(
                                "scheduler.media_gen_failed",
                                post_id=str(post.id),
                                error=str(e),
                            )
                            use_media = False

                    if use_media and photo_bytes:
                        url = f"{TELEGRAM_API}/bot{BOT_TOKEN}/sendPhoto"
                        form = aiohttp.FormData()
                        form.add_field("chat_id", target_channel_id)
                        form.add_field(
                            "photo",
                            photo_bytes,
                            filename="post.jpg",
                            content_type="image/jpeg",
                        )
                        async with http.post(url, data=form) as resp:
                            data = await resp.json()
                            resp_status = resp.status
                    else:
                        url = f"{TELEGRAM_API}/bot{BOT_TOKEN}/sendMessage"
                        async with http.post(
                            url,
                            json={"chat_id": target_channel_id, "text": post.text},
                        ) as resp:
                            data = await resp.json()
                            resp_status = resp.status

                    if resp_status != 200 or not data.get("ok"):
                        desc = data.get("description", "unknown")
                        log.error(
                            "scheduler.telegram_error",
                            post_id=str(post.id),
                            status=resp_status,
                            description=desc,
                        )
                        continue

                    post.status = PostStatus.posted
                    await session.commit()

                    scheduled_msk = (
                        post.scheduled_at.astimezone(MSK).isoformat()
                        if post.scheduled_at
                        else None
                    )
                    text_preview = post.text[:100] + "..." if len(post.text) > 100 else post.text
                    log.info(
                        "post_published",
                        post_id=str(post.id),
                        text=text_preview,
                        scheduled_at_msk=scheduled_msk,
                        has_media=use_media,
                    )

                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    log.error(
                        "scheduler.telegram_request_error",
                        post_id=str(post.id),
                        error=str(e),
                        exc_info=True,
                    )
                except Exception as e:
                    log.error(
                        "scheduler.unexpected_error",
                        post_id=str(post.id),
                        error=str(e),
                        exc_info=True,
                    )
                    await session.rollback()


def setup_scheduler() -> None:
    """Добавляет job публикации постов (раз в минуту)."""
    scheduler.add_job(
        _publish_scheduled_posts,
        "interval",
        minutes=1,
        id="publish_scheduled_posts",
    )



================================================
FILE: bot/__init__.py
================================================




================================================
FILE: bot/bot.py
================================================
"""
Telegram-бот для генерации и модерации постов.
Шаг 6: Ручной ввод времени (FSM).
"""

import html
import os
import random
import re
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from dotenv import load_dotenv


class EditPhraseStates(StatesGroup):
    waiting_for_text = State()


class ManualTimeStates(StatesGroup):
    waiting_for_time = State()


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")
BACKEND_API_KEY = os.getenv("BACKEND_API_KEY", "")

# Список Telegram ID админов (через запятую)
_ADMIN_IDS: set[int] = set()
_raw = os.getenv("ADMIN_TELEGRAM_IDS", "")
if _raw:
    for s in _raw.split(","):
        s = s.strip()
        if s.isdigit():
            _ADMIN_IDS.add(int(s))


def _is_admin(user_id: int) -> bool:
    return user_id in _ADMIN_IDS


# --- Reply-меню ---
def get_main_keyboard() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    builder.button(text="🎲 Сгенерировать")
    builder.button(text="📅 Ожидают постинга")
    builder.button(text="📤 Отправить на планирование")
    builder.adjust(2, 1)
    return builder


# --- Inline-кнопки для фразы ---
def get_phrase_keyboard(phrase_idx: int) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Approve", callback_data=f"approve:{phrase_idx}")
    builder.button(text="❌ Reject", callback_data=f"reject:{phrase_idx}")
    builder.button(text="✏️ Edit", callback_data=f"edit:{phrase_idx}")
    builder.adjust(3)
    return builder


def _append_status(text: str, status: str) -> str:
    """Добавляет строку статуса к тексту сообщения."""
    return f"{text}\n\n{status}"


def _update_message_status(msg: Message, new_status: str) -> str:
    """
    Возвращает обновлённый текст: если уже есть «Статус:», заменяет последний.
    Иначе добавляет.
    """
    text = msg.text or msg.caption or ""
    if "Статус:" in text:
        parts = text.rsplit("\n\n", 1)
        if len(parts) == 2 and "Статус:" in parts[1]:
            return f"{parts[0]}\n\n{new_status}"
    return _append_status(text, new_status)


def _has_phrase_number_in_text(text: str) -> bool:
    """Проверяет, содержит ли текст «Фраза N» — может привести к мусору в канале."""
    return bool(re.search(r"Фраза\s*\d+", text, re.IGNORECASE))


PHRASE_WARNING = "\n\n⚠️ <b>Обнаружено «Фраза N» в тексте</b> — возможна ошибка выкладывания, в канал может попасть мусор!"


def _parse_phrase_text(msg: Message) -> str:
    """Извлекает сырой текст из формата «Фраза N:\n{text}» или с суффиксом «Статус:»."""
    text = msg.text or msg.caption or ""
    if "\n" not in text:
        return text.strip()
    after_prefix = text.split("\n", 1)[1]
    if "\n\n" in after_prefix:
        result = after_prefix.split("\n\n", 1)[0].strip()
    else:
        result = after_prefix.strip()
    # Убираем префикс «Фраза N:» если остался (для первой фразы с «Канал: X\n\nФраза 1:\n...»)
    result = re.sub(r"^Фраза\s*\d+\s*:?\s*", "", result).strip()
    # Извлекаем текст из <pre>...</pre> (моноширинный формат)
    pre_match = re.search(r"<pre>(.*?)</pre>", result, re.DOTALL)
    if pre_match:
        result = html.unescape(pre_match.group(1).strip())
    return result


def _posting_channel_ids(channels_data: dict[str, Any]) -> set[str]:
    """Из ответа _get_channels извлекает множество id постинг-каналов."""
    return {str(c["id"]) for c in channels_data.get("channels", [])}


async def _get_channels(posting_only: bool = True) -> dict[str, Any]:
    """GET /api/v1/channels — возвращает {"channels": [{"id", "name", "telegram_id"}, ...]}.
    posting_only: если True — только каналы для постинга (без dataset-only).
    """
    async with aiohttp.ClientSession() as session:
        params = {"posting_only": "true"} if posting_only else {}
        async with session.get(
            f"{BACKEND_URL}/api/v1/channels",
            params=params,
            headers={"X-API-Key": BACKEND_API_KEY},
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"API error {resp.status}: {text}")
            return await resp.json()


async def _post_generate(channel_id: str) -> dict[str, Any]:
    """POST /api/v1/generate — возвращает {"phrases": [...], "channel_name": ...}."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BACKEND_URL}/api/v1/generate",
            json={"channel_id": channel_id},
            headers={"X-API-Key": BACKEND_API_KEY, "Content-Type": "application/json"},
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"API error {resp.status}: {text}")
            return await resp.json()


async def _get_scheduled_posts() -> dict[str, Any]:
    """GET /api/v1/posts?status=scheduled."""
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{BACKEND_URL}/api/v1/posts",
            params={"status": "scheduled"},
            headers={"X-API-Key": BACKEND_API_KEY},
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"API error {resp.status}: {text}")
            return await resp.json()


async def _post_approve(channel_id: str, phrases: list[str]) -> dict[str, Any]:
    """POST /api/v1/posts/approve — возвращает draft_posts."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BACKEND_URL}/api/v1/posts/approve",
            json={"channel_id": channel_id, "phrases": phrases},
            headers={"X-API-Key": BACKEND_API_KEY, "Content-Type": "application/json"},
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"API error {resp.status}: {text}")
            return await resp.json()


async def _post_approve_one(channel_id: str, text: str) -> dict[str, Any]:
    """POST /api/v1/posts/approve-one — создаёт один draft-пост."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BACKEND_URL}/api/v1/posts/approve-one",
            json={"channel_id": channel_id, "text": text},
            headers={"X-API-Key": BACKEND_API_KEY, "Content-Type": "application/json"},
        ) as resp:
            if resp.status != 200:
                text_err = await resp.text()
                raise RuntimeError(f"API error {resp.status}: {text_err}")
            return await resp.json()


async def _patch_post(post_id: str, text: str) -> dict[str, Any]:
    """PATCH /api/v1/posts/{post_id} — обновляет текст draft-поста."""
    async with aiohttp.ClientSession() as session:
        async with session.patch(
            f"{BACKEND_URL}/api/v1/posts/{post_id}",
            json={"text": text},
            headers={"X-API-Key": BACKEND_API_KEY, "Content-Type": "application/json"},
        ) as resp:
            if resp.status != 200:
                text_err = await resp.text()
                raise RuntimeError(f"API error {resp.status}: {text_err}")
            return await resp.json()


async def _get_draft_posts(channel_id: str | None = None) -> dict[str, Any]:
    """GET /api/v1/posts?status=draft — черновики, опционально по каналу."""
    params: dict[str, str] = {"status": "draft"}
    if channel_id:
        params["channel_id"] = channel_id
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{BACKEND_URL}/api/v1/posts",
            params=params,
            headers={"X-API-Key": BACKEND_API_KEY},
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"API error {resp.status}: {text}")
            return await resp.json()


async def _post_post_now(post_id: str) -> dict[str, Any]:
    """POST /api/v1/posts/post-now — публикует пост немедленно."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BACKEND_URL}/api/v1/posts/post-now",
            json={"post_id": post_id},
            headers={"X-API-Key": BACKEND_API_KEY, "Content-Type": "application/json"},
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"API error {resp.status}: {text}")
            return await resp.json()


async def _post_cancel_post(post_id: str) -> dict[str, Any]:
    """POST /api/v1/posts/{post_id}/cancel — отмена поста из расписания."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BACKEND_URL}/api/v1/posts/{post_id}/cancel",
            headers={"X-API-Key": BACKEND_API_KEY},
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"API error {resp.status}: {text}")
            return await resp.json()


async def _post_schedule_batch(items: list[dict[str, Any]]) -> dict[str, Any]:
    """POST /api/v1/posts/schedule-batch."""
    payload = [
        {"post_id": str(it["id"]), "channel_id": str(it["channel_id"]), "time": it["suggested_time"]}
        for it in items
    ]
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BACKEND_URL}/api/v1/posts/schedule-batch",
            json=payload,
            headers={"X-API-Key": BACKEND_API_KEY, "Content-Type": "application/json"},
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"API error {resp.status}: {text}")
            return await resp.json()


def _format_time_display(iso_time: str) -> str:
    """Преобразует ISO8601 в читаемый формат ДД.ММ.ГГГГ ЧЧ:ММ."""
    if not iso_time or iso_time == "—":
        return "—"
    try:
        dt = datetime.fromisoformat(iso_time.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%Y %H:%M")
    except (ValueError, TypeError):
        return iso_time


MAX_MESSAGE_LEN = 3800  # запас под заголовок и HTML
PER_PAGE = 5


def _format_slots_message(
    draft_posts: list[dict[str, Any]],
    channel_name: str | None = None,
    page: int = 0,
    per_page: int = 5,
) -> tuple[str, int]:
    """Форматирует слоты для отображения. Возвращает (text, total_pages)."""
    total_pages = max(1, (len(draft_posts) + per_page - 1) // per_page)
    page = max(0, min(page, total_pages - 1))
    start = page * per_page
    end = min(start + per_page, len(draft_posts))
    page_posts = draft_posts[start:end]

    header = f"<b>Канал:</b> {channel_name}\n\n" if channel_name else ""
    lines = []
    for i, p in enumerate(page_posts, start=start + 1):
        text = p.get("text", "")
        at = _format_time_display(p.get("suggested_time", "—"))
        lines.append(f"• {text}\n  📅 {at} (МСК)")
    body = "\n\n".join(lines)
    result = header + body
    if total_pages > 1:
        result += f"\n\nСтраница {page + 1} из {total_pages}"
    return result, total_pages


MSK = ZoneInfo("Europe/Moscow")


def _parse_manual_time(text: str) -> str | None:
    """
    Парсит время в формате ДД.ММ.ГГГГ ЧЧ:ММ (МСК).
    Возвращает ISO8601 строку или None при ошибке.
    """
    text = (text or "").strip()
    if not text:
        return None
    try:
        dt = datetime.strptime(text, "%d.%m.%Y %H:%M")
        dt = dt.replace(tzinfo=MSK)
        return dt.isoformat()
    except ValueError:
        return None


def _get_slots_keyboard(
    draft_posts: list[dict[str, Any]],
    page: int = 0,
    per_page: int = 5,
    show_back_channel: bool = False,
) -> InlineKeyboardBuilder:
    """Inline-кнопки: Post Now, Manual Time, Confirm под постами страницы, Shuffle, Confirm All, пагинация, «← Другой канал»."""
    builder = InlineKeyboardBuilder()
    total_pages = max(1, (len(draft_posts) + per_page - 1) // per_page)
    page = max(0, min(page, total_pages - 1))
    start = page * per_page
    end = min(start + per_page, len(draft_posts))
    page_posts = draft_posts[start:end]

    for i, p in enumerate(page_posts, start=start + 1):
        post_id = str(p.get("id", ""))
        builder.button(text=f"🚀 Post Now ({i})", callback_data=f"post_now:{post_id}")
        builder.button(text="⏰ Задать время вручную", callback_data=f"manual_time:{post_id}")
        builder.button(text="✅", callback_data=f"slots_confirm_one:{post_id}")

    if total_pages > 1:
        if page > 0:
            builder.button(text="◀", callback_data=f"slots_page:{page - 1}")
        if page < total_pages - 1:
            builder.button(text="▶", callback_data=f"slots_page:{page + 1}")

    builder.button(text="🔀 Shuffle", callback_data="slots:shuffle")
    builder.button(text="✅ Confirm All", callback_data="slots:confirm")
    if show_back_channel:
        builder.button(text="← Другой канал", callback_data="planning_back")
    builder.adjust(3)  # 3 кнопки на пост
    return builder


def _get_channels_with_scheduled(
    posts: list[dict[str, Any]],
    posting_channel_ids: set[str] | None = None,
) -> list[tuple[str, str, int]]:
    """Каналы с запланированными постами: (channel_id, channel_name, count).
    posting_channel_ids: если задано — только каналы из этого множества (исключает dataset-only).
    """
    from collections import defaultdict

    by_channel: dict[str, tuple[str, int]] = {}  # channel_id -> (channel_name, count)
    for p in posts:
        cid = str(p.get("channel_id", ""))
        if posting_channel_ids is not None and cid not in posting_channel_ids:
            continue
        cname = p.get("channel_name") or "Без канала"
        if cid not in by_channel:
            by_channel[cid] = (cname, 0)
        by_channel[cid] = (cname, by_channel[cid][1] + 1)
    return [(cid, cname, cnt) for cid, (cname, cnt) in sorted(by_channel.items(), key=lambda x: x[1][0])]


def _filter_posts_by_channel(posts: list[dict[str, Any]], channel_id: str) -> list[dict[str, Any]]:
    """Фильтрует посты по channel_id, сортирует по scheduled_at."""
    filtered = [p for p in posts if str(p.get("channel_id")) == channel_id]
    return sorted(filtered, key=lambda p: p.get("scheduled_at") or "")


def _format_scheduled_channel_posts(
    ordered_posts: list[dict[str, Any]],
    page: int = 0,
    per_page: int = 5,
) -> tuple[str, int]:
    """Форматирует посты канала с нумерацией. Возвращает (text, total_pages)."""
    total_pages = max(1, (len(ordered_posts) + per_page - 1) // per_page)
    page = max(0, min(page, total_pages - 1))
    start = page * per_page
    end = min(start + per_page, len(ordered_posts))
    page_posts = ordered_posts[start:end]

    lines = []
    for i, p in enumerate(page_posts, start=start + 1):
        text = p.get("text", "")
        at = _format_time_display(p.get("scheduled_at", "—"))
        lines.append(f"<b>{i}.</b> {text}\n  📅 {at}")
    result = "\n\n".join(lines)
    if total_pages > 1:
        result += f"\n\nСтраница {page + 1} из {total_pages}"
    return result, total_pages


def _get_scheduled_channel_keyboard(
    ordered_posts: list[dict[str, Any]],
    page: int = 0,
    per_page: int = 5,
) -> InlineKeyboardBuilder:
    """Кнопки отмены для постов страницы + пагинация + «← Другой канал»."""
    builder = InlineKeyboardBuilder()
    total_pages = max(1, (len(ordered_posts) + per_page - 1) // per_page)
    page = max(0, min(page, total_pages - 1))
    start = page * per_page
    end = min(start + per_page, len(ordered_posts))
    page_posts = ordered_posts[start:end]

    for i, p in enumerate(page_posts, start=start + 1):
        post_id = str(p.get("id", ""))
        builder.button(text=f"🗑️ Отменить ({i})", callback_data=f"cancel_scheduled:{post_id}")

    if total_pages > 1:
        if page > 0:
            builder.button(text="◀", callback_data=f"scheduled_page:{page - 1}")
        if page < total_pages - 1:
            builder.button(text="▶", callback_data=f"scheduled_page:{page + 1}")

    builder.button(text="← Другой канал", callback_data="scheduled_back")

    n_cancel = len(page_posts)
    n_pag = 2 if (page > 0 and page < total_pages - 1) else (1 if total_pages > 1 else 0)
    sizes = [1] * n_cancel + ([n_pag] if n_pag else []) + [1]
    builder.adjust(*sizes)
    return builder


def _get_scheduled_channels_keyboard(
    channels: list[tuple[str, str, int]],
) -> InlineKeyboardBuilder:
    """Кнопки выбора канала: «Канал 1 (3)» и т.д."""
    builder = InlineKeyboardBuilder()
    for cid, cname, cnt in channels:
        builder.button(
            text=f"{cname} ({cnt})",
            callback_data=f"scheduled_channel:{cid}",
        )
    builder.adjust(1)
    return builder


# --- Dispatcher и Middleware ---
dp = Dispatcher(storage=MemoryStorage())


@dp.update.outer_middleware()
async def admin_check(handler, event, data):
    """Проверяет ADMIN_TELEGRAM_IDS, игнорирует апдейты от остальных."""
    user = None
    msg = None
    if hasattr(event, "message") and event.message:
        user = event.message.from_user
        msg = event.message
    elif hasattr(event, "callback_query") and event.callback_query:
        user = event.callback_query.from_user
        msg = event.callback_query.message
    if user is None:
        return await handler(event, data)

    if not _is_admin(user.id):
        if msg:
            await msg.answer("Доступ запрещён. Ваш ID не в списке администраторов.")
        if hasattr(event, "callback_query") and event.callback_query:
            await event.callback_query.answer("Доступ запрещён.", show_alert=True)
        return
    return await handler(event, data)


# --- Handlers ---


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        await message.answer("Доступ запрещён. Ваш ID не в списке администраторов.")
        return
    await message.answer(
        "Привет! Используй кнопки ниже.",
        reply_markup=get_main_keyboard().as_markup(resize_keyboard=True),
    )


@dp.message(F.text == "🎲 Сгенерировать")
async def handle_generate(message: Message, state: FSMContext) -> None:
    if not _is_admin(message.from_user.id):
        return
    await state.clear()
    try:
        data = await _get_channels()
        channels = data.get("channels", [])
    except Exception as e:
        await message.answer(f"Ошибка API: {e}")
        return

    if not channels:
        await message.answer("Нет каналов. Добавь каналы в БД.")
        return

    builder = InlineKeyboardBuilder()
    for ch in channels:
        builder.button(text=ch.get("name", ch["id"]), callback_data=f"channel_select:{ch['id']}")
    builder.adjust(1)
    await message.answer("Выберите канал:", reply_markup=builder.as_markup())


@dp.callback_query(F.data.startswith("channel_select:"))
async def cb_channel_select(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    await callback.answer()  # Сразу — иначе "query is too old" при долгой генерации
    _, channel_id = callback.data.split(":", 1)
    await callback.message.edit_text("Генерирую фразы...")
    try:
        data = await _post_generate(channel_id)
        phrases = data.get("phrases", [])
        channel_name = data.get("channel_name", "")
        await state.update_data(channel_id=channel_id, channel_name=channel_name)
    except Exception as e:
        await callback.message.answer(f"Ошибка API: {e}")
        return

    if not phrases:
        await callback.message.answer("Фразы не сгенерированы. Проверь каналы в БД и LLM.")
        return

    await state.update_data(
        phrases={i: p for i, p in enumerate(phrases)},
        approved_indices=[],
        approved_post_ids={},
    )
    for i, phrase in enumerate(phrases):
        kb = get_phrase_keyboard(i)
        header = f"<b>Канал:</b> {channel_name}\n\n" if i == 0 else ""
        escaped = html.escape(phrase)
        body = f"{header}<b>Фраза {i + 1}:</b>\n<pre>{escaped}</pre>"
        if _has_phrase_number_in_text(phrase):
            body += PHRASE_WARNING
        await callback.message.answer(
            body,
            reply_markup=kb.as_markup(),
        )


@dp.message(F.text == "📅 Ожидают постинга")
async def handle_scheduled(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        return
    try:
        data = await _get_scheduled_posts()
        posts = data.get("posts", [])
        ch_data = await _get_channels(posting_only=True)
        posting_ids = _posting_channel_ids(ch_data)
    except Exception as e:
        await message.answer(f"Ошибка API: {e}")
        return

    if not posts:
        await message.answer("Нет постов, ожидающих постинга.")
        return

    channels = _get_channels_with_scheduled(posts, posting_channel_ids=posting_ids)
    kb = _get_scheduled_channels_keyboard(channels)
    await message.answer("Выберите канал:", reply_markup=kb.as_markup())


@dp.callback_query(F.data.startswith("scheduled_channel:"))
async def cb_scheduled_channel_select(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    _, channel_id = callback.data.split(":", 1)
    await callback.answer()
    try:
        data = await _get_scheduled_posts()
        posts = data.get("posts", [])
    except Exception as e:
        await callback.message.edit_text(f"Ошибка API: {e}")
        return
    channel_posts = _filter_posts_by_channel(posts, channel_id)
    channel_name = channel_posts[0].get("channel_name", "Канал") if channel_posts else "Канал"
    await state.update_data(scheduled_channel_id=channel_id, scheduled_page=0)
    if not channel_posts:
        kb = InlineKeyboardBuilder()
        kb.button(text="← Другой канал", callback_data="scheduled_back")
        kb.adjust(1)
        await callback.message.edit_text(
            f"Нет постов для канала «{channel_name}».",
            reply_markup=kb.as_markup(),
        )
        return
    text, _ = _format_scheduled_channel_posts(channel_posts, page=0, per_page=PER_PAGE)
    kb = _get_scheduled_channel_keyboard(channel_posts, page=0, per_page=PER_PAGE)
    await callback.message.edit_text(
        f"<b>Ожидают постинга — {channel_name}:</b>\n\n{text}",
        reply_markup=kb.as_markup(),
    )


@dp.callback_query(F.data == "scheduled_back")
async def cb_scheduled_back(callback: CallbackQuery) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    await callback.answer()
    try:
        data = await _get_scheduled_posts()
        posts = data.get("posts", [])
        ch_data = await _get_channels(posting_only=True)
        posting_ids = _posting_channel_ids(ch_data)
    except Exception as e:
        await callback.message.edit_text(f"Ошибка API: {e}")
        return
    if not posts:
        await callback.message.edit_text("Нет постов, ожидающих постинга.", reply_markup=None)
        return
    channels = _get_channels_with_scheduled(posts, posting_channel_ids=posting_ids)
    kb = _get_scheduled_channels_keyboard(channels)
    await callback.message.edit_text("Выберите канал:", reply_markup=kb.as_markup())


@dp.callback_query(F.data.startswith("scheduled_page:"))
async def cb_scheduled_page(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    _, page_str = callback.data.split(":", 1)
    page = int(page_str)
    await callback.answer()
    data = await state.get_data()
    channel_id = data.get("scheduled_channel_id")
    if not channel_id:
        return
    try:
        resp = await _get_scheduled_posts()
        posts = resp.get("posts", [])
    except Exception as e:
        await callback.message.edit_text(f"Ошибка API: {e}")
        return
    channel_posts = _filter_posts_by_channel(posts, channel_id)
    channel_name = channel_posts[0].get("channel_name", "Канал") if channel_posts else "Канал"
    if not channel_posts:
        kb = InlineKeyboardBuilder()
        kb.button(text="← Другой канал", callback_data="scheduled_back")
        kb.adjust(1)
        await callback.message.edit_text("Нет постов для этого канала.", reply_markup=kb.as_markup())
        return
    await state.update_data(scheduled_page=page)
    text, _ = _format_scheduled_channel_posts(channel_posts, page=page, per_page=PER_PAGE)
    kb = _get_scheduled_channel_keyboard(channel_posts, page=page, per_page=PER_PAGE)
    await callback.message.edit_text(
        f"<b>Ожидают постинга — {channel_name}:</b>\n\n{text}",
        reply_markup=kb.as_markup(),
    )


@dp.callback_query(F.data.startswith("cancel_scheduled:"))
async def cb_cancel_scheduled(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    _, post_id = callback.data.split(":", 1)
    try:
        await _post_cancel_post(post_id)
    except Exception as e:
        await callback.answer(f"Ошибка: {e}", show_alert=True)
        return
    state_data = await state.get_data()
    channel_id = state_data.get("scheduled_channel_id")
    try:
        resp = await _get_scheduled_posts()
        posts = resp.get("posts", [])
        ch_data = await _get_channels(posting_only=True)
        posting_ids = _posting_channel_ids(ch_data)
    except Exception as e:
        await callback.answer(f"Ошибка API: {e}", show_alert=True)
        return
    if not channel_id:
        channels = _get_channels_with_scheduled(posts, posting_channel_ids=posting_ids)
        kb = _get_scheduled_channels_keyboard(channels)
        await callback.message.edit_text("Выберите канал:", reply_markup=kb.as_markup())
        await callback.answer("Пост отменён")
        return
    channel_posts = _filter_posts_by_channel(posts, channel_id)
    channel_name = channel_posts[0].get("channel_name", "Канал") if channel_posts else "Канал"
    if not channel_posts:
        kb = InlineKeyboardBuilder()
        kb.button(text="← Другой канал", callback_data="scheduled_back")
        kb.adjust(1)
        await callback.message.edit_text(
            "Нет постов для этого канала. Все отменены.",
            reply_markup=kb.as_markup(),
        )
    else:
        page = state_data.get("scheduled_page", 0)
        total_pages = max(1, (len(channel_posts) + PER_PAGE - 1) // PER_PAGE)
        page = min(page, total_pages - 1)
        await state.update_data(scheduled_page=page)
        text, _ = _format_scheduled_channel_posts(channel_posts, page=page, per_page=PER_PAGE)
        kb = _get_scheduled_channel_keyboard(channel_posts, page=page, per_page=PER_PAGE)
        await callback.message.edit_text(
            f"<b>Ожидают постинга — {channel_name}:</b>\n\n{text}",
            reply_markup=kb.as_markup(),
        )
    await callback.answer("Пост отменён")


@dp.message(F.text == "📤 Отправить на планирование")
async def handle_send_to_planning(message: Message, state: FSMContext) -> None:
    if not _is_admin(message.from_user.id):
        return
    try:
        data = await _get_draft_posts()
        posts = data.get("posts", [])
        ch_data = await _get_channels(posting_only=True)
        posting_ids = _posting_channel_ids(ch_data)
    except Exception as e:
        await message.answer(f"Ошибка API: {e}")
        return

    if not posts:
        await message.answer(
            "Нет черновиков. Нажми Approve на фразах.",
            reply_markup=get_main_keyboard().as_markup(resize_keyboard=True),
        )
        return

    channels = _get_channels_with_scheduled(posts, posting_channel_ids=posting_ids)
    builder = InlineKeyboardBuilder()
    for cid, cname, cnt in channels:
        builder.button(
            text=f"{cname} ({cnt})",
            callback_data=f"planning_channel:{cid}",
        )
    builder.adjust(1)
    await message.answer("Выберите канал:", reply_markup=builder.as_markup())


@dp.callback_query(F.data.startswith("planning_channel:"))
async def cb_planning_channel_select(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    _, channel_id = callback.data.split(":", 1)
    await callback.answer()
    try:
        data = await _get_draft_posts(channel_id)
        draft_posts = data.get("posts", [])
    except Exception as e:
        await callback.message.edit_text(f"Ошибка API: {e}")
        return

    if not draft_posts:
        await callback.message.edit_text("Нет черновиков для этого канала.")
        return

    channel_name = draft_posts[0].get("channel_name", "Канал") if draft_posts else "Канал"
    await state.update_data(draft_posts=draft_posts, planning_channel_id=channel_id, channel_name=channel_name, slots_page=0)
    slots_text, _ = _format_slots_message(draft_posts, channel_name, page=0, per_page=PER_PAGE)
    kb = _get_slots_keyboard(draft_posts, page=0, per_page=PER_PAGE, show_back_channel=True)
    await callback.message.edit_text(
        f"<b>Слоты для планирования:</b>\n\n{slots_text}",
        reply_markup=kb.as_markup(),
    )


@dp.callback_query(F.data.startswith("slots_page:"))
async def cb_slots_page(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    _, page_str = callback.data.split(":", 1)
    page = int(page_str)
    await callback.answer()
    data = await state.get_data()
    draft_posts = list(data.get("draft_posts", []))
    channel_name = data.get("channel_name", "")
    if not draft_posts:
        await callback.message.edit_text("Нет слотов.", reply_markup=None)
        return
    await state.update_data(slots_page=page)
    slots_text, _ = _format_slots_message(draft_posts, channel_name, page=page, per_page=PER_PAGE)
    show_back = bool(data.get("planning_channel_id"))
    kb = _get_slots_keyboard(draft_posts, page=page, per_page=PER_PAGE, show_back_channel=show_back)
    await callback.message.edit_text(
        f"<b>Слоты для планирования:</b>\n\n{slots_text}",
        reply_markup=kb.as_markup(),
    )


@dp.callback_query(F.data == "planning_back")
async def cb_planning_back(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    await callback.answer()
    try:
        data = await _get_draft_posts()
        posts = data.get("posts", [])
        ch_data = await _get_channels(posting_only=True)
        posting_ids = _posting_channel_ids(ch_data)
    except Exception as e:
        await callback.message.edit_text(f"Ошибка API: {e}")
        return

    if not posts:
        await callback.message.edit_text("Нет черновиков. Нажми Approve на фразах.", reply_markup=None)
        await state.clear()
        return

    channels = _get_channels_with_scheduled(posts, posting_channel_ids=posting_ids)
    builder = InlineKeyboardBuilder()
    for cid, cname, cnt in channels:
        builder.button(
            text=f"{cname} ({cnt})",
            callback_data=f"planning_channel:{cid}",
        )
    builder.adjust(1)
    await callback.message.edit_text("Выберите канал:", reply_markup=builder.as_markup())


@dp.callback_query(F.data.startswith("approve:"))
async def cb_approve(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    _, idx = callback.data.split(":", 1)
    phrase_idx = int(idx)
    raw_text = _parse_phrase_text(callback.message)
    data = await state.get_data()
    channel_id = data.get("channel_id")
    if not channel_id:
        await callback.answer("Канал не выбран.", show_alert=True)
        return
    phrases = dict(data.get("phrases", {}))
    approved_indices = list(data.get("approved_indices", []))
    approved_post_ids = dict(data.get("approved_post_ids", {}))
    phrases[phrase_idx] = raw_text
    try:
        if phrase_idx in approved_post_ids:
            await _patch_post(approved_post_ids[phrase_idx], raw_text)
        else:
            resp = await _post_approve_one(channel_id, raw_text)
            post_id = resp.get("id")
            if post_id:
                approved_post_ids[phrase_idx] = post_id
    except Exception as e:
        await callback.answer(f"Ошибка API: {e}", show_alert=True)
        return
    if phrase_idx not in approved_indices:
        approved_indices.append(phrase_idx)
    await state.update_data(phrases=phrases, approved_indices=approved_indices, approved_post_ids=approved_post_ids)
    new_text = _update_message_status(callback.message, "✅ Статус: Approved")
    if _has_phrase_number_in_text(raw_text):
        new_text += PHRASE_WARNING
    await callback.message.edit_text(new_text, reply_markup=None)
    await callback.answer("Одобрено")


@dp.callback_query(F.data.startswith("reject:"))
async def cb_reject(callback: CallbackQuery) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    # Не удаляем — обновляем текст со статусом, сохраняем историю в чате
    new_text = _update_message_status(callback.message, "❌ Статус: Rejected")
    await callback.message.edit_text(new_text, reply_markup=None)
    await callback.answer("Отклонено")


@dp.callback_query(F.data.startswith("edit:"))
async def cb_edit(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    _, idx = callback.data.split(":", 1)
    phrase_idx = int(idx)
    msg = callback.message
    await state.update_data(
        edit_message_id=msg.message_id,
        edit_chat_id=msg.chat.id,
        edit_phrase_idx=phrase_idx,
        edit_phrase_num=phrase_idx + 1,
    )
    await state.set_state(EditPhraseStates.waiting_for_text)
    await callback.answer()
    await msg.reply(
        f"Введи новый текст для фразы {phrase_idx + 1}. Или /cancel для отмены.",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(EditPhraseStates.waiting_for_text, Command("cancel"))
@dp.message(EditPhraseStates.waiting_for_text, F.text.casefold() == "cancel")
async def cancel_edit(message: Message, state: FSMContext) -> None:
    await state.set_state(None)
    await message.reply("Отменено.", reply_markup=get_main_keyboard().as_markup(resize_keyboard=True))


@dp.message(EditPhraseStates.waiting_for_text)
async def process_edit_text(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.reply("Отправь текст. Или /cancel для отмены.")
        return
    data = await state.get_data()
    msg_id = data["edit_message_id"]
    chat_id = data["edit_chat_id"]
    phrase_idx = data["edit_phrase_idx"]
    phrase_num = data["edit_phrase_num"]
    phrases = dict(data.get("phrases", {}))
    approved_post_ids = dict(data.get("approved_post_ids", {}))
    phrases[phrase_idx] = message.text
    if phrase_idx in approved_post_ids:
        post_id = approved_post_ids[phrase_idx]
        try:
            await _patch_post(post_id, message.text)
        except Exception as e:
            await message.reply(f"Ошибка обновления поста в БД: {e}")
            return
    await state.update_data(phrases=phrases)
    await state.set_state(None)
    escaped = html.escape(message.text)
    new_text = f"<b>Фраза {phrase_num}:</b>\n<pre>{escaped}</pre>\n\n✏️ Статус: Отредактировано"
    if _has_phrase_number_in_text(message.text):
        new_text += PHRASE_WARNING
    kb = get_phrase_keyboard(phrase_idx).as_markup()
    await message.bot.edit_message_text(
        chat_id=chat_id,
        message_id=msg_id,
        text=new_text,
        reply_markup=kb,
    )
    await message.reply(
        "Текст обновлён. Можно снова Approve/Reject/Edit.",
        reply_markup=get_main_keyboard().as_markup(resize_keyboard=True),
    )


@dp.callback_query(F.data.startswith("manual_time:"))
async def cb_manual_time(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    _, post_id = callback.data.split(":", 1)
    data = await state.get_data()
    draft_posts = data.get("draft_posts", [])
    if not any(str(p.get("id")) == post_id for p in draft_posts):
        await callback.answer("Пост не найден в слотах.", show_alert=True)
        return
    await state.update_data(
        manual_time_post_id=post_id,
        manual_time_message_id=callback.message.message_id,
        manual_time_chat_id=callback.message.chat.id,
    )
    await state.set_state(ManualTimeStates.waiting_for_time)
    await callback.answer()
    await callback.message.reply(
        "Введи время в формате ДД.ММ.ГГГГ ЧЧ:ММ (МСК). Или /cancel для отмены.",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(ManualTimeStates.waiting_for_time, Command("cancel"))
@dp.message(ManualTimeStates.waiting_for_time, F.text.casefold() == "cancel")
async def cancel_manual_time(message: Message, state: FSMContext) -> None:
    await state.set_state(None)
    await message.reply("Отменено.", reply_markup=get_main_keyboard().as_markup(resize_keyboard=True))


@dp.message(ManualTimeStates.waiting_for_time)
async def process_manual_time(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.reply("Введи время в формате ДД.ММ.ГГГГ ЧЧ:ММ (МСК). Или /cancel для отмены.")
        return
    iso_time = _parse_manual_time(message.text)
    if iso_time is None:
        await message.reply("Неверный формат, попробуй снова. Или /cancel для отмены.")
        return
    data = await state.get_data()
    post_id = data.get("manual_time_post_id")
    msg_id = data.get("manual_time_message_id")
    chat_id = data.get("manual_time_chat_id")
    draft_posts = list(data.get("draft_posts", []))
    channel_name = data.get("channel_name", "")
    idx = next((i for i, p in enumerate(draft_posts) if str(p.get("id")) == post_id), None)
    if idx is None:
        await state.set_state(None)
        await message.reply("Пост не найден в слотах.", reply_markup=get_main_keyboard().as_markup(resize_keyboard=True))
        return
    draft_posts[idx] = {**draft_posts[idx], "suggested_time": iso_time}
    await state.update_data(draft_posts=draft_posts)
    await state.set_state(None)
    page = data.get("slots_page", 0)
    slots_text, _ = _format_slots_message(draft_posts, channel_name, page=page, per_page=PER_PAGE)
    show_back = bool(data.get("planning_channel_id"))
    kb = _get_slots_keyboard(draft_posts, page=page, per_page=PER_PAGE, show_back_channel=show_back)
    await message.bot.edit_message_text(
        chat_id=chat_id,
        message_id=msg_id,
        text=f"<b>Слоты для планирования:</b>\n\n{slots_text}",
        reply_markup=kb.as_markup(),
    )
    await message.reply(
        "Время обновлено.",
        reply_markup=get_main_keyboard().as_markup(resize_keyboard=True),
    )


@dp.callback_query(F.data == "slots:shuffle")
async def cb_slots_shuffle(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    data = await state.get_data()
    draft_posts = list(data.get("draft_posts", []))
    channel_name = data.get("channel_name", "")
    if not draft_posts:
        await callback.answer("Нет слотов для перемешивания.", show_alert=True)
        return
    times = [p["suggested_time"] for p in draft_posts]
    random.shuffle(times)
    for i, p in enumerate(draft_posts):
        draft_posts[i] = {**p, "suggested_time": times[i]}
    await state.update_data(draft_posts=draft_posts, slots_page=0)
    slots_text, _ = _format_slots_message(draft_posts, channel_name, page=0, per_page=PER_PAGE)
    show_back = bool(data.get("planning_channel_id"))
    kb = _get_slots_keyboard(draft_posts, page=0, per_page=PER_PAGE, show_back_channel=show_back)
    await callback.message.edit_text(
        f"<b>Слоты для планирования:</b>\n\n{slots_text}",
        reply_markup=kb.as_markup(),
    )
    await callback.answer("Слоты перемешаны")


@dp.callback_query(F.data.startswith("post_now:"))
async def cb_post_now(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    _, post_id = callback.data.split(":", 1)
    try:
        await _post_post_now(post_id)
    except Exception as e:
        await callback.answer(f"Ошибка: {e}", show_alert=True)
        return

    data = await state.get_data()
    old_draft = next((p for p in data.get("draft_posts", []) if str(p.get("id")) == post_id), None)
    t = old_draft.get("text", "") if old_draft else ""
    published_text = t[:50] + "..." if len(t) > 50 else t
    draft_posts = [p for p in data.get("draft_posts", []) if str(p.get("id")) != post_id]
    await state.update_data(draft_posts=draft_posts)
    channel_name = data.get("channel_name", "")
    header = f"<b>Слоты для планирования:</b>\n\n✅ Опубликовано прямо сейчас: {published_text}\n\n"
    if draft_posts:
        page = data.get("slots_page", 0)
        total_pages = max(1, (len(draft_posts) + PER_PAGE - 1) // PER_PAGE)
        page = min(page, total_pages - 1)
        await state.update_data(draft_posts=draft_posts, slots_page=page)
        slots_text, _ = _format_slots_message(draft_posts, channel_name, page=page, per_page=PER_PAGE)
        show_back = bool(data.get("planning_channel_id"))
        kb = _get_slots_keyboard(draft_posts, page=page, per_page=PER_PAGE, show_back_channel=show_back)
        await callback.message.edit_text(
            header + slots_text,
            reply_markup=kb.as_markup(),
        )
    else:
        await callback.message.edit_text(
            header + "Все посты опубликованы.",
            reply_markup=None,
        )
    await callback.answer("Опубликовано")


@dp.callback_query(F.data.startswith("slots_confirm_one:"))
async def cb_slots_confirm_one(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    _, post_id = callback.data.split(":", 1)
    data = await state.get_data()
    draft_posts = list(data.get("draft_posts", []))
    channel_name = data.get("channel_name", "")
    post = next((p for p in draft_posts if str(p.get("id")) == post_id), None)
    if not post:
        await callback.answer("Пост не найден.", show_alert=True)
        return
    try:
        await _post_schedule_batch([post])
    except Exception as e:
        await callback.answer(f"Ошибка API: {e}", show_alert=True)
        return
    draft_posts = [p for p in draft_posts if str(p.get("id")) != post_id]
    page = data.get("slots_page", 0)
    total_pages = max(1, (len(draft_posts) + PER_PAGE - 1) // PER_PAGE)
    page = min(page, total_pages - 1)
    await state.update_data(draft_posts=draft_posts, slots_page=page)
    if draft_posts:
        slots_text, _ = _format_slots_message(draft_posts, channel_name, page=page, per_page=PER_PAGE)
        show_back = bool(data.get("planning_channel_id"))
        kb = _get_slots_keyboard(draft_posts, page=page, per_page=PER_PAGE, show_back_channel=show_back)
        await callback.message.edit_text(
            f"<b>Слоты для планирования:</b>\n\n{slots_text}",
            reply_markup=kb.as_markup(),
        )
    else:
        await state.clear()
        await callback.message.edit_text(
            "Все посты подтверждены. Используй «📅 Ожидают постинга» для просмотра.",
            reply_markup=None,
        )
        await callback.message.answer(
            "Готово.",
            reply_markup=get_main_keyboard().as_markup(resize_keyboard=True),
        )
    await callback.answer("Пост подтверждён")


@dp.callback_query(F.data == "slots:confirm")
async def cb_slots_confirm(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    data = await state.get_data()
    draft_posts = data.get("draft_posts", [])
    if not draft_posts:
        await callback.answer("Нет слотов для подтверждения.", show_alert=True)
        return
    try:
        await _post_schedule_batch(draft_posts)
    except Exception as e:
        await callback.answer(f"Ошибка API: {e}", show_alert=True)
        return
    await state.clear()
    await callback.message.edit_text(
        "Расписание подтверждено. Посты ожидают постинга. Используй «📅 Ожидают постинга» для просмотра.",
        reply_markup=None,
    )
    await callback.message.answer(
        "Готово.",
        reply_markup=get_main_keyboard().as_markup(resize_keyboard=True),
    )
    await callback.answer("Готово")


async def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN не задан в .env")
    if not BACKEND_API_KEY:
        raise RuntimeError("BACKEND_API_KEY не задан в .env")

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    import logging

    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())



================================================
FILE: config/media.yaml
================================================
# Настройки медиа: картинки с текстом постов

image_probability: 0.1

# Позиции текста на картинке (доли 0–1: center=0.5, top≈0.15, bottom≈0.85)
text_positions:
  - x: 0.5
    y: 0.5   # center
  - x: 0.5
    y: 0.15  # top
  - x: 0.5
    y: 0.85  # bottom



================================================
FILE: config/prompts.yaml
================================================
# Промпты Генератора и Критика (LLM pipeline)

# Сколько случайных фраз из датасета подставлять в промпт (для разнообразия тем)
dataset_sample_size: 50

default_dataset:
  - "У тебя обязательно все получится!"
  - "Разреши себе чувствовать и проживать все эмоции"
  - "Перестань жертвовать собой ради других!"
  - "Страх уходит во время движения!"
  - "У тебя есть суперсила и это ты!"
  - "Если соблюдаешь все правила, пропускаешь всё веселье"
  - "Страх выглядеть глупо не даёт тебе двигаться вперёд!"
  - "Неидеальное действие лучше идеального бездействия!"
  - "Не спеши все предсказывать, обними неизвестное и пусть жизнь тебя удивит!"
  - "Ты никогда не ошибёшься с расчётом, если будешь расчитывать только на себя!"
  - "Никогда не извиняйся за то, как себя чувствуешь!"
  - "Перестань ожидать, что люди, которые не могут разобраться в себе, помогут это сделать тебе!"
  - "Если ты будешь таким как все, то кто будет таким как ты?"
  - "Если кто то скажет, что ты не сможешь, сделай это дважды и сфоткай!"

generator:
  system: |
    Ты — автор вирального Telegram-канала. Твоя задача — писать короткие, хлесткие мотивационные фразы.
    Твой Tone of Voice (стиль): заботливый, но дерзкий старший брат/сестра; современный психолог. Обращение строго на "ты".

    ПРАВИЛА ГЕНЕРАЦИИ:
    1. Длина: Строго 1-2 коротких предложения.
    2. Формат: Никаких эмодзи, никаких хештегов, никаких кавычек. Только чистый текст.
    3. Смысл: Разрешение быть неидеальным, защита личных границ, решительность, анти-токсичность.
    4. СТОП-СЛОВА И ЗАПРЕТЫ (КРИТИЧНО):
       - Не используй канцелярит и сложные метафоры (никаких "жизненный путь", "горизонты", "преодолевая преграды").
       - Не пиши банальностей ("улыбнись новому дню", "все в твоих руках", "после дождя будет радуга").
       - Избегай токсичного позитива ("просто не грусти").

    Сгенерируй ровно 15 уникальных фраз, которые идеально впишутся в предоставленный эталонный датасет.
  user_template: |
    Изучи эталонные фразы нашего канала:
    {dataset}

    Опираясь на их вайб, структуру и длину, сгенерируй 15 новых фраз. Выдай только массив строк, без лишних вступлений.

critic:
  system: |
    Ты — безжалостный главный редактор (Критик). Твоя задача — отфильтровать сгенерированный текст, выкинув все фразы, которые звучат неестественно, сгенерировано нейросетью или банально.

    КРИТЕРИИ ОЦЕНКИ (от 1 до 10):
    - Скор 9-10: Хлестко, жизненно, хочется сделать репост. Звучит как слова живого, дерзкого человека.
    - Скор 7-8: Хорошая, крепкая фраза по правилам канала. Подходит для публикации.
    - Скор 1-6 (Сразу в мусор): Звучит как типичный искусственный интеллект (ChatGPT), слишком длинно, присутствуют заезженные цитаты, ванильная чушь или поучительный тон.

    ТВОЯ ЗАДАЧА:
    1. Оцени каждую из 15 предложенных фраз.
    2. Оставь ТОЛЬКО те фразы, чей скор $\ge 7$.
    3. Ограничь итоговый список максимум 7 самыми лучшими фразами (если хороших мало — верни меньше, хоть 2, но не пропускай мусор).
    4. Верни данные строго в запрошенной JSON/Pydantic структуре.
  user_template: |
    Оцени эти 15 фраз. Выведи до 7 лучших (скор $\ge 7$), отсеяв весь ИИ-кринж и банальности:

    {phrases}

# Шаблон aesthetic — для канала "Канал 2" (формат «ЭТО ЗНАК»). Seed INSERT/UPDATE в prompt_templates.
aesthetic:
  generator:
    system: |
      Ты — главный автор популярного канала формата «ЭТО ЗНАК».
      Твоя задача — закрывать эмоциональную боль читателей (выгорание, апатия, тревога, неуверенность) через короткий текстовый импульс.
      Твой тон: абсолютно искренний, поддерживающий, безусловно любящий. Вызывающий ощущение: "обо мне заботятся".

      ТЫ ДОЛЖЕН ПИСАТЬ ФРАЗЫ В 3 КАТЕГОРИЯХ (чередуй их):
      1. ПОДДЕРЖИВАЮЩИЕ: Смысл — "Ты не для всех, двигайся в своем ритме", "Всё что ушло — к лучшему", "Выбирай себя".
      2. МОТИВИРУЮЩИЕ: Смысл — "У тебя всё получится", "Я в тебя верю", "Трудный путь ведет в красивые места", "Зеленый свет твоим планам".
      3. КОМПЛИМЕНТЫ И ФАКТЫ: Смысл — Напоминания о временах года ("Через месяц весна", "Завтра март"), либо прямые комплименты ("Ты потрясающе выглядишь сегодня", "Ты заслуживаешь лучшего").

      ПРАВИЛА ГЕНЕРАЦИИ:
      - Краткость: Строго до 10-15 слов. Одно, максимум два простых предложения.
      - Грамматика: Начинай с большой буквы. Простой словарный запас.
      - АНТИПОД (ЗАПРЕЩЕНО): Категорически запрещены ирония, сарказм, шуточки ("желаю просто выжить"), нытье. Никакого птичьего языка психологов ("сепарация", "ресурс"). Избегай конструкций, которые ты сам повторяешь: "успешный успех", "достигаторство".
      - ВНЕЗАПНЫЙ ВАРИАНТ: Одна из 15 фраз обязательно должна быть неожиданной — основанной на случайной корреляции примеров из датасета, чтобы удивить или выбить читателя из привычной колеи. Неожиданный поворот, неочевидная связь, сюрприз.
    user_template: |
      Изучи 50 реальных постов из нашего эталонного канала:

      {dataset}

      Пойми их главную механику: они дают читателю веру в лучшее и приятное ощущение теплоты. Сгенерируй 15 уникальных фраз, миксуя три категории (Поддержка, Мотивация, Комплименты). Одна фраза обязательно должна быть ВНЕЗАПНОЙ — основанной на случайной корреляции примеров, чтобы шокировать или выбить читателя из колеи. Выдай только текстовый массив.
  critic:
    system: |
      Ты — строгий модератор канала «ЭТО ЗНАК». Твоя задача — пропустить только 100% искренние, поддерживающие фразы без грамма цинизма, нытья или ИИ-воды.

      КРИТЕРИИ ОЦЕНКИ (Скор от 1 до 10):
      - Скор 9-10 (Идеал): Короткая (до 15 слов), очень простая фраза. Искренняя поддержка, добрая мотивация или уютный факт (про весну/выходные). Дает читателю ощущение "я не один".
      - Скор 1-6 (Мусор): Есть ирония, сарказм, шутки, негатив ("мы будем ныть из-за жары"). Длинные нравоучения. Банальные нейросетевые метафоры про "преодоление преград".

      ТВОЯ ЗАДАЧА:
      1. Оцени 15 предложенных фраз.
      2. Оставь ТОЛЬКО фразы со скором $\ge 7$.
      3. Ограничь список до 7 самых лучших, искренних и РАЗНООБРАЗНЫХ фраз.
      4. Верни данные в запрошенной JSON/Pydantic структуре.
    user_template: |
      Оцени 15 фраз. Оставь до 7 самых коротких, поддерживающих и теплых (скор $\ge 7$). Жестко отбракуй любой сарказм, шутки и нытье про жизнь:

      {phrases}



================================================
FILE: docs/SUPABASE_DB.md
================================================
[Binary file]


================================================
FILE: docs/tz/epics logic todos.md
================================================
[Binary file]


================================================
FILE: docs/tz/tehdolg.md
================================================
# Техдолг

Осознанные отрезы. Закрываем по мере итераций.

---

## Закрыто в v2.0

- [x] Конфиги в YAML (промпты, медиа)
- [x] Мультитенантность (каналы, выбор в боте)
- [x] Датасеты в БД
- [x] Post Now
- [x] Ручное время (FSM)
- [x] Случайные позиции текста на картинке

---

## Остаётся

### БД и API
- **Промпты в БД** — таблица `channel_prompts` (channel_id, prompt_type, content). Сейчас все каналы используют одни промпты из YAML. Нужно: разные промпты для разных каналов, редактирование без деплоя.
- **PATCH /posts/{id}** — обновление поста поштучно. Сейчас бот тасует в памяти и шлёт schedule-batch.

### LLM
- **Рефлексия (Prompt 3)** — агент смотрит на ошибки и переделывает. Отложено: циклы, перерасход токенов.
- **Авто-апрув 10/10** — посты с идеальной оценкой в расписание без человека.

### Медиа
- **Видео (FFmpeg)** — наложение текста на стоковые видео.
- **Бренд-тайминги** — слоты 09:09, 12:12, 18:18.

### Bot UX
- **Regenerate** — перегенерировать один пост, не всю пачку.
- **Часовые пояса** — сейчас только MSK. Нужно: timezone юзера, UTC в БД.
- **Кнопки удаления в «Ожидают постинга»** — добавить под каждым постом кнопку удаления (отмена записи в расписание, отмена поста).

### Скрипты и датасеты
- **Парсинг ТГК в датасет** — Telethon/Pyrogram скрипт для выгрузки постов чужого канала в таблицу `datasets`. Таблица и логика есть, нужен парсер.
- **Внесение датасета** — скрипт или UI для массового добавления фраз в датасет (из HTML-экспорта, из файла, вручную). Сейчас — разово через seed; в будущем — нормальная автоматизация.
- **Занести все посты из references в dataset** — распарсить messages.html, messages2.html, messages3.html, messages4.html (references/eto znak/) и добавить все подходящие фразы в таблицу `datasets`. Сейчас seed берёт только 5 фраз из messages4.html.



================================================
FILE: docs/tz/tz.md
================================================
# Техническое Задание (TZ)
**Проект:** Автоматизированная система генерации и отложенного постинга контента для сети Telegram-каналов.

## 📌 1. Цели и принципы системы
*   **Цель:** Свести к минимуму ручной труд по ведению 5+ Telegram-каналов за счет автоматической генерации, удобной модерации и автопостинга.
*   **Архитектурный принцип:** Telegram-бот выступает исключительно интерфейсом (тупой роутер). Вся бизнес-логика, генерация, взаимодействие с БД и планирование живут на независимом бэкенде. Общение между ними происходит в формате JSON.
*   **Асинхронность:** Проект полностью асинхронный — бот (aiogram), бэкенд (FastAPI), LLM-вызовы и доступ к БД используют `async/await`. Это позволяет не блокировать event loop при долгих операциях (LLM, запросы к БД).
*   **Принцип MVP:** Делаем жестко заданный пайплайн. Агенты не используются (это усложняет дебаг и замедляет работу). Сначала генерируем текст. Генерацию картинок делаем **в последнюю очередь MVP** — после того как весь пайплайн (генерация, модерация, планирование, постинг) работает на чистом тексте.
*   **Каналы для MVP:** Один канал. При старте бот/бэкенд берёт первый `channel_id` из БД (или создаёт дефолтный сидом). Выбор канала в UI не делаем.
*   **Доступ:** Бот доступен только администраторам. Список Telegram ID админов задаётся в `.env`. Пользователи, чей ID не в списке, не могут использовать бота (игнорирование или сообщение «Доступ запрещён»).

---

## 🏗 2. Архитектура и Технический Стек

**Поток данных:**
`Пользователь -> TG Бот -> FastAPI Бэкенд -> LLM / DB -> Scheduler -> TG Каналы`

<details open>
<summary><b>Выбранный стек технологий (Развернуть)</b></summary>

*   **Язык / Core:** Python 3.x
*   **Bot / UI:** Telegram Bot (`aiogram` + `pydantic`)
*   **Backend / API:** FastAPI (асинхронный, все эндпоинты — `async def`) + `uvicorn`
*   **LLM-пайплайн:** `pydantic-ai` + LLM через OpenRouter
*   **База Данных:** Supabase (PostgreSQL)
*   **Доступ к БД:** SQLAlchemy (Асинхронный движок)
*   **Миграции:** Alembic
*   **Планировщик (Scheduler):** `APScheduler` (подходит для MVP: легко встраивается в FastAPI, позволяет планировать задачи по времени).
*   **Медиа:** `Pillow` (генерация картинок с текстом) — **в конце MVP**, после стабилизации текстового пайплайна.
*   **Логирование:** `structlog` (вывод логов в структурированном JSON-формате).
</details>

**🔒 Защита API Бэкенда:**
Бот закрыт по Telegram ID, но бэкенд (FastAPI) тоже нужно минимально защитить, чтобы никто не дернул эндпоинт `/generate` напрямую по IP.
*Решение в 1 строчку:* Задаем в `.env` секретный токен `BACKEND_API_KEY`. Бот при каждом запросе прикладывает его в заголовки (`X-API-Key: ...`), а FastAPI проверяет совпадение.

---

## ⚙️ 3. Основной Workflow (Пайплайн)

Жизненный цикл контента состоит из 4 шагов.

### Шаг 1: Генерация
1. Пользователь в боте нажимает кнопку **"Сгенерировать"** (постоянная кнопка под полем ввода).
2. Бот отправляет POST-запрос на бэкенд.
3. Бэкенд берет хардкод-датасет успешных постов (для конкретного канала) и отправляет запрос в LLM.
4. LLM генерирует $N = 15$ новых фраз.

### Шаг 2: Отбор (Ранжирование)
1. Бэкенд прогоняет сгенерированные $N=15$ фраз через второй промпт LLM (Prompt 2: Критик).
2. LLM оценивает фразы и возвращает JSON с отфильтрованным списком, где количество фраз $M \le 7$.
3. *Опционально (не для MVP):* Prompt 3 (Рефлексия), но пока этот шаг пропускается во избежание зацикливания.

### Шаг 3: Модерация человеком
1. Бот получает от бэкенда $M$ фраз и выводит их списком.
2. Пользователь видит меню с фразами и настраивает их судьбу (Кнопки: `Approve`, `Reject`, `Edit`).
3. Утвержденные посты переходят на этап планирования.

### Шаг 4: Планирование и Постинг
1. Для апрувленных постов генератор времени раскидывает слоты постинга (например: Пост 1 → Канал А → 12:00, Пост 2 → Канал B → 14:00).
2. Пользователь может: `Confirm All`, `Shuffle` (бот тасует слоты в памяти) или изменить время точечно.
3. При подтверждении бэкенд записывает посты в БД со статусом `scheduled`.
4. `APScheduler` каждую минуту проверяет БД:
   $$T_{\text{post}} \le T_{\text{now}}$$
5. Если условие выполняется, бэкенд отправляет пост в канал. *В конце MVP:* при вероятности $P = 0.3$ генерируется и прикрепляется картинка (см. раздел 7).

---

<details>
<summary><b>🧠 4. LLM Пайплайн (Prompts & pydantic-ai) - Нажми чтобы развернуть</b></summary>

Используем `pydantic-ai` для гарантии структуры ответа (JSON). Отдельного шага «парсинг текста в JSON» нет: задаём Pydantic-модель как `output_type`, библиотека передаёт схему в LLM (через tool calling / structured output), и модель сразу возвращает готовые структурированные данные. Валидация и парсинг выполняет pydantic-ai.

**Prompt 1 (Генератор):**
*   **Вход:** Системный промпт + 10-20 эталонных фраз (DataSet).
*   **Задача:** Сгенерировать 15 фраз в идентичном стиле, тоне и длине.
*   **Выход:** Массив строк (15 шт).

**Prompt 2 (Критик/Ранжировщик):**
*   **Вход:** 15 сгенерированных фраз.
*   **Задача:** Оценить каждую фразу от 1 до 10 на соответствие стилю и здравому смыслу. Оставить только те, чей скор $\ge 7$, ограничив итоговый список 7 лучшими.
*   **Выход (Pydantic Schema):**
    ```python
    class RankedPhrase(BaseModel):
        text: str
        score: int

    class LLMResponse(BaseModel):
        approved_phrases: list[RankedPhrase]
    ```

*Почему пайплайн, а не агенты?* Жесткий конвейер предсказуем, не тратит лишние токены на "раздумья" и легко дебажится.
</details>

<details>
<summary><b>🗄 5. База Данных (Supabase / SQLAlchemy) - Нажми чтобы развернуть</b></summary>

Минимальная схема для MVP:

**Таблица `channels`**
*   `id` (UUID, PK)
*   `telegram_id` (String / BigInt)
*   `name` (String)

**Таблица `posts`**
*   `id` (UUID, PK)
*   `channel_id` (FK -> channels.id)
*   `text` (Text)
*   `scheduled_at` (Timestamp)
*   `status` (Enum: `draft`, `scheduled`, `posted`, `failed`)
*   `created_at` (Timestamp)

*Примечание:* Таблицы `prompts` и `datasets` на этапе MVP не создаем. Хардкодим их в `backend/core/prompts.py`.

**📋 Жизненный цикл статусов поста:**
*   `draft` — создан при approve, время ещё не подтверждено
*   `scheduled` — время подтверждено, ожидает постинга
*   `posted` / `failed` — после попытки публикации

**⏱ Правило часовых поясов (Timezones):**
Чтобы не сойти с ума при дебаге постинга, принимаем жесткое правило: **Вся система работает исключительно в Московском времени (UTC+3).**
*   Сервер, FastAPI и `APScheduler` настраиваются на таймзону `Europe/Moscow`.
*   Пользователь в боте видит и вводит время по МСК.
*   В БД (`scheduled_at`) время летит тоже в МСК.
*Вайбкодинг-подход:* Никаких сложных конвертаций "UTC -> Локал -> UTC". В Docker/сервере просто задаем переменную среды `TZ=Europe/Moscow` и везде используем локальное время.
</details>

<details>
<summary><b>🔌 6. API Бэкенда - Нажми чтобы развернуть</b></summary>

Протокол взаимодействия (REST API) между ботом и бэкендом:

1.  `POST /api/v1/generate`
    *   **Body:** `{"channel_id": "uuid"}` — для MVP бот берёт единственный `channel_id` из БД при старте (первый канал или дефолтный сид).
    *   **Response:** `{"phrases": ["text1", "text2", ...]}`
2.  `POST /api/v1/posts/approve`
    *   **Body:** `{"phrases": ["text1", "text2"]}` — массив финальных текстов (в т.ч. после Edit на стороне бота). `generation_id` не нужен. Бэкенд создаёт записи в БД.
    *   **Response:**
    ```json
    {
      "draft_posts": [
        {
          "id": "uuid",
          "text": "...",
          "channel_id": "uuid",
          "suggested_time": "2025-03-10T14:30:00+03:00"
        }
      ]
    }
    ```
3.  `POST /api/v1/posts/schedule-batch`
    *   **Body:** `[{"post_id": "uuid", "channel_id": "uuid", "time": "ISO8601"}, ...]` — пакетное подтверждение расписания.
</details>

---

## 🎨 7. Работа с Медиа (Медиа Генератор)

**⚠️ Делать в последнюю очередь MVP** — после того как текстовый пайплайн полностью работает. Сначала постим только текст.

Чтобы избежать сложностей с сеттингом нейросетей-генераторов картинок и видео в MVP:

*   **Алгоритм графики:** Перед публикацией поста `APScheduler` применяет рандомайзер. Если выпадает вероятность $P \le 0.3$, вызывается медиа-сервис.
*   **Реализация (`Pillow`):** Берется случайная картинка из локальной папки `assets/templates/` (10-20 стоковых фонов). С помощью библиотеки `Pillow` текст поста центрируется, накладывается красивый шрифт (например, Arial/Impact с тенью) и сохраняется во временный буфер для отправки в Telegram.
*   **Видео:** (FFmpeg) для MVP **Исключено**. Оставлено на v2.0.

---

## 📱 8. Telegram Bot UX (Карта интерфейса)

Бот должен быть максимально простым, без лишних шагов.

**Аутентификация (доступ только для админов):**
*   В `.env` задаётся переменная `ADMIN_TELEGRAM_IDS` — список Telegram ID администраторов через запятую (например: `123456789,987654321`).
*   Бот проверяет `message.from_user.id` при каждом апдейте. Если ID не в списке — хендлер не выполняется, пользователю отправляется сообщение «Доступ запрещён» (или апдейт игнорируется).
*   Команда `/start` доступна всем (для приветствия), но функционал генерации, модерации и планирования — только админам.

**Базовое меню:**
Кнопки под полем ввода (ReplyKeyboardMarkup, постоянно видны):
`[ 🎲 Сгенерировать ]` `[ 📅 Ожидают постинга ]` `[ 📊 Статистика ]`

**Флоу модерации (Inline кнопки):**
Бот присылает сообщение:
> 📝 Фраза 1: *"Пример сгенерированного крутого текста"*

Inline-клавиатура под сообщением:
`[ ✅ Approve ]` `[ ❌ Reject ]` `[ ✏️ Edit ]`

**🕹 Редактирование текстов (FSM — только на стороне бота):**
Редактирование происходит **исключительно в памяти бота**. Бот собирает финальные тексты и только потом шлёт их в `POST /approve`. Отдельный `PATCH /posts/{id}` для MVP не нужен.
*Пайплайн:*
1. Юзер жмет inline-кнопку `[ ✏️ Edit ]` под конкретной фразой.
2. Бот переходит в состояние ожидания (`State: waiting_for_text`) и сохраняет индекс/идентификатор фразы в `state_data`.
3. Юзер отправляет новое сообщение с текстом в чат.
4. Бот обновляет текст в локальном списке фраз, благодарит юзера и сбрасывает состояние (`state.clear()`).
5. При нажатии Approve бот отправляет весь финальный список текстов в `POST /approve`.

**Флоу планирования (после Approve):**
> 📅 **Расписание для апрувленных постов:**
> Пост 1 ➡️ Канал A ➡️ Завтра 14:30
> Пост 2 ➡️ Канал B ➡️ Завтра 18:00

Inline-клавиатура:
`[ 🚀 Approve All & Schedule ]` `[ 🔀 Shuffle время ]` `[ ⏰ Изменить время точечно ]`

*Примечание:* **Shuffle** выполняется только на стороне бота — бот тасует `suggested_time` в памяти перед отправкой на `POST /schedule-batch`. API для Shuffle не нужен.

---

## 🪵 9. Логирование и мониторинг
Используется библиотека `structlog`. Все критические действия выводятся в формате JSON для легкого поиска проблем.
*Пример лога автопостинга:*
```json
{
  "event": "post_published",
  "level": "info",
  "channel_id": "crypto_memes",
  "post_id": "123e4567-e89b-12d3",
  "has_media": true,
  "timestamp": "2023-10-27T14:30:00Z"
}
```

---

## 🚀 10. План развития (Roadmap)

### Этап 1: MVP (Фокус текущего ТЗ)
- [x] Развернуть FastAPI с `uvicorn` и Бота на `aiogram`.
- [x] Аутентификация по `ADMIN_TELEGRAM_IDS` в `.env` — доступ только для админов.
- [x] Подключить Supabase через SQLAlchemy.
- [x] Настроить Pydantic-AI + OpenRouter (Промпт 1 и 2).
- [x] Реализовать модерацию и назначение времени в TG Боте.
- [x] Настроить `APScheduler` для вытаскивания постов из БД в указанное время.
- [ ] Реализовать вероятность постинга картинок-заглушек через `Pillow` — **в последнюю очередь MVP**.

### Этап 2: Масштабирование (Later)
- [ ] Опционально: режим зеркальных часов (09:09, 12:12, 18:18) при генерации слотов — бренд/эстетика (см. `docs/tz/инсайты.md`).
- [ ] Добавить генерацию видео через `FFmpeg` (наложение текста поверх видео стоков).
- [ ] Полноценный Агент рефлексии (Промпт 3) для самоулучшения промптов.
- [ ] Перенос промптов и датасетов из кода в Supabase с возможностью редактирования через бота.
- [ ] Автоапрув части постов (без участия человека), если LLM дала оценку 10/10.

---
## 📁 11. Структура проекта

**Текущее состояние:** есть `docs/`, `references/`. Остальное — целевая структура для реализации.

```text
project_root/
├── docs/                  # Документация (есть)
│   └── tz/
│       ├── tz.md
│       ├── инсайты.md
│       └── ...
├── references/            # Референсы, экспорты (есть)
│   └── eto znak/
│       ├── css/, images/, js/, stickers/
│       └── messages*.html
├── bot/                   # Тупой роутер и UI
│   ├── bot.py
│   ├── handlers/
│   └── keyboards/
├── backend/               # Вся логика
│   ├── main.py            # Точка входа FastAPI
│   ├── api/               # Роуты (generate, schedule)
│   ├── core/              # Конфиги, structlog, prompts.py
│   ├── services/
│   │   ├── llm_pipeline.py  # pydantic-ai логика
│   │   ├── media_gen.py     # Pillow склейка (в конце MVP)
│   │   └── scheduler.py     # APScheduler
│   └── db/
│       ├── models.py
│       └── repository.py
├── alembic/               # Миграции
├── assets/                # Стоковые картинки и шрифты
│   └── templates/        # Фоны для Pillow
├── .env                   # BOT_TOKEN, ADMIN_TELEGRAM_IDS, BACKEND_API_KEY, DB_URL, OPENROUTER_API_KEY
├── .env.example           # Шаблон без секретов
└── docker-compose.yml
```


================================================
FILE: docs/tz/инсайты.md
================================================
# Инсайты

---

## 1. Постинг по «нумерологическому» времени (09:09, 12:12, 18:18)

**Вывод:** 99% вероятности, что это не реальная стратегия роста, а психологический или бренд-эффект. Но у этого мува есть несколько практических причин.

### 1.1. Визуальный паттерн
Время вроде `09:09`, `12:12`, `18:18`, `21:21` — люди замечают такие числа быстрее (pattern recognition, мозг любит симметрию). `12:07` — обычное время, `12:12` — мозг фиксирует. Микро-CTR-хак.

### 1.2. Бренд-стратегия
Каналы постят в `11:11`, `13:13`, `17:17` — узнаваемый стиль, создаёт мем, повышает запоминаемость.

### 1.3. Эзотерическая аудитория
Каналы цитат/психологии играют на «ангельские числа», знаки, судьбу. «Увидел пост в 11:11 — это знак» = эмоциональный триггер.

### 1.4. Технический хак
`09:09`, `12:12`, `15:15`, `18:18` проще программировать (каждые 3 часа + 9 минут).

### 1.5. Ограничение
На реальный охват почти не влияет. Важно окно (7–9, 12–14, 20–22), а не конкретная минута.

### 1.6. Temporal habit loop
Постинг в одинаковые минуты каждый день — аудитория привыкает и начинает ждать.

### 1.7. Оценка вероятностей
```
45% эстетика | 25% бренд | 15% эзотерика | 10% удобство автопостинга | 5% SMM-логика
```

---

## 2. Перелив трафика между каналами

В больших Telegram-сетках делают хитрый трюк со временем:

```
канал A → 12:01
канал B → 12:03
канал C → 12:05
```

Схема используется для **перелива трафика между каналами**. Механизм гениальный, почти никто не замечает.



================================================
FILE: docs/tz/archive/обудмывание с ллмкой.md
================================================
Ок, давай превратим это в **нормальное ТЗ**, чтобы:
* можно было **реально начать кодить**,
* не усложнить архитектуру,
* оставить **возможность масштабировать**.

Я разобью на блоки:

1️⃣ Цель системы
2️⃣ Архитектура
3️⃣ Основной workflow
4️⃣ Компоненты системы
5️⃣ LLM пайплайн
6️⃣ База данных (Supabase)
7️⃣ Планировщик постов
8️⃣ Медиа (картинки / видео)
9️⃣ Telegram Bot UX
10️⃣ API backend
11️⃣ Логирование
12️⃣ MVP vs Later
13️⃣ Пример структуры проекта

---

# 1. Цель системы

Система для **автоматической генерации и публикации коротких фраз** в сеть Telegram-каналов.

Функции:

* анализ существующих каналов
* генерация похожих фраз через LLM
* ручная модерация
* планирование постинга
* автоматический постинг
* опциональная генерация медиа

Система должна **минимизировать ручной труд**.

---

# 2. Архитектура

```
Telegram Bot
     |
     v
FastAPI Backend
     |
     |---- LLM (OpenRouter)
     |
     |---- Supabase (Postgres)
     |
     |---- Scheduler
     |
     |---- Media generator
     |
     v
Telegram Channels
```

### Поток

```
User
 ↓
TG Bot
 ↓
FastAPI
 ↓
LLM generation
 ↓
Moderation
 ↓
Schedule
 ↓
DB
 ↓
Scheduler
 ↓
Post to TG channels
```

---

# 3. Основной Workflow

## 1 Генерация

Юзер:

```
/generate
```

Бот → backend

backend:

1. получает dataset фраз канала
2. вызывает LLM
3. генерирует **15 фраз**

---

## 2 Отбор

LLM:

* оценивает
* ранжирует

результат:

```
15 -> 7
```

---

## 3 Модерация

Юзер видит список:

```
1
2
3
4
5
6
7
```

Кнопки:

```
Approve
Reject
Edit
Regenerate
```

---

## 4 Планирование

После approval:

бот показывает:

```
Post 1 → Channel A → 12:00
Post 2 → Channel B → 14:00
Post 3 → Channel C → 18:00
```

Кнопки:

```
edit time
post now
approve all
shuffle
```

---

## 5 Сохранение

После подтверждения:

в DB:

```
post_text
channel_id
scheduled_at
status
```

---

## 6 Постинг

Scheduler:

каждую минуту:

```
select * from posts
where scheduled_at <= now
and status = scheduled
```

постит

---

# 4. Компоненты системы

## 1 Telegram Bot

роль:

**UI + Router**

логики почти нет.

Функции:

* кнопки
* отправка команд backend
* получение результатов

Можно использовать:

* aiogram
* python-telegram-bot

Я бы выбрал **aiogram**.

---

## 2 Backend

FastAPI сервер.

Функции:

* генерация
* LLM пайплайн
* scheduling
* media generation
* API для бота

---

## 3 Supabase

Postgres база.

Хранит:

* посты
* каналы
* промпты
* dataset

---

## 4 Scheduler

варианты:

### простой

```
APScheduler
```

или

```
cron job
```

или

```
celery
```

Для MVP:

**APScheduler**

---

# 5. LLM Pipeline

### Prompt 1 — generation

вход:

```
dataset: 100 фраз
```

выход:

```
15 новых фраз
```

пример:

```
Generate 15 short phrases similar in style.

Rules:
- same tone
- short
- ironic
- max 12 words
```

---

### Prompt 2 — ranking

вход:

```
15 phrases
```

выход:

```
score each phrase
select best 7
```

---

### Prompt 3 (optional)

reflection

но я бы **убрал для MVP**

слишком сложно.

---

# 6. Database Schema (Supabase)

## channels

```
id
name
telegram_id
topic
created_at
```

---

## posts

```
id
text
channel_id
scheduled_at
status

status:
draft
approved
scheduled
posted
failed
```

---

## datasets

```
id
channel_id
text
created_at
```

dataset = фразы канала

---

## prompts

```
id
name
content
version
created_at
```

---

## generations

```
id
channel_id
raw_output
created_at
```

---

## generation_items

```
id
generation_id
text
score
selected
```

---

# 7. Scheduler

Каждую минуту:

```
SELECT * FROM posts
WHERE status = 'scheduled'
AND scheduled_at <= now()
```

далее:

```
send_message(channel)
```

если успех:

```
status = posted
```

если ошибка:

```
status = failed
retry_count++
```

---

# 8. Медиа

Ты предложил **правильный простой подход**.

## Картинки

вероятность:

```
p = 0.3
```

если true:

генерируется картинка.

---

## как

берем:

```
stock image
+
overlay text
```

библиотеки:

```
Pillow
```

или

```
moviepy
```

---

## Видео (опционально)

pipeline:

```
video.mp4
+
ffmpeg
+
drawtext filter
```

пример:

```
ffmpeg -i video.mp4 \
-vf drawtext="text='phrase':x=100:y=100" \
output.mp4
```

---

# 9. Telegram Bot UX

### Команды

```
/generate
/pending
/schedule
/stats
```

---

### Generate

```
Generate phrases?
[ YES ]
```

---

### Approval

```
1 phrase
2 phrase
3 phrase
```

кнопки:

```
Approve
Reject
Edit
```

---

### Scheduling

```
Post #1
Channel A
Time: 14:30

[edit]
[post now]
```

---

# 10. API Backend

## generate

```
POST /generate
```

response

```
generation_id
phrases[]
```

---

## approve

```
POST /approve
```

body

```
generation_item_id
```

---

## schedule

```
POST /schedule
```

body

```
post_id
channel_id
time
```

---

## post_now

```
POST /post-now
```

---

# 11. Логирование

использовать:

```
structlog
```

пример:

```
event="post_published"
channel="crypto_memes"
post_id=123
```

---

# 12. MVP vs Later

## MVP

✔ генерация
✔ модерация
✔ планирование
✔ автопостинг
✔ базовые картинки

---

## Later

❌ видео
❌ reflection agent
❌ auto approval
❌ analytics
❌ TikTok

---

# 13. Структура проекта

```
project/

bot/
    bot.py
    handlers/
    keyboards/

backend/
    main.py
    api/
    services/

services/
    llm_service.py
    generation_service.py
    scheduler_service.py
    posting_service.py
    media_service.py

db/
    models.py
    repository.py

agents/
    generation_agent.py
    ranking_agent.py

utils/
    logging.py

workers/
    scheduler.py
```

---

# 14. Важные архитектурные решения

### 1 не делать агента сейчас

Сделай **pipeline**.

агенты = переусложнение.

---

### 2 LLM только 2 шага

```
generate
rank
```

---

### 3 бот максимально тупой

вся логика backend.

---

# 15. Стоимость

примерно:

LLM:

```
~3000 генераций
* 0.002
= ~6$
```

копейки.

---

# 16. Что реально самое сложное

не LLM.

а:

1️⃣ UX бота
2️⃣ scheduling
3️⃣ Telegram rate limits
4️⃣ dataset extraction

---

# 17. Очень важный момент

сейчас **самая большая ошибка которую можно сделать**:

❌ делать универсальную систему

нужно сделать:

```
hardcoded pipeline
```

---

# 18. Я бы упростил еще сильнее

в MVP:

```
generate 15
human select 5
schedule
post
```

без авто-ранкинга.

---

# Если хочешь — я могу дальше:

* расписать **идеальную схему Supabase (SQL)**
* написать **архитектуру FastAPI сервера**
* сделать **промпты generation + ranking**
* и показать **как сделать LLM pipeline на pydantic-ai**.



================================================
FILE: docs/tz/archive/отфильтрованные идеи ллмки с тз.md
================================================
нормальное ТЗ, чтобы:

можно было реально начать кодить,

не усложнить архитектуру,

оставить возможность масштабировать.

Я разобью на блоки:

1️⃣ Цель системы
2️⃣ Архитектура
3️⃣ Основной workflow
4️⃣ Компоненты системы
5️⃣ LLM пайплайн
6️⃣ База данных (Supabase)
7️⃣ Планировщик постов
8️⃣ Медиа (картинки / видео)
9️⃣ Telegram Bot UX
10️⃣ API backend
11️⃣ Логирование
12️⃣ MVP vs Later
13️⃣ Пример структуры проекта

1. Цель системы

Система для автоматической генерации и публикации коротких фраз в сеть Telegram-каналов.

Функции:
- генериация фраз с промптом где будет кучка датасетных фраз эталонных
- ручная модерация
- планирование постинга
- автоматический постинг
- опциональная генерация медиа

Система должна минимизировать ручной труд. 

Архитектура сверху вниз взаимодействие:
- телеграм бот
- фастапи бэкэнд
ллм
супабейз
скедулер
медиа генератор
- телеграм каналы 

поток:
User
 ↓
TG Bot
 ↓
FastAPI
 ↓
LLM generation
 ↓
Moderation user
 ↓
Schedule
 ↓
DB
 ↓
Scheduler
 ↓
Post to TG channels

общение НА JSON 

Основной workflow:
1. генерация
Кнопка сгенерируй в чате с ботом

Бот -> backend

бэкенд дергает промпт, вызывает ллм, генерирует 15 фраз

2. отбор:
ллм оценивает + ранжирует
результат примерно 15->7 достойных вариантов, но надо чекнуть как реально справляется ллмка. 

3. Модерация
юзер видит список 1-7 фраз
кнопки 
- апрув
- reject 
- edit
- regenerate

Хранить ли стейты fsm или похуй? вопрос MCP и оверинжиниринга

4. Планирование
после approval 
бот показывает 
Post 1 → Channel A → 12:00 + data
Post 2 → Channel B → 14:00 + data
Post 3 → Channel C → 18:00 + data

кнопки:
edit time (тут сетка с выбором поста, потом написанием времени, надо аккуратно в 1-2 шага написать чтобы карту пользователя не раздувать)
post now (additional)
approve all (напрямую в бд ебашит)
shuffle (меняет местами время просто)

5. сохранение
в бд 
айди канала
текст поста 
время постинга
статус (МОЖЕТ ТУТ СТАТУС ПОСТА ТИПА)

6. Постинг 
действительно ли он должен селекты делать и в бд запросы делать? 
но тем не менее приммерно 
select * from posts
where scheduled_at <= now
and status = scheduled
но sql запрос надо попросить сгенерировать получше

Тех стек
1. tg bot aiogram + pydantic
это ui + router 
функции: 
кнопки
отправка команд backend 
получение результатов

2. фастапи сервер backend
функции
генерация
ллм пайплайн / pydantic ai крч работа хуй знает как не знаю эту технолгию совсем
scheduling
media generation? (по-минимому)
api для взаимодействия с ботом

3. супабейз
хранит 
посты
каналы
промпты
датаест (опционально, на первых порах в промпте)

4. скедулер
celery / cron job? 

для мвп APScheduler что это такое? 

5. Ллм пайплайн
- промпт 1
вход промпт + датасет 10-100 фраз проверить
пример:
сгенерируй 15 фраз в подобном стиле: 

Правила: 
- - -
Примеры: 
- - - 

- промпт 2 
вход 15 фраз ака выход промпта 1
выход 
оценка each phrase 
select best 7 

- промпт 3 
reflection и решение ллмки начать заново процесс или не трогать и апрувить внутренним критиком.

6. Датабейз схема
есть 2 таблицы
каналы
посты (id
text
channel_id
scheduled_at
status

status:
draft
approved
scheduled
posted
failed) 
датасет? (похуй не нужен)
промпты? (для mvp не нужен, требуется 1) 

7. Скедулер
"Каждую минуту:

SELECT * FROM posts
WHERE status = 'scheduled'
AND scheduled_at <= now()

далее:

send_message(channel)

если успех:

status = posted

если ошибка:

status = failed
retry_count++" это гипотетически надо отрефлексировать как бест практика в этом работает

8. Медиа
генерировать картинки с вероятностью 0.3 перед постом чтобы никто не знал будет ли картинка, но это надо отдельным доп шагом, сначала тексты

как
берем сток картинку и пост , мб ffmpeg либо бест практики склеивания картинок в питорне, потому что ффмпег заеб

видео похуй не будем но там ффмпег

9. 
Кнопки под окошком чата: 
генерировать 
pending
schedule
stats? (зачем? пока плейсхолдер) 

генерировать (запускает пайплайн) -> approval 
"1 phrase
2 phrase
3 phrase" и кнопки 
->
скедулер, 
"Post #1
Channel A
Time: 14:30

Post #1
Channel A
Time: 14:30

Post #1
Channel A
Time: 14:30"

кнопки
edit, regenerate, крч выше написал

10. Продумать api backend, мб "generate
POST /generate

response

generation_id
phrases[]
approve
POST /approve

body

generation_item_id
schedule
POST /schedule

body

post_id
channel_id
time
post_now
POST /post-now" но лучше - чтобы были json с ллм взаимодействия и запросы норм

11. Логирование

использовать:

structlog

пример:

event="post_published"
channel="crypto_memes"
post_id=123

12. MVP 
генерация
модерация
планирование
автопостинг
базовые картинки

Later
видео
аналитика
автоапрув
рефлексия сложная


13. Важные архитектурные вопросы или решения: 
Почему агент медленнее ссделать длля проверки гипотезы чем пайплайн? 
бот максимально тупой вся логика в бэкенде
ллм 2-3 шага только, чтобы можно было выключить в конфиге
стоимость копеечная

16. Самое сложное это код не ллм
17. самая главная ошибка - переусложнить и сделать универсальную систему без проверки как будет пайплайн действовать

18. самый простой вариант для проверки гипотезы
generate 15
human select 5
schedule
post

главное не построить говнокод который испортит масштабирование. не навреди. 

тех стек примерно "Язык / Core: Python 3.x
Bot / UI: Telegram Bot (aiogram + pydantic)
Backend / API: FastAPI (+ uvicorn для сервера)
LLM‑пайплайн: pydantic-ai + LLM через OpenRouter
БД: Supabase (PostgreSQL)
Доступ к БД: SQLAlchemy (+ клиент Supabase по желанию)
Миграции БД: Alembic
Планировщик: APScheduler (MVP), позже можно cron / Celery
Медиа: Pillow, опционально moviepy + ffmpeg
Логирование: structlog

" вот я так думаю 


================================================
FILE: docs/tz/archive/черновик идеи.md
================================================
[Binary file]


================================================
FILE: scripts/create_bg.py
================================================
"""Создаёт тестовый фон assets/templates/bg.jpg, если файл отсутствует."""

from pathlib import Path

from PIL import Image

TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "assets" / "templates"
BG_PATH = TEMPLATES_DIR / "bg.jpg"
WIDTH, HEIGHT = 1080, 1080


def create_gradient_bg() -> None:
    """Генерирует градиентный фон и сохраняет в bg.jpg."""
    img = Image.new("RGB", (WIDTH, HEIGHT))
    pixels = img.load()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            # Градиент от тёмно-синего к тёмно-фиолетовому
            r = int(30 + (x / WIDTH) * 80)
            g = int(20 + (y / HEIGHT) * 60)
            b = int(100 + (x / WIDTH) * 80)
            pixels[x, y] = (r, g, b)
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    img.save(BG_PATH, "JPEG", quality=85)
    print(f"Создан: {BG_PATH}")


if __name__ == "__main__":
    if BG_PATH.exists():
        print(f"Файл уже существует: {BG_PATH}")
    else:
        create_gradient_bg()



================================================
FILE: scripts/load_dataset_from_html.py
================================================
#!/usr/bin/env python3
"""
Загрузка датасета из HTML-экспорта канала «ЭТО ЗНАК» в таблицу datasets.
Парсит messages.html, messages2.html, messages3.html, messages4.html.
Включает только посты БЕЗ ссылок (длина 15–400 символов).

Запуск:
  uv run python scripts/load_dataset_from_html.py --dry-run   # только статистика
  uv run python scripts/load_dataset_from_html.py --apply    # загрузка в БД
"""

import argparse
import asyncio
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

import uuid

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert

from backend.db.models import Channel, Dataset
from backend.db.session import async_session_factory

REFERENCES_DIR = Path(__file__).resolve().parent.parent / "references" / "eto znak"
HTML_FILES = ["messages.html", "messages2.html", "messages3.html", "messages4.html"]

MIN_LEN = 15
MAX_LEN = 400
BATCH_SIZE = 300


def _strip_html(text: str) -> str:
    """Убирает HTML-теги, заменяет <br> на пробел."""
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    return " ".join(text.split()).strip()


def _parse_post(raw_html: str) -> str | None:
    """
    Извлекает текст поста, если он подходит.
    Возвращает None для постов с ссылками или не подходящих по длине.
    """
    if "<a href" in raw_html or "<a " in raw_html:
        return None
    clean = _strip_html(raw_html)
    if not clean or len(clean) < MIN_LEN or len(clean) > MAX_LEN:
        return None
    return clean


def _deduplicate(phrases: list[str]) -> list[str]:
    """Дедупликация по text, сохраняя порядок первого появления."""
    seen: set[str] = set()
    result: list[str] = []
    for p in phrases:
        text = p.strip()
        if text not in seen:
            seen.add(text)
            result.append(text)
    return result


def parse_and_filter() -> tuple[list[str], dict]:
    """
    Парсит все файлы, фильтрует и дедуплицирует.
    Возвращает (уникальные фразы, статистика).
    """
    pattern = re.compile(r'<div class="text">\s*(.*?)\s*</div>', re.DOTALL)
    total_raw = 0
    phrases: list[str] = []

    for filename in HTML_FILES:
        path = REFERENCES_DIR / filename
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        matches = pattern.findall(content)
        total_raw += len(matches)
        for raw in matches:
            if parsed := _parse_post(raw):
                phrases.append(parsed)

    unique = _deduplicate(phrases)
    stats = {
        "files_processed": sum(1 for f in HTML_FILES if (REFERENCES_DIR / f).exists()),
        "raw_extracted": total_raw,
        "after_filter": len(phrases),
        "unique": len(unique),
    }
    return unique, stats


async def main() -> None:
    parser = argparse.ArgumentParser(description="Загрузка датасета из HTML в БД")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Только парсинг и статистика (по умолчанию)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Выполнить insert в БД",
    )
    parser.add_argument(
        "--channel-name",
        default="ЭТО ЗНАК",
        help="Имя канала (default: ЭТО ЗНАК)",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Очистить датасет канала перед загрузкой",
    )
    args = parser.parse_args()
    apply_mode = args.apply

    phrases, stats = parse_and_filter()

    print("=== Статистика парсинга ===")
    print(f"  Файлов обработано: {stats['files_processed']}")
    print(f"  Всего div.text извлечено: {stats['raw_extracted']}")
    print(f"  После фильтра (без ссылок, 15–400 символов): {stats['after_filter']}")
    print(f"  Уникальных фраз: {stats['unique']}")

    if apply_mode:
        async with async_session_factory() as session:
            result = await session.execute(
                select(Channel).where(Channel.name == args.channel_name)
            )
            channel = result.scalar_one_or_none()
            if not channel:
                print(f"\nОШИБКА: Канал '{args.channel_name}' не найден в БД.")
                sys.exit(1)

            if args.replace:
                result_del = await session.execute(
                    select(Dataset).where(Dataset.channel_id == channel.id)
                )
                existing_count = len(result_del.scalars().all())
                if existing_count:
                    await session.execute(delete(Dataset).where(Dataset.channel_id == channel.id))
                    await session.commit()
                    print(f"  Датасет канала очищен ({existing_count} записей).")
                to_insert = phrases
            else:
                rows = await session.execute(
                    select(Dataset.text).where(Dataset.channel_id == channel.id)
                )
                existing_texts = {r[0].strip() for r in rows.scalars().all()}
                to_insert = [p for p in phrases if p.strip() not in existing_texts]
                skipped = len(phrases) - len(to_insert)
                if skipped:
                    print(f"  Пропущено (уже в БД): {skipped}")

            if not to_insert:
                print("\nНет новых фраз для вставки.")
                return

            inserted = 0
            for i in range(0, len(to_insert), BATCH_SIZE):
                batch = to_insert[i : i + BATCH_SIZE]
                values = [
                    {"id": uuid.uuid4(), "channel_id": channel.id, "text": t.strip()}
                    for t in batch
                ]
                stmt = insert(Dataset.__table__).values(values)
                stmt = stmt.on_conflict_do_nothing(
                    constraint="uq_datasets_channel_id_text"
                )
                await session.execute(stmt)
                await session.commit()
                inserted += len(batch)
                print(f"  Вставлено батч: {len(batch)} (всего {inserted})")

            print(f"\nГотово. Добавлено {inserted} фраз в датасет канала '{args.channel_name}'.")
    else:
        print(f"\n[--dry-run] Готово к вставке: {len(phrases)} фраз.")
        print("Запустите с --apply для загрузки в БД.")


if __name__ == "__main__":
    asyncio.run(main())



================================================
FILE: scripts/run_backend.py
================================================
[Empty file]


================================================
FILE: scripts/seed.py
================================================
#!/usr/bin/env python3
"""
Скрипт сидирования: 2 канала, по 5 постов на каждый, 5 фраз в датасете из messages4.html.
Запуск: uv run python scripts/seed.py
"""

import asyncio
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import select
from zoneinfo import ZoneInfo

from backend.core.config_loader import get_prompts
from backend.db.models import Channel, Dataset, Post, PostStatus, PromptTemplate
from backend.db.session import async_session_factory

MSK = ZoneInfo("Europe/Moscow")

CHANNELS = [
    {"telegram_id": "-1003812297034", "name": "ЭТО ЗНАК", "is_posting_channel": False},
    {"telegram_id": "-1003592368865", "name": "Канал 2", "is_posting_channel": True, "dataset_source_name": "ЭТО ЗНАК"},
]

# Плейсхолдеры для постов (для проверки постинга)
POST_TEXTS = [
    "Тестовый пост 1 — проверка постинга.",
    "Тестовый пост 2 — проверка постинга.",
    "Тестовый пост 3 — проверка постинга.",
    "Тестовый пост 4 — проверка постинга.",
    "Тестовый пост 5 — проверка постинга.",
]


def _parse_phrases_from_html(html_path: Path) -> list[str]:
    """Извлекает текстовые посты из div.text внутри div.message.default."""
    content = html_path.read_text(encoding="utf-8")
    # Ищем div.text (внутри message default)
    pattern = re.compile(r'<div class="text">\s*(.*?)\s*</div>', re.DOTALL)
    matches = pattern.findall(content)

    def strip_html(text: str) -> str:
        # Убираем теги, заменяем <br> на пробел
        text = re.sub(r"<br\s*/?>", " ", text, flags=re.IGNORECASE)
        text = re.sub(r"<[^>]+>", "", text)
        return " ".join(text.split()).strip()

    phrases = []
    for m in matches:
        clean = strip_html(m)
        if clean and len(clean) > 10:
            phrases.append(clean)

    return phrases


def _pick_motivational_phrases(phrases: list[str], count: int = 5) -> list[str]:
    """Выбирает мотивационные фразы в стиле канала (средней длины, без рекламы)."""
    # Исключаем слишком короткие, слишком длинные, рекламные
    filtered = []
    skip_keywords = ["яндекс", "еда", "ресторан", "valentine", "valentines", "8 марта", "цветы"]
    for p in phrases:
        if len(p) < 15 or len(p) > 400:
            continue
        lower = p.lower()
        if any(kw in lower for kw in skip_keywords):
            continue
        filtered.append(p)

    # Берём первые count подходящих (они уже в хронологическом порядке)
    return filtered[:count]


async def main() -> None:
    async with async_session_factory() as session:
        # 1. Создаём каналы
        channels_created: list[Channel] = []
        for ch_data in CHANNELS:
            result = await session.execute(
                select(Channel).where(Channel.telegram_id == ch_data["telegram_id"])
            )
            existing = result.scalar_one_or_none()
            is_posting = ch_data.get("is_posting_channel", True)
            if existing:
                updated = False
                if existing.name != ch_data["name"]:
                    existing.name = ch_data["name"]
                    updated = True
                if getattr(existing, "is_posting_channel", True) != is_posting:
                    existing.is_posting_channel = is_posting
                    updated = True
                ds_source_name = ch_data.get("dataset_source_name")
                if ds_source_name:
                    result_src = await session.execute(
                        select(Channel).where(Channel.name == ds_source_name)
                    )
                    src_channel = result_src.scalar_one_or_none()
                    if src_channel and (getattr(existing, "dataset_source_channel_id", None) != src_channel.id):
                        existing.dataset_source_channel_id = src_channel.id
                        updated = True
                if updated:
                    print(f"Обновлён канал: {ch_data['name']} (telegram_id={existing.telegram_id})")
                else:
                    print(f"Канал уже есть: {existing.name} (telegram_id={existing.telegram_id})")
                channels_created.append(existing)
            else:
                ch = Channel(
                    telegram_id=ch_data["telegram_id"],
                    name=ch_data["name"],
                    is_posting_channel=is_posting,
                )
                session.add(ch)
                await session.flush()
                ds_source_name = ch_data.get("dataset_source_name")
                if ds_source_name:
                    result_src = await session.execute(
                        select(Channel).where(Channel.name == ds_source_name)
                    )
                    src_channel = result_src.scalar_one_or_none()
                    if src_channel:
                        ch.dataset_source_channel_id = src_channel.id
                channels_created.append(ch)
                print(f"Добавлен канал: {ch.name} (id={ch.id})")

        # 1.5. Шаблоны промптов из YAML (идемпотентно) → INSERT в prompt_templates (БД)
        prompts = get_prompts()

        result_tpl = await session.execute(
            select(PromptTemplate).where(PromptTemplate.name == "default")
        )
        default_template = result_tpl.scalar_one_or_none()
        if default_template is None:
            gen = prompts.get("generator", {})
            crit = prompts.get("critic", {})
            default_template = PromptTemplate(
                name="default",
                generator_system=gen.get("system", ""),
                generator_user_template=gen.get("user_template", ""),
                critic_system=crit.get("system", ""),
                critic_user_template=crit.get("user_template", ""),
                created_at=datetime.now(timezone.utc),
            )
            session.add(default_template)
            await session.flush()
            print("Создан шаблон промптов: default")
        else:
            gen = prompts.get("generator", {})
            crit = prompts.get("critic", {})
            default_template.generator_system = gen.get("system", "")
            default_template.generator_user_template = gen.get("user_template", "")
            default_template.critic_system = crit.get("system", "")
            default_template.critic_user_template = crit.get("user_template", "")
            print("Обновлён шаблон промптов: default")

        result_aesthetic = await session.execute(
            select(PromptTemplate).where(PromptTemplate.name == "aesthetic")
        )
        aesthetic_template = result_aesthetic.scalar_one_or_none()
        if aesthetic_template is None:
            aesthetic_data = prompts.get("aesthetic", {})
            gen = aesthetic_data.get("generator", {})
            crit = aesthetic_data.get("critic", {})
            aesthetic_template = PromptTemplate(
                name="aesthetic",
                generator_system=gen.get("system", ""),
                generator_user_template=gen.get("user_template", ""),
                critic_system=crit.get("system", ""),
                critic_user_template=crit.get("user_template", ""),
                created_at=datetime.now(timezone.utc),
            )
            session.add(aesthetic_template)
            await session.flush()
            print("Создан шаблон промптов: aesthetic")
        else:
            aesthetic_data = prompts.get("aesthetic", {})
            gen = aesthetic_data.get("generator", {})
            crit = aesthetic_data.get("critic", {})
            aesthetic_template.generator_system = gen.get("system", "")
            aesthetic_template.generator_user_template = gen.get("user_template", "")
            aesthetic_template.critic_system = crit.get("system", "")
            aesthetic_template.critic_user_template = crit.get("user_template", "")
            print("Обновлён шаблон промптов: aesthetic")

        # Привязка шаблона к каналу: channels.prompt_template_id -> prompt_templates.id
        # llm_pipeline при генерации загружает channel с selectinload(prompt_template)
        # и берёт промпты из channel.prompt_template (БД)
        for ch in channels_created:
            if ch.name == "Канал 2":
                ch.prompt_template_id = aesthetic_template.id
            else:
                ch.prompt_template_id = default_template.id
        print("Шаблоны привязаны: ЭТО ЗНАК -> default, Канал 2 -> aesthetic")

        await session.commit()
        # Перезагружаем сессию для дальнейших операций
        async with async_session_factory() as session2:
            # 2. Добавляем по 5 постов на каждый канал
            now = datetime.now(MSK)
            for i, ch in enumerate(channels_created):
                result = await session2.execute(
                    select(Post).where(Post.channel_id == ch.id).limit(1)
                )
                if result.scalar_one_or_none():
                    print(f"Посты для канала {ch.name} уже есть, пропускаем")
                    continue

                for j, text in enumerate(POST_TEXTS):
                    scheduled_at = now + timedelta(minutes=j + 1)
                    post = Post(
                        channel_id=ch.id,
                        text=text,
                        scheduled_at=scheduled_at,
                        status=PostStatus.scheduled,
                    )
                    session2.add(post)
                print(f"Добавлено 5 постов для канала {ch.name} (scheduled_at в ближайшие минуты)")

            # 3. Парсим messages4.html и вставляем 5 фраз в датасет первого канала
            html_path = Path(__file__).resolve().parent.parent / "references" / "eto znak" / "messages4.html"
            if not html_path.exists():
                print(f"Файл не найден: {html_path}")
            else:
                all_phrases = _parse_phrases_from_html(html_path)
                selected = _pick_motivational_phrases(all_phrases, 5)
                if len(selected) < 5:
                    # Fallback: берём любые 5
                    selected = all_phrases[:5]

                first_channel = channels_created[0]
                result = await session2.execute(
                    select(Dataset).where(Dataset.channel_id == first_channel.id).limit(1)
                )
                if result.scalar_one_or_none():
                    print(f"Датасет для канала {first_channel.name} уже есть, пропускаем")
                else:
                    for text in selected:
                        ds = Dataset(channel_id=first_channel.id, text=text)
                        session2.add(ds)
                    print(f"Добавлено {len(selected)} фраз в датасет канала {first_channel.name}")

            await session2.commit()
            print("Сидирование завершено.")


if __name__ == "__main__":
    asyncio.run(main())



================================================
FILE: scripts/seed_channel.py
================================================
#!/usr/bin/env python3
"""
Скрипт для добавления тестового канала в БД.
Запуск: uv run python scripts/seed_channel.py
"""

import asyncio
import os
import sys

# Добавляем корень проекта в path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import select

from backend.db.models import Channel
from backend.db.session import async_session_factory


async def main() -> None:
    async with async_session_factory() as session:
        result = await session.execute(select(Channel).limit(1))
        existing = result.scalar_one_or_none()
        if existing:
            print(f"Канал уже есть: {existing.name} (id={existing.id})")
            return

        channel = Channel(
            telegram_id="-1001234567890",
            name="Тестовый канал",
        )
        session.add(channel)
        await session.commit()
        print(f"Добавлен канал: {channel.name} (id={channel.id})")


if __name__ == "__main__":
    asyncio.run(main())


