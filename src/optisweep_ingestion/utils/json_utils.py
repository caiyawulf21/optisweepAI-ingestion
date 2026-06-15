"""JSON helpers for local ingestion outputs."""

from __future__ import annotations

import json
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


def write_json(path: str | Path, data: Any) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(_to_jsonable(data), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))
