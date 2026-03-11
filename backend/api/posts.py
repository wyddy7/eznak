"""Роутер постов: approve, schedule-batch, post-now."""

import random
from datetime import datetime, timedelta
from uuid import UUID

import aiohttp
import structlog
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from zoneinfo import ZoneInfo

from backend.api.deps import get_api_key
from backend.core.config import BOT_TOKEN
from backend.core.config_loader import get_media
from backend.db.models import Channel, Post, PostStatus
from backend.db.session import get_session

log = structlog.get_logger(__name__)
router = APIRouter(prefix="/posts", tags=["posts"])

MSK = ZoneInfo("Europe/Moscow")

# Слоты по МСК для suggested_time (часы дня)
DEFAULT_SLOT_HOURS = [9, 12, 15, 18, 21]
MAX_POSTS_PER_DAY = 2


def _generate_suggested_times(count: int) -> list[datetime]:
    """Генерирует слоты времени по МСК. Не более MAX_POSTS_PER_DAY постов в день."""
    now = datetime.now(MSK)
    start = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    hours_to_use = DEFAULT_SLOT_HOURS[:MAX_POSTS_PER_DAY]
    slots: list[datetime] = []
    for i in range(count):
        day_offset = i // MAX_POSTS_PER_DAY
        hour_idx = i % MAX_POSTS_PER_DAY
        day = start + timedelta(days=day_offset)
        hour = hours_to_use[hour_idx]
        slot = day.replace(hour=hour, minute=0, second=0, microsecond=0)
        slots.append(slot)
    return slots


# --- Schemas ---

class ApproveRequest(BaseModel):
    channel_id: UUID = Field(..., description="UUID канала")
    phrases: list[str] = Field(..., min_length=1, description="Финальные тексты постов")


class DraftPostResponse(BaseModel):
    id: UUID
    text: str
    channel_id: UUID
    channel_name: str
    suggested_time: str  # ISO8601 с таймзоной

    class Config:
        from_attributes = True


class ScheduleItem(BaseModel):
    post_id: UUID
    channel_id: UUID
    time: str  # ISO8601


class PostNowRequest(BaseModel):
    post_id: UUID = Field(..., description="UUID поста для немедленной публикации")


class ApproveOneRequest(BaseModel):
    channel_id: UUID = Field(..., description="UUID канала")
    text: str = Field(..., min_length=1, description="Текст поста")


class PatchPostRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Новый текст поста")


TELEGRAM_API = "https://api.telegram.org"


# --- Endpoints ---

