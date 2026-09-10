from __future__ import annotations

import json
from pathlib import Path

from brain_service.adapters.operational_stage4 import operational_context_records_to_records

OPERATIONAL_CONTEXT = (
    Path(__file__).resolve().parents[2]
    / "operationalknowledgeingestion"
    / "data"
    / "output"
    / "manual_optisweep_om_v3"
    / "stage_4_operational_context"
    / "operational_context.json"
)


def test_operational_context_to_records_against_real_data() -> None:
    contexts = json.loads(OPERATIONAL_CONTEXT.read_text(encoding="utf-8"))

    records = operational_context_records_to_records(contexts)

    assert len(records) == len(contexts)
    record = records[0]
    context = contexts[0]
    assert record["context_id"] == context["context_id"]
    assert context["summary"] in record["text"]
    assert context["details"] in record["text"]


def test_operational_context_to_records_handles_empty_list() -> None:
    assert operational_context_records_to_records([]) == []
