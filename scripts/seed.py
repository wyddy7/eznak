#!/usr/bin/env python3
"""
Скрипт сидирования: 2 канала, по 5 постов на каждый, 5 фраз в датасете из messages4.html.
Запуск: uv run python scripts/seed.py
"""

import asyncio
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import select
from zoneinfo import ZoneInfo

from backend.db.models import Channel, Dataset, Post, PostStatus
from backend.db.session import async_session_factory

MSK = ZoneInfo("Europe/Moscow")

CHANNELS = [
    {"telegram_id": "-1003812297034", "name": "Канал 1"},
    {"telegram_id": "-1003592368865", "name": "Канал 2"},
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
            if existing:
                print(f"Канал уже есть: {existing.name} (telegram_id={existing.telegram_id})")
                channels_created.append(existing)
            else:
                ch = Channel(
                    telegram_id=ch_data["telegram_id"],
                    name=ch_data["name"],
                )
                session.add(ch)
                await session.flush()
                channels_created.append(ch)
                print(f"Добавлен канал: {ch.name} (id={ch.id})")

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
