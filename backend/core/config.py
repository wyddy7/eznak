"""Конфигурация приложения из переменных окружения."""

import os

TARGET_CHANNEL_ID: str = os.getenv("TARGET_CHANNEL_ID", "")
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
