"""Tool 3 -- reconcile_candidate (AGENT_DESIGN_NOTES.md §4.2, folding in the
duplicate-check from §4.1/§10.3).

Given one classified candidate + retrieved existing Brain records of the
same type, decides Reinforce / Patch / Conflict / Gap / New-candidate. For
New-candidate, runs find_audit_candidates as the mandatory duplicate check
before finalizing -- a name/evidence match alone is never sufficient
grounds to merge (§3's confirmed lesson); this tool only PROPOSES the
outcome, it does not write anything to the corpus itself (that is Tool 4's
job, after validation).
"""

from __future__ import annotations

import json
from pathlib import Path

from brain.schemas.claim import Claim
from brain.schemas.common import RecordType
from brain_service.audit import find_audit_candidates
from brain_service.context import get_brain_context
from brain_service.types import ClassifiedCandidate, ClassifiedRecordKind, ReconciliationDecision
from providers.llm import LLMProvider
from providers.storage import StorageProvider

_PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "reconcile_candidate.md"

_RECORD_TYPE_BY_KIND = {
    ClassifiedRecordKind.ENTITY: RecordType.ENTITY,
    ClassifiedRecordKind.CAPABILITY: RecordType.CAPABILITY,
    ClassifiedRecordKind.CLAIM: RecordType.CLAIM,
    ClassifiedRecordKind.RELATIONSHIP: RecordType.RELATIONSHIP,
}


def _load_prompt() -> str:
    return _PROMPT_PATH.read_text(encoding="utf-8")


def reconcile_candidate(
    llm: LLMProvider,
    storage: StorageProvider,
    classified: ClassifiedCandidate,
) -> ReconciliationDecision:
    record_type = _RECORD_TYPE_BY_KIND.get(classified.record_kind)
    existing_records = storage.load_brain_context(record_type=record_type) if record_type else []

    subject_entity_id = classified.proposed_fields.get("subject_entity_id")
    context_packet = get_brain_context(
        storage,
        task={"tool": "reconcile_candidate", "record_kind": classified.record_kind.value},
        entity_ids=[subject_entity_id] if subject_entity_id else None,
        hops=1,
    )

    user_content = json.dumps(
        {
            "classified_candidate": classified.model_dump(mode="json"),
            "retrieved_existing_records": [record.model_dump(mode="json") for record in existing_records[:50]],
            "retrieved_context_packet": context_packet.model_dump(mode="json"),
        },
        ensure_ascii=False,
    )

    decision = llm.generate_json(
        system_prompt=_load_prompt(),
        user_content=user_content,
        schema=ReconciliationDecision,
        label="reconcile_candidate",
    )

    if decision.outcome.value == "new_candidate" and not decision.duplicate_check_performed:
        # The mandatory duplicate check (§4.1/§10.3): find_audit_candidates
        # always scans the whole corpus (a duplicate is a relationship to
        # something else already in it), filtered here to findings that
        # actually touch this candidate's own likely ids.
        candidate_ids = list({*decision.affected_record_ids, *context_packet.entities})
        find_audit_candidates(storage, record_ids=candidate_ids or None)
        decision = decision.model_copy(update={"duplicate_check_performed": True})

    return decision
