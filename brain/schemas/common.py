from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

SCHEMA_VERSION = "1.0"


class RecordType(str, Enum):
    EVIDENCE_UNIT = "evidence_unit"
    ENTITY = "entity"
    CLAIM = "claim"
    RELATIONSHIP = "relationship"
    CAPABILITY = "capability"
    PROCEDURE = "procedure"
    PLAYBOOK = "playbook"
    REVIEW = "review"


class ValidationStatus(str, Enum):
    """Governance status of a Brain record (AGENT_DESIGN_NOTES.md §14, closing
    the gap named repeatedly in §4/§6: nothing previously distinguished
    hand-curated/SME-approved knowledge from unreviewed extraction).

    CATALOG_AUTHORITATIVE and OPERATIONAL_UNREVIEWED describe how a record
    ENTERED the corpus (backfill-time classification, assigned once).
    NEEDS_SME_REVIEW / SME_APPROVED / CONFLICTING / DEPRECATED describe where
    a record is in the review lifecycle (assigned/transitioned by
    Reconciliation/Curation, per the design doc §12 learning loop). A record
    moves from an entry status toward a lifecycle status as it goes through
    review — the two families are sequential, not a single flat enum by
    accident.
    """

    CATALOG_AUTHORITATIVE = "catalog_authoritative"
    OPERATIONAL_UNREVIEWED = "operational_unreviewed"
    NEEDS_SME_REVIEW = "needs_sme_review"
    SME_APPROVED = "sme_approved"
    CONFLICTING = "conflicting"
    DEPRECATED = "deprecated"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Constraints(BaseModel):
    """Scope limits for a record. Empty/omitted fields mean globally applicable (Part 1 §3.3)."""

    model_config = ConfigDict(extra="forbid")

    sites: list[str] = Field(default_factory=list)
    product_versions: list[str] = Field(default_factory=list)
    environments: list[str] = Field(default_factory=list)


class BrainRecord(BaseModel):
    """Shared MVP envelope every Part 1 Brain record uses (Part 1 §3)."""

    model_config = ConfigDict(extra="forbid")

    id: str
    type: RecordType
    schema_version: str = SCHEMA_VERSION
    source_refs: list[str] = Field(default_factory=list)
    constraints: Constraints = Field(default_factory=Constraints)
    validation_status: ValidationStatus = ValidationStatus.OPERATIONAL_UNREVIEWED
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
