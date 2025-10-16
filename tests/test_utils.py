# Тесты: проверяют корректность работы функций модуля.

import json
from pathlib import Path

from src.utils import read_json_file

# Создаём временный JSON-файл со списком и проверяем, что функция вернёт тот же список.


def test_read_existing_json(tmp_path: Path) -> None:
    p = tmp_path / "data.json"
    sample = [{"a": 1}, {"b": 2}]
    p.write_text(json.dumps(sample), encoding="utf-8")
    assert read_json_file(str(p)) == sample


# Если JSON не список (например объект) — ожидаем пустой список.


def test_read_non_list_json(tmp_path: Path) -> None:
    p = tmp_path / "obj.json"
    p.write_text(json.dumps({"a": 1}), encoding="utf-8")
    assert read_json_file(str(p)) == []


# Если файла не существует — функция возвращает пустой список.


def test_read_not_found() -> None:
    assert read_json_file("/non/existent/file.json") == []
