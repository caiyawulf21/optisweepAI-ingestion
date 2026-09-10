"""JSON helpers for local ingestion outputs."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


def _to_jsonable(data: Any) -> Any:
    if hasattr(data, "model_dump"):
        return data.model_dump(mode="json")
    if hasattr(data, "dict"):
        return data.dict()
    if isinstance(data, list):
        return [_to_jsonable(item) for item in data]
    if isinstance(data, tuple):
        return [_to_jsonable(item) for item in data]
    if isinstance(data, dict):
        return {key: _to_jsonable(value) for key, value in data.items()}
    return data


def _windows_long_path(path: Path) -> str:
    raw = str(path.resolve())
    if os.name == "nt" and not raw.startswith("\\\\?\\"):
        return "\\\\?\\" + raw
    return raw


def write_json(path: str | Path, data: Any) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(_to_jsonable(data), ensure_ascii=False, indent=2) + "\n"
    with open(_windows_long_path(output_path), "w", encoding="utf-8") as handle:
        handle.write(payload)


def read_json(path: str | Path) -> Any:
    with open(_windows_long_path(Path(path)), encoding="utf-8-sig") as handle:
        return json.loads(handle.read())
