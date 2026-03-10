"""Роутер генерации фраз через LLM."""

from uuid import UUID

import structlog
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps import get_api_key
from backend.db.models import Channel
from backend.db.session import get_session
from backend.services.llm_pipeline import run_llm_pipeline

log = structlog.get_logger(__name__)
router = APIRouter(prefix="/generate", tags=["generation"])


@router.post("")
async def generate_phrases(
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Генерирует фразы через LLM-пайплайн.
    Для MVP: channel_id — первый канал из БД.
    """
    log.info("api.generate.request")
    structlog.get_logger(__name__).info("Hit generate endpoint!")
    result = await session.execute(select(Channel).limit(1))
    channel = result.scalar_one_or_none()
    if not channel:
        log.warning("api.generate.no_channel", reason="Таблица channels пуста. Добавь канал в БД.")
        return {"status": "ok", "test_marker": "123", "phrases": []}

    channel_id: UUID = channel.id
    log.info("api.generate.channel_found", channel_id=str(channel_id), channel_name=channel.name)
    try:
        ranked = await run_llm_pipeline(channel_id=channel_id)
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
        return {"status": "ok", "test_marker": "123", "phrases": []}

    log.info("api.generate.success", channel_id=str(channel_id), count=len(phrases))
    return {"status": "ok", "test_marker": "123", "phrases": phrases}
