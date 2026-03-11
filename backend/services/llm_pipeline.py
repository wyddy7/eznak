"""LLM-пайплайн: генерация 15 фраз -> ранжирование -> топ M фраз (Pydantic)."""

import os
import random
from datetime import datetime
from uuid import UUID
from zoneinfo import ZoneInfo

import structlog
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.core.config_loader import get_prompts
from backend.core.prompts import DEFAULT_DATASET
from backend.db.models import Channel, Dataset

log = structlog.get_logger(__name__)

MSK = ZoneInfo("Europe/Moscow")
MONTHS_RU = [
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря",
]
WEEKDAYS_RU = [
    "понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье",
]


def _format_today_msk() -> str:
    """Человекочитаемая дата для промпта: '12 марта 2026, среда'."""
    now = datetime.now(MSK)
    return f"{now.day} {MONTHS_RU[now.month - 1]} {now.year}, {WEEKDAYS_RU[now.weekday()]}"


def _get_sample_size() -> int:
    """Размер выборки из датасета (из config/prompts.yaml)."""
    return int(get_prompts().get("dataset_sample_size", 50))


# --- Pydantic-модели для structured output ---

class GeneratedPhrases(BaseModel):
    """Выход Prompt 1: 15 сгенерированных фраз."""

    phrases: list[str] = Field(description="Ровно 15 мотивационных фраз")


class RankedPhrase(BaseModel):
    """Одна фраза с оценкой."""

    text: str = Field(description="Текст фразы")
    score: int = Field(ge=1, le=10, description="Оценка от 1 до 10")


class LLMResponse(BaseModel):
    """Выход Prompt 2: отфильтрованные фразы со скором >= 7, макс. 7 шт."""

    approved_phrases: list[RankedPhrase] = Field(
        description="Лучшие фразы (скор >= 7), максимум 7"
    )


# --- Агенты pydantic-ai ---

def _get_openrouter_model() -> str:
    """Модель OpenRouter из env. Fallback: anthropic/claude-sonnet-4."""
    return os.environ.get("OPENROUTER_MODEL", "anthropic/claude-sonnet-4")


def _create_generator_agent(system_prompt: str) -> Agent[None, GeneratedPhrases]:
    """Агент для генерации 15 фраз."""
    return Agent(
        f"openrouter:{_get_openrouter_model()}",
        output_type=GeneratedPhrases,
        system_prompt=system_prompt,
    )


def _create_ranker_agent(system_prompt: str) -> Agent[None, LLMResponse]:
    """Агент для ранжирования и отбора фраз."""
    return Agent(
        f"openrouter:{_get_openrouter_model()}",
        output_type=LLMResponse,
        system_prompt=system_prompt,
    )


async def _get_prompts_for_channel(
    session: AsyncSession, channel_id: UUID
) -> tuple[str, str, str, str, str]:
    """
    Возвращает (gen_system, gen_user_template, critic_system, critic_user_template, prompt_source).
    prompt_source: имя шаблона или "yaml_fallback".
    """
    result = await session.execute(
        select(Channel)
        .options(selectinload(Channel.prompt_template))
        .where(Channel.id == channel_id)
    )
    channel = result.scalar_one_or_none()
    if channel and channel.prompt_template_id and channel.prompt_template:
        t = channel.prompt_template
        return (
            t.generator_system,
            t.generator_user_template,
            t.critic_system,
            t.critic_user_template,
            t.name,
        )
    prompts = get_prompts()
    gen = prompts.get("generator", {})
    crit = prompts.get("critic", {})
    return (
        gen.get("system", ""),
        gen.get("user_template", ""),
        crit.get("system", ""),
        crit.get("user_template", ""),
        "yaml_fallback",
    )


async def _fetch_dataset_for_channel(session: AsyncSession, channel_id: UUID) -> list[str]:
    """
    Загружает фразы из datasets.
    Если у канала задан dataset_source_channel_id — берёт датасет из того канала.
    Иначе — из своего channel_id.
    Если пусто — fallback на default_dataset из YAML.
    Случайная выборка (размер из config: dataset_sample_size) для вариативности.
    """
    channel_result = await session.execute(select(Channel).where(Channel.id == channel_id))
    channel = channel_result.scalar_one_or_none()
    effective_id = channel.dataset_source_channel_id if channel and channel.dataset_source_channel_id else channel_id

    result = await session.execute(
        select(Dataset.text).where(Dataset.channel_id == effective_id)
    )
    rows = result.scalars().all()
    phrases = [r for r in rows if r and r.strip()]

    if not phrases:
        log.info(
            "llm_pipeline_dataset_empty",
            channel_id=str(channel_id),
            source_channel_id=str(effective_id),
            fallback="default_dataset",
        )
        phrases = list(DEFAULT_DATASET)

    sample_count = min(_get_sample_size(), len(phrases))
    sampled = random.sample(phrases, sample_count)
    source = "datasets" if rows else "default_dataset"
    log.info(
        "llm_pipeline_dataset_loaded",
        channel_id=str(channel_id),
        source_channel_id=str(effective_id),
        total=len(phrases),
        sampled=sample_count,
        source=source,
    )
    return sampled


