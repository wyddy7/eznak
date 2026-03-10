"""APScheduler для автопостинга одобренных постов в Telegram."""

import asyncio
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import aiohttp
import structlog
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

from backend.core.config import BOT_TOKEN, TARGET_CHANNEL_ID
from backend.db.models import Post, PostStatus
from backend.db.session import async_session_factory

log = structlog.get_logger(__name__)
MSK = ZoneInfo("Europe/Moscow")

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

TELEGRAM_API = "https://api.telegram.org"


async def _publish_scheduled_posts() -> None:
    """
    Job: раз в минуту ищем посты со status=scheduled и scheduled_at <= now (UTC).
    Отправляем в Telegram, при успехе — status=posted.
    """
    if not BOT_TOKEN or not TARGET_CHANNEL_ID:
        log.warning("scheduler.skip", reason="BOT_TOKEN или TARGET_CHANNEL_ID не заданы")
        return

    now_utc = datetime.now(timezone.utc)

    async with async_session_factory() as session:
        try:
            result = await session.execute(
                select(Post)
                .where(Post.status == PostStatus.scheduled)
                .where(Post.scheduled_at <= now_utc)
                .order_by(Post.scheduled_at.asc())
            )
            posts = result.scalars().all()
        except Exception as e:
            log.error("scheduler.db_error", error=str(e), exc_info=True)
            return

        if not posts:
            return

        url = f"{TELEGRAM_API}/bot{BOT_TOKEN}/sendMessage"

        async with aiohttp.ClientSession() as http:
            for post in posts:
                try:
                    async with http.post(
                        url,
                        json={"chat_id": TARGET_CHANNEL_ID, "text": post.text},
                    ) as resp:
                        data = await resp.json()

                        if resp.status != 200 or not data.get("ok"):
                            desc = data.get("description", "unknown")
                            log.error(
                                "scheduler.telegram_error",
                                post_id=str(post.id),
                                status=resp.status,
                                description=desc,
                            )
                            continue

                    post.status = PostStatus.posted
                    await session.commit()

                    scheduled_msk = (
                        post.scheduled_at.astimezone(MSK).isoformat()
                        if post.scheduled_at
                        else None
                    )
                    text_preview = post.text[:100] + "..." if len(post.text) > 100 else post.text
                    log.info(
                        "post_published",
                        post_id=str(post.id),
                        text=text_preview,
                        scheduled_at_msk=scheduled_msk,
                    )

                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    log.error(
                        "scheduler.telegram_request_error",
                        post_id=str(post.id),
                        error=str(e),
                        exc_info=True,
                    )
                except Exception as e:
                    log.error(
                        "scheduler.unexpected_error",
                        post_id=str(post.id),
                        error=str(e),
                        exc_info=True,
                    )
                    await session.rollback()


def setup_scheduler() -> None:
    """Добавляет job публикации постов (раз в минуту)."""
    scheduler.add_job(
        _publish_scheduled_posts,
        "interval",
        minutes=1,
        id="publish_scheduled_posts",
    )
