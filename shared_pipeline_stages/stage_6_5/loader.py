from __future__ import annotations

from pathlib import Path
from typing import Any

from shared_pipeline_stages.stage_6_5.json_utils import read_json

STAGE6_GLOB = "**/stage_6_finalized_runbooks/finalized_runbooks/*.json"


def discover_finalized_runbook_paths(source_roots: list[str | Path]) -> list[Path]:
    discovered: set[Path] = set()
    for root in source_roots:
        base = Path(root)
        if not base.exists():
            raise FileNotFoundError(f"Source root not found: {base}")
        if base.is_file() and base.suffix.lower() == ".json":
            discovered.add(base.resolve())
            continue
        if base.name == "finalized_runbooks" and base.is_dir():
            discovered.update(path.resolve() for path in base.glob("*.json"))
            continue
        if base.name == "stage_6_finalized_runbooks" and base.is_dir():
            finalized_dir = base / "finalized_runbooks"
            if finalized_dir.is_dir():
                discovered.update(path.resolve() for path in finalized_dir.glob("*.json"))
                continue
        discovered.update(path.resolve() for path in base.glob(STAGE6_GLOB))
    paths = sorted(discovered)
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
    if str(metadata.get("merge_status") or "") != "source_finalized":
        errors.append('metadata.merge_status must be "source_finalized"')
    return errors