async def run_llm_pipeline(
    channel_id: UUID,
    session: AsyncSession | None = None,
    dataset: list[str] | None = None,
) -> list[RankedPhrase]:
    """
    Цепочка: Prompt 1 (15 фраз) -> Prompt 2 (ранжирование).
    Возвращает список RankedPhrase (макс. 7).
    dataset: если передан — используется как есть; иначе — запрос в БД + рандомизация (session обязателен).
    """
    if dataset is not None:
        phrases_data = dataset
        log.info("llm_pipeline_dataset_override", channel_id=str(channel_id), size=len(phrases_data))
    else:
        if session is None:
            raise ValueError("session обязателен, когда dataset не передан (нужен запрос в БД)")
        phrases_data = await _fetch_dataset_for_channel(session, channel_id)

    if session is not None:
        gen_system, gen_user_tpl, critic_system, critic_user_tpl, prompt_source = (
            await _get_prompts_for_channel(session, channel_id)
        )
    else:
        prompts = get_prompts()
        gen = prompts.get("generator", {})
        crit = prompts.get("critic", {})
        gen_system = gen.get("system", "")
        gen_user_tpl = gen.get("user_template", "")
        critic_system = crit.get("system", "")
        critic_user_tpl = crit.get("user_template", "")
        prompt_source = "yaml_fallback"

    log.info(
        "llm_pipeline_start",
        channel_id=str(channel_id),
        dataset_size=len(phrases_data),
        model=_get_openrouter_model(),
        prompt_source=prompt_source,
    )

    dataset_text = "\n".join(f"- {p}" for p in phrases_data)
    log.debug(
        "llm_pipeline_dataset",
        channel_id=str(channel_id),
        dataset=phrases_data,
        dataset_text=dataset_text,
    )

    # --- Шаг 1: Генерация 15 фраз ---
    gen_agent = _create_generator_agent(gen_system)
    user_prompt_1 = gen_user_tpl.format(dataset=dataset_text)
    user_prompt_1 += f"\n\nКонтекст: сегодня {_format_today_msk()}. Учитывай сезон при упоминании погоды и времени года."

    log.debug(
        "llm_pipeline_prompt1",
        channel_id=str(channel_id),
        system_prompt=gen_system,
        user_prompt=user_prompt_1,
    )

    result_1 = await gen_agent.run(user_prompt_1)
    generated = result_1.output

    if not generated.phrases:
        log.warning("llm_pipeline_empty_generation", channel_id=str(channel_id))
        return []

    # Берём до 15 фраз (модель может вернуть меньше)
    phrases_to_rank = generated.phrases[:15]
    log.info(
        "llm_pipeline_generated",
        channel_id=str(channel_id),
        count=len(phrases_to_rank),
    )
    log.debug(
        "llm_pipeline_generated_phrases",
        channel_id=str(channel_id),
        phrases=phrases_to_rank,
    )

    # --- Шаг 2: Ранжирование ---
    phrases_block = "\n".join(f"{i+1}. {p}" for i, p in enumerate(phrases_to_rank))
    user_prompt_2 = critic_user_tpl.format(phrases=phrases_block)

    log.debug(
        "llm_pipeline_prompt2",
        channel_id=str(channel_id),
        system_prompt=critic_system,
        user_prompt=user_prompt_2,
        input_phrases=phrases_to_rank,
    )

    rank_agent = _create_ranker_agent(critic_system)
    result_2 = await rank_agent.run(user_prompt_2)
    ranked = result_2.output

    approved = ranked.approved_phrases
    log.info(
        "llm_pipeline_ranked",
        channel_id=str(channel_id),
        approved_count=len(approved),
    )
    if not approved:
        log.warning(
            "llm_pipeline_empty_ranker",
            channel_id=str(channel_id),
            reason="Ранжировщик отфильтровал все фразы (скор < 7). Попробуй другой датасет или модель.",
        )
    log.debug(
        "llm_pipeline_ranked_output",
        channel_id=str(channel_id),
        approved_phrases=[{"text": p.text, "score": p.score} for p in approved],
    )

    return approved
