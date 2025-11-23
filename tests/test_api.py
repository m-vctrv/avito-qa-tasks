import pytest
import requests
import random

BASE_URL = "https://qa-internship.avito.com"


def create_test_advertisement():
    """Вспомогательная функция для создания обьявления"""
    url = f"{BASE_URL}/api/1/item"
    data = {
        "sellerID": random.randint(111111, 999999),
        "name": "Тестовый товар",
        "price": 1000,
        "statistics": {"likes": 5, "viewCount": 50, "contacts": 2},
    }

    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()["status"].split(" - ")[1]
    return None
    print("Status Code:", response.status_code)


def test_create_advertisement():
    print("\n=== ID.01: Создание обьявления ===")

    item_id = create_test_advertisement()
    assert item_id is not None, "Не удалось создать обьявление"


def test_get_statistics():
    print("\n=== ID.02: Получение статистики существующего обьявления")

    item_id = create_test_advertisement()
    assert item_id is not None, "Не удалось создать обьявление для теста"

    url = f"{BASE_URL}/api/1/statistic/{item_id}"
    response = requests.get(url)

    assert response.status_code == 200, f"Ошибка статистики: {response.status_code}"
    assert len(response.json()) > 0, "Пустая статистика"
    print("     Status Code:", response.status_code)
    print("     Тело ответа", response.json())


def test_get_advertisement():
    print("\n=== ID.03: Получение данных обьявления по идентификатору ===")

    item_id = create_test_advertisement()
    assert item_id is not None, "Не удалось создать обьявление для теста"

    url = f"{BASE_URL}/api/1/item/{item_id}"
    response = requests.get(url)

    assert response.status_code == 200, f"Ошибка получения: {response.status_code}"
    assert len(response.json()) > 0, "Пустой ответ"
    print("     Status Code:", response.status_code)
    print("     Тело ответа", response.json(), sep="\n")


def test_get_seller_advertisements():
    print("\n=== ID.04: Получение списка обьявлений по sellerID ===")

    seller_id = random.randint(111111, 999999)

    # Создание обьявления
    url = f"{BASE_URL}/api/1/item"
    data = {
        "sellerID": seller_id,
        "name": "Товар продавца",
        "price": 4000,
        "statistics": {"likes": 10, "viewCount": 100, "contacts": 5},
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200, "Не удалось создать обьявление"

    # Получение обьявления продавца
    url = f"{BASE_URL}/api/1/{seller_id}/item"
    response = requests.get(url)

    assert response.status_code == 200, f"Ошибка: {response.status_code}"
    assert isinstance(response.json(), list), "Ответ не является списком"
    print("Status Code:", response.status_code)


def test_create_invalid_data():
    print("\n=== Id.05: Обработка невалидных данных при создании обьявления ===")

    url = f"{BASE_URL}/api/1/item"
    data = {
        "sellerID": "это не число",
        "name": "Тест",
        "price": 1000,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
    }

    response = requests.post(url, json=data)
    assert (
        response.status_code == 400
    ), f"Ожидалась ошибка 400, получен {response.status_code}"
    print("Status Code:", response.status_code)


def test_get_nonexistent_statistics():
    print("\n=== ID.06: Получение статистики несуществующего обьявления ===")

    url = f"{BASE_URL}/api/1/statistic/неправильный_id_123"
    response = requests.get(url)

    assert response.status_code in [
        400,
        404,
    ], f"Ожидалась ошибка, получен {response.status_code}"
    print("Status Code:", response.status_code)
