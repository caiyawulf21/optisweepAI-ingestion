"""ingest_stage_output -- the in-tandem integration point every pipeline
stage module calls on its own new output before returning (plan §5:
"Ingestion and Brain-building run in tandem, per stage").

Gated by BRAIN_INGESTION_ENABLED, defaulting to ON (2026-09-09,
user-directed: "brain ingestion should always be enabled"). Brain
ingestion is now the normal behavior of every pipeline stage call --
existing tests/scripts that need pipeline-only behavior (no network/LLM
calls, e.g. to run offline or without Azure credentials) must explicitly
set BRAIN_INGESTION_ENABLED=0/false/no to opt out; nothing opts out
implicitly anymore.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Literal

from brain_service.create_chain import run_create_chain
from providers.llm import LLMProvider
from providers.storage import StorageProvider

_CONSECUTIVE_FAILURE_THRESHOLD = 3


def brain_enabled() -> bool:
    value = os.getenv("BRAIN_INGESTION_ENABLED")
    if value is None:
        return True
    return value.strip().lower() in {"1", "true", "yes"}


@dataclass
class RecordOutcome:
    record_index: int
    status: Literal["succeeded", "needs_human_review", "failed"]
    detail: str = ""
    review_ids: list[str] = field(default_factory=list)


@dataclass
class PipelineHookResult:
    pipeline: str
    stage_name: str
    source_id: str
    outcomes: list[RecordOutcome] = field(default_factory=list)
    systemic_failure_detected: bool = False
    systemic_failure_detail: str = ""

    @property
    def succeeded_count(self) -> int:
        return sum(1 for o in self.outcomes if o.status == "succeeded")

    @property
    def failed_count(self) -> int:
        return sum(1 for o in self.outcomes if o.status == "failed")

    @property
    def needs_human_review_count(self) -> int:
        return sum(1 for o in self.outcomes if o.status == "needs_human_review")


def ingest_stage_output(
    *,
    llm: LLMProvider,
    storage: StorageProvider,
    pipeline: Literal["operational", "incidence"],
    stage_name: str,
    source_id: str,
    scope: str,
    records: list[dict[str, Any]],
    record_kind: str,
) -> PipelineHookResult:
    """Runs extract_evidence -> classify_candidate -> reconcile_candidate ->
    validate_and_prepare_for_review once per record in `records`, against
    the live Brain corpus. Never raises on a single record's failure --
    collects it into the result and continues, surfacing (not swallowing)
    3+ consecutive same-error failures the same way run_migration_batch
    does, since this is the identical per-item loop shape at stage-scope
    instead of batch-scope."""
    result = PipelineHookResult(pipeline=pipeline, stage_name=stage_name, source_id=source_id)
    consecutive_failures: list[str] = []
    total = len(records)

    for index, record in enumerate(records):
        print(
            f"[brain] {pipeline}/{stage_name} {source_id}: ingesting {record_kind} {index + 1}/{total}...",
            flush=True,
        )
        try:
            outcome = _ingest_one_record(
                llm, storage, source_id=source_id, record=record, record_kind=record_kind, index=index, scope=scope
            )
        except Exception as exc:  # noqa: BLE001 -- must record, not raise, so the stage continues
            outcome = RecordOutcome(record_index=index, status="failed", detail=str(exc))

        print(
            f"[brain] {pipeline}/{stage_name} {source_id}: {record_kind} {index + 1}/{total} -> "
            f"{outcome.status} ({len(outcome.review_ids)} review(s))",
            flush=True,
        )
        result.outcomes.append(outcome)

        if outcome.status == "failed":
            consecutive_failures.append(outcome.detail)
        else:
            consecutive_failures.clear()

        if len(consecutive_failures) >= _CONSECUTIVE_FAILURE_THRESHOLD:
            from collections import Counter

            most_common_detail, count = Counter(consecutive_failures).most_common(1)[0]
            if count >= _CONSECUTIVE_FAILURE_THRESHOLD:
                result.systemic_failure_detected = True
                result.systemic_failure_detail = (
                    f"{count} consecutive failures with the same error in {pipeline}/{stage_name} "
                    f"for {source_id} -- likely systemic, not per-record: {most_common_detail}"
                )
                break

    ids_created = [rid for outcome in result.outcomes for rid in outcome.review_ids]
    if ids_created:
        from brain_service.audit import find_audit_candidates

        find_audit_candidates(storage, record_ids=ids_created)

    return result


def _ingest_one_record(
    llm: LLMProvider,
    storage: StorageProvider,
    *,
    source_id: str,
    record: dict[str, Any],
    record_kind: str,
    index: int,
    scope: str,
) -> RecordOutcome:
    source_packet = {
        "source_id": source_id,
        "record_kind": record_kind,
        **record,
    }
    result = run_create_chain(
        llm,
        storage,
        source_packet=source_packet,
        evidence_id_prefix=f"{source_id}:{record_kind}:{index}",
        scope=scope,
    )
    return RecordOutcome(
        record_index=index,
        status=result.status,
        detail=result.detail,
        review_ids=result.review_ids,
    )
