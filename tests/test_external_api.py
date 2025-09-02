# Тесты для external_api.convert_to_rub.
# Мокируем requests.get, чтобы не обращаться к реальному API и проверить поведение при разных вариантах ответа.

from unittest.mock import Mock, patch

import pytest

from src.external_api import API_KEY_ENV, convert_to_rub


def test_convert_rub_no_api_call() -> None:
    tx = {"operationAmount": {"amount": "123.45", "currency": {"code": "RUB"}}}
    assert convert_to_rub(tx) == 123.45


@patch("src.external_api.requests.get")
def test_convert_api_result_field(mock_get: Mock, monkeypatch: pytest.MonkeyPatch) -> None:
    mock_resp = Mock()
    mock_resp.raise_for_status = Mock()
    mock_resp.json.return_value = {"result": 250.0}
    mock_get.return_value = mock_resp

    # Подменяем переменную окружения с API-ключом для теста
    monkeypatch.setenv(API_KEY_ENV, "testkey")

    tx = {"operationAmount": {"amount": "2", "currency": {"code": "USD"}}}
    assert convert_to_rub(tx) == 250.0


@patch("src.external_api.requests.get")
def test_convert_api_fallback_rate(mock_get: Mock, monkeypatch: pytest.MonkeyPatch) -> None:
    mock_resp = Mock()
    mock_resp.raise_for_status = Mock()
    mock_resp.json.return_value = {"info": {"rate": 75.0}}
    mock_get.return_value = mock_resp

    monkeypatch.setenv(API_KEY_ENV, "testkey")
    tx = {"operationAmount": {"amount": "2", "currency": {"code": "USD"}}}
    assert convert_to_rub(tx) == 150.0


@patch("src.external_api.requests.get")
def test_api_error_returns_zero(mock_get: Mock) -> None:
    mock_get.side_effect = Exception("network error")
    tx = {"operationAmount": {"amount": "1", "currency": {"code": "EUR"}}}
    assert convert_to_rub(tx) == 0.0
