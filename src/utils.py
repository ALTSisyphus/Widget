import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Iterator

# Настройка ведения журнала для модуля utils
_project_root = Path(__file__).resolve().parents[1]
_logs_dir = _project_root / "logs"
_logs_dir.mkdir(parents=True, exist_ok=True)
_logger = logging.getLogger("utils")
if not _logger.handlers:
    _file_handler = logging.FileHandler(_logs_dir / "utils.log", mode="w", encoding="utf-8")
    _file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    _file_handler.setFormatter(_file_formatter)
    _logger.addHandler(_file_handler)
_logger.setLevel(logging.DEBUG)
_logger.propagate = False


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
    _logger.debug("read_json_file called with path=%s", path)
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
    except (OSError, json.JSONDecodeError) as e:
        _logger.exception("Failed to read or parse JSON file %s: %s", path, e)
        return []
