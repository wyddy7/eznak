"""
Telegram-бот для генерации и модерации постов.
Шаг 4: Reply-меню, генерация, Inline-кнопки Approve/Reject/Edit.
"""

import os
from typing import Any

import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from dotenv import load_dotenv

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
    builder.adjust(2)
    return builder


# --- Inline-кнопки для фразы ---
def get_phrase_keyboard(phrase_idx: int) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Approve", callback_data=f"approve:{phrase_idx}")
    builder.button(text="❌ Reject", callback_data=f"reject:{phrase_idx}")
    builder.button(text="✏️ Edit", callback_data=f"edit:{phrase_idx}")
    builder.adjust(3)
    return builder


async def _post_generate() -> dict[str, Any]:
    """POST /api/v1/generate — возвращает {"phrases": [...]}."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BACKEND_URL}/api/v1/generate",
            headers={"X-API-Key": BACKEND_API_KEY},
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


# --- Dispatcher и Middleware ---
dp = Dispatcher()


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
async def handle_generate(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        return
    await message.answer("Генерирую фразы...")
    try:
        data = await _post_generate()
        phrases = data.get("phrases", [])
    except Exception as e:
        await message.answer(f"Ошибка API: {e}")
        return

    if not phrases:
        await message.answer("Фразы не сгенерированы. Проверь каналы в БД и LLM.")
        return

    for i, phrase in enumerate(phrases):
        kb = get_phrase_keyboard(i)
        await message.answer(
            f"<b>Фраза {i + 1}:</b>\n{phrase}",
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

    lines = []
    for p in posts:
        text = p.get("text", "")
        at = p.get("scheduled_at", "—")
        lines.append(f"• {text}\n  📅 {at}")
    await message.answer("\n\n".join(lines))


@dp.callback_query(F.data.startswith("approve:"))
async def cb_approve(callback: CallbackQuery) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    # Пока только подтверждаем — полная логика в Шаге 5
    await callback.answer("Approve — в следующем шаге")
    await callback.message.edit_reply_markup(reply_markup=None)


@dp.callback_query(F.data.startswith("reject:"))
async def cb_reject(callback: CallbackQuery) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    await callback.message.delete()
    await callback.answer("Удалено")


@dp.callback_query(F.data.startswith("edit:"))
async def cb_edit(callback: CallbackQuery) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    # FSM для редактирования — в Шаге 5
    await callback.answer("Edit — в следующем шаге")




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
