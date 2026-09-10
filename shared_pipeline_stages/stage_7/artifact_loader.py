from __future__ import annotations

from pathlib import Path
from typing import Any

from shared_pipeline_stages.stage_6_5.json_utils import read_json
from shared_pipeline_stages.stage_6_5.schemas import RunbookPoolEntry

ARTIFACT_RELATIVE_PATHS = (
    "stage_3_artifact_enrichment/source_artifacts_enriched.json",
    "stage_2_ocr_artifacts/source_artifacts_enriched.json",
    "stage_2_ocr_artifacts/source_artifacts.json",
    "stage_2_source_artifacts/source_artifacts_enriched.json",
    "stage_2_source_artifacts/source_artifacts.json",
    "stage_8_relationship_linking/source_artifacts_linked.json",
)


def load_artifact_index_from_pool(pool_dir: str | Path) -> dict[str, dict[str, Any]]:
    pool_path = Path(pool_dir) / "runbook_pool.json"
    payload = read_json(pool_path)
    entries = payload.get("entries") if isinstance(payload, dict) else payload
    if not isinstance(entries, list):
        raise ValueError("runbook_pool.json must contain an entries list.")
    source_roots: set[Path] = set()
    for item in entries:
        entry = RunbookPoolEntry.model_validate(item)
        if not entry.source_path:
            continue
        source_roots.add(_source_root_from_runbook_path(Path(entry.source_path)))
    artifact_index: dict[str, dict[str, Any]] = {}
    for source_root in sorted(source_roots):
        artifact_path = _find_artifacts_file(source_root)
        if artifact_path is None:
            continue
        artifacts = read_json(artifact_path)
        if not isinstance(artifacts, list):
            continue
        for artifact in artifacts:
            if not isinstance(artifact, dict):
                continue
            artifact_id = str(artifact.get("artifact_id") or "").strip()
            if artifact_id:
                artifact_index[artifact_id] = artifact
    return artifact_index


def _source_root_from_runbook_path(runbook_path: Path) -> Path:
    parts = runbook_path.parts
    if "stage_6_finalized_runbooks" in parts:
        index = parts.index("stage_6_finalized_runbooks")
        return Path(*parts[:index])
    return runbook_path.parent.parent.parent


def _find_artifacts_file(source_root: Path) -> Path | None:
    for relative in ARTIFACT_RELATIVE_PATHS:
        candidate = source_root / relative
        if candidate.is_file():
            return candidate
    return None
