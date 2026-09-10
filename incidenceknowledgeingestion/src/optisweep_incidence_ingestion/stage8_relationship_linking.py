"""Stage 8 deterministic relationship linking for incident source packages."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any
import hashlib
import sys

from optisweep_incidence_ingestion.tools.incident_relationship_linker import (
    apply_incident_relationship_links,
    build_incident_relationship_links,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from optisweep_ingestion.stage6_runbook_finalization import (
    write_runbook_review_html,
    write_runbook_review_markdown,
)

STAGE8_DIR_NAME = "stage_8_relationship_linking"


def load_finalized_runbooks(finalized_dir: Path) -> list[dict[str, Any]]:
    runbooks: list[dict[str, Any]] = []
    for path in sorted(finalized_dir.glob("*.json")):
        payload = _read_json(path)
        if isinstance(payload, dict):
            runbooks.append(payload)
    return runbooks


def link_incident_relationships(
    *,
    output_dir: str | Path,
    source_artifacts_path: str | Path | None = None,
    canonical_incident_record_path: str | Path | None = None,
    timeline_events_path: str | Path | None = None,
    finalized_runbooks_dir: str | Path | None = None,
    runbook_candidates_path: str | Path | None = None,
    infer_shared_artifact_links: bool = True,
) -> dict[str, Any]:
    output_path = Path(output_dir)
    stage8_dir = output_path / STAGE8_DIR_NAME
    stage8_dir.mkdir(parents=True, exist_ok=True)

    artifacts_path = Path(source_artifacts_path) if source_artifacts_path else _first_existing(
        output_path,
        "stage_3_artifact_enrichment/source_artifacts_enriched.json",
        "stage_2_ocr_artifacts/source_artifacts_enriched.json",
        "stage_2_ocr_artifacts/source_artifacts.json",
    )
    if artifacts_path is None:
        raise FileNotFoundError("Stage 8 requires enriched or raw source artifacts from Stage 2 or Stage 3.")

    canonical_path = Path(canonical_incident_record_path) if canonical_incident_record_path else _first_existing(
        output_path,
        "stage_4_canonical_incident_record/canonical_incident_record.json",
    )
    if canonical_path is None:
        raise FileNotFoundError("Stage 8 requires canonical_incident_record.json from Stage 4.")

    timeline_path = Path(timeline_events_path) if timeline_events_path else _first_existing(
        output_path,
        "stage_4_canonical_incident_record/timeline_events.json",
    )
    if timeline_path is None:
        raise FileNotFoundError("Stage 8 requires timeline_events.json from Stage 4.")

    runbooks_dir = Path(finalized_runbooks_dir) if finalized_runbooks_dir else output_path / "stage_6_finalized_runbooks/finalized_runbooks"
    runbooks = load_finalized_runbooks(runbooks_dir) if runbooks_dir.exists() else []

    candidates_path = Path(runbook_candidates_path) if runbook_candidates_path else _first_existing(
        output_path,
        "stage_5_runbook_candidates/runbook_candidates.json",
    )
    candidates = _read_list(candidates_path)

    artifacts = _read_list(artifacts_path)
    canonical_incident_record = _read_json(canonical_path)
    timeline_events = _read_json(timeline_path)
    if not isinstance(canonical_incident_record, dict):
        raise ValueError(f"{canonical_path} must contain a JSON object.")
    if not isinstance(timeline_events, dict):
        raise ValueError(f"{timeline_path} must contain a JSON object.")

    links, link_payload = build_incident_relationship_links(
        artifacts=artifacts,
        canonical_incident_record=canonical_incident_record,
        timeline_events=timeline_events,
        runbooks=runbooks,
        candidates=candidates,
        infer_shared_artifact_links=infer_shared_artifact_links,
    )
    linked_artifacts, linked_incident, linked_timeline, linked_runbooks = apply_incident_relationship_links(
        artifacts=artifacts,
        canonical_incident_record=canonical_incident_record,
        timeline_events=timeline_events,
        runbooks=runbooks,
        adjacency=link_payload["adjacency"],
    )

    artifact_index = {
        str(artifact.get("artifact_id")): artifact for artifact in linked_artifacts if artifact.get("artifact_id")
    }
    linked_runbooks_dir = stage8_dir / "finalized_runbooks_linked"
    linked_runbooks_dir.mkdir(parents=True, exist_ok=True)
    review_dir = stage8_dir / "review_markdown"
    for stale_review in (*review_dir.glob("*.md"), *review_dir.glob("*.html")):
        stale_review.unlink()
    review_dir.mkdir(parents=True, exist_ok=True)
    for runbook in linked_runbooks:
        candidate_id = str(runbook.get("candidate_id") or runbook.get("procedure_id") or "runbook").strip()
        filename = _safe_runbook_filename(candidate_id)
        _write_json(linked_runbooks_dir / f"{filename}.json", runbook)
        review_filename = _safe_runbook_filename(candidate_id, max_stem_length=60)
        md_path = review_dir / f"{review_filename}.md"
        html_path = review_dir / f"{review_filename}.html"
        md_path.write_text(
            write_runbook_review_markdown(runbook, artifact_index=artifact_index, review_markdown_path=md_path),
            encoding="utf-8",
        )
        html_path.write_text(
            write_runbook_review_html(runbook, artifact_index=artifact_index, review_html_path=html_path),
            encoding="utf-8",
        )
    _write_json(stage8_dir / "finalized_runbooks_linked.json", linked_runbooks)
    _write_json(stage8_dir / "source_artifacts_linked.json", linked_artifacts)
    _write_json(stage8_dir / "canonical_incident_record_linked.json", linked_incident)
    _write_json(stage8_dir / "timeline_events_linked.json", linked_timeline)
    _write_json(stage8_dir / "relationship_links.json", links)

    stats = link_payload["stats"]
    report = {
        "stage": "8",
        "stage_name": "relationship_linking",
        "generated_at": datetime.now(UTC).isoformat(),
        "incident_id": canonical_incident_record.get("incident_id"),
        "source_case_id": canonical_incident_record.get("source_case_id"),
        "input_paths": {
            "source_artifacts": str(artifacts_path),
            "canonical_incident_record": str(canonical_path),
            "timeline_events": str(timeline_path),
            "finalized_runbooks_dir": str(runbooks_dir),
            "runbook_candidates": str(candidates_path) if candidates_path else None,
        },
        "record_counts": {
            "artifacts": len(linked_artifacts),
            "timeline_events": len(linked_timeline.get("events") or []),
            "finalized_runbooks": len(linked_runbooks),
            "runbook_candidates": len(candidates),
        },
        "link_stats": stats,
        "warnings": _build_warnings(stats, runbook_count=len(linked_runbooks)),
        "outputs": {
            "relationship_links": str(stage8_dir / "relationship_links.json"),
            "source_artifacts_linked": str(stage8_dir / "source_artifacts_linked.json"),
            "canonical_incident_record_linked": str(stage8_dir / "canonical_incident_record_linked.json"),
            "timeline_events_linked": str(stage8_dir / "timeline_events_linked.json"),
            "finalized_runbooks_linked": str(stage8_dir / "finalized_runbooks_linked.json"),
            "finalized_runbooks_linked_dir": str(linked_runbooks_dir),
            "finalized_runbooks_linked_review_dir": str(review_dir),
        },
    }
    _write_json(stage8_dir / "relationship_linking_report.json", report)

    _ingest_relationship_links_into_brain(links, canonical_incident_record)

    return report


def _ingest_relationship_links_into_brain(
    links: list[dict[str, Any]], canonical_incident_record: dict[str, Any]
) -> None:
    """Fires the in-tandem Brain hook on this stage's own new relationship
    links. Gated by BRAIN_INGESTION_ENABLED (default on) -- see
    stage4_canonical_incident_record._ingest_timeline_events_into_brain for
    the identical pattern and its rationale."""
    from brain_service.pipeline_hook import brain_enabled

    if not brain_enabled():
        return

    from brain_service.adapters.relationship_links import relationship_links_to_records
    from brain_service.pipeline_hook import ingest_stage_output
    from providers.azure_openai_llm import AzureOpenAILLMProvider
    from providers.local_storage import LocalStorageProvider

    case_id = str(canonical_incident_record.get("source_case_id") or "").strip()
    if not case_id:
        return

    ingest_stage_output(
        llm=AzureOpenAILLMProvider(),
        storage=LocalStorageProvider(),
        pipeline="incidence",
        stage_name="stage8_relationship_linking",
        source_id=f"case:{case_id}",
        scope=f"incidents/case_{case_id}",
        records=relationship_links_to_records(links),
        record_kind="relationship_link",
    )


def _first_existing(output_path: Path, *relative_paths: str) -> Path | None:
    for relative in relative_paths:
        candidate = output_path / relative
        if candidate.exists():
            return candidate
    return None


def _read_list(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not path.exists():
        return []
    payload = _read_json(path)
    if not isinstance(payload, list):
        raise ValueError(f"{path} must contain a JSON list.")
    return payload


def _read_json(path: Path) -> Any:
    import json

    return json.loads(path.read_text(encoding="utf-8-sig"))


def _write_json(path: Path, data: Any) -> None:
    import json

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _safe_runbook_filename(candidate_id: str, max_stem_length: int = 80) -> str:
    stem = "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in candidate_id).strip("_")
    if len(stem) <= max_stem_length:
        return stem
    digest = hashlib.sha1(candidate_id.encode("utf-8")).hexdigest()[:12]
    return f"{stem[:max_stem_length].rstrip('_')}_{digest}"


def _build_warnings(stats: dict[str, Any], *, runbook_count: int = 0) -> list[str]:
    warnings: list[str] = []
    if stats.get("link_count", 0) == 0:
        warnings.append("No relationship links were generated.")
    if stats.get("unresolved_event_refs", 0):
        warnings.append(
            f"{stats['unresolved_event_refs']} runbook event references could not be resolved to known timeline events."
        )
    if stats.get("unresolved_artifact_refs", 0):
        warnings.append(
            f"{stats['unresolved_artifact_refs']} runbook artifact references could not be resolved to known source artifacts."
        )
    return warnings
