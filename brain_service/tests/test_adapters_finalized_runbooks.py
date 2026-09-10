from __future__ import annotations

import json
from pathlib import Path

from brain_service.adapters.finalized_runbooks import finalized_runbooks_to_records

REPO_ROOT = Path(__file__).resolve().parents[2]
CASE_228086_FINALIZED_RUNBOOK = (
    REPO_ROOT
    / "incidenceknowledgeingestion"
    / "data"
    / "output"
    / "incidents"
    / "case_228086"
    / "stage_6_finalized_runbooks"
    / "finalized_runbooks"
    / "candidate_incident_228086_ssms_agv_state_diagnostic.json"
)
OPERATIONAL_FINALIZED_RUNBOOK = (
    REPO_ROOT
    / "operationalknowledgeingestion"
    / "data"
    / "output"
    / "manual_optisweep_om_v3"
    / "stage_6_finalized_runbooks"
    / "finalized_runbooks"
    / "candidate_manual_acb_system_statistics_screen_check.json"
)


def test_finalized_runbooks_to_records_against_real_incidence_data() -> None:
    runbook = json.loads(CASE_228086_FINALIZED_RUNBOOK.read_text(encoding="utf-8"))

    records = finalized_runbooks_to_records([runbook])

    assert len(records) == 1
    record = records[0]
    assert record["procedure_id"] == runbook["procedure_id"]
    assert runbook["summary"] in record["text"]
    for step in runbook["steps"]:
        assert step["title"] in record["text"]
        assert step["instruction"] in record["text"]


def test_finalized_runbooks_to_records_against_real_operational_data() -> None:
    """Confirms the adapter is genuinely shared -- the operational
    pipeline's Stage 6 output uses the identical finalized-runbook shape."""
    runbook = json.loads(OPERATIONAL_FINALIZED_RUNBOOK.read_text(encoding="utf-8"))

    records = finalized_runbooks_to_records([runbook])

    assert len(records) == 1
    assert records[0]["procedure_id"] == runbook["procedure_id"]
    assert runbook["summary"] in records[0]["text"]


def test_finalized_runbooks_to_records_handles_empty_list() -> None:
    assert finalized_runbooks_to_records([]) == []


def test_finalized_runbooks_to_records_skips_non_dict_steps() -> None:
    runbook = {"procedure_id": "p1", "summary": "s", "steps": ["not a dict"]}
    records = finalized_runbooks_to_records([runbook])
    assert records[0]["text"] == "s"
