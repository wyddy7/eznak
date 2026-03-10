"""Роутер генерации фраз через LLM."""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps import get_api_key
from backend.db.models import Channel
from backend.db.session import get_session
from backend.services.llm_pipeline import run_llm_pipeline

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
    result = await session.execute(select(Channel).limit(1))
    channel = result.scalar_one_or_none()
    if not channel:
        return {"phrases": []}

    channel_id: UUID = channel.id
    ranked = await run_llm_pipeline(channel_id=channel_id)
    phrases = [p.text for p in ranked]
    return {"phrases": phrases}
