"""Создаёт тестовый фон assets/templates/bg.jpg, если файл отсутствует."""

from pathlib import Path

from PIL import Image

TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "assets" / "templates"
BG_PATH = TEMPLATES_DIR / "bg.jpg"
WIDTH, HEIGHT = 1080, 1080


def create_gradient_bg() -> None:
    """Генерирует градиентный фон и сохраняет в bg.jpg."""
    img = Image.new("RGB", (WIDTH, HEIGHT))
    pixels = img.load()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            # Градиент от тёмно-синего к тёмно-фиолетовому
            r = int(30 + (x / WIDTH) * 80)
            g = int(20 + (y / HEIGHT) * 60)
            b = int(100 + (x / WIDTH) * 80)
            pixels[x, y] = (r, g, b)
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    img.save(BG_PATH, "JPEG", quality=85)
    print(f"Создан: {BG_PATH}")


if __name__ == "__main__":
    if BG_PATH.exists():
        print(f"Файл уже существует: {BG_PATH}")
    else:
        create_gradient_bg()
