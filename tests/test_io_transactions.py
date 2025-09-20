"""Тесты для функций чтения транзакций из CSV и Excel."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

from src.io_transactions import read_transactions_csv, read_transactions_excel


@pytest.fixture()
def sample_df() -> pd.DataFrame:
    """Пример датафрейма для подмены данных."""
    return pd.DataFrame(
        [
            {"date": "2024-01-01", "amount": 100.5, "category": "Еда"},
            {"date": "2024-01-02", "amount": -20.0, "category": "Транспорт"},
        ]
    )


def test_read_transactions_csv_with_mock(
    sample_df: pd.DataFrame, tmp_path: Path
) -> None:
    """Тест чтения CSV с использованием мока pandas.read_csv."""
    fake_path = tmp_path / "fake.csv"
    fake_path.write_text("ignored")
    with patch(
        "src.io_transactions.pd.read_csv", return_value=sample_df
    ) as mocked_read:
        rows = read_transactions_csv(fake_path)
        assert isinstance(rows, list)
        assert rows[0]["amount"] == 100.5
        mocked_read.assert_called_once()


def test_read_transactions_excel_with_mock(
    sample_df: pd.DataFrame, tmp_path: Path
) -> None:
    """Тест чтения Excel с использованием мока pandas.read_excel."""
    fake_path = tmp_path / "fake.xlsx"
    fake_path.write_text("ignored")
    with patch(
        "src.io_transactions.pd.read_excel", return_value=sample_df
    ) as mocked_read:
        rows = read_transactions_excel(fake_path, sheet_name=0)
        assert len(rows) == 2
        assert rows[1]["category"] == "Транспорт"
        mocked_read.assert_called_once()


def test_read_transactions_csv_integration(tmp_path: Path) -> None:
    """Интеграционный тест: создаём временный CSV и читаем его."""
    df = pd.DataFrame(
        [
            {"date": "2024-01-01", "amount": 100.5, "category": "Еда"},
            {"date": "2024-01-02", "amount": -20.0, "category": "Транспорт"},
        ]
    )
    target = tmp_path / "transactions.csv"
    df.to_csv(target, index=False)
    rows = read_transactions_csv(target)
    assert isinstance(rows, list)
    assert len(rows) == 2
    assert rows[0]["category"] == "Еда"


def test_read_transactions_excel_integration(tmp_path: Path) -> None:
    """Интеграционный тест: создаём временный Excel и читаем его."""
    df = pd.DataFrame(
        [
            {"date": "2024-01-01", "amount": 100.5, "category": "Еда"},
            {"date": "2024-01-02", "amount": -20.0, "category": "Транспорт"},
        ]
    )
    target = tmp_path / "transactions.xlsx"
    df.to_excel(target, index=False)
    rows = read_transactions_excel(target)
    assert isinstance(rows, list)
    assert len(rows) == 2
    assert rows[1]["amount"] == -20.0


def test_missing_file_raises() -> None:
    """Функции должны выбрасывать FileNotFoundError, если файла нет."""
    with pytest.raises(FileNotFoundError):
        read_transactions_csv("nope.csv")
    with pytest.raises(FileNotFoundError):
        read_transactions_excel("nope.xlsx")
