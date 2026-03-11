"""
Telegram-бот для генерации и модерации постов.
Шаг 6: Ручной ввод времени (FSM).
"""

import html
import os
import random
import re
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from dotenv import load_dotenv


class EditPhraseStates(StatesGroup):
    waiting_for_text = State()


class ManualTimeStates(StatesGroup):
    waiting_for_time = State()


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")
BACKEND_API_KEY = os.getenv("BACKEND_API_KEY", "")

# Список Telegram ID админов (через запятую)
_ADMIN_IDS: set[int] = set()
_raw = os.getenv("ADMIN_TELEGRAM_IDS", "")
if _raw:
    for s in _raw.split(","):
        s = s.strip()
        if s.isdigit():
            _ADMIN_IDS.add(int(s))


def _is_admin(user_id: int) -> bool:
    return user_id in _ADMIN_IDS


# --- Reply-меню ---
def get_main_keyboard() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    builder.button(text="🎲 Сгенерировать")
    builder.button(text="📅 Ожидают постинга")
    builder.button(text="📤 Отправить на планирование")
    builder.adjust(2, 1)
    return builder


# --- Inline-кнопки для фразы ---
def get_phrase_keyboard(phrase_idx: int) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Approve", callback_data=f"approve:{phrase_idx}")
    builder.button(text="❌ Reject", callback_data=f"reject:{phrase_idx}")
    builder.button(text="✏️ Edit", callback_data=f"edit:{phrase_idx}")
    builder.adjust(3)
    return builder


def _append_status(text: str, status: str) -> str:
    """Добавляет строку статуса к тексту сообщения."""
    return f"{text}\n\n{status}"


def _update_message_status(msg: Message, new_status: str) -> str:
    """
    Возвращает обновлённый текст: если уже есть «Статус:», заменяет последний.
    Иначе добавляет.
    """
    text = msg.text or msg.caption or ""
    if "Статус:" in text:
        parts = text.rsplit("\n\n", 1)
        if len(parts) == 2 and "Статус:" in parts[1]:
            return f"{parts[0]}\n\n{new_status}"
    return _append_status(text, new_status)


def _has_phrase_number_in_text(text: str) -> bool:
    """Проверяет, содержит ли текст «Фраза N» — может привести к мусору в канале."""
    return bool(re.search(r"Фраза\s*\d+", text, re.IGNORECASE))


PHRASE_WARNING = "\n\n⚠️ <b>Обнаружено «Фраза N» в тексте</b> — возможна ошибка выкладывания, в канал может попасть мусор!"


def _parse_phrase_text(msg: Message) -> str:
    """Извлекает сырой текст из формата «Фраза N:\n{text}» или с суффиксом «Статус:»."""
    text = msg.text or msg.caption or ""
    if "\n" not in text:
        return text.strip()
    after_prefix = text.split("\n", 1)[1]
    if "\n\n" in after_prefix:
        result = after_prefix.split("\n\n", 1)[0].strip()
    else:
        result = after_prefix.strip()
    # Убираем префикс «Фраза N:» если остался (для первой фразы с «Канал: X\n\nФраза 1:\n...»)
    result = re.sub(r"^Фраза\s*\d+\s*:?\s*", "", result).strip()
    # Извлекаем текст из <pre>...</pre> (моноширинный формат)
    pre_match = re.search(r"<pre>(.*?)</pre>", result, re.DOTALL)
    if pre_match:
        result = html.unescape(pre_match.group(1).strip())
    return result


async def _get_channels() -> dict[str, Any]:
    """GET /api/v1/channels — возвращает {"channels": [{"id", "name", "telegram_id"}, ...]}."""
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{BACKEND_URL}/api/v1/channels",
            headers={"X-API-Key": BACKEND_API_KEY},
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"API error {resp.status}: {text}")
            return await resp.json()


async def _post_generate(channel_id: str) -> dict[str, Any]:
    """POST /api/v1/generate — возвращает {"phrases": [...], "channel_name": ...}."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BACKEND_URL}/api/v1/generate",
            json={"channel_id": channel_id},
            headers={"X-API-Key": BACKEND_API_KEY, "Content-Type": "application/json"},
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"API error {resp.status}: {text}")
            return await resp.json()


async def _get_scheduled_posts() -> dict[str, Any]:
    """GET /api/v1/posts?status=scheduled."""
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{BACKEND_URL}/api/v1/posts",
            params={"status": "scheduled"},
            headers={"X-API-Key": BACKEND_API_KEY},
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"API error {resp.status}: {text}")
            return await resp.json()


async def _post_approve(channel_id: str, phrases: list[str]) -> dict[str, Any]:
    """POST /api/v1/posts/approve — возвращает draft_posts."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BACKEND_URL}/api/v1/posts/approve",
            json={"channel_id": channel_id, "phrases": phrases},
            headers={"X-API-Key": BACKEND_API_KEY, "Content-Type": "application/json"},
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"API error {resp.status}: {text}")
            return await resp.json()


