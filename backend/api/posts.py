"""Роутер постов: approve и schedule-batch."""

from datetime import datetime, timedelta
from uuid import UUID

import structlog
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from zoneinfo import ZoneInfo

from backend.api.deps import get_api_key
from backend.db.models import Channel, Post, PostStatus
from backend.db.session import get_session

log = structlog.get_logger(__name__)
router = APIRouter(prefix="/posts", tags=["posts"])

MSK = ZoneInfo("Europe/Moscow")

# Слоты по МСК для suggested_time (часы дня)
DEFAULT_SLOT_HOURS = [9, 12, 15, 18, 21]


def _generate_suggested_times(count: int) -> list[datetime]:
    """Генерирует слоты времени по МСК на ближайшие дни."""
    now = datetime.now(MSK)
    # Начинаем с завтрашнего дня, чтобы было время на планирование
    start = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    slots: list[datetime] = []
    day_offset = 0
    hour_idx = 0
    while len(slots) < count:
        day = start + timedelta(days=day_offset)
        hour = DEFAULT_SLOT_HOURS[hour_idx % len(DEFAULT_SLOT_HOURS)]
        slot = day.replace(hour=hour, minute=0, second=0, microsecond=0)
        slots.append(slot)
        hour_idx += 1
        if hour_idx % len(DEFAULT_SLOT_HOURS) == 0:
            day_offset += 1
    return slots[:count]


# --- Schemas ---

class ApproveRequest(BaseModel):
    phrases: list[str] = Field(..., min_length=1, description="Финальные тексты постов")


class DraftPostResponse(BaseModel):
    id: UUID
    text: str
    channel_id: UUID
    suggested_time: str  # ISO8601 с таймзоной

    class Config:
        from_attributes = True


class ScheduleItem(BaseModel):
    post_id: UUID
    channel_id: UUID
    time: str  # ISO8601


# --- Endpoints ---

@router.get("")
async def list_posts(
    status: PostStatus | None = Query(None, description="Фильтр по статусу"),
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Список постов. Для бота: status=scheduled — ожидающие постинга.
    """
    log.info("api.posts.list", status=status.value if status else "all")
    q = select(Post).order_by(Post.scheduled_at.asc())
    if status is not None:
        q = q.where(Post.status == status)
    result = await session.execute(q)
    posts = result.scalars().all()
    log.info("api.posts.list.result", count=len(posts))
    return {
        "posts": [
            {
                "id": str(p.id),
                "text": p.text[:100] + "..." if len(p.text) > 100 else p.text,
                "scheduled_at": p.scheduled_at.isoformat() if p.scheduled_at else None,
                "status": p.status.value,
            }
            for p in posts
        ]
    }


@router.post("/approve")
async def approve_posts(
    body: ApproveRequest,
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Создаёт записи в БД со статусом draft.
    Возвращает draft_posts с id, text, channel_id, suggested_time.
    """
    log.info("api.posts.approve", phrases_count=len(body.phrases))
    result = await session.execute(select(Channel).limit(1))
    channel = result.scalar_one_or_none()
    if not channel:
        log.warning("api.posts.approve.no_channel", reason="Таблица channels пуста")
        return {"draft_posts": []}

    channel_id = channel.id
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
            "suggested_time": slot.isoformat(),
        })

    log.info("api.posts.approve.success", draft_count=len(draft_posts))
    return {"draft_posts": draft_posts}


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
