import pytest

from src.processing import filter_by_state, sort_by_date


# Фикстура для тестовых операций
@pytest.fixture
def operations_data() -> list[dict]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "CANCELED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 3, "state": "EXECUTED", "date": "2020-01-01T00:00:00.000000"},
        {"id": 4, "state": "PENDING", "date": "2019-12-31T23:59:59.999999"},
        {"id": 5, "state": "EXECUTED", "date": "2018-01-01T00:00:00.000000"},
    ]


# Тесты фильтрации по статусу
@pytest.mark.parametrize(
    "state, expected_ids", [("EXECUTED", [1, 3, 5]), ("CANCELED", [2]), ("PENDING", [4]), ("UNKNOWN", [])]
)
def test_filter_by_state(operations_data: list[dict], state: str, expected_ids: list[int]) -> None:
    result = filter_by_state(operations_data, state)
    assert [op["id"] for op in result] == expected_ids


# Тесты сортировки по дате
def test_sort_by_date(operations_data: list[dict]) -> None:
    # Сортировка по убыванию (новые первые)
    result_desc = sort_by_date(operations_data)
    assert [op["id"] for op in result_desc] == [3, 1, 4, 2, 5]

    # Сортировка по возрастанию (старые первые)
    result_asc = sort_by_date(operations_data, reverse=False)
    assert [op["id"] for op in result_asc] == [5, 2, 4, 1, 3]