async def _post_approve_one(channel_id: str, text: str) -> dict[str, Any]:
    """POST /api/v1/posts/approve-one — создаёт один draft-пост."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BACKEND_URL}/api/v1/posts/approve-one",
            json={"channel_id": channel_id, "text": text},
            headers={"X-API-Key": BACKEND_API_KEY, "Content-Type": "application/json"},
        ) as resp:
            if resp.status != 200:
                text_err = await resp.text()
                raise RuntimeError(f"API error {resp.status}: {text_err}")
            return await resp.json()


async def _patch_post(post_id: str, text: str) -> dict[str, Any]:
    """PATCH /api/v1/posts/{post_id} — обновляет текст draft-поста."""
    async with aiohttp.ClientSession() as session:
        async with session.patch(
            f"{BACKEND_URL}/api/v1/posts/{post_id}",
            json={"text": text},
            headers={"X-API-Key": BACKEND_API_KEY, "Content-Type": "application/json"},
        ) as resp:
            if resp.status != 200:
                text_err = await resp.text()
                raise RuntimeError(f"API error {resp.status}: {text_err}")
            return await resp.json()


async def _get_draft_posts(channel_id: str | None = None) -> dict[str, Any]:
    """GET /api/v1/posts?status=draft — черновики, опционально по каналу."""
    params: dict[str, str] = {"status": "draft"}
    if channel_id:
        params["channel_id"] = channel_id
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{BACKEND_URL}/api/v1/posts",
            params=params,
            headers={"X-API-Key": BACKEND_API_KEY},
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"API error {resp.status}: {text}")
            return await resp.json()


async def _post_post_now(post_id: str) -> dict[str, Any]:
    """POST /api/v1/posts/post-now — публикует пост немедленно."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BACKEND_URL}/api/v1/posts/post-now",
            json={"post_id": post_id},
            headers={"X-API-Key": BACKEND_API_KEY, "Content-Type": "application/json"},
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"API error {resp.status}: {text}")
            return await resp.json()


