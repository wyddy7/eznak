"""Роутер каналов: datasets bulk insert."""

from uuid import UUID

import structlog
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps import get_api_key
from backend.db.models import Channel, Dataset
from backend.db.session import get_session

log = structlog.get_logger(__name__)
router = APIRouter(prefix="/channels", tags=["channels"])


class BulkDatasetsRequest(BaseModel):
    phrases: list[str] = Field(..., min_length=1, description="Фразы для эталонного датасета")


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
