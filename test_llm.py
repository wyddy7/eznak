"""Тест LLM-пайплайна: генерация и ранжирование фраз."""

import asyncio
import json
import os
from uuid import uuid4

# Загружаем .env и настраиваем логирование (LOG_LEVEL из env)
from dotenv import load_dotenv

load_dotenv()

from backend.core.logging import configure_logging

configure_logging()


async def main() -> None:
    from backend.services.llm_pipeline import run_llm_pipeline

    channel_id = uuid4()
    mock_dataset = [
        "У тебя обязательно все получится!",
        "Разреши себе чувствовать и проживать все эмоции",
        "Перестань жертвовать собой ради других!",
        "Страх уходит во время движения!",
        "У тебя есть суперсила и это ты!",
    ]

    print("Запуск LLM-пайплайна...")
    print(f"channel_id: {channel_id}")
    print(f"OPENROUTER_API_KEY: {'***' + os.environ.get('OPENROUTER_API_KEY', '')[-4:] if os.environ.get('OPENROUTER_API_KEY') else 'НЕ ЗАДАН!'}")
    print()

    result = await run_llm_pipeline(channel_id=channel_id, dataset=mock_dataset)

    print("\n--- Результат (RankedPhrase) ---")
    output = [{"text": r.text, "score": r.score} for r in result]
    print(json.dumps(output, ensure_ascii=False, indent=2))
    print(f"\nВсего фраз: {len(result)}")


if __name__ == "__main__":
    asyncio.run(main())
