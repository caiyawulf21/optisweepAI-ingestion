from __future__ import annotations

from pathlib import Path
from typing import Any

from shared_pipeline_stages.stage_6_5.json_utils import read_json

CONTEXT_PATHS = (
    "stage_4_operational_context/operational_context.json",
)
# Prefer enriched/latest first. Cover both incidence (OCR) and operational
# (source_artifacts) layouts so Stage 10/11 never silently skip a source root.
ARTIFACT_PATHS = (
    "stage_3_artifact_enrichment/source_artifacts_enriched.json",
    "stage_2_ocr_artifacts/source_artifacts_enriched.json",
    "stage_2_ocr_artifacts/source_artifacts.json",
    "stage_2_source_artifacts/source_artifacts_enriched.json",
    "stage_2_source_artifacts/source_artifacts.json",
    "stage_8_relationship_linking/source_artifacts_linked.json",
)


def load_source_roots_contexts_and_artifacts(
    source_roots: list[str | Path],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    contexts: list[dict[str, Any]] = []
    artifacts: list[dict[str, Any]] = []
    warnings: list[str] = []
    seen_context: set[str] = set()
    seen_artifact: set[str] = set()

    for source_root in source_roots:
        root = Path(source_root)
        source_id = root.name
        for relative in CONTEXT_PATHS:
            path = root / relative
            if not path.exists():
                continue
            payload = read_json(path)
            if not isinstance(payload, list):
                warnings.append(f"{path} must contain a JSON list.")
                continue
            for record in payload:
                if not isinstance(record, dict):
                    continue
                context_id = str(record.get("context_id") or "").strip()
                if not context_id or context_id in seen_context:
                    continue
                seen_context.add(context_id)
                enriched = dict(record)
                enriched.setdefault("source_id", source_id)
                enriched.setdefault("source_root", str(root))
                contexts.append(enriched)

        artifact_path = _first_existing(root, ARTIFACT_PATHS)
        if artifact_path is None:
            warnings.append(f"No source artifacts found under {root}.")
            continue
        payload = read_json(artifact_path)
        if not isinstance(payload, list):
            warnings.append(f"{artifact_path} must contain a JSON list.")
            continue
        for record in payload:
            if not isinstance(record, dict):
                continue
            artifact_id = str(record.get("artifact_id") or "").strip()
            if not artifact_id or artifact_id in seen_artifact:
                continue
            seen_artifact.add(artifact_id)
            enriched = dict(record)
            enriched.setdefault("source_id", source_id)
            enriched.setdefault("source_root", str(root))
            artifacts.append(enriched)

    return contexts, artifacts, warnings


def _first_existing(root: Path, relatives: tuple[str, ...]) -> Path | None:
    for relative in relatives:
        path = root / relative
        if path.exists():
            return path
    return None
