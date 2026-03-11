"""Генерация картинок с текстом поста через Pillow."""

import io
import random
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Позиции — доли от ширины/высоты (0.5 = центр). MVP: только center.
# Будущее: "top", "bottom", "top_left" и т.д. (см. tehdolg.md)
POSITIONS = {"center": (0.5, 0.5)}

TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "assets" / "templates"
FONTS_DIR = Path(__file__).resolve().parents[2] / "assets" / "fonts"
FONT_SIZE = 32  # 48 / 1.5
TEXT_COLOR = (255, 255, 255)
PADDING_RATIO = 0.85  # текст занимает до 85% ширины


def _get_font(size: int = FONT_SIZE) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Загружает Arial, fallback — Cormorant Unicase, затем дефолтный шрифт."""
    candidates = [
        "arial.ttf",
        "Arial.ttf",
        "C:/Windows/Fonts/arial.ttf",
        str(FONTS_DIR / "CormorantUnicase-Regular.ttf"),
        str(FONTS_DIR / "CormorantUnicase-Regular.otf"),
        "C:/Windows/Fonts/CormorantUnicase-Regular.ttf",
        "C:/Windows/Fonts/CormorantUnicase-Regular.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/msttcorefonts/arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _pick_background() -> Path:
    """Выбирает случайный фон из assets/templates/."""
    if not TEMPLATES_DIR.exists():
        raise FileNotFoundError(f"Папка шаблонов не найдена: {TEMPLATES_DIR}")
    exts = {".jpg", ".jpeg", ".png"}
    files = [f for f in TEMPLATES_DIR.iterdir() if f.suffix.lower() in exts]
    if not files:
        raise FileNotFoundError(
            f"Нет фонов в {TEMPLATES_DIR}. Добавьте bg.jpg или другой файл."
        )
    return random.choice(files)


def generate_post_image(text: str, position: str = "center") -> bytes:
    """
    Генерирует изображение с текстом поста на случайном фоне.

    Args:
        text: Текст поста.
        position: Позиция текста ("center" по умолчанию). Позиции задаются
            относительными координатами для работы с фонами любого размера.

    Returns:
        Байты JPEG-изображения.
    """
    bg_path = _pick_background()
    img = Image.open(bg_path).convert("RGB")
    w, h = img.size

    text = text.lower()
    font_size = FONT_SIZE
    font = _get_font(font_size)
    max_chars = max(10, int(w * PADDING_RATIO / (font_size * 0.5)))
    lines = textwrap.wrap(text, width=max_chars)
    wrapped = "\n".join(lines)

    draw = ImageDraw.Draw(img)
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Уменьшаем шрифт, если текст не помещается
    while (text_w > w * PADDING_RATIO or text_h > h * PADDING_RATIO) and font_size > 12:
        font_size -= 4
        font = _get_font(font_size)
        max_chars = max(10, max_chars - 2)
        lines = textwrap.wrap(text, width=max_chars)
        wrapped = "\n".join(lines)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

    px, py = POSITIONS.get(position, (0.5, 0.5))
    xy = (int(w * px), int(h * py))

    draw.multiline_text(
        xy,
        wrapped,
        font=font,
        fill=TEXT_COLOR,
        align="center",
        anchor="mm",
    )

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()
