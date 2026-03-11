"""Промпты и датасет — загружаются из config/prompts.yaml."""

from backend.core.config_loader import get_prompts

_prompts = get_prompts()
_generator = _prompts.get("generator", {})
_critic = _prompts.get("critic", {})

DEFAULT_DATASET: list[str] = _prompts.get("default_dataset", [])
PROMPT_1_SYSTEM: str = _generator.get("system", "")
PROMPT_1_USER_TEMPLATE: str = _generator.get("user_template", "")
PROMPT_2_SYSTEM: str = _critic.get("system", "")
PROMPT_2_USER_TEMPLATE: str = _critic.get("user_template", "")
