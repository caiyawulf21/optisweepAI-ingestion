from __future__ import annotations

import json
from pathlib import Path

from brain_service.adapters.runbook_candidates import runbook_candidates_to_records

REPO_ROOT = Path(__file__).resolve().parents[2]
CASE_228086_RUNBOOK_CANDIDATES = (
    REPO_ROOT
    / "incidenceknowledgeingestion"
    / "data"
    / "output"
    / "incidents"
    / "case_228086"
    / "stage_5_runbook_candidates"
    / "runbook_candidates.json"
)
OPERATIONAL_RUNBOOK_CANDIDATES = (
    REPO_ROOT
    / "operationalknowledgeingestion"
    / "data"
    / "output"
    / "manual_optisweep_om_v3"
    / "stage_5_runbook_candidates"
    / "runbook_candidates.json"
)


def test_runbook_candidates_to_records_against_real_incidence_data() -> None:
    candidates = json.loads(CASE_228086_RUNBOOK_CANDIDATES.read_text(encoding="utf-8"))

    records = runbook_candidates_to_records(candidates)

    assert len(records) == len(candidates)
    first_record = records[0]
    first_candidate = candidates[0]
    assert first_record["candidate_id"] == first_candidate["candidate_id"]
    assert first_candidate["candidate_goal"] in first_record["text"]
    assert first_candidate["summary"] in first_record["text"]
    for step in first_candidate["rough_steps"]:
        assert step in first_record["text"]


def test_runbook_candidates_to_records_against_real_operational_data() -> None:
    """Confirms the adapter is genuinely shared -- the operational
    pipeline's Stage 5 output uses the identical candidate shape, so the
    same adapter (not a duplicate) handles both pipelines."""
    candidates = json.loads(OPERATIONAL_RUNBOOK_CANDIDATES.read_text(encoding="utf-8"))

    records = runbook_candidates_to_records(candidates)

    assert len(records) == len(candidates)
    first_record = records[0]
    first_candidate = candidates[0]
    assert first_record["candidate_id"] == first_candidate["candidate_id"]
    assert first_candidate["summary"] in first_record["text"]


def test_runbook_candidates_to_records_handles_empty_list() -> None:
    assert runbook_candidates_to_records([]) == []