async def _post_cancel_post(post_id: str) -> dict[str, Any]:
    """POST /api/v1/posts/{post_id}/cancel — отмена поста из расписания."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BACKEND_URL}/api/v1/posts/{post_id}/cancel",
            headers={"X-API-Key": BACKEND_API_KEY},
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"API error {resp.status}: {text}")
            return await resp.json()


async def _post_schedule_batch(items: list[dict[str, Any]]) -> dict[str, Any]:
    """POST /api/v1/posts/schedule-batch."""
    payload = [
        {"post_id": str(it["id"]), "channel_id": str(it["channel_id"]), "time": it["suggested_time"]}
        for it in items
    ]
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BACKEND_URL}/api/v1/posts/schedule-batch",
            json=payload,
            headers={"X-API-Key": BACKEND_API_KEY, "Content-Type": "application/json"},
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"API error {resp.status}: {text}")
            return await resp.json()


def _format_time_display(iso_time: str) -> str:
    """Преобразует ISO8601 в читаемый формат ДД.ММ.ГГГГ ЧЧ:ММ."""
    if not iso_time or iso_time == "—":
        return "—"
    try:
        dt = datetime.fromisoformat(iso_time.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%Y %H:%M")
    except (ValueError, TypeError):
        return iso_time


MAX_MESSAGE_LEN = 3800  # запас под заголовок и HTML
PER_PAGE = 5


def _format_slots_message(
    draft_posts: list[dict[str, Any]],
    channel_name: str | None = None,
    page: int = 0,
    per_page: int = 5,
) -> tuple[str, int]:
    """Форматирует слоты для отображения. Возвращает (text, total_pages)."""
    total_pages = max(1, (len(draft_posts) + per_page - 1) // per_page)
    page = max(0, min(page, total_pages - 1))
    start = page * per_page
    end = min(start + per_page, len(draft_posts))
    page_posts = draft_posts[start:end]

    header = f"<b>Канал:</b> {channel_name}\n\n" if channel_name else ""
    lines = []
    for i, p in enumerate(page_posts, start=start + 1):
        text = p.get("text", "")
        at = _format_time_display(p.get("suggested_time", "—"))
        lines.append(f"• {text}\n  📅 {at} (МСК)")
    body = "\n\n".join(lines)
    result = header + body
    if total_pages > 1:
        result += f"\n\nСтраница {page + 1} из {total_pages}"
    return result, total_pages


MSK = ZoneInfo("Europe/Moscow")


def _parse_manual_time(text: str) -> str | None:
    """
    Парсит время в формате ДД.ММ.ГГГГ ЧЧ:ММ (МСК).
    Возвращает ISO8601 строку или None при ошибке.
    """
    text = (text or "").strip()
    if not text:
        return None
    try:
        dt = datetime.strptime(text, "%d.%m.%Y %H:%M")
        dt = dt.replace(tzinfo=MSK)
        return dt.isoformat()
    except ValueError:
        return None


def _get_slots_keyboard(
    draft_posts: list[dict[str, Any]],
    page: int = 0,
    per_page: int = 5,
    show_back_channel: bool = False,
) -> InlineKeyboardBuilder:
    """Inline-кнопки: Post Now, Manual Time, Confirm под постами страницы, Shuffle, Confirm All, пагинация, «← Другой канал»."""
    builder = InlineKeyboardBuilder()
    total_pages = max(1, (len(draft_posts) + per_page - 1) // per_page)
    page = max(0, min(page, total_pages - 1))
    start = page * per_page
    end = min(start + per_page, len(draft_posts))
    page_posts = draft_posts[start:end]

    for i, p in enumerate(page_posts, start=start + 1):
        post_id = str(p.get("id", ""))
        builder.button(text=f"🚀 Post Now ({i})", callback_data=f"post_now:{post_id}")
        builder.button(text="⏰ Задать время вручную", callback_data=f"manual_time:{post_id}")
        builder.button(text="✅", callback_data=f"slots_confirm_one:{post_id}")

    if total_pages > 1:
        if page > 0:
            builder.button(text="◀", callback_data=f"slots_page:{page - 1}")
        if page < total_pages - 1:
            builder.button(text="▶", callback_data=f"slots_page:{page + 1}")

    builder.button(text="🔀 Shuffle", callback_data="slots:shuffle")
    builder.button(text="✅ Confirm All", callback_data="slots:confirm")
    if show_back_channel:
        builder.button(text="← Другой канал", callback_data="planning_back")
    builder.adjust(3)  # 3 кнопки на пост
    return builder


def _get_channels_with_scheduled(posts: list[dict[str, Any]]) -> list[tuple[str, str, int]]:
    """Каналы с запланированными постами: (channel_id, channel_name, count)."""
    from collections import defaultdict

    by_channel: dict[str, tuple[str, int]] = {}  # channel_id -> (channel_name, count)
    for p in posts:
        cid = str(p.get("channel_id", ""))
        cname = p.get("channel_name") or "Без канала"
        if cid not in by_channel:
            by_channel[cid] = (cname, 0)
        by_channel[cid] = (cname, by_channel[cid][1] + 1)
    return [(cid, cname, cnt) for cid, (cname, cnt) in sorted(by_channel.items(), key=lambda x: x[1][0])]


def _filter_posts_by_channel(posts: list[dict[str, Any]], channel_id: str) -> list[dict[str, Any]]:
    """Фильтрует посты по channel_id, сортирует по scheduled_at."""
    filtered = [p for p in posts if str(p.get("channel_id")) == channel_id]
    return sorted(filtered, key=lambda p: p.get("scheduled_at") or "")


def _format_scheduled_channel_posts(
    ordered_posts: list[dict[str, Any]],
    page: int = 0,
    per_page: int = 5,
) -> tuple[str, int]:
    """Форматирует посты канала с нумерацией. Возвращает (text, total_pages)."""
    total_pages = max(1, (len(ordered_posts) + per_page - 1) // per_page)
    page = max(0, min(page, total_pages - 1))
    start = page * per_page
    end = min(start + per_page, len(ordered_posts))
    page_posts = ordered_posts[start:end]

    lines = []
    for i, p in enumerate(page_posts, start=start + 1):
        text = p.get("text", "")
        at = _format_time_display(p.get("scheduled_at", "—"))
        lines.append(f"<b>{i}.</b> {text}\n  📅 {at}")
    result = "\n\n".join(lines)
    if total_pages > 1:
        result += f"\n\nСтраница {page + 1} из {total_pages}"
    return result, total_pages


def _get_scheduled_channel_keyboard(
    ordered_posts: list[dict[str, Any]],
    page: int = 0,
    per_page: int = 5,
) -> InlineKeyboardBuilder:
    """Кнопки отмены для постов страницы + пагинация + «← Другой канал»."""
    builder = InlineKeyboardBuilder()
    total_pages = max(1, (len(ordered_posts) + per_page - 1) // per_page)
    page = max(0, min(page, total_pages - 1))
    start = page * per_page
    end = min(start + per_page, len(ordered_posts))
    page_posts = ordered_posts[start:end]

    for i, p in enumerate(page_posts, start=start + 1):
        post_id = str(p.get("id", ""))
        builder.button(text=f"🗑️ Отменить ({i})", callback_data=f"cancel_scheduled:{post_id}")

    if total_pages > 1:
        if page > 0:
            builder.button(text="◀", callback_data=f"scheduled_page:{page - 1}")
        if page < total_pages - 1:
            builder.button(text="▶", callback_data=f"scheduled_page:{page + 1}")

    builder.button(text="← Другой канал", callback_data="scheduled_back")

    n_cancel = len(page_posts)
    n_pag = 2 if (page > 0 and page < total_pages - 1) else (1 if total_pages > 1 else 0)
    sizes = [1] * n_cancel + ([n_pag] if n_pag else []) + [1]
    builder.adjust(*sizes)
    return builder


def _get_scheduled_channels_keyboard(
    channels: list[tuple[str, str, int]],
) -> InlineKeyboardBuilder:
    """Кнопки выбора канала: «Канал 1 (3)» и т.д."""
    builder = InlineKeyboardBuilder()
    for cid, cname, cnt in channels:
        builder.button(
            text=f"{cname} ({cnt})",
            callback_data=f"scheduled_channel:{cid}",
        )
    builder.adjust(1)
    return builder


# --- Dispatcher и Middleware ---
dp = Dispatcher(storage=MemoryStorage())


@dp.update.outer_middleware()
async def admin_check(handler, event, data):
    """Проверяет ADMIN_TELEGRAM_IDS, игнорирует апдейты от остальных."""
    user = None
    msg = None
    if hasattr(event, "message") and event.message:
        user = event.message.from_user
        msg = event.message
    elif hasattr(event, "callback_query") and event.callback_query:
        user = event.callback_query.from_user
        msg = event.callback_query.message
    if user is None:
        return await handler(event, data)

    if not _is_admin(user.id):
        if msg:
            await msg.answer("Доступ запрещён. Ваш ID не в списке администраторов.")
        if hasattr(event, "callback_query") and event.callback_query:
            await event.callback_query.answer("Доступ запрещён.", show_alert=True)
        return
    return await handler(event, data)


# --- Handlers ---


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        await message.answer("Доступ запрещён. Ваш ID не в списке администраторов.")
        return
    await message.answer(
        "Привет! Используй кнопки ниже.",
        reply_markup=get_main_keyboard().as_markup(resize_keyboard=True),
    )


@dp.message(F.text == "🎲 Сгенерировать")
async def handle_generate(message: Message, state: FSMContext) -> None:
    if not _is_admin(message.from_user.id):
        return
    await state.clear()
    try:
        data = await _get_channels()
        channels = data.get("channels", [])
    except Exception as e:
        await message.answer(f"Ошибка API: {e}")
        return

    if not channels:
        await message.answer("Нет каналов. Добавь каналы в БД.")
        return

    builder = InlineKeyboardBuilder()
    for ch in channels:
        builder.button(text=ch.get("name", ch["id"]), callback_data=f"channel_select:{ch['id']}")
    builder.adjust(1)
    await message.answer("Выберите канал:", reply_markup=builder.as_markup())


@dp.callback_query(F.data.startswith("channel_select:"))
async def cb_channel_select(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    await callback.answer()  # Сразу — иначе "query is too old" при долгой генерации
    _, channel_id = callback.data.split(":", 1)
    await callback.message.edit_text("Генерирую фразы...")
    try:
        data = await _post_generate(channel_id)
        phrases = data.get("phrases", [])
        channel_name = data.get("channel_name", "")
        await state.update_data(channel_id=channel_id, channel_name=channel_name)
    except Exception as e:
        await callback.message.answer(f"Ошибка API: {e}")
        return

    if not phrases:
        await callback.message.answer("Фразы не сгенерированы. Проверь каналы в БД и LLM.")
        return

    await state.update_data(
        phrases={i: p for i, p in enumerate(phrases)},
        approved_indices=[],
        approved_post_ids={},
    )
    for i, phrase in enumerate(phrases):
        kb = get_phrase_keyboard(i)
        header = f"<b>Канал:</b> {channel_name}\n\n" if i == 0 else ""
        escaped = html.escape(phrase)
        body = f"{header}<b>Фраза {i + 1}:</b>\n<pre>{escaped}</pre>"
        if _has_phrase_number_in_text(phrase):
            body += PHRASE_WARNING
        await callback.message.answer(
            body,
            reply_markup=kb.as_markup(),
        )


@dp.message(F.text == "📅 Ожидают постинга")
async def handle_scheduled(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        return
    try:
        data = await _get_scheduled_posts()
        posts = data.get("posts", [])
    except Exception as e:
        await message.answer(f"Ошибка API: {e}")
        return

    if not posts:
        await message.answer("Нет постов, ожидающих постинга.")
        return

    channels = _get_channels_with_scheduled(posts)
    kb = _get_scheduled_channels_keyboard(channels)
    await message.answer("Выберите канал:", reply_markup=kb.as_markup())


@dp.callback_query(F.data.startswith("scheduled_channel:"))
async def cb_scheduled_channel_select(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    _, channel_id = callback.data.split(":", 1)
    await callback.answer()
    try:
        data = await _get_scheduled_posts()
        posts = data.get("posts", [])
    except Exception as e:
        await callback.message.edit_text(f"Ошибка API: {e}")
        return
    channel_posts = _filter_posts_by_channel(posts, channel_id)
    channel_name = channel_posts[0].get("channel_name", "Канал") if channel_posts else "Канал"
    await state.update_data(scheduled_channel_id=channel_id, scheduled_page=0)
    if not channel_posts:
        kb = InlineKeyboardBuilder()
        kb.button(text="← Другой канал", callback_data="scheduled_back")
        kb.adjust(1)
        await callback.message.edit_text(
            f"Нет постов для канала «{channel_name}».",
            reply_markup=kb.as_markup(),
        )
        return
    text, _ = _format_scheduled_channel_posts(channel_posts, page=0, per_page=PER_PAGE)
    kb = _get_scheduled_channel_keyboard(channel_posts, page=0, per_page=PER_PAGE)
    await callback.message.edit_text(
        f"<b>Ожидают постинга — {channel_name}:</b>\n\n{text}",
        reply_markup=kb.as_markup(),
    )


@dp.callback_query(F.data == "scheduled_back")
async def cb_scheduled_back(callback: CallbackQuery) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    await callback.answer()
    try:
        data = await _get_scheduled_posts()
        posts = data.get("posts", [])
    except Exception as e:
        await callback.message.edit_text(f"Ошибка API: {e}")
        return
    if not posts:
        await callback.message.edit_text("Нет постов, ожидающих постинга.", reply_markup=None)
        return
    channels = _get_channels_with_scheduled(posts)
    kb = _get_scheduled_channels_keyboard(channels)
    await callback.message.edit_text("Выберите канал:", reply_markup=kb.as_markup())


@dp.callback_query(F.data.startswith("scheduled_page:"))
async def cb_scheduled_page(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    _, page_str = callback.data.split(":", 1)
    page = int(page_str)
    await callback.answer()
    data = await state.get_data()
    channel_id = data.get("scheduled_channel_id")
    if not channel_id:
        return
    try:
        resp = await _get_scheduled_posts()
        posts = resp.get("posts", [])
    except Exception as e:
        await callback.message.edit_text(f"Ошибка API: {e}")
        return
    channel_posts = _filter_posts_by_channel(posts, channel_id)
    channel_name = channel_posts[0].get("channel_name", "Канал") if channel_posts else "Канал"
    if not channel_posts:
        kb = InlineKeyboardBuilder()
        kb.button(text="← Другой канал", callback_data="scheduled_back")
        kb.adjust(1)
        await callback.message.edit_text("Нет постов для этого канала.", reply_markup=kb.as_markup())
        return
    await state.update_data(scheduled_page=page)
    text, _ = _format_scheduled_channel_posts(channel_posts, page=page, per_page=PER_PAGE)
    kb = _get_scheduled_channel_keyboard(channel_posts, page=page, per_page=PER_PAGE)
    await callback.message.edit_text(
        f"<b>Ожидают постинга — {channel_name}:</b>\n\n{text}",
        reply_markup=kb.as_markup(),
    )


@dp.callback_query(F.data.startswith("cancel_scheduled:"))
async def cb_cancel_scheduled(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    _, post_id = callback.data.split(":", 1)
    try:
        await _post_cancel_post(post_id)
    except Exception as e:
        await callback.answer(f"Ошибка: {e}", show_alert=True)
        return
    state_data = await state.get_data()
    channel_id = state_data.get("scheduled_channel_id")
    try:
        resp = await _get_scheduled_posts()
        posts = resp.get("posts", [])
    except Exception as e:
        await callback.answer(f"Ошибка API: {e}", show_alert=True)
        return
    if not channel_id:
        channels = _get_channels_with_scheduled(posts)
        kb = _get_scheduled_channels_keyboard(channels)
        await callback.message.edit_text("Выберите канал:", reply_markup=kb.as_markup())
        await callback.answer("Пост отменён")
        return
    channel_posts = _filter_posts_by_channel(posts, channel_id)
    channel_name = channel_posts[0].get("channel_name", "Канал") if channel_posts else "Канал"
    if not channel_posts:
        kb = InlineKeyboardBuilder()
        kb.button(text="← Другой канал", callback_data="scheduled_back")
        kb.adjust(1)
        await callback.message.edit_text(
            "Нет постов для этого канала. Все отменены.",
            reply_markup=kb.as_markup(),
        )
    else:
        page = state_data.get("scheduled_page", 0)
        total_pages = max(1, (len(channel_posts) + PER_PAGE - 1) // PER_PAGE)
        page = min(page, total_pages - 1)
        await state.update_data(scheduled_page=page)
        text, _ = _format_scheduled_channel_posts(channel_posts, page=page, per_page=PER_PAGE)
        kb = _get_scheduled_channel_keyboard(channel_posts, page=page, per_page=PER_PAGE)
        await callback.message.edit_text(
            f"<b>Ожидают постинга — {channel_name}:</b>\n\n{text}",
            reply_markup=kb.as_markup(),
        )
    await callback.answer("Пост отменён")


@dp.message(F.text == "📤 Отправить на планирование")
async def handle_send_to_planning(message: Message, state: FSMContext) -> None:
    if not _is_admin(message.from_user.id):
        return
    try:
        data = await _get_draft_posts()
        posts = data.get("posts", [])
    except Exception as e:
        await message.answer(f"Ошибка API: {e}")
        return

    if not posts:
        await message.answer(
            "Нет черновиков. Нажми Approve на фразах.",
            reply_markup=get_main_keyboard().as_markup(resize_keyboard=True),
        )
        return

    channels = _get_channels_with_scheduled(posts)
    builder = InlineKeyboardBuilder()
    for cid, cname, cnt in channels:
        builder.button(
            text=f"{cname} ({cnt})",
            callback_data=f"planning_channel:{cid}",
        )
    builder.adjust(1)
    await message.answer("Выберите канал:", reply_markup=builder.as_markup())


@dp.callback_query(F.data.startswith("planning_channel:"))
async def cb_planning_channel_select(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    _, channel_id = callback.data.split(":", 1)
    await callback.answer()
    try:
        data = await _get_draft_posts(channel_id)
        draft_posts = data.get("posts", [])
    except Exception as e:
        await callback.message.edit_text(f"Ошибка API: {e}")
        return

    if not draft_posts:
        await callback.message.edit_text("Нет черновиков для этого канала.")
        return

    channel_name = draft_posts[0].get("channel_name", "Канал") if draft_posts else "Канал"
    await state.update_data(draft_posts=draft_posts, planning_channel_id=channel_id, channel_name=channel_name, slots_page=0)
    slots_text, _ = _format_slots_message(draft_posts, channel_name, page=0, per_page=PER_PAGE)
    kb = _get_slots_keyboard(draft_posts, page=0, per_page=PER_PAGE, show_back_channel=True)
    await callback.message.edit_text(
        f"<b>Слоты для планирования:</b>\n\n{slots_text}",
        reply_markup=kb.as_markup(),
    )


@dp.callback_query(F.data.startswith("slots_page:"))
async def cb_slots_page(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    _, page_str = callback.data.split(":", 1)
    page = int(page_str)
    await callback.answer()
    data = await state.get_data()
    draft_posts = list(data.get("draft_posts", []))
    channel_name = data.get("channel_name", "")
    if not draft_posts:
        await callback.message.edit_text("Нет слотов.", reply_markup=None)
        return
    await state.update_data(slots_page=page)
    slots_text, _ = _format_slots_message(draft_posts, channel_name, page=page, per_page=PER_PAGE)
    show_back = bool(data.get("planning_channel_id"))
    kb = _get_slots_keyboard(draft_posts, page=page, per_page=PER_PAGE, show_back_channel=show_back)
    await callback.message.edit_text(
        f"<b>Слоты для планирования:</b>\n\n{slots_text}",
        reply_markup=kb.as_markup(),
    )


@dp.callback_query(F.data == "planning_back")
async def cb_planning_back(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    await callback.answer()
    try:
        data = await _get_draft_posts()
        posts = data.get("posts", [])
    except Exception as e:
        await callback.message.edit_text(f"Ошибка API: {e}")
        return

    if not posts:
        await callback.message.edit_text("Нет черновиков. Нажми Approve на фразах.", reply_markup=None)
        await state.clear()
        return

    channels = _get_channels_with_scheduled(posts)
    builder = InlineKeyboardBuilder()
    for cid, cname, cnt in channels:
        builder.button(
            text=f"{cname} ({cnt})",
            callback_data=f"planning_channel:{cid}",
        )
    builder.adjust(1)
    await callback.message.edit_text("Выберите канал:", reply_markup=builder.as_markup())


@dp.callback_query(F.data.startswith("approve:"))
async def cb_approve(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    _, idx = callback.data.split(":", 1)
    phrase_idx = int(idx)
    raw_text = _parse_phrase_text(callback.message)
    data = await state.get_data()
    channel_id = data.get("channel_id")
    if not channel_id:
        await callback.answer("Канал не выбран.", show_alert=True)
        return
    phrases = dict(data.get("phrases", {}))
    approved_indices = list(data.get("approved_indices", []))
    approved_post_ids = dict(data.get("approved_post_ids", {}))
    phrases[phrase_idx] = raw_text
    try:
        if phrase_idx in approved_post_ids:
            await _patch_post(approved_post_ids[phrase_idx], raw_text)
        else:
            resp = await _post_approve_one(channel_id, raw_text)
            post_id = resp.get("id")
            if post_id:
                approved_post_ids[phrase_idx] = post_id
    except Exception as e:
        await callback.answer(f"Ошибка API: {e}", show_alert=True)
        return
    if phrase_idx not in approved_indices:
        approved_indices.append(phrase_idx)
    await state.update_data(phrases=phrases, approved_indices=approved_indices, approved_post_ids=approved_post_ids)
    new_text = _update_message_status(callback.message, "✅ Статус: Approved")
    if _has_phrase_number_in_text(raw_text):
        new_text += PHRASE_WARNING
    await callback.message.edit_text(new_text, reply_markup=None)
    await callback.answer("Одобрено")


@dp.callback_query(F.data.startswith("reject:"))
async def cb_reject(callback: CallbackQuery) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    # Не удаляем — обновляем текст со статусом, сохраняем историю в чате
    new_text = _update_message_status(callback.message, "❌ Статус: Rejected")
    await callback.message.edit_text(new_text, reply_markup=None)
    await callback.answer("Отклонено")


@dp.callback_query(F.data.startswith("edit:"))
async def cb_edit(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    _, idx = callback.data.split(":", 1)
    phrase_idx = int(idx)
    msg = callback.message
    await state.update_data(
        edit_message_id=msg.message_id,
        edit_chat_id=msg.chat.id,
        edit_phrase_idx=phrase_idx,
        edit_phrase_num=phrase_idx + 1,
    )
    await state.set_state(EditPhraseStates.waiting_for_text)
    await callback.answer()
    await msg.reply(
        f"Введи новый текст для фразы {phrase_idx + 1}. Или /cancel для отмены.",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(EditPhraseStates.waiting_for_text, Command("cancel"))
@dp.message(EditPhraseStates.waiting_for_text, F.text.casefold() == "cancel")
async def cancel_edit(message: Message, state: FSMContext) -> None:
    await state.set_state(None)
    await message.reply("Отменено.", reply_markup=get_main_keyboard().as_markup(resize_keyboard=True))


@dp.message(EditPhraseStates.waiting_for_text)
async def process_edit_text(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.reply("Отправь текст. Или /cancel для отмены.")
        return
    data = await state.get_data()
    msg_id = data["edit_message_id"]
    chat_id = data["edit_chat_id"]
    phrase_idx = data["edit_phrase_idx"]
    phrase_num = data["edit_phrase_num"]
    phrases = dict(data.get("phrases", {}))
    approved_post_ids = dict(data.get("approved_post_ids", {}))
    phrases[phrase_idx] = message.text
    if phrase_idx in approved_post_ids:
        post_id = approved_post_ids[phrase_idx]
        try:
            await _patch_post(post_id, message.text)
        except Exception as e:
            await message.reply(f"Ошибка обновления поста в БД: {e}")
            return
    await state.update_data(phrases=phrases)
    await state.set_state(None)
    escaped = html.escape(message.text)
    new_text = f"<b>Фраза {phrase_num}:</b>\n<pre>{escaped}</pre>\n\n✏️ Статус: Отредактировано"
    if _has_phrase_number_in_text(message.text):
        new_text += PHRASE_WARNING
    kb = get_phrase_keyboard(phrase_idx).as_markup()
    await message.bot.edit_message_text(
        chat_id=chat_id,
        message_id=msg_id,
        text=new_text,
        reply_markup=kb,
    )
    await message.reply(
        "Текст обновлён. Можно снова Approve/Reject/Edit.",
        reply_markup=get_main_keyboard().as_markup(resize_keyboard=True),
    )


@dp.callback_query(F.data.startswith("manual_time:"))
async def cb_manual_time(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    _, post_id = callback.data.split(":", 1)
    data = await state.get_data()
    draft_posts = data.get("draft_posts", [])
    if not any(str(p.get("id")) == post_id for p in draft_posts):
        await callback.answer("Пост не найден в слотах.", show_alert=True)
        return
    await state.update_data(
        manual_time_post_id=post_id,
        manual_time_message_id=callback.message.message_id,
        manual_time_chat_id=callback.message.chat.id,
    )
    await state.set_state(ManualTimeStates.waiting_for_time)
    await callback.answer()
    await callback.message.reply(
        "Введи время в формате ДД.ММ.ГГГГ ЧЧ:ММ (МСК). Или /cancel для отмены.",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(ManualTimeStates.waiting_for_time, Command("cancel"))
@dp.message(ManualTimeStates.waiting_for_time, F.text.casefold() == "cancel")
async def cancel_manual_time(message: Message, state: FSMContext) -> None:
    await state.set_state(None)
    await message.reply("Отменено.", reply_markup=get_main_keyboard().as_markup(resize_keyboard=True))


@dp.message(ManualTimeStates.waiting_for_time)
async def process_manual_time(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.reply("Введи время в формате ДД.ММ.ГГГГ ЧЧ:ММ (МСК). Или /cancel для отмены.")
        return
    iso_time = _parse_manual_time(message.text)
    if iso_time is None:
        await message.reply("Неверный формат, попробуй снова. Или /cancel для отмены.")
        return
    data = await state.get_data()
    post_id = data.get("manual_time_post_id")
    msg_id = data.get("manual_time_message_id")
    chat_id = data.get("manual_time_chat_id")
    draft_posts = list(data.get("draft_posts", []))
    channel_name = data.get("channel_name", "")
    idx = next((i for i, p in enumerate(draft_posts) if str(p.get("id")) == post_id), None)
    if idx is None:
        await state.set_state(None)
        await message.reply("Пост не найден в слотах.", reply_markup=get_main_keyboard().as_markup(resize_keyboard=True))
        return
    draft_posts[idx] = {**draft_posts[idx], "suggested_time": iso_time}
    await state.update_data(draft_posts=draft_posts)
    await state.set_state(None)
    page = data.get("slots_page", 0)
    slots_text, _ = _format_slots_message(draft_posts, channel_name, page=page, per_page=PER_PAGE)
    show_back = bool(data.get("planning_channel_id"))
    kb = _get_slots_keyboard(draft_posts, page=page, per_page=PER_PAGE, show_back_channel=show_back)
    await message.bot.edit_message_text(
        chat_id=chat_id,
        message_id=msg_id,
        text=f"<b>Слоты для планирования:</b>\n\n{slots_text}",
        reply_markup=kb.as_markup(),
    )
    await message.reply(
        "Время обновлено.",
        reply_markup=get_main_keyboard().as_markup(resize_keyboard=True),
    )


@dp.callback_query(F.data == "slots:shuffle")
async def cb_slots_shuffle(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    data = await state.get_data()
    draft_posts = list(data.get("draft_posts", []))
    channel_name = data.get("channel_name", "")
    if not draft_posts:
        await callback.answer("Нет слотов для перемешивания.", show_alert=True)
        return
    times = [p["suggested_time"] for p in draft_posts]
    random.shuffle(times)
    for i, p in enumerate(draft_posts):
        draft_posts[i] = {**p, "suggested_time": times[i]}
    await state.update_data(draft_posts=draft_posts, slots_page=0)
    slots_text, _ = _format_slots_message(draft_posts, channel_name, page=0, per_page=PER_PAGE)
    show_back = bool(data.get("planning_channel_id"))
    kb = _get_slots_keyboard(draft_posts, page=0, per_page=PER_PAGE, show_back_channel=show_back)
    await callback.message.edit_text(
        f"<b>Слоты для планирования:</b>\n\n{slots_text}",
        reply_markup=kb.as_markup(),
    )
    await callback.answer("Слоты перемешаны")


@dp.callback_query(F.data.startswith("post_now:"))
async def cb_post_now(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    _, post_id = callback.data.split(":", 1)
    try:
        await _post_post_now(post_id)
    except Exception as e:
        await callback.answer(f"Ошибка: {e}", show_alert=True)
        return

    data = await state.get_data()
    old_draft = next((p for p in data.get("draft_posts", []) if str(p.get("id")) == post_id), None)
    t = old_draft.get("text", "") if old_draft else ""
    published_text = t[:50] + "..." if len(t) > 50 else t
    draft_posts = [p for p in data.get("draft_posts", []) if str(p.get("id")) != post_id]
    await state.update_data(draft_posts=draft_posts)
    channel_name = data.get("channel_name", "")
    header = f"<b>Слоты для планирования:</b>\n\n✅ Опубликовано прямо сейчас: {published_text}\n\n"
    if draft_posts:
        page = data.get("slots_page", 0)
        total_pages = max(1, (len(draft_posts) + PER_PAGE - 1) // PER_PAGE)
        page = min(page, total_pages - 1)
        await state.update_data(draft_posts=draft_posts, slots_page=page)
        slots_text, _ = _format_slots_message(draft_posts, channel_name, page=page, per_page=PER_PAGE)
        show_back = bool(data.get("planning_channel_id"))
        kb = _get_slots_keyboard(draft_posts, page=page, per_page=PER_PAGE, show_back_channel=show_back)
        await callback.message.edit_text(
            header + slots_text,
            reply_markup=kb.as_markup(),
        )
    else:
        await callback.message.edit_text(
            header + "Все посты опубликованы.",
            reply_markup=None,
        )
    await callback.answer("Опубликовано")


@dp.callback_query(F.data.startswith("slots_confirm_one:"))
async def cb_slots_confirm_one(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    _, post_id = callback.data.split(":", 1)
    data = await state.get_data()
    draft_posts = list(data.get("draft_posts", []))
    channel_name = data.get("channel_name", "")
    post = next((p for p in draft_posts if str(p.get("id")) == post_id), None)
    if not post:
        await callback.answer("Пост не найден.", show_alert=True)
        return
    try:
        await _post_schedule_batch([post])
    except Exception as e:
        await callback.answer(f"Ошибка API: {e}", show_alert=True)
        return
    draft_posts = [p for p in draft_posts if str(p.get("id")) != post_id]
    page = data.get("slots_page", 0)
    total_pages = max(1, (len(draft_posts) + PER_PAGE - 1) // PER_PAGE)
    page = min(page, total_pages - 1)
    await state.update_data(draft_posts=draft_posts, slots_page=page)
    if draft_posts:
        slots_text, _ = _format_slots_message(draft_posts, channel_name, page=page, per_page=PER_PAGE)
        show_back = bool(data.get("planning_channel_id"))
        kb = _get_slots_keyboard(draft_posts, page=page, per_page=PER_PAGE, show_back_channel=show_back)
        await callback.message.edit_text(
            f"<b>Слоты для планирования:</b>\n\n{slots_text}",
            reply_markup=kb.as_markup(),
        )
    else:
        await state.clear()
        await callback.message.edit_text(
            "Все посты подтверждены. Используй «📅 Ожидают постинга» для просмотра.",
            reply_markup=None,
        )
        await callback.message.answer(
            "Готово.",
            reply_markup=get_main_keyboard().as_markup(resize_keyboard=True),
        )
    await callback.answer("Пост подтверждён")


@dp.callback_query(F.data == "slots:confirm")
async def cb_slots_confirm(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    data = await state.get_data()
    draft_posts = data.get("draft_posts", [])
    if not draft_posts:
        await callback.answer("Нет слотов для подтверждения.", show_alert=True)
        return
    try:
        await _post_schedule_batch(draft_posts)
    except Exception as e:
        await callback.answer(f"Ошибка API: {e}", show_alert=True)
        return
    await state.clear()
    await callback.message.edit_text(
        "Расписание подтверждено. Посты ожидают постинга. Используй «📅 Ожидают постинга» для просмотра.",
        reply_markup=None,
    )
    await callback.message.answer(
        "Готово.",
        reply_markup=get_main_keyboard().as_markup(resize_keyboard=True),
    )
    await callback.answer("Готово")


async def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN не задан в .env")
    if not BACKEND_API_KEY:
        raise RuntimeError("BACKEND_API_KEY не задан в .env")

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    import logging

    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
