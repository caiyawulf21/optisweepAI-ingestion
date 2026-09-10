from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


def _windows_long_path(path: Path) -> str:
    raw = str(path if path.is_absolute() else path.absolute())
    if os.name == "nt" and not raw.startswith("\\\\?\\"):
        return "\\\\?\\" + raw
    return raw


def to_jsonable(data: Any) -> Any:
    if hasattr(data, "model_dump"):
        return data.model_dump(mode="json")
    if isinstance(data, list):
        return [to_jsonable(item) for item in data]
    if isinstance(data, dict):
        return {key: to_jsonable(value) for key, value in data.items()}
    return data


def write_json(path: str | Path, data: Any) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(to_jsonable(data), ensure_ascii=False, indent=2) + "\n"
    with open(_windows_long_path(output_path), "w", encoding="utf-8") as handle:
        handle.write(payload)


def read_json(path: str | Path) -> Any:
    with open(_windows_long_path(Path(path)), encoding="utf-8-sig") as handle:
        return json.loads(handle.read())
