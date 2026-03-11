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
            print("Шаблон default уже есть")

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
            print("Шаблон aesthetic уже есть")

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
