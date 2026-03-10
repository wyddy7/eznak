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
