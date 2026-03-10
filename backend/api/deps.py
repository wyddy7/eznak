"""Зависимости API: проверка API-ключа."""

import os

from fastapi import HTTPException, Request

BACKEND_API_KEY = os.getenv("BACKEND_API_KEY", "")


async def get_api_key(request: Request) -> str:
    """
    Проверяет заголовок X-API-Key на совпадение с BACKEND_API_KEY из .env.
    Защищает все роуты от несанкционированного доступа.
    Возвращает 401 при отсутствии или неверном ключе.
    """
    if not BACKEND_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="BACKEND_API_KEY не настроен на сервере",
        )
    x_api_key = request.headers.get("X-API-Key")
    if not x_api_key or x_api_key != BACKEND_API_KEY:
        raise HTTPException(status_code=401, detail="Неверный или отсутствующий API-ключ")
    return x_api_key
