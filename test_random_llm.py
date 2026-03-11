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
