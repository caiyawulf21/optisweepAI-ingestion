"""Stage 8 deterministic relationship linking for source artifacts, context, and runbooks."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any
import hashlib

from operationalknowledgeingestion.src.optisweep_ingestion.stage_paths import stage_dir
from operationalknowledgeingestion.src.optisweep_ingestion.tools.relationship_linker import (
    apply_relationship_links,
    build_relationship_links,
)
from operationalknowledgeingestion.src.optisweep_ingestion.utils.json_utils import read_json, write_json


def load_finalized_runbooks(finalized_dir: Path) -> list[dict[str, Any]]:
    runbooks: list[dict[str, Any]] = []
    for path in sorted(finalized_dir.glob("*.json")):
        payload = read_json(path)
        if isinstance(payload, dict):
            runbooks.append(payload)
    return runbooks


def _first_existing(output_dir: Path, stage: str, filename: str) -> Path | None:
    candidates = [stage_dir(output_dir, stage) / filename, output_dir / filename]
    for path in candidates:
        if path.exists():
            return path
    return None


def _read_list(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not path.exists():
        return []
    payload = read_json(path)
    if not isinstance(payload, list):
        raise ValueError(f"{path} must contain a JSON list.")
    return payload


def link_source_relationships(
    *,
    output_dir: str | Path,
    source_artifacts_path: str | Path | None = None,
    operational_context_path: str | Path | None = None,
    finalized_runbooks_dir: str | Path | None = None,
    runbook_candidates_path: str | Path | None = None,
    infer_shared_artifact_links: bool = True,
) -> dict[str, Any]:
    output_path = Path(output_dir)
    stage8_dir = stage_dir(output_path, "8")
    stage8_dir.mkdir(parents=True, exist_ok=True)

    artifacts_path = Path(source_artifacts_path) if source_artifacts_path else _first_existing(output_path, "3", "source_artifacts_enriched.json")
    if artifacts_path is None or not artifacts_path.exists():
        artifacts_path = _first_existing(output_path, "2", "source_artifacts_enriched.json")
    if artifacts_path is None or not artifacts_path.exists():
        artifacts_path = _first_existing(output_path, "2", "source_artifacts.json")
    if artifacts_path is None or not artifacts_path.exists():
        raise FileNotFoundError("Stage 8 requires source artifacts from Stage 2 or Stage 3.")

    context_path = Path(operational_context_path) if operational_context_path else _first_existing(output_path, "4", "operational_context.json")
    if context_path is None or not context_path.exists():
        raise FileNotFoundError("Stage 8 requires operational_context.json from Stage 4.")

    runbooks_dir = Path(finalized_runbooks_dir) if finalized_runbooks_dir else stage_dir(output_path, "6") / "finalized_runbooks"
    if not runbooks_dir.exists() or not any(runbooks_dir.glob("*.json")):
        raise FileNotFoundError(f"Stage 8 requires finalized runbooks in {runbooks_dir}.")

    candidates_path = Path(runbook_candidates_path) if runbook_candidates_path else _first_existing(output_path, "5", "runbook_candidates.json")
    candidates = _read_list(candidates_path)

    artifacts = _read_list(artifacts_path)
    contexts = _read_list(context_path)
    runbooks = load_finalized_runbooks(runbooks_dir)

    links, link_payload = build_relationship_links(
        artifacts=artifacts,
        contexts=contexts,
        runbooks=runbooks,
        candidates=candidates,
        infer_shared_artifact_links=infer_shared_artifact_links,
    )
    linked_artifacts, linked_contexts, linked_runbooks = apply_relationship_links(
        artifacts=artifacts,
        contexts=contexts,
        runbooks=runbooks,
        adjacency=link_payload["adjacency"],
    )

    linked_runbooks_dir = stage8_dir / "finalized_runbooks_linked"
    linked_runbooks_dir.mkdir(parents=True, exist_ok=True)
    for runbook in linked_runbooks:
        candidate_id = str(runbook.get("candidate_id") or runbook.get("procedure_id") or "runbook").strip()
        safe_name = _safe_runbook_filename(candidate_id)
        write_json(linked_runbooks_dir / f"{safe_name}.json", runbook)
    write_json(stage8_dir / "finalized_runbooks_linked.json", linked_runbooks)

    write_json(stage8_dir / "source_artifacts_linked.json", linked_artifacts)
    write_json(stage8_dir / "operational_context_linked.json", linked_contexts)
    write_json(stage8_dir / "relationship_links.json", links)

    stats = link_payload["stats"]
    report = {
        "stage": "8",
        "stage_name": "relationship_linking",
        "generated_at": datetime.now(UTC).isoformat(),
        "source_id": _source_id_from_records(artifacts, contexts, runbooks),
        "input_paths": {
            "source_artifacts": str(artifacts_path),
            "operational_context": str(context_path),
            "finalized_runbooks_dir": str(runbooks_dir),
            "runbook_candidates": str(candidates_path) if candidates_path else None,
        },
        "record_counts": {
            "artifacts": len(linked_artifacts),
            "operational_context": len(linked_contexts),
            "finalized_runbooks": len(linked_runbooks),
            "runbook_candidates": len(candidates),
        },
        "link_stats": stats,
        "warnings": _build_warnings(stats),
        "outputs": {
            "relationship_links": str(stage8_dir / "relationship_links.json"),
            "source_artifacts_linked": str(stage8_dir / "source_artifacts_linked.json"),
            "operational_context_linked": str(stage8_dir / "operational_context_linked.json"),
            "finalized_runbooks_linked": str(stage8_dir / "finalized_runbooks_linked.json"),
            "finalized_runbooks_linked_dir": str(linked_runbooks_dir),
        },
    }
    write_json(stage8_dir / "relationship_linking_report.json", report)

    _ingest_relationship_links_into_brain(links, report["source_id"])

    return report


def _ingest_relationship_links_into_brain(links: list[dict[str, Any]], source_id: str | None) -> None:
    """Fires the in-tandem Brain hook on this stage's own new relationship
    links. Gated by BRAIN_INGESTION_ENABLED (default on) -- same pattern
    as every other stage hook in this repo."""
    from brain_service.pipeline_hook import brain_enabled

    if not brain_enabled():
        return

    source_id = str(source_id or "").strip()
    if not source_id:
        return

    from brain_service.adapters.relationship_links import relationship_links_to_records
    from brain_service.pipeline_hook import ingest_stage_output
    from providers.azure_openai_llm import AzureOpenAILLMProvider
    from providers.local_storage import LocalStorageProvider

    ingest_stage_output(
        llm=AzureOpenAILLMProvider(),
        storage=LocalStorageProvider(),
        pipeline="operational",
        stage_name="stage8_relationship_linking",
        source_id=source_id,
        scope=f"operational_sources/{source_id}",
        records=relationship_links_to_records(links),
        record_kind="relationship_link",
    )


def _safe_runbook_filename(candidate_id: str, max_stem_length: int = 80) -> str:
    stem = "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in candidate_id).strip("_")
    if len(stem) <= max_stem_length:
        return stem
    digest = hashlib.sha1(candidate_id.encode("utf-8")).hexdigest()[:12]
    return f"{stem[:max_stem_length].rstrip('_')}_{digest}"


def _source_id_from_records(*groups: list[dict[str, Any]]) -> str | None:
    for group in groups:
        for record in group:
            source_id = str(record.get("source_id") or record.get("metadata", {}).get("source_id") or "").strip()
            if source_id:
                return source_id
    return None


def _build_warnings(stats: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    if stats.get("link_count", 0) == 0:
        warnings.append("No relationship links were generated.")
    if stats.get("unresolved_context_refs", 0):
        warnings.append(
            f"{stats['unresolved_context_refs']} runbook related_context_ids could not be resolved to known context records."
        )
    if stats.get("unresolved_artifact_refs", 0):
        warnings.append(
            f"{stats['unresolved_artifact_refs']} runbook artifact references could not be resolved to known source artifacts."
        )
    return warnings
