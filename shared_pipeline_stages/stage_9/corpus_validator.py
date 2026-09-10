"""Shared Stage 9 corpus validation before embedding and publish."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from shared_pipeline_stages.stage_6_5.json_utils import read_json, write_json
from shared_pipeline_stages.stage_7.normalize import validate_canonical_runbook
from shared_pipeline_stages.stage_8.normalize import validate_finalized_playbook

STAGE9_DIR_NAME = "stage_9_validation"
STAGE7_CANONICAL = "canonical_runbooks.json"
STAGE8_VARIANTS = ("prompt_a_one_per_incident", "prompt_b_multi_flow")
STAGE85_LINKS = Path("stage_8_5_relationship_linking") / "relationship_links.json"
HARD_FAIL_CODES = {
    "missing_input",
    "canonical_runbook_invalid",
    "playbook_unresolved_link",
    "playbook_unknown_procedure",
    "playbook_graph_error",
    "relationship_link_invalid",
}


@dataclass
class CorpusValidationResult:
    passed: bool
    error_count: int
    warning_count: int
    runbook_count: int
    playbook_count: int
    relationship_link_count: int
    issues: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def validate_corpus(
    *,
    stage7_dir: str | Path,
    stage8_dir: str | Path,
    stage85_dir: str | Path | None = None,
    output_dir: str | Path | None = None,
    expected_source_roots: list[str | Path] | None = None,
) -> CorpusValidationResult:
    stage7_path = Path(stage7_dir)
    stage8_path = _resolve_stage8_dir(Path(stage8_dir))
    stage85_path = Path(stage85_dir) if stage85_dir else None
    generated_at = datetime.now(UTC).isoformat()

    issues: list[dict[str, Any]] = []
    warnings: list[str] = []

    canonical_path = stage7_path / STAGE7_CANONICAL
    if not canonical_path.exists():
        issues.append(_issue("missing_input", "stage7", f"Missing {canonical_path}"))
        canonical_runbooks: list[dict[str, Any]] = []
    else:
        payload = read_json(canonical_path)
        canonical_runbooks = payload.get("runbooks") if isinstance(payload, dict) else payload
        if not isinstance(canonical_runbooks, list):
            issues.append(_issue("missing_input", "stage7", f"{canonical_path} must contain a runbooks list."))
            canonical_runbooks = []

    runbooks_by_id = {
        str(item.get("procedure_id") or ""): item
        for item in canonical_runbooks
        if isinstance(item, dict) and str(item.get("procedure_id") or "").strip()
    }
    for runbook in canonical_runbooks:
        if not isinstance(runbook, dict):
            issues.append(_issue("canonical_runbook_invalid", "stage7", "Non-object runbook entry."))
            continue
        procedure_id = str(runbook.get("procedure_id") or "")
        for error in validate_canonical_runbook(runbook):
            issues.append(
                _issue("canonical_runbook_invalid", "stage7", f"{procedure_id or '<unknown>'}: {error}")
            )

    playbooks: list[dict[str, Any]] = []
    playbook_link_rows: list[dict[str, Any]] = []
    for variant in STAGE8_VARIANTS:
        variant_dir = stage8_path / variant
        canonical_playbooks_path = variant_dir / "canonical_playbooks.json"
        links_path = variant_dir / "playbook_runbook_links.json"
        if not canonical_playbooks_path.exists():
            issues.append(_issue("missing_input", "stage8", f"Missing {canonical_playbooks_path}"))
            continue
        payload = read_json(canonical_playbooks_path)
        variant_playbooks = payload.get("playbooks") if isinstance(payload, dict) else payload
        if not isinstance(variant_playbooks, list):
            issues.append(_issue("missing_input", "stage8", f"{canonical_playbooks_path} must contain a playbooks list."))
            continue
        playbooks.extend(variant_playbooks)
        for playbook in variant_playbooks:
            if not isinstance(playbook, dict):
                continue
            playbook_id = str(playbook.get("playbook_id") or "")
            for warning in validate_finalized_playbook(playbook, runbooks_by_id=runbooks_by_id):
                if "unknown procedure_id" in warning or "next_node_id not found" in warning:
                    issues.append(_issue("playbook_graph_error", "stage8", f"{playbook_id}: {warning}"))
                else:
                    warnings.append(f"{variant}/{playbook_id}: {warning}")
            for node in playbook.get("nodes") or []:
                if not isinstance(node, dict):
                    continue
                for link in node.get("runbook_links") or []:
                    if not isinstance(link, dict):
                        continue
                    confidence = str(link.get("link_confidence") or "").lower()
                    procedure_id = str(link.get("procedure_id") or "")
                    if confidence == "unresolved" or not procedure_id:
                        issues.append(
                            _issue(
                                "playbook_unresolved_link",
                                "stage8",
                                f"{playbook_id}/{node.get('node_id')}: unresolved runbook link",
                            )
                        )
                    elif procedure_id not in runbooks_by_id:
                        issues.append(
                            _issue(
                                "playbook_unknown_procedure",
                                "stage8",
                                f"{playbook_id}/{node.get('node_id')}: unknown procedure_id {procedure_id}",
                            )
                        )
        if links_path.exists():
            links_payload = read_json(links_path)
            rows = links_payload.get("links") if isinstance(links_payload, dict) else links_payload
            if isinstance(rows, list):
                playbook_link_rows.extend(row for row in rows if isinstance(row, dict))

    relationship_links: list[dict[str, Any]] = []
    if stage85_path is None:
        warnings.append("Stage 8.5 relationship graph not provided; skipping corpus link validation.")
    else:
        links_path = stage85_path / "relationship_links.json" if stage85_path.is_dir() else stage85_path
        if not links_path.exists():
            issues.append(_issue("missing_input", "stage8.5", f"Missing {links_path}"))
        else:
            payload = read_json(links_path)
            if not isinstance(payload, list):
                issues.append(_issue("missing_input", "stage8.5", f"{links_path} must contain a JSON list."))
            else:
                relationship_links = payload
                _validate_relationship_links(
                    relationship_links,
                    runbooks_by_id=runbooks_by_id,
                    playbook_ids={str(item.get("playbook_id") or "") for item in playbooks},
                    expected_source_roots=expected_source_roots,
                    issues=issues,
                    warnings=warnings,
                )

    for row in playbook_link_rows:
        procedure_id = str(row.get("procedure_id") or "")
        if not procedure_id:
            issues.append(_issue("playbook_unresolved_link", "stage8", "playbook_runbook_links row missing procedure_id"))
        elif procedure_id not in runbooks_by_id:
            issues.append(
                _issue(
                    "playbook_unknown_procedure",
                    "stage8",
                    f"playbook_runbook_links references unknown procedure_id {procedure_id}",
                )
            )

    error_count = sum(1 for item in issues if item["severity"] == "error")
    warning_count = len(warnings)
    result = CorpusValidationResult(
        passed=error_count == 0,
        error_count=error_count,
        warning_count=warning_count,
        runbook_count=len(canonical_runbooks),
        playbook_count=len(playbooks),
        relationship_link_count=len(relationship_links),
        issues=issues,
        warnings=warnings,
    )

    if output_dir is not None:
        output_path = _resolve_output_path(Path(output_dir))
        output_path.mkdir(parents=True, exist_ok=True)
        validation_report = {
            "stage": "9",
            "stage_name": "corpus_validation",
            "generated_at": generated_at,
            "passed": result.passed,
            "summary": {
                "error_count": result.error_count,
                "warning_count": result.warning_count,
                "runbook_count": result.runbook_count,
                "playbook_count": result.playbook_count,
                "relationship_link_count": result.relationship_link_count,
            },
            "inputs": {
                "stage7_dir": str(stage7_path),
                "stage8_dir": str(stage8_path),
                "stage85_dir": str(stage85_path) if stage85_path else "",
            },
            "issues": result.issues,
            "warnings": result.warnings,
        }
        write_json(output_path / "validation_report.json", validation_report)
        write_json(
            output_path / "extraction_report.json",
            {
                "stage": "9",
                "stage_name": "corpus_validation",
                "generated_at": generated_at,
                "status": "passed" if result.passed else "failed",
                "record_counts": validation_report["summary"],
                "warnings": result.warnings,
            },
        )
    return result


def _validate_relationship_links(
    relationship_links: list[dict[str, Any]],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
    playbook_ids: set[str],
    expected_source_roots: list[str | Path] | None,
    issues: list[dict[str, Any]],
    warnings: list[str],
) -> None:
    seen_source_roots: set[str] = set()
    link_types: dict[str, int] = {}
    for link in relationship_links:
        if not isinstance(link, dict):
            issues.append(_issue("relationship_link_invalid", "stage8.5", "Non-object relationship link."))
            continue
        link_type = str(link.get("link_type") or "")
        link_types[link_type] = link_types.get(link_type, 0) + 1
        source_root = str(link.get("source_root") or "")
        if source_root:
            seen_source_roots.add(source_root)
        source_id = str(link.get("source_record_id") or "")
        target_id = str(link.get("target_record_id") or "")
        if not link_type or not source_id or not target_id:
            issues.append(_issue("relationship_link_invalid", "stage8.5", "Link missing link_type or endpoint IDs."))
        if link_type == "playbook_runbook" and target_id and target_id not in runbooks_by_id:
            issues.append(
                _issue(
                    "relationship_link_invalid",
                    "stage8.5",
                    f"playbook_runbook target not in canonical catalog: {target_id}",
                )
            )
        if link_type == "playbook_runbook":
            playbook_id = str(link.get("source_record_id") or link.get("playbook_id") or "")
            if playbook_id and playbook_ids and playbook_id not in playbook_ids:
                warnings.append(f"playbook_runbook source not found in canonical playbooks: {playbook_id}")

    if expected_source_roots:
        expected = {str(Path(root)) for root in expected_source_roots}
        missing = sorted(expected - seen_source_roots)
        for root in missing:
            warnings.append(f"Expected source root missing from Stage 8.5 graph: {root}")


def _issue(code: str, component: str, message: str) -> dict[str, Any]:
    return {
        "code": code,
        "component": component,
        "severity": "error" if code in HARD_FAIL_CODES else "warning",
        "message": message,
    }


def _resolve_stage8_dir(stage8_dir: Path) -> Path:
    if stage8_dir.name == "stage_8_finalized_playbooks":
        return stage8_dir
    nested = stage8_dir / "stage_8_finalized_playbooks"
    return nested if nested.exists() else stage8_dir


def _resolve_output_path(output_dir: Path) -> Path:
    if output_dir.name == STAGE9_DIR_NAME:
        return output_dir
    return output_dir / STAGE9_DIR_NAME
