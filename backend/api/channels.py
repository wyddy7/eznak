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
