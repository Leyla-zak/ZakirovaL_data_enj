"""
read_api.py

Скрипт для сбора данных о породах собак и их фотографий через Dog API.
Собирает список пород, скачивает по одному фото каждой породы,
сохраняет метаданные в CSV, а картинки - в папку images/.

Источник: https://dog.ceo/dog-api/
"""

import requests
import pandas as pd
from pathlib import Path


BASE_URL = "https://dog.ceo/api"
IMAGES_DIR = Path("images")


def fetch_all_breeds() -> list[str]:
    """
    Получает список всех пород собак.

    Returns:
        list[str]: Список названий пород.
    """
    response = requests.get(f"{BASE_URL}/breeds/list/all", timeout=10)
    response.raise_for_status()
    data = response.json()

    breeds = []
    for breed, subbreeds in data["message"].items():
        if subbreeds:
            for sub in subbreeds:
                breeds.append(f"{sub} {breed}")
        else:
            breeds.append(breed)

    print(f"Получено пород: {len(breeds)}")
    return breeds


def fetch_random_image(breed: str) -> str | None:
    """
    Получает URL случайного фото для указанной породы.

    Args:
        breed (str): Название породы (например, "labrador").

    Returns:
        str | None: URL картинки или None при ошибке.
    """
    # Для подпород (например, "australian shepherd") используем другой формат
    parts = breed.split()
    if len(parts) == 2:
        sub, main = parts
        url = f"{BASE_URL}/breed/{main}/{sub}/images/random"
    else:
        url = f"{BASE_URL}/breed/{breed}/images/random"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("message")
    except requests.RequestException as e:
        print(f"{breed}: ошибка - {e}")
        return None


def download_image(url: str, save_path: Path) -> bool:
    """
    Скачивает картинку по URL и сохраняет её.

    Args:
        url (str): URL картинки.
        save_path (Path): Путь для сохранения.

    Returns:
        bool: True, если успешно.
    """
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        save_path.write_bytes(response.content)
        return True
    except requests.RequestException as e:
        print(f"Не удалось скачать {url}: {e}")
        return False


def collect_dog_data(max_breeds: int = 30) -> pd.DataFrame:
    """
    Собирает данные о породах и скачивает фото.

    Args:
        max_breeds (int): Максимум пород для сбора.

    Returns:
        pd.DataFrame: Датафрейм с метаданными.
    """
    IMAGES_DIR.mkdir(exist_ok=True)

    breeds = fetch_all_breeds()[:max_breeds]
    rows = []

    for i, breed in enumerate(breeds, 1):
        print(f"\n [{i}/{len(breeds)}] {breed}")

        image_url = fetch_random_image(breed)
        if not image_url:
            continue

        filename = f"{breed.replace(' ', '_')}.jpg"
        save_path = IMAGES_DIR / filename

        if download_image(image_url, save_path):
            rows.append({
                "breed": breed,
                "image_url": image_url,
                "filename": filename,
            })
            print(f"Сохранено: {filename}")

    return pd.DataFrame(rows)


if __name__ == "__main__":
    print("Сбор данных о породах собак...\n")

    df = collect_dog_data(max_breeds=30)

    print(f"\n Собрано записей: {len(df)}")

    print("\nПервые 10 строк:")
    print(df.head(10))

    df.to_csv("dog_breeds.csv", index=False)
    print(f"\nМетаданные сохранены в dog_breeds.csv")
    print(f"Картинки сохранены в {IMAGES_DIR}/")