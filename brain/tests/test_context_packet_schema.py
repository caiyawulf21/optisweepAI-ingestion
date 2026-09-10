from __future__ import annotations

import pytest
from pydantic import ValidationError

from brain.schemas.common import ValidationStatus
from brain.schemas.context_packet import APPROVED_KNOWLEDGE_STATUSES, ContextPacket


def test_context_packet_minimal_construction() -> None:
    packet = ContextPacket(task={"type": "draft_playbook_node", "issue_family": "tote_state_mismatch"})
    assert packet.entities == []
    assert packet.approved_knowledge == []
    assert packet.required_output_schema is None


def test_context_packet_full_construction() -> None:
    packet = ContextPacket(
        task={"type": "draft_playbook_node"},
        current_state={"symptoms": ["tote remains in RMS"]},
        entities=["entity:system:wcs"],
        approved_knowledge=["capability:confirm_tote_lifecycle_state"],
        evidence_excerpts=["evidence:manual_om_v3:section_4"],
        relevant_incidents=["playbook:one_per_incident:223554:hospital_induct_flow"],
        policies=["policy_state_verification_requires_sql"],
        conflicts=["review:tote_state_conflict:001"],
        required_output_schema={"must_cite_evidence": True},
    )
    assert packet.approved_knowledge == ["capability:confirm_tote_lifecycle_state"]
    assert packet.required_output_schema == {"must_cite_evidence": True}


def test_context_packet_requires_task() -> None:
    with pytest.raises(ValidationError):
        ContextPacket()  # type: ignore[call-arg]


def test_context_packet_rejects_unknown_field() -> None:
    with pytest.raises(ValidationError):
        ContextPacket(task={"type": "x"}, unexpected_field="nope")  # type: ignore[call-arg]


def test_approved_knowledge_statuses_excludes_unreviewed_and_pending() -> None:
    assert ValidationStatus.CATALOG_AUTHORITATIVE in APPROVED_KNOWLEDGE_STATUSES
    assert ValidationStatus.SME_APPROVED in APPROVED_KNOWLEDGE_STATUSES
    assert ValidationStatus.OPERATIONAL_UNREVIEWED not in APPROVED_KNOWLEDGE_STATUSES
    assert ValidationStatus.NEEDS_SME_REVIEW not in APPROVED_KNOWLEDGE_STATUSES
    assert ValidationStatus.CONFLICTING not in APPROVED_KNOWLEDGE_STATUSES
    assert ValidationStatus.DEPRECATED not in APPROVED_KNOWLEDGE_STATUSES
