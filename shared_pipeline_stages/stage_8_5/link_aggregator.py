"""Aggregate per-source relationship links into a shared corpus graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
import hashlib

from shared_pipeline_stages.stage_6_5.json_utils import read_json, write_json

STAGE85_DIR_NAME = "stage_8_5_relationship_linking"
PER_SOURCE_LINKS_RELATIVE = Path("stage_8_relationship_linking") / "relationship_links.json"
STAGE8_VARIANTS = ("prompt_a_one_per_incident", "prompt_b_multi_flow")


@dataclass
class Stage85BuildConfig:
    remap_to_canonical_runbooks: bool = True
    include_playbook_links: bool = True


@dataclass
class Stage85BuildResult:
    link_count: int
    per_source_link_count: int
    playbook_link_count: int
    source_roots: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def build_stage8_5_corpus_relationship_links(
    *,
    source_roots: list[str | Path],
    output_dir: str | Path,
    stage7_dir: str | Path | None = None,
    stage8_dir: str | Path | None = None,
    config: Stage85BuildConfig | None = None,
) -> Stage85BuildResult:
    build_config = config or Stage85BuildConfig()
    output_path = _resolve_output_path(Path(output_dir))
    output_path.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(UTC).isoformat()

    procedure_remap = _load_procedure_remap(stage7_dir) if build_config.remap_to_canonical_runbooks else {}
    corpus_links: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str, str, str]] = set()
    per_source_reports: list[dict[str, Any]] = []
    warnings: list[str] = []
    per_source_link_count = 0

    for source_root in source_roots:
        root = Path(source_root)
        links_path = root / PER_SOURCE_LINKS_RELATIVE
        if not links_path.exists():
            warnings.append(f"Missing per-source relationship links at {links_path}. Skipping {root}.")
            continue
        payload = read_json(links_path)
        if not isinstance(payload, list):
            raise ValueError(f"{links_path} must contain a JSON list.")
        source_meta = _source_metadata(root)
        source_meta["source_root"] = str(root)
        for link in payload:
            if not isinstance(link, dict):
                continue
            enriched = _enrich_per_source_link(link, source_meta, procedure_remap)
            if _append_corpus_link(corpus_links, seen, enriched):
                per_source_link_count += 1
        per_source_reports.append(
            {
                "source_root": str(root),
                **source_meta,
                "link_count": len(payload),
            }
        )

    playbook_link_count = 0
    if build_config.include_playbook_links and stage8_dir:
        playbook_links, playbook_warnings = _load_playbook_links(stage8_dir)
        warnings.extend(playbook_warnings)
        for link in playbook_links:
            if _append_corpus_link(corpus_links, seen, link):
                playbook_link_count += 1

    write_json(output_path / "relationship_links.json", corpus_links)
    report = {
        "stage": "8.5",
        "stage_name": "shared_relationship_linking",
        "generated_at": generated_at,
        "source_roots": [str(Path(root)) for root in source_roots],
        "per_source_reports": per_source_reports,
        "link_stats": {
            "link_count": len(corpus_links),
            "per_source_link_count": per_source_link_count,
            "playbook_link_count": playbook_link_count,
            "procedure_remap_count": len(procedure_remap),
            "source_roots_with_links": len(per_source_reports),
        },
        "warnings": warnings,
        "outputs": {
            "relationship_links": str(output_path / "relationship_links.json"),
        },
    }
    write_json(output_path / "relationship_linking_report.json", report)
    return Stage85BuildResult(
        link_count=len(corpus_links),
        per_source_link_count=per_source_link_count,
        playbook_link_count=playbook_link_count,
        source_roots=[str(Path(root)) for root in source_roots],
        warnings=warnings,
    )


def _resolve_output_path(output_dir: Path) -> Path:
    if output_dir.name == STAGE85_DIR_NAME:
        return output_dir
    return output_dir / STAGE85_DIR_NAME


def _load_procedure_remap(stage7_dir: str | Path | None) -> dict[str, str]:
    if stage7_dir is None:
        return {}
    mapping_path = Path(stage7_dir)
    if mapping_path.is_dir():
        mapping_path = mapping_path / "candidate_to_procedure_mapping.json"
    if not mapping_path.exists():
        return {}
    payload = read_json(mapping_path)
    mappings = payload.get("mappings") if isinstance(payload, dict) else payload
    if not isinstance(mappings, list):
        return {}
    remap: dict[str, str] = {}
    for entry in mappings:
        if not isinstance(entry, dict):
            continue
        canonical = str(entry.get("canonical_procedure_id") or "").strip()
        if not canonical:
            continue
        for key in ("source_procedure_id", "candidate_id"):
            source_id = str(entry.get(key) or "").strip()
            if source_id:
                remap[source_id] = canonical
    return remap


def _source_metadata(source_root: Path) -> dict[str, str]:
    report_path = source_root / PER_SOURCE_LINKS_RELATIVE.parent / "relationship_linking_report.json"
    if report_path.exists():
        report = read_json(report_path)
        if isinstance(report, dict):
            return {
                "source_id": str(report.get("source_id") or report.get("incident_id") or source_root.name),
                "source_case_id": str(report.get("source_case_id") or ""),
                "source_type": _infer_source_type(source_root),
            }
    return {
        "source_id": source_root.name,
        "source_case_id": source_root.name.removeprefix("case_") if "case_" in source_root.name else "",
        "source_type": _infer_source_type(source_root),
    }


def _infer_source_type(source_root: Path) -> str:
    parts = {part.lower() for part in source_root.parts}
    if "incidents" in parts:
        return "incident"
    if "training_video" in source_root.name:
        return "training_video"
    return "manual"


def _enrich_per_source_link(
    link: dict[str, Any],
    source_meta: dict[str, str],
    procedure_remap: dict[str, str],
) -> dict[str, Any]:
    enriched = dict(link)
    enriched["link_scope"] = "per_source"
    enriched["source_root"] = source_meta.get("source_root", "")
    enriched["source_id"] = source_meta.get("source_id", "")
    enriched["source_type"] = source_meta.get("source_type", "")
    if source_meta.get("source_case_id"):
        enriched["source_case_id"] = source_meta["source_case_id"]
    enriched["source_record_id"] = _remap_record_id(
        enriched.get("source_record_type"),
        str(enriched.get("source_record_id") or ""),
        procedure_remap,
    )
    enriched["target_record_id"] = _remap_record_id(
        enriched.get("target_record_type"),
        str(enriched.get("target_record_id") or ""),
        procedure_remap,
    )
    if procedure_remap and (
        enriched.get("source_record_id") != link.get("source_record_id")
        or enriched.get("target_record_id") != link.get("target_record_id")
    ):
        enriched["link_method"] = f"{enriched.get('link_method', 'unknown')}_canonical_remapped"
    return enriched


def _remap_record_id(record_type: Any, record_id: str, procedure_remap: dict[str, str]) -> str:
    if not record_id:
        return record_id
    if str(record_type) in {"finalized_runbook", "runbook_candidate"}:
        return procedure_remap.get(record_id, record_id)
    return record_id


def _load_playbook_links(stage8_dir: str | Path) -> tuple[list[dict[str, Any]], list[str]]:
    root = Path(stage8_dir)
    if root.name != "stage_8_finalized_playbooks" and (root / "stage_8_finalized_playbooks").exists():
        root = root / "stage_8_finalized_playbooks"
    links: list[dict[str, Any]] = []
    warnings: list[str] = []
    found = False
    for variant in STAGE8_VARIANTS:
        path = root / variant / "playbook_runbook_links.json"
        if not path.exists():
            continue
        found = True
        payload = read_json(path)
        rows = payload.get("links") if isinstance(payload, dict) else payload
        if not isinstance(rows, list):
            warnings.append(f"{path} did not contain a links list.")
            continue
        for row in rows:
            if not isinstance(row, dict):
                continue
            playbook_id = str(row.get("playbook_id") or "").strip()
            node_id = str(row.get("node_id") or "").strip()
            procedure_id = str(row.get("procedure_id") or "").strip()
            if not playbook_id or not node_id or not procedure_id:
                continue
            links.append(
                {
                    "link_id": _link_id("playbook_runbook", f"{playbook_id}:{node_id}", procedure_id),
                    "link_type": "playbook_runbook",
                    "source_record_type": "playbook_node",
                    "source_record_id": f"{playbook_id}:{node_id}",
                    "target_record_type": "canonical_runbook",
                    "target_record_id": procedure_id,
                    "link_method": "shared_stage8_playbook_finalization",
                    "confidence": str(row.get("link_confidence") or "medium"),
                    "needs_sme_review": True,
                    "link_scope": "shared_playbook",
                    "source_case_id": str(row.get("case_id") or ""),
                    "extraction_mode": str(row.get("extraction_mode") or variant),
                    "link_rank": row.get("link_rank"),
                }
            )
    if not found:
        warnings.append(f"No Shared Stage 8 playbook_runbook_links.json files found under {root}.")
    return links, warnings


def _link_id(link_type: str, source_id: str, target_id: str) -> str:
    digest = hashlib.sha1(f"{link_type}:{source_id}:{target_id}".encode("utf-8")).hexdigest()[:16]
    return f"link_{link_type}_{digest}"


def _append_corpus_link(
    corpus_links: list[dict[str, Any]],
    seen: set[tuple[str, str, str, str, str]],
    link: dict[str, Any],
) -> bool:
    key = (
        str(link.get("link_scope") or ""),
        str(link.get("source_id") or ""),
        str(link.get("link_type") or ""),
        str(link.get("source_record_id") or ""),
        str(link.get("target_record_id") or ""),
    )
    if key in seen:
        return False
    seen.add(key)
    corpus_links.append(link)
    return True
