"""The shared Create-path chain: extract_evidence -> classify_candidate ->
reconcile_candidate -> apply_reconciliation (validates AND writes), run
once per raw claim candidate found in one source packet.

Both run_migration_batch (Tool 7, per-batch-item) and ingest_stage_output
(the per-stage tandem-ingestion hook) loop this same function per unit of
work -- factored out here so the loop body exists once, not duplicated
between a "batch item" caller and a "stage record" caller.

Write model (2026-09-09, user-directed, see brain_service/persistence.py):
every outcome except GAP writes its record immediately, tagged
validation_status=operational_unreviewed (or conflicting for CONFLICT) --
"written vs not written" is not the safety gate here, validation_status
is: ContextPacket.approved_knowledge already filters to only
catalog_authoritative/sme_approved records, so an unreviewed write is
visible and citable everywhere except as "approved" until an SME reviews
it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from brain_service.classification import classify_candidate
from brain_service.extraction import extract_evidence
from brain_service.persistence import apply_reconciliation
from brain_service.reconciliation import reconcile_candidate
from providers.llm import LLMProvider
from providers.storage import StorageProvider


@dataclass
class CreateChainResult:
    status: str  # "succeeded" | "needs_human_review" | "failed"
    detail: str = ""
    review_ids: list[str] = field(default_factory=list)
    written_record_ids: list[str] = field(default_factory=list)


def run_create_chain(
    llm: LLMProvider,
    storage: StorageProvider,
    *,
    source_packet: dict[str, Any],
    evidence_id_prefix: str,
    scope: str,
) -> CreateChainResult:
    """Runs the full chain against one bounded source packet. `evidence_id_prefix`
    disambiguates candidates within this packet from candidates in any
    other packet processed in the same run (e.g. "case:228086:timeline:7").
    `scope` is where any resulting write (record or review) is persisted
    -- e.g. "incidents/case_228086"."""
    extraction = extract_evidence(llm, source_packet)

    review_ids: list[str] = []
    written_record_ids: list[str] = []
    needs_review = False
    for candidate_index, candidate in enumerate(extraction.candidates):
        for raw_claim in candidate.raw_claim_candidates or [candidate.content_text]:
            classified = classify_candidate(
                llm,
                storage,
                candidate_text=raw_claim,
                evidence_id=f"{evidence_id_prefix}:{candidate_index}",
            )
            reconciled = reconcile_candidate(llm, storage, classified)
            result = apply_reconciliation(storage, reconciled, scope=scope)
            review_ids.append(result.review.id)
            if result.written_record is not None:
                written_record_ids.append(result.written_record.id)

            if result.skipped_reason and "VALIDATION FAILED" in (result.skipped_reason or ""):
                return CreateChainResult(
                    status="failed", detail=result.skipped_reason,
                    review_ids=review_ids, written_record_ids=written_record_ids,
                )
            if reconciled.outcome.value in {"gap", "new_candidate", "conflict"}:
                needs_review = True

    return CreateChainResult(
        status="needs_human_review" if needs_review else "succeeded",
        review_ids=review_ids,
        written_record_ids=written_record_ids,
    )
