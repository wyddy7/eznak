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
