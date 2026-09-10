"""Shared BrainReview-construction helper, used by validation.py (Tool 4)
and audit.py (Tools 5/6) so both build the envelope the same way instead
of hand-rolling it twice.
"""

from __future__ import annotations

import hashlib
from typing import Any

from brain.schemas.common import Constraints
from brain.schemas.review import BrainReview, ReviewKind, ReviewResolution


def build_review(
    *,
    kind: ReviewKind,
    affected_record_ids: list[str],
    proposed_change: str,
    source_refs: list[str] | None = None,
    check_name: str | None = None,
    status: str = "open",
    resolution: ReviewResolution | None = None,
    resolved_by: str | None = None,
    constraints: Constraints | None = None,
    fields_to_rewrite: dict[str, Any] | None = None,
) -> BrainReview:
    """Builds a BrainReview with a deterministic id (hash of kind + sorted
    affected_record_ids) so re-running the same finding doesn't create a
    duplicate review record -- mirrors the deterministic-id rationale
    AGENT_DESIGN_NOTES.md §10.2.1 specified for the (never-built,
    superseded) AuditCandidate sketch."""
    digest = hashlib.sha256(
        "|".join([kind.value, *sorted(affected_record_ids)]).encode("utf-8")
    ).hexdigest()[:16]
    return BrainReview(
        id=f"review:{kind.value}:{digest}",
        kind=kind,
        affected_record_ids=affected_record_ids,
        check_name=check_name,
        proposed_change=proposed_change,
        status=status,  # type: ignore[arg-type]
        resolution=resolution,
        resolved_by=resolved_by,  # type: ignore[arg-type]
        source_refs=source_refs or [],
        constraints=constraints or Constraints(),
        fields_to_rewrite=fields_to_rewrite or {},
    )
