"""Shared helpers for brain/migration/ scripts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]


def content_hash(*parts: str) -> str:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"sha256:{digest}"


def load_json(path: Path) -> Any:
    # utf-8-sig transparently strips a BOM if present and behaves exactly
    # like utf-8 when it is not; several stage outputs in this repo are
    # BOM-prefixed (Windows tooling) and a plain utf-8 read raises on them.
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _extended_length_path(path: Path) -> Path:
    """Prefix an absolute Windows path with \\\\?\\ so paths beyond the
    classic 260-char MAX_PATH (several generated finalized-runbook filenames
    exceed it) are still readable. A no-op on non-Windows or already-prefixed
    paths.
    """
    raw = str(path.resolve())
    if raw.startswith("\\\\?\\") or not raw[1:3] == ":\\":
        return path
    return Path("\\\\?\\" + raw)


def load_json_dir(dir_path: Path) -> list[Any]:
    """Load every *.json file in a directory. Falls back to an extended-length
    path for any file that raises OSError on a normal open (Windows MAX_PATH),
    and only skips (with a warning) if that also fails, so migration never
    silently drops a record it could have read.
    """
    records = []
    skipped = []
    if not dir_path.is_dir():
        return records
    for name in sorted(dir_path.iterdir()):
        if name.suffix != ".json":
            continue
        try:
            records.append(load_json(name))
        except OSError:
            try:
                records.append(load_json(_extended_length_path(name)))
            except OSError:
                skipped.append(str(name))
    if skipped:
        print(f"  WARNING: skipped {len(skipped)} unreadable file(s) in {dir_path}")
        for s in skipped:
            print(f"    - {s}")
    return records


def dump_records(records: list, output_path: Path) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [json.loads(r.model_dump_json()) for r in records]
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return len(payload)