@router.get("")
async def list_posts(
    status: PostStatus | None = Query(None, description="Фильтр по статусу"),
    channel_id: UUID | None = Query(None, description="Фильтр по каналу"),
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Список постов. Для бота: status=scheduled — ожидающие постинга, status=draft — черновики.
    """
    log.info("api.posts.list", status=status.value if status else "all", channel_id=str(channel_id) if channel_id else None)
    q = select(Post).options(selectinload(Post.channel))
    if status == PostStatus.draft:
        q = q.order_by(Post.created_at.asc())
    else:
        q = q.order_by(Post.scheduled_at.asc())
    if status is not None:
        q = q.where(Post.status == status)
    if channel_id is not None:
        q = q.where(Post.channel_id == channel_id)
    result = await session.execute(q)
    posts = result.scalars().all()
    log.info("api.posts.list.result", count=len(posts))
    full_text = status == PostStatus.scheduled or status == PostStatus.draft
    suggested_times = _generate_suggested_times(len(posts)) if status == PostStatus.draft and posts else []
    return {
        "posts": [
            {
                "id": str(p.id),
                "text": p.text if full_text else (p.text[:100] + "..." if len(p.text) > 100 else p.text),
                "channel_id": str(p.channel_id),
                "channel_name": p.channel.name if p.channel else None,
                "scheduled_at": p.scheduled_at.isoformat() if p.scheduled_at else None,
                "status": p.status.value,
                **({"suggested_time": suggested_times[i].isoformat()} if status == PostStatus.draft and i < len(suggested_times) else {}),
            }
            for i, p in enumerate(posts)
        ]
    }


@router.post("/{post_id}/cancel")
async def cancel_post(
    post_id: UUID,
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Отмена поста из расписания. Переводит status в draft, scheduled_at в None.
    """
    log.info("api.posts.cancel", post_id=str(post_id))
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    if post.status != PostStatus.scheduled:
        raise HTTPException(status_code=400, detail="Можно отменить только пост со статусом scheduled")
    post.status = PostStatus.draft
    post.scheduled_at = None
    await session.commit()
    log.info("api.posts.cancel.success", post_id=str(post_id))
    return {"status": "cancelled", "post_id": str(post_id)}


@router.post("/approve")
async def approve_posts(
    body: ApproveRequest,
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Создаёт посты для указанного канала со статусом draft.
    Возвращает draft_posts с id, text, channel_id, channel_name, suggested_time.
    """
    log.info("api.posts.approve", channel_id=str(body.channel_id), phrases_count=len(body.phrases))
    result = await session.execute(select(Channel).where(Channel.id == body.channel_id))
    channel = result.scalar_one_or_none()
    if not channel:
        raise HTTPException(status_code=404, detail="Канал не найден")

    channel_id = channel.id
    channel_name = channel.name
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
            "channel_name": channel_name,
            "suggested_time": slot.isoformat(),
        })

    log.info("api.posts.approve.success", draft_count=len(draft_posts))
    return {"draft_posts": draft_posts}


@router.post("/approve-one")
async def approve_one(
    body: ApproveOneRequest,
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Создаёт один пост со статусом draft.
    Возвращает id, text, channel_id, channel_name.
    """
    log.info("api.posts.approve_one", channel_id=str(body.channel_id))
    result = await session.execute(select(Channel).where(Channel.id == body.channel_id))
    channel = result.scalar_one_or_none()
    if not channel:
        raise HTTPException(status_code=404, detail="Канал не найден")
    post = Post(
        channel_id=channel.id,
        text=body.text,
        status=PostStatus.draft,
        scheduled_at=None,
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    log.info("api.posts.approve_one.success", post_id=str(post.id))
    return {
        "id": str(post.id),
        "text": post.text,
        "channel_id": str(post.channel_id),
        "channel_name": channel.name,
    }


@router.patch("/{post_id}")
async def patch_post(
    post_id: UUID,
    body: PatchPostRequest,
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Обновляет текст поста. Только для status=draft.
    """
    log.info("api.posts.patch", post_id=str(post_id))
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    if post.status != PostStatus.draft:
        raise HTTPException(status_code=400, detail="Можно редактировать только черновик")
    post.text = body.text
    await session.commit()
    log.info("api.posts.patch.success", post_id=str(post_id))
    return {"id": str(post.id), "text": post.text}


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


@router.post("/post-now")
async def post_now(
    body: PostNowRequest,
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Немедленная публикация поста в канал.
    Находит пост, достаёт post.channel.telegram_id, отправляет туда
    (sendMessage или sendPhoto с вероятностью из config/media.yaml, 0.3).
    Меняет статус на posted.
    """
    log.info("api.posts.post_now", post_id=str(body.post_id))
    result = await session.execute(
        select(Post).options(selectinload(Post.channel)).where(Post.id == body.post_id)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    if not post.channel:
        raise HTTPException(status_code=500, detail="Канал поста не найден")

    if not BOT_TOKEN:
        raise HTTPException(status_code=503, detail="BOT_TOKEN не задан")

    target_channel_id = post.channel.telegram_id
    channel_name = post.channel.name

    image_prob = get_media().get("image_probability", 0.3)
    use_media = random.random() <= image_prob
    photo_bytes = None

    if use_media:
        try:
            from backend.services.media_gen import generate_post_image

            photo_bytes = generate_post_image(post.text)
        except Exception as e:
            log.warning("api.posts.post_now.media_gen_failed", post_id=str(post.id), error=str(e))
            use_media = False

    async with aiohttp.ClientSession() as http:
        if use_media and photo_bytes:
            url = f"{TELEGRAM_API}/bot{BOT_TOKEN}/sendPhoto"
            form = aiohttp.FormData()
            form.add_field("chat_id", target_channel_id)
            form.add_field("photo", photo_bytes, filename="post.jpg", content_type="image/jpeg")
            async with http.post(url, data=form) as resp:
                data = await resp.json()
                status_code = resp.status
        else:
            url = f"{TELEGRAM_API}/bot{BOT_TOKEN}/sendMessage"
            async with http.post(url, json={"chat_id": target_channel_id, "text": post.text}) as resp:
                data = await resp.json()
                status_code = resp.status

    if status_code != 200 or not data.get("ok"):
        desc = data.get("description", "unknown")
        log.error("api.posts.post_now.telegram_error", post_id=str(post.id), description=desc)
        raise HTTPException(status_code=502, detail=f"Telegram API: {desc}")

    post.status = PostStatus.posted
    await session.commit()

    log.info(
        "api.posts.post_now.success",
        post_id=str(post.id),
        channel_name=channel_name,
        has_media=use_media,
    )
    return {
        "status": "posted",
        "post_id": str(post.id),
        "channel_id": str(post.channel_id),
        "channel_name": channel_name,
        "has_media": use_media,
    }
