"""Output contract tests for Active AGV error Query 1 ingestion."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "data" / "output" / "active_agv_error_query_1"
SHARED_ROOT = ROOT.parent / "shared_pipeline_stages" / "data" / "output" / "shared"

EXPECTED_CANDIDATE_ID = "candidate_manual_query_active_agv_errors"
EXPECTED_PROCEDURE_ID = "proc_query_active_agv_errors_from_the_wcs_database_v1"
SOURCE_ID = "active_agv_error_query_1"

QUERY_MARKERS = (
    "SystemActiveErrorModel",
    "active agv error",
    "wcs",
)
STATE_MARKERS = (
    "error",
    "agv",
    "query",
)


def _require_source_output() -> Path:
    if not SOURCE_ROOT.exists():
        pytest.skip(f"Missing source output: {SOURCE_ROOT}")
    return SOURCE_ROOT


def _load_json(path: Path):
    assert path.exists(), f"Missing artifact: {path}"
    return json.loads(path.read_text(encoding="utf-8"))


def test_stage1_uses_document_level_section_fallback() -> None:
    root = _require_source_output()
    bundle = _load_json(root / "stage_1_source_bundle" / "source_bundle.json")
    assert bundle["source_metadata"]["source_id"] == SOURCE_ID
    assert len(bundle["sections"]) == 1
    assert bundle["build_metadata"].get("section_detection") == "document_level_section_fallback"
    assert "Formatted:" not in bundle["pages"][0]["text"]
    assert any("SystemActiveErrorModel" in page.get("text", "") for page in bundle["pages"])


def test_stage5_produces_singular_agv_error_query_candidate() -> None:
    root = _require_source_output()
    candidates = _load_json(root / "stage_5_runbook_candidates" / "runbook_candidates.json")
    assert isinstance(candidates, list)
    assert len(candidates) == 1
    candidate = candidates[0]
    assert candidate["candidate_id"] == EXPECTED_CANDIDATE_ID
    blob = json.dumps(candidate).lower()
    assert all(marker in blob for marker in ("agv", "error", "wcs"))


def test_stage6_finalized_runbook_answers_agv_state_and_failure_checks() -> None:
    root = _require_source_output()
    runbooks_dir = root / "stage_6_finalized_runbooks" / "finalized_runbooks"
    runbook_paths = sorted(runbooks_dir.glob("*.json"))
    assert len(runbook_paths) == 1
    runbook = _load_json(runbook_paths[0])

    assert runbook["candidate_id"] == EXPECTED_CANDIDATE_ID
    assert runbook["procedure_id"] == EXPECTED_PROCEDURE_ID
    assert runbook["procedure_type"] == "diagnostic"
    assert runbook["support_safe"] is True
    assert runbook["role_required"] in {"L2_support", "support", "remote_support", "operator"}
    assert len(runbook.get("steps") or []) >= 4

    blob = json.dumps(runbook).lower()
    assert "systemactiveerrormodel" in blob
    assert "active agv" in blob or "agv error" in blob
    assert any(marker in blob for marker in STATE_MARKERS)
    assert any("select" in blob and "error" in blob for _ in [0])

    review_md = root / "stage_6_finalized_runbooks" / "review_markdown" / "runbooks" / f"{EXPECTED_CANDIDATE_ID}.md"
    assert review_md.exists()
    review_text = review_md.read_text(encoding="utf-8").lower()
    assert "agv" in review_text
    assert "error" in review_text


def test_stage8_links_runbook_to_context_and_artifacts() -> None:
    root = _require_source_output()
    links = _load_json(root / "stage_8_relationship_linking" / "relationship_links.json")
    assert isinstance(links, list)
    assert links

    linked_runbooks = root / "stage_8_relationship_linking" / "finalized_runbooks_linked"
    linked = list(linked_runbooks.glob(f"*{EXPECTED_CANDIDATE_ID}*.json")) if linked_runbooks.exists() else []
    if not linked:
        linked = list((root / "stage_8_relationship_linking").glob(f"**/*{EXPECTED_CANDIDATE_ID}*.json"))
    assert linked, "Expected linked runbook artifact for active AGV error query"


def test_shared_pool_and_canonical_include_agv_error_query_runbook() -> None:
    if not SHARED_ROOT.exists():
        pytest.skip(f"Missing shared output: {SHARED_ROOT}")

    pool_path = SHARED_ROOT / "stage_6_5_runbook_pool" / "runbook_pool.json"
    canonical_path = SHARED_ROOT / "stage_7_merged_runbooks" / "canonical_runbooks.json"
    if not pool_path.exists() or not canonical_path.exists():
        pytest.skip("Shared stages 6.5/7 outputs not present yet")

    pool = _load_json(pool_path)
    pool_blob = json.dumps(pool).lower()
    assert SOURCE_ID in pool_blob
    assert "query_active_agv" in pool_blob or EXPECTED_CANDIDATE_ID in pool_blob

    canonical = _load_json(canonical_path)
    canonical_blob = json.dumps(canonical).lower()
    assert "systemactiveerrormodel" in canonical_blob or "active agv error" in canonical_blob
    assert SOURCE_ID in canonical_blob or EXPECTED_PROCEDURE_ID in canonical_blob
