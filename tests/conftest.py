import os
from typing import Any, Dict, Generator, List

import pytest


# Фикстура для тестовых данных карт (из test_masks.py)
@pytest.fixture
def card_numbers() -> list[tuple[str, str]]:
    return [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1596837868705199", "1596 83** **** 5199"),
        ("", ""),
        ("1234", "1234"),
    ]


# Фикстура для тестовых данных счетов (из test_masks.py)
@pytest.fixture
def account_numbers() -> list[tuple[str, str]]:
    return [
        ("73654108430135874305", "**4305"),
        ("64686473678894779589", "**9589"),
        ("", ""),
        ("123", "**123"),
    ]


# Фикстура для тестовых операций (из test_processing.py)
@pytest.fixture
def operations_data() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "CANCELED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 3, "state": "EXECUTED", "date": "2020-01-01T00:00:00.000000"},
        {"id": 4, "state": "PENDING", "date": "2019-12-31T23:59:59.999999"},
        {"id": 5, "state": "EXECUTED", "date": "2018-01-01T00:00:00.000000"},
    ]


# Фикстура для тестовых данных карт и счетов (из test_widget.py)
@pytest.fixture
def account_card_data() -> list[tuple[str, str]]:
    return [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 123", "Счет **123"),
        ("Карта 1234567890123456", "Карта 1234 56** **** 3456"),
        ("Invalid Input", "Invalid Input"),
    ]


# Фикстура для тестовых дат (из test_widget.py)
@pytest.fixture
def date_data() -> list[tuple[str, str]]:
    return [
        ("2019-07-03T18:35:29.512364", "03.07.2019"),
        ("2018-06-30T02:08:58.425572", "30.06.2018"),
        ("2020-01-01T00:00:00.000000", "01.01.2020"),
        ("", ""),
        ("Invalid Date", "Invalid Date"),
    ]


# Фикстура для тестовых транзакций по операциям (из generators.py)
@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
        {
            "id": 939719570,
            "operationAmount": {"amount": "9824.07", "currency": {"code": "USD"}},
            "description": "Перевод организации",
        },
        {
            "id": 142264268,
            "operationAmount": {"amount": "79114.93", "currency": {"code": "USD"}},
            "description": "Перевод со счета на счет",
        },
        {
            "id": 873106923,
            "operationAmount": {"amount": "43318.34", "currency": {"code": "RUB"}},
            "description": "Перевод со счета на счет",
        },
        {
            "id": 895315941,
            "operationAmount": {"amount": "56883.54", "currency": {"code": "USD"}},
            "description": "Перевод с карты на карту",
        },
    ]


# Фикстура для автоматическое удаление тестовых файлов (из decorators.py)
@pytest.fixture(autouse=True)
def clean_log_files() -> Generator[None, None, None]:
    """Автоматически удаляет лог-файлы после тестов"""
    yield
    for filename in ["file_success.log", "file_error.log"]:
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass
