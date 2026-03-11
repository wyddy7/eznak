"""Роутер шаблонов промптов."""

from uuid import UUID

import structlog
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps import get_api_key
from backend.db.models import PromptTemplate
from backend.db.session import get_session

log = structlog.get_logger(__name__)
router = APIRouter(prefix="/prompt-templates", tags=["prompt-templates"])


@router.get("")
async def list_prompt_templates(
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Список шаблонов промптов (id, name).
    """
    log.info("api.prompt_templates.list")
    result = await session.execute(select(PromptTemplate).order_by(PromptTemplate.name))
    templates = result.scalars().all()
    return {
        "prompt_templates": [
            {"id": str(t.id), "name": t.name}
            for t in templates
        ]
    }


@router.get("/{template_id}")
async def get_prompt_template(
    template_id: UUID,
    _: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Детали шаблона: все 4 промпта.
    """
    log.info("api.prompt_templates.get", template_id=str(template_id))
    result = await session.execute(
        select(PromptTemplate).where(PromptTemplate.id == template_id)
    )
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="Шаблон не найден")
    return {
        "id": str(template.id),
        "name": template.name,
        "generator_system": template.generator_system,
        "generator_user_template": template.generator_user_template,
        "critic_system": template.critic_system,
        "critic_user_template": template.critic_user_template,
    }
