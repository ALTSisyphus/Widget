# Тесты: проверяют корректность работы функций модуля.
# Эти тесты используют pytest и unittest.mock для изоляции сетевых вызовов.

import json

import pytest

from src.utils import read_json_file

# Создаём временный JSON-файл со списком и проверяем, что функция вернёт тот же список.


def test_read_existing_json(tmp_path):
    data = [{"a": 1}, {"b": 2}]
    p = tmp_path / "ops.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    got = read_json_file(str(p))
    assert isinstance(got, list)
    assert got == data


# Тест на случай пустого файла: функция должна вернуть пустой список.


def test_read_empty_file(tmp_path):
    p = tmp_path / "empty.json"
    p.write_text("", encoding="utf-8")
    assert read_json_file(str(p)) == []


# Если JSON не список (например объект) — ожидаем пустой список.


def test_read_non_list_json(tmp_path):
    p = tmp_path / "obj.json"
    p.write_text(json.dumps({"a": 1}), encoding="utf-8")
    assert read_json_file(str(p)) == []


# Если файла не существует — функция возвращает пустой список.


def test_read_not_found():
    assert read_json_file("/non/existent/file.json") == []
