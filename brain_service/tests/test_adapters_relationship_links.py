from __future__ import annotations

import json
from pathlib import Path

from brain_service.adapters.relationship_links import relationship_links_to_records

REPO_ROOT = Path(__file__).resolve().parents[2]
CASE_228086_RELATIONSHIP_LINKS = (
    REPO_ROOT
    / "incidenceknowledgeingestion"
    / "data"
    / "output"
    / "incidents"
    / "case_228086"
    / "stage_8_relationship_linking"
    / "relationship_links.json"
)
OPERATIONAL_RELATIONSHIP_LINKS = (
    REPO_ROOT
    / "operationalknowledgeingestion"
    / "data"
    / "output"
    / "manual_optisweep_om_v3"
    / "stage_8_relationship_linking"
    / "relationship_links.json"
)


def test_relationship_links_to_records_against_real_incidence_data() -> None:
    links = json.loads(CASE_228086_RELATIONSHIP_LINKS.read_text(encoding="utf-8"))

    records = relationship_links_to_records(links)

    assert len(records) == len(links)
    record = records[0]
    link = links[0]
    assert record["link_id"] == link["link_id"]
    assert record["source_record_id"] == link["source_record_id"]
    assert record["target_record_id"] == link["target_record_id"]
    assert link["source_record_id"] in record["text"]
    assert link["target_record_id"] in record["text"]
    assert link["link_type"] in record["text"]


def test_relationship_links_to_records_against_real_operational_data() -> None:
    """Confirms the adapter is genuinely shared -- the operational
    pipeline's Stage 8 output uses the identical link shape."""
    links = json.loads(OPERATIONAL_RELATIONSHIP_LINKS.read_text(encoding="utf-8"))

    records = relationship_links_to_records(links[:20])

    assert len(records) == 20
    assert records[0]["link_id"] == links[0]["link_id"]


def test_relationship_links_to_records_handles_empty_list() -> None:
    assert relationship_links_to_records([]) == []
