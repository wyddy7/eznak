"""Загрузка конфигов из YAML (промпты, медиа)."""

from pathlib import Path

import yaml

# Корень проекта (родитель backend/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"


def _load_yaml(filename: str) -> dict:
    path = CONFIG_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Конфиг не найден: {path}")
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_prompts() -> dict:
    """Загружает config/prompts.yaml."""
    return _load_yaml("prompts.yaml")


def load_media() -> dict:
    """Загружает config/media.yaml."""
    return _load_yaml("media.yaml")


# Кэш при первом обращении
_prompts_cache: dict | None = None
_media_cache: dict | None = None


def get_prompts() -> dict:
    """Возвращает промпты (кэшировано)."""
    global _prompts_cache
    if _prompts_cache is None:
        _prompts_cache = load_prompts()
    return _prompts_cache


def get_media() -> dict:
    """Возвращает настройки медиа (кэшировано)."""
    global _media_cache
    if _media_cache is None:
        _media_cache = load_media()
    return _media_cache
