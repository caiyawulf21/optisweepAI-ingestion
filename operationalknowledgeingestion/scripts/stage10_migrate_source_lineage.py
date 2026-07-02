"""Backfill source lineage on existing Stage 1-5 outputs without LLM reruns."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import typer

from operationalknowledgeingestion.src.optisweep_ingestion.stage_paths import stage_dir
from optisweep_ingestion.stage10_report_writer import write_source_extraction_report
from operationalknowledgeingestion.src.optisweep_ingestion.utils.json_utils import read_json, write_json

app = typer.Typer(add_completion=False)


def migrate_output_dir(output_dir: Path, source_id: str | None = None) -> dict[str, Any]:
    output_dir = output_dir.resolve()
    bundle_path = _first_stage_file(output_dir, [("1", "source_bundle.json"), ("2", "source_bundle.json")])
    if not bundle_path.exists():
        raise FileNotFoundError(f"Missing source bundle: {bundle_path}")

    bundle = read_json(bundle_path)
    source_document = bundle.get("source_document") or {}
    resolved_source_id = source_id or output_dir.name
    lineage = {
        "source_id": resolved_source_id,
        "source_type": "manual",
        "source_title": source_document.get("title") or resolved_source_id,
        "source_version": source_document.get("version"),
        "ingestion_batch_id": (bundle.get("source_metadata") or {}).get("ingestion_batch_id")
        or f"batch_migrated_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "source_document_id": source_document.get("source_document_id") or resolved_source_id,
    }

    bundle["source_metadata"] = lineage
    if source_document:
        source_document["source_type"] = "manual"
        bundle["source_document"] = source_document
    write_json(bundle_path, bundle)

    artifact_id_map: dict[str, str] = {}
    for path in (
        _stage_file(output_dir, "2", "source_artifacts.json"),
        _stage_file(output_dir, "3", "source_artifacts_enriched.json"),
    ):
        if not path.exists():
            continue
        artifacts = read_json(path)
        if not isinstance(artifacts, list):
            continue
        migrated = [_migrate_artifact(record, lineage) for record in artifacts]
        for old, new in zip(artifacts, migrated):
            old_id = str(old.get("artifact_id") or "")
            new_id = str(new.get("artifact_id") or "")
            if old_id:
                artifact_id_map[old_id] = new_id
        write_json(path, migrated)

    context_path = _stage_file(output_dir, "4", "operational_context.json")
    contexts: list[dict[str, Any]] = []
    if context_path.exists():
        raw_contexts = read_json(context_path)
        if isinstance(raw_contexts, list):
            contexts = [_migrate_context(record, lineage, artifact_id_map) for record in raw_contexts]
            write_json(context_path, contexts)

    candidate_path = _stage_file(output_dir, "5", "runbook_candidates.json")
    candidates: list[dict[str, Any]] = []
    if candidate_path.exists():
        raw_candidates = read_json(candidate_path)
        if isinstance(raw_candidates, list):
            candidates = [
                _migrate_candidate(record, lineage, artifact_id_map)
                for record in raw_candidates
            ]
            write_json(candidate_path, candidates)

    context_ids = {str(c.get("context_id")) for c in contexts if c.get("context_id")}
    for context in contexts:
        related = [
            str(candidate.get("candidate_id"))
            for candidate in candidates
            if str(context.get("context_id")) in (candidate.get("related_context_ids") or [])
        ]
        context["related_runbook_candidate_ids"] = sorted(set(related))

    if contexts:
        write_json(context_path, contexts)

    for report_path in (
        _stage_file(output_dir, "2", "artifact_extraction_report.json"),
        _stage_file(output_dir, "3", "artifact_enrichment_report.json"),
        _stage_file(output_dir, "4", "operational_context_extraction_report.json"),
        _stage_file(output_dir, "5", "runbook_candidate_extraction_report.json"),
    ):
        if report_path.exists():
            report = read_json(report_path)
            if isinstance(report, dict):
                report.update(
                    {
                        "source_id": lineage["source_id"],
                        "source_type": lineage["source_type"],
                        "ingestion_batch_id": lineage["ingestion_batch_id"],
                        "migration_note": "Source lineage backfilled without LLM rerun.",
                    }
                )
                write_json(report_path, report)

    extraction_report = write_source_extraction_report(output_dir)
    return {
        "output_dir": str(output_dir),
        "source_id": lineage["source_id"],
        "artifacts_updated": len(artifact_id_map),
        "contexts_updated": len(contexts),
        "candidates_updated": len(candidates),
        "extraction_report": extraction_report,
    }


def _stage_file(output_dir: Path, stage: str, filename: str) -> Path:
    staged = stage_dir(output_dir, stage) / filename
    if staged.exists():
        return staged
    legacy = output_dir / filename
    if legacy.exists():
        return legacy
    return staged


def _first_stage_file(output_dir: Path, stage_files: list[tuple[str, str]]) -> Path:
    fallback = stage_dir(output_dir, stage_files[0][0]) / stage_files[0][1]
    for stage, filename in stage_files:
        candidate = _stage_file(output_dir, stage, filename)
        if candidate.exists():
            return candidate
    return fallback


def _migrate_artifact(record: dict[str, Any], lineage: dict[str, Any]) -> dict[str, Any]:
    updated = dict(record)
    updated["source_id"] = lineage["source_id"]
    updated["source_type"] = lineage["source_type"]
    updated["source_title"] = lineage["source_title"]
    updated["source_version"] = lineage["source_version"]
    updated["ingestion_batch_id"] = lineage["ingestion_batch_id"]
    updated["source_refs"] = [_migrate_source_ref(ref, lineage) for ref in updated.get("source_refs") or []]
    updated.setdefault("linked_context_ids", [])
    updated.setdefault("linked_runbook_ids", [])
    updated.setdefault("linked_procedure_ids", [])
    return updated


def _migrate_context(
    record: dict[str, Any],
    lineage: dict[str, Any],
    artifact_id_map: dict[str, str],
) -> dict[str, Any]:
    updated = dict(record)
    updated["source_id"] = lineage["source_id"]
    updated["source_type"] = lineage["source_type"]
    updated["source_title"] = lineage["source_title"]
    updated["ingestion_batch_id"] = lineage["ingestion_batch_id"]
    updated["related_artifact_ids"] = [
        artifact_id_map.get(artifact_id, artifact_id)
        for artifact_id in updated.get("related_artifact_ids") or []
    ]
    image_refs = list(updated.get("image_refs") or updated.get("related_artifact_ids") or [])
    updated["image_refs"] = image_refs
    updated.setdefault("related_runbook_candidate_ids", [])
    updated["source_refs"] = [_migrate_source_ref(ref, lineage) for ref in updated.get("source_refs") or []]
    metadata = dict(updated.get("metadata") or {})
    metadata["source_quality"] = lineage["source_type"]
    updated["metadata"] = metadata
    return updated


def _migrate_candidate(
    record: dict[str, Any],
    lineage: dict[str, Any],
    artifact_id_map: dict[str, str],
) -> dict[str, Any]:
    updated = dict(record)
    updated["source_id"] = lineage["source_id"]
    updated["source_type"] = lineage["source_type"]
    updated["source_title"] = lineage["source_title"]
    updated["source_version"] = lineage["source_version"]
    updated["ingestion_batch_id"] = lineage["ingestion_batch_id"]
    updated["related_artifact_ids"] = [
        artifact_id_map.get(artifact_id, artifact_id)
        for artifact_id in updated.get("related_artifact_ids") or []
    ]
    source_refs = [_migrate_source_ref(ref, lineage) for ref in updated.get("source_refs") or []]
    updated["source_refs"] = source_refs
    if not updated.get("evidence_source_refs"):
        updated["evidence_source_refs"] = list(source_refs)
    metadata = dict(updated.get("metadata") or {})
    metadata["source_quality"] = lineage["source_type"]
    updated["metadata"] = metadata
    return updated


def _migrate_source_ref(ref: Any, lineage: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(ref, dict):
        return ref
    updated = dict(ref)
    updated["source_id"] = lineage["source_id"]
    updated["source_type"] = "manual" if updated.get("source_type") == "official_manual" else lineage["source_type"]
    updated["source_title"] = lineage["source_title"]
    updated["source_version"] = lineage["source_version"]
    updated["ingestion_batch_id"] = lineage["ingestion_batch_id"]
    updated.setdefault("source_document_id", lineage["source_document_id"])
    return updated


@app.command()
def main(
    output_dir: Path = typer.Option(..., "--output-dir", exists=True, file_okay=False),
    source_id: str | None = typer.Option(None, "--source-id"),
) -> None:
    summary = migrate_output_dir(output_dir, source_id=source_id)
    typer.echo(json.dumps(summary, indent=2))


if __name__ == "__main__":
    app()
