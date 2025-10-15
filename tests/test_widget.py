import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "data, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card(data: str, expected: str) -> None:
    assert mask_account_card(data) == expected


def test_get_date() -> None:
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"
