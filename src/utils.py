import json
from pathlib import Path
from typing import Any, Dict, List


def read_json_file(path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл по пути `path` и возвращает список словарей.

    Возвращает пустой список, если:
      - путь пустой или файл не найден,
      - файл пустой,
      - файл содержит некорректный JSON,
      - JSON является не списком.

    :param path: путь к JSON-файлу
    :return: список словарей (transactions) или пустой список
    """
    if not path:
        return []

    p = Path(path)
    try:
        if not p.exists():
            return []
        if p.stat().st_size == 0:
            return []

        text = p.read_text(encoding="utf-8")
        if not text or not text.strip():
            return []

        data = json.loads(text)
        if not isinstance(data, list):
            return []

        return [item for item in data if isinstance(item, dict)]
    except (OSError, json.JSONDecodeError):
        return []
