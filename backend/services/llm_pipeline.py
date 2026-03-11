"""LLM-пайплайн: генерация 15 фраз -> ранжирование -> топ M фраз (Pydantic)."""

import os
import random
from uuid import UUID

import structlog
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.prompts import (
    DEFAULT_DATASET,
    PROMPT_1_SYSTEM,
    PROMPT_1_USER_TEMPLATE,
    PROMPT_2_SYSTEM,
    PROMPT_2_USER_TEMPLATE,
)
from backend.db.models import Dataset

log = structlog.get_logger(__name__)

SAMPLE_SIZE = 20


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


def _create_generator_agent() -> Agent[None, GeneratedPhrases]:
    """Агент для генерации 15 фраз."""
    return Agent(
        f"openrouter:{_get_openrouter_model()}",
        output_type=GeneratedPhrases,
        system_prompt=PROMPT_1_SYSTEM,
    )


def _create_ranker_agent() -> Agent[None, LLMResponse]:
    """Агент для ранжирования и отбора фраз."""
    return Agent(
        f"openrouter:{_get_openrouter_model()}",
        output_type=LLMResponse,
        system_prompt=PROMPT_2_SYSTEM,
    )


async def _fetch_dataset_for_channel(session: AsyncSession, channel_id: UUID) -> list[str]:
    """
    Загружает фразы из datasets WHERE channel_id = ?.
    Если пусто — fallback на default_dataset из YAML.
    Случайная выборка 15–20 фраз для вариативности.
    """
    result = await session.execute(
        select(Dataset.text).where(Dataset.channel_id == channel_id)
    )
    rows = result.scalars().all()
    phrases = [r for r in rows if r and r.strip()]

    if not phrases:
        log.info(
            "llm_pipeline_dataset_empty",
            channel_id=str(channel_id),
            fallback="default_dataset",
        )
        phrases = list(DEFAULT_DATASET)

    sample_count = min(SAMPLE_SIZE, len(phrases))
    sampled = random.sample(phrases, sample_count)
    log.info(
        "llm_pipeline_dataset_loaded",
        channel_id=str(channel_id),
        total=len(phrases),
        sampled=sample_count,
        source="datasets" if rows else "default_dataset",
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

    dataset_text = "\n".join(f"- {p}" for p in phrases_data)
    model = _get_openrouter_model()

    log.info("llm_pipeline_start", channel_id=str(channel_id), dataset_size=len(phrases_data), model=model)
    log.debug(
        "llm_pipeline_dataset",
        channel_id=str(channel_id),
        dataset=phrases_data,
        dataset_text=dataset_text,
    )

    # --- Шаг 1: Генерация 15 фраз ---
    gen_agent = _create_generator_agent()
    user_prompt_1 = PROMPT_1_USER_TEMPLATE.format(dataset=dataset_text)

    log.debug(
        "llm_pipeline_prompt1",
        channel_id=str(channel_id),
        system_prompt=PROMPT_1_SYSTEM,
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
    user_prompt_2 = PROMPT_2_USER_TEMPLATE.format(phrases=phrases_block)

    log.debug(
        "llm_pipeline_prompt2",
        channel_id=str(channel_id),
        system_prompt=PROMPT_2_SYSTEM,
        user_prompt=user_prompt_2,
        input_phrases=phrases_to_rank,
    )

    rank_agent = _create_ranker_agent()
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
