import os

import pytest

from src.decorators import log


# Тестовые функции
@log()
def console_success(a: int, b: int) -> int:
    return a + b


@log()
def console_error(a: int, b: int) -> float:  # Исправлен тип возвращаемого значения
    return a / b


@log("file_success.log")
def file_success(a: int, b: int) -> int:
    return a * b


@log("file_error.log")
def file_error(a: int, b: int) -> float:  # Исправлен тип возвращаемого значения
    return a / b


def test_successful_console_log(capsys: pytest.CaptureFixture) -> None:  # Добавлена аннотация типа
    """Тест успешного выполнения с выводом в консоль"""
    assert console_success(2, 3) == 5
    captured = capsys.readouterr()
    assert "console_success ok" in captured.out


def test_error_console_log(capsys: pytest.CaptureFixture) -> None:  # Добавлена аннотация типа
    """Тест ошибки с выводом в консоль"""
    try:
        console_error(5, 0)
    except ZeroDivisionError:
        pass

    captured = capsys.readouterr()
    assert "console_error error: ZeroDivisionError" in captured.out
    assert "Inputs: (5, 0)" in captured.out


def test_successful_file_logging() -> None:
    """Тест успешной записи в файл"""
    if os.path.exists("file_success.log"):
        os.remove("file_success.log")

    assert file_success(3, 4) == 12

    with open("file_success.log", "r", encoding="utf-8") as f:
        content = f.read()

    assert "file_success ok" in content


def test_error_file_logging() -> None:
    """Тест записи ошибки в файл"""
    if os.path.exists("file_error.log"):
        os.remove("file_error.log")

    try:
        file_error(10, 0)
    except ZeroDivisionError:
        pass

    with open("file_error.log", "r", encoding="utf-8") as f:
        content = f.read()

    assert "file_error error: ZeroDivisionError" in content
    assert "Inputs: (10, 0)" in content
