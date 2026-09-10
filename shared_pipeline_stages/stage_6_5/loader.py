from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from shared_pipeline_stages.stage_6_5.json_utils import read_json

STAGE6_GLOB = "**/stage_6_finalized_runbooks/finalized_runbooks/*.json"


def _list_finalized_json_files(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    names = sorted(name for name in os.listdir(directory) if name.lower().endswith(".json"))
    return [directory / name for name in names]


def discover_finalized_runbook_paths(source_roots: list[str | Path]) -> list[Path]:
    discovered: set[Path] = set()
    for root in source_roots:
        base = Path(root)
        if not base.exists():
            raise FileNotFoundError(f"Source root not found: {base}")
        if base.is_file() and base.suffix.lower() == ".json":
            discovered.add(base)
            continue
        if base.name == "finalized_runbooks" and base.is_dir():
            discovered.update(_list_finalized_json_files(base))
            continue
        if base.name == "stage_6_finalized_runbooks" and base.is_dir():
            finalized_dir = base / "finalized_runbooks"
            if finalized_dir.is_dir():
                discovered.update(_list_finalized_json_files(finalized_dir))
                continue
        if (base / "stage_6_finalized_runbooks" / "finalized_runbooks").is_dir():
            discovered.update(
                _list_finalized_json_files(base / "stage_6_finalized_runbooks" / "finalized_runbooks")
            )
            continue
        for stage6 in base.glob("**/stage_6_finalized_runbooks"):
            discovered.update(_list_finalized_json_files(stage6 / "finalized_runbooks"))
    paths = sorted(discovered, key=lambda p: str(p).lower())
    if not paths:
        raise FileNotFoundError(
            "No Stage 6 finalized runbooks found. Expected "
            f"{STAGE6_GLOB} under each --source-root."
        )
    return paths


def load_finalized_runbooks(source_roots: list[str | Path]) -> tuple[list[dict[str, Any]], list[str]]:
    runbooks: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    warnings: list[str] = []
    for path in discover_finalized_runbook_paths(source_roots):
        payload = read_json(path)
        if not isinstance(payload, dict):
            raise ValueError(f"Finalized runbook must be a JSON object: {path}")
        errors = validate_finalized_runbook(payload)
        if errors:
            raise ValueError(f"Invalid finalized runbook {path}: " + "; ".join(errors))
        procedure_id = str(payload.get("procedure_id") or "")
        if procedure_id in seen_ids:
            warnings.append(
                f"Skipped duplicate procedure_id {procedure_id} from {path}"
            )
            continue
        seen_ids.add(procedure_id)
        payload["_source_path"] = str(path)
        runbooks.append(payload)
    return runbooks, warnings


def validate_finalized_runbook(runbook: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not str(runbook.get("procedure_id") or "").strip():
        errors.append("procedure_id is required")
    if not str(runbook.get("candidate_id") or "").strip():
        errors.append("candidate_id is required")
    if not str(runbook.get("title") or "").strip():
        errors.append("title is required")
    steps = runbook.get("steps")
    if not isinstance(steps, list) or not steps:
        errors.append("steps must be a non-empty list")
    metadata = runbook.get("metadata") or {}
    if not isinstance(metadata, dict):
        errors.append("metadata must be an object when present")
    return errors
