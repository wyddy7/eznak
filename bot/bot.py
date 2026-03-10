"""
Telegram-бот для генерации и модерации постов.
Шаг 5: Планирование — Approve/Reject/Edit, Отправить на планирование, Shuffle, Confirm All.
"""

import os
import random
from typing import Any

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


def _parse_phrase_text(msg: Message) -> str:
    """Извлекает сырой текст из формата «Фраза N:\n{text}» или с суффиксом «Статус:»."""
    text = msg.text or msg.caption or ""
    if "\n" not in text:
        return text.strip()
    after_prefix = text.split("\n", 1)[1]
    if "\n\n" in after_prefix:
        return after_prefix.split("\n\n", 1)[0].strip()
    return after_prefix.strip()


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


async def _post_approve(phrases: list[str]) -> dict[str, Any]:
    """POST /api/v1/posts/approve — возвращает draft_posts."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BACKEND_URL}/api/v1/posts/approve",
            json={"phrases": phrases},
            headers={"X-API-Key": BACKEND_API_KEY, "Content-Type": "application/json"},
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


def _format_slots_message(draft_posts: list[dict[str, Any]]) -> str:
    """Форматирует слоты для отображения."""
    lines = []
    for p in draft_posts:
        text = p.get("text", "")
        at = p.get("suggested_time", "—")
        lines.append(f"• {text}\n  📅 {at} (МСК)")
    return "\n\n".join(lines)


def _get_slots_keyboard() -> InlineKeyboardBuilder:
    """Inline-кнопки Shuffle и Confirm All."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🔀 Shuffle", callback_data="slots:shuffle")
    builder.button(text="✅ Confirm All", callback_data="slots:confirm")
    builder.adjust(2)
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

    await state.update_data(
        phrases={i: p for i, p in enumerate(phrases)},
        approved_indices=[],
    )
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


@dp.message(F.text == "📤 Отправить на планирование")
async def handle_send_to_planning(message: Message, state: FSMContext) -> None:
    if not _is_admin(message.from_user.id):
        return
    data = await state.get_data()
    phrases = data.get("phrases", {})
    approved_indices = data.get("approved_indices", [])
    approved_texts = [phrases[i] for i in sorted(approved_indices) if i in phrases]
    if not approved_texts:
        await message.answer(
            "Нет одобренных фраз. Нажмите Approve на нужных фразах.",
            reply_markup=get_main_keyboard().as_markup(resize_keyboard=True),
        )
        return
    try:
        resp = await _post_approve(approved_texts)
    except Exception as e:
        await message.answer(f"Ошибка API: {e}")
        return
    draft_posts = resp.get("draft_posts", [])
    if not draft_posts:
        await message.answer("Не удалось создать черновики. Проверь каналы в БД.")
        return
    await state.update_data(draft_posts=draft_posts)
    slots_text = _format_slots_message(draft_posts)
    kb = _get_slots_keyboard()
    await message.answer(
        f"<b>Слоты для планирования:</b>\n\n{slots_text}",
        reply_markup=kb.as_markup(),
    )


@dp.callback_query(F.data.startswith("approve:"))
async def cb_approve(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    _, idx = callback.data.split(":", 1)
    phrase_idx = int(idx)
    raw_text = _parse_phrase_text(callback.message)
    data = await state.get_data()
    phrases = dict(data.get("phrases", {}))
    approved_indices = list(data.get("approved_indices", []))
    phrases[phrase_idx] = raw_text
    if phrase_idx not in approved_indices:
        approved_indices.append(phrase_idx)
    await state.update_data(phrases=phrases, approved_indices=approved_indices)
    new_text = _update_message_status(callback.message, "✅ Статус: Approved")
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
    phrases[phrase_idx] = message.text
    await state.update_data(phrases=phrases)
    await state.set_state(None)
    new_text = f"<b>Фраза {phrase_num}:</b>\n{message.text}\n\n✏️ Статус: Отредактировано"
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


@dp.callback_query(F.data == "slots:shuffle")
async def cb_slots_shuffle(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещён.", show_alert=True)
        return
    data = await state.get_data()
    draft_posts = list(data.get("draft_posts", []))
    if not draft_posts:
        await callback.answer("Нет слотов для перемешивания.", show_alert=True)
        return
    times = [p["suggested_time"] for p in draft_posts]
    random.shuffle(times)
    for i, p in enumerate(draft_posts):
        draft_posts[i] = {**p, "suggested_time": times[i]}
    await state.update_data(draft_posts=draft_posts)
    slots_text = _format_slots_message(draft_posts)
    kb = _get_slots_keyboard()
    await callback.message.edit_text(
        f"<b>Слоты для планирования:</b>\n\n{slots_text}",
        reply_markup=kb.as_markup(),
    )
    await callback.answer("Слоты перемешаны")


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
