"""Тестовый скрипт для проверки генерации картинок с текстом."""

from backend.services.media_gen import generate_post_image

TEST_TEXT = (
    "Это тестовая фраза для проверки генерации изображения. "
    "Текст должен переноситься на несколько строк и не вылезать за края картинки."
)

if __name__ == "__main__":
    photo_bytes = generate_post_image(TEST_TEXT)
    with open("output.jpg", "wb") as f:
        f.write(photo_bytes)
    print("Сохранено: output.jpg")
