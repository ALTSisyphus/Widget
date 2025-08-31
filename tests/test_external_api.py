# Тесты для external_api.convert_to_rub.
# Мокируем requests.get чтобы не обращаться к реальному API и проверяем поведение при разных вариантах ответа от сервера.

import os
from unittest.mock import Mock, patch

from src.external_api import API_KEY_ENV, convert_to_rub


def test_convert_rub_no_api_call():
    tx = {"operationAmount": {"amount": "123.45", "currency": {"code": "RUB"}}}
    assert convert_to_rub(tx) == 123.45


# Мокаем вызов requests.get чтобы контролировать ответы внешнего API
@patch("src.external_api.requests.get")
def test_convert_usd_calls_api(mock_get, monkeypatch):
    # Prepare mock response
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"result": 7654.32}
    mock_get.return_value = mock_resp

    # Ensure API key exists in env for header behavior
    # Подменяем переменную окружения с API-ключом для теста
    monkeypatch.setenv(API_KEY_ENV, "testkey")

    tx = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}
    res = convert_to_rub(tx)
    assert isinstance(res, float)
    assert res == 7654.32
    # Ensure requests.get was called with expected params
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    # params must include conversion fields
    assert kwargs.get("params") is not None
    assert kwargs["params"]["from"] == "USD"
    assert kwargs["params"]["to"] == "RUB"


# Мокаем вызов requests.get чтобы контролировать ответы внешнего API
@patch("src.external_api.requests.get")
def test_convert_api_fallback_rate(mock_get, monkeypatch):
    mock_resp = Mock()
    mock_resp.status_code = 200
    # No 'result' but 'info' -> 'rate'
    mock_resp.json.return_value = {"info": {"rate": 75.0}}
    mock_get.return_value = mock_resp

    # Подменяем переменную окружения с API-ключом для теста
    monkeypatch.setenv(API_KEY_ENV, "testkey")
    tx = {"operationAmount": {"amount": "2", "currency": {"code": "USD"}}}
    assert convert_to_rub(tx) == 150.0


# Мокаем вызов requests.get чтобы контролировать ответы внешнего API
@patch("src.external_api.requests.get")
def test_api_error_returns_zero(mock_get):
    mock_get.side_effect = Exception("network error")
    tx = {"operationAmount": {"amount": "1", "currency": {"code": "EUR"}}}
    assert convert_to_rub(tx) == 0.0
