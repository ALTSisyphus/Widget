from typing import Callable

import pytest

from main import main


def make_input_responses(responses: list[str]) -> Callable[[str], str]:
    iterator = iter(responses)

    def _inner(_: str = "") -> str:
        try:
            return next(iterator)
        except StopIteration:  # pragma: no cover - defensive branch
            raise AssertionError("Недостаточно данных для имитации пользовательского ввода") from None

    return _inner


def test_main_success_flow(capsys: pytest.CaptureFixture[str]) -> None:
    responses = [
        "1",  # меню
        "test",  # некорректный статус
        "executed",  # корректный статус
        "да",  # сортировка по дате
        "по возрастанию",  # порядок
        "нет",  # только рублевые
        "да",  # фильтр по описанию
        "перевод",  # ключевое слово
    ]
    main(make_input_responses(responses))
    captured = capsys.readouterr().out
    assert "Для обработки выбран JSON-файл." in captured
    assert "Статус операции \"TEST\" недоступен." in captured
    assert "Операции отфильтрованы по статусу \"EXECUTED\"" in captured
    assert "Всего банковских операций в выборке" in captured
    assert "Перевод с карты на карту" in captured
    assert "Перевод организации" in captured


def test_main_empty_selection(capsys: pytest.CaptureFixture[str]) -> None:
    responses = [
        "2",  # меню
        "pending",  # статус
        "нет",  # сортировка
        "да",  # только рублевые
        "да",  # фильтр по описанию
        "несуществующее слово",  # поиск
    ]
    main(make_input_responses(responses))
    captured = capsys.readouterr().out
    assert "Для обработки выбран CSV-файл." in captured
    assert "Не найдено ни одной транзакции" in captured
