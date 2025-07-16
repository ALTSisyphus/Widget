import pytest

from src.processing import filter_by_state, sort_by_date


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
    assert [op["id"] for op in result_desc] == [3, 4, 1, 2, 5]  # Исправленный порядок

    # Сортировка по возрастанию (старые первые)
    result_asc = sort_by_date(operations_data, reverse=False)
    assert [op["id"] for op in result_asc] == [5, 2, 1, 4, 3]  # Исправленный порядок
