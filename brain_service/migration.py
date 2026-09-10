"""Tool 7 -- run_migration_batch (AGENT_DESIGN_NOTES.md §10.3).

Pure orchestration: loops the Create-path chain (extract_evidence ->
classify_candidate -> reconcile_candidate -> validate_and_prepare_for_review)
once per item, collecting a per-item outcome into one batch report.
Contains zero extraction/classification/reconciliation logic of its own --
every judgment call still happens inside the four existing tools.

Must not retry a failed item with looser validation, must not silently
skip a needs_human_review outcome, must not continue past a pattern of
repeated failures without surfacing it.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Callable

from brain_service.audit import find_audit_candidates
from brain_service.create_chain import run_create_chain
from providers.llm import LLMProvider
from providers.storage import StorageProvider

_CONSECUTIVE_FAILURE_THRESHOLD = 3


@dataclass
class ItemOutcome:
    item: str
    status: str  # "succeeded" | "needs_human_review" | "failed"
    detail: str = ""
    review_ids: list[str] = field(default_factory=list)


@dataclass
class MigrationBatchReport:
    outcomes: list[ItemOutcome] = field(default_factory=list)
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


def run_migration_batch(
    llm: LLMProvider,
    storage: StorageProvider,
    items: list[str],
    *,
    load_source_packet: Callable[[str], dict[str, Any]],
    scope_for_item: Callable[[str], str] | None = None,
) -> MigrationBatchReport:
    """`load_source_packet(item) -> dict` turns one batch item identifier
    (a case id, a source id) into the bounded packet extract_evidence
    expects -- this is the one caller-supplied seam, since what "one item"
    means is specific to the caller's backlog, not something this generic
    orchestrator should know. `scope_for_item(item) -> str` does the same
    for where a resulting write lands (e.g. "incidents/case_228086");
    defaults to using `item` itself as the scope when not given."""
    report = MigrationBatchReport()
    consecutive_failures: list[str] = []
    resolve_scope = scope_for_item or (lambda item: item)

    for item in items:
        try:
            outcome = _run_one_item(llm, storage, item, load_source_packet, resolve_scope(item))
        except Exception as exc:  # noqa: BLE001 -- must record, not raise, so the batch continues
            outcome = ItemOutcome(item=item, status="failed", detail=str(exc))

        report.outcomes.append(outcome)

        if outcome.status == "failed":
            consecutive_failures.append(outcome.detail)
        else:
            consecutive_failures.clear()

        if len(consecutive_failures) >= _CONSECUTIVE_FAILURE_THRESHOLD:
            most_common_detail, count = Counter(consecutive_failures).most_common(1)[0]
            if count >= _CONSECUTIVE_FAILURE_THRESHOLD:
                report.systemic_failure_detected = True
                report.systemic_failure_detail = (
                    f"{count} consecutive failures with the same error -- likely systemic, "
                    f"not per-item: {most_common_detail}"
                )
                break

    ids_created = [rid for outcome in report.outcomes for rid in outcome.review_ids]
    if ids_created:
        find_audit_candidates(storage, record_ids=ids_created)

    return report


def _run_one_item(
    llm: LLMProvider,
    storage: StorageProvider,
    item: str,
    load_source_packet: Callable[[str], dict[str, Any]],
    scope: str,
) -> ItemOutcome:
    packet = load_source_packet(item)
    result = run_create_chain(llm, storage, source_packet=packet, evidence_id_prefix=item, scope=scope)
    return ItemOutcome(item=item, status=result.status, detail=result.detail, review_ids=result.review_ids)
