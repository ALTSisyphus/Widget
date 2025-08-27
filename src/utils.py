from __future__ import annotations

import json
import os
from typing import Any, Dict, List


def read_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список словарей с транзакциями.
    Если файл пустой, не найден, некорректен или верхний уровень не список — вернёт [].

    :param file_path: Путь до JSON-файла (например, "data/operations.json").
    :return: Список транзакций (List[Dict[str, Any]]) либо пустой список.
    """
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

    return data if isinstance(data, list) else []
