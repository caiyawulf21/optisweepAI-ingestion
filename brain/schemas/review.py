from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import Field, model_validator

from brain.id_generation import is_well_formed_id
from brain.schemas.common import BrainRecord, RecordType


class ReviewKind(str, Enum):
    """Which of the design doc §12 learning-loop branches (or an audit
    finding, AGENT_DESIGN_NOTES.md §10.2) this review represents."""

    REINFORCE = "reinforce"
    PATCH = "patch"
    CONFLICT = "conflict"
    GAP = "gap"
    NEW_CANDIDATE = "new_candidate"
    AUDIT_FINDING = "audit_finding"


class ReviewResolution(str, Enum):
    MERGE = "merge"
    RETYPE = "retype"
    RECLASSIFY = "reclassify"
    NOT_A_DUPLICATE = "not_a_duplicate"
    NEEDS_HUMAN = "needs_human"
    APPROVED = "approved"
    REJECTED = "rejected"


class BrainReview(BrainRecord):
    """The Brain's own record of pending or resolved review work —
    generalizes AGENT_DESIGN_NOTES.md §10.2.1's narrower `AuditCandidate`
    sketch (never implemented) to cover all five Reconciliation branches
    from the design doc §12 learning loop, not just audit findings.

    Matches the original design doc §7 `reviews` Cosmos container
    (partition key /status) exactly — this is the durable record that
    container holds.
    """

    type: RecordType = RecordType.REVIEW

    kind: ReviewKind
    affected_record_ids: list[str] = Field(default_factory=list)
    check_name: str | None = None
    proposed_change: str = ""
    status: Literal["open", "resolved"] = "open"
    resolution: ReviewResolution | None = None
    resolved_by: Literal["agent", "human"] | None = None
    # Carries the one extra piece of judgment a resolution needs beyond its
    # own kind (2026-09-10) -- e.g. {"entity_type": "symptom"} for RETYPE,
    # {"winner_record_id": "..."} for MERGE when resolve_audit_candidate
    # (not an SME's direct HTTP call) is the one proposing it. Optional/
    # empty-default so every existing BrainReview in Cosmos (written before
    # this field existed) still validates unchanged.
    fields_to_rewrite: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _affected_record_ids_present(self) -> "BrainReview":
        if not self.affected_record_ids:
            raise ValueError("BrainReview.affected_record_ids must name at least one record")
        return self

    @model_validator(mode="after")
    def _affected_record_ids_well_formed(self) -> "BrainReview":
        for record_id in self.affected_record_ids:
            if not is_well_formed_id(record_id):
                raise ValueError(f"affected_record_ids contains a malformed id: {record_id!r}")
        return self

    @model_validator(mode="after")
    def _resolution_requires_resolved_status(self) -> "BrainReview":
        if self.resolution is not None and self.status != "resolved":
            raise ValueError("resolution is set but status is not 'resolved'")
        if self.status == "resolved" and self.resolution is None:
            raise ValueError("status is 'resolved' but resolution is not set")
        return self

    @model_validator(mode="after")
    def _check_name_only_for_audit_finding(self) -> "BrainReview":
        if self.check_name is not None and self.kind != ReviewKind.AUDIT_FINDING:
            raise ValueError("check_name is only meaningful when kind is 'audit_finding'")
        return self
