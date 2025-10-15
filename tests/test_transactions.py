from pathlib import Path

import pytest

from src.transactions import (
    count_transactions_by_categories,
    filter_transactions_by_currency,
    filter_transactions_by_description,
    filter_transactions_by_status,
    format_transaction,
    load_transactions,
    sort_transactions_by_date,
)


@pytest.fixture()
def sample_transactions() -> list[dict[str, object]]:
    return [
        {
            "id": 1,
            "date": "2020-01-01T10:00:00",
            "description": "Оплата мобильной связи",
            "from": "Visa Classic 1234567812345678",
            "to": "МТС",
            "state": "EXECUTED",
            "operationAmount": {"amount": "500", "currency": {"code": "RUB", "name": "руб."}},
        },
        {
            "id": 2,
            "date": "2020-01-02T10:00:00",
            "description": "Перевод другу",
            "from": "MasterCard 9876543210987654",
            "to": "Счет 1234567890",
            "state": "CANCELED",
            "operationAmount": {"amount": "100", "currency": {"code": "USD", "name": "USD"}},
        },
        {
            "id": 3,
            "date": "2019-12-25T10:00:00",
            "description": "Оплата мобильной связи",
            "from": "Счет 12345678901234567890",
            "to": "Tele2",
            "state": "EXECUTED",
            "operationAmount": {"amount": "300", "currency": {"code": "RUB", "name": "руб."}},
        },
    ]


def test_filter_transactions_by_description(sample_transactions: list[dict[str, object]]) -> None:
    result = filter_transactions_by_description(sample_transactions, "оплата")
    assert len(result) == 2
    assert all("оплата" in item["description"].lower() for item in result)


def test_filter_transactions_by_description_empty_search(sample_transactions: list[dict[str, object]]) -> None:
    assert filter_transactions_by_description(sample_transactions, "") == sample_transactions


def test_count_transactions_by_categories(sample_transactions: list[dict[str, object]]) -> None:
    counts = count_transactions_by_categories(sample_transactions, ["оплата", "перевод"])
    assert counts == {"оплата": 2, "перевод": 1}


def test_filter_transactions_by_status(sample_transactions: list[dict[str, object]]) -> None:
    executed = filter_transactions_by_status(sample_transactions, "executed")
    assert len(executed) == 2


def test_sort_transactions_by_date(sample_transactions: list[dict[str, object]]) -> None:
    sorted_transactions = sort_transactions_by_date(sample_transactions, ascending=True)
    assert [item["id"] for item in sorted_transactions] == [3, 1, 2]


def test_filter_transactions_by_currency(sample_transactions: list[dict[str, object]]) -> None:
    rub_transactions = filter_transactions_by_currency(sample_transactions, "rub")
    assert [item["id"] for item in rub_transactions] == [1, 3]


def test_format_transaction(sample_transactions: list[dict[str, object]]) -> None:
    formatted = format_transaction(sample_transactions[0])
    assert "Оплата мобильной связи" in formatted
    assert "Сумма: 500 руб." in formatted
    assert "Visa Classic 1234 56** **** 5678 -> МТС" in formatted


def test_load_transactions_json(tmp_path: Path) -> None:
    data_path = tmp_path / "ops.json"
    data_path.write_text("""[{\"date\": \"2020-01-01T10:00:00\", \"description\": \"Test\", \"operationAmount\": {\"amount\": \"10\", \"currency\": {\"code\": \"RUB\", \"name\": \"руб.\"}}, \"state\": \"EXECUTED\"}]""", encoding="utf-8")
    result = load_transactions(data_path)
    assert result[0]["description"] == "Test"


def test_load_transactions_csv(tmp_path: Path) -> None:
    data_path = tmp_path / "ops.csv"
    data_path.write_text(
        "id,date,description,from,to,state,amount,currency_code,currency_name\n"
        "1,2020-01-01T10:00:00,Test,Card 1234,Account 4321,EXECUTED,100,RUB,руб.\n",
        encoding="utf-8",
    )
    result = load_transactions(data_path)
    assert result[0]["operationAmount"]["currency"]["code"] == "RUB"


def test_load_transactions_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_transactions(tmp_path / "missing.json")


def test_load_transactions_invalid_format(tmp_path: Path) -> None:
    data_path = tmp_path / "ops.txt"
    data_path.write_text("data", encoding="utf-8")
    with pytest.raises(ValueError):
        load_transactions(data_path)
