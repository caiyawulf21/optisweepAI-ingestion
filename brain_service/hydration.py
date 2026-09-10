"""Resolves a ContextPacket's bare record ids into actual, truncated,
status-labeled content -- the "critical response rule" from the appcode
HTTP boundary agreement (2026-09-09): runtime callers must never receive
an ID-only ContextPacket, since ContextPacket.entities/approved_knowledge/
evidence_excerpts/etc. are all `list[str]` by design (see that schema's
own docstring: "never inlined record content"). This module is the one
place that resolution happens, so /context/retrieve and
/context/troubleshoot (and any future HTTP route) hydrate identically.

Only a record whose validation_status is in APPROVED_KNOWLEDGE_STATUSES
is labeled "approved" guidance; everything else comes back labeled
"working" or "conflict" so a caller can never cite unreviewed material as
fact -- this filter already existed as APPROVED_KNOWLEDGE_STATUSES
(brain/schemas/context_packet.py); this module applies it to real content,
it does not re-derive it.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from brain.schemas.common import ValidationStatus
from brain.schemas.context_packet import APPROVED_KNOWLEDGE_STATUSES, ContextPacket
from brain.schemas.review import BrainReview
from brain.validators import BrainRecordUnion
from brain_service.embedding_text import embedding_text_for
from providers.storage import StorageProvider

# Anchor: get_brain_context's own semantic-search default is top_k=10 per
# record type. Proposed to and confirmed with appcode (2026-09-09):
# roughly the same excerpt COUNT, but far more room per excerpt than the
# ~500-char convention embedding_text_for uses for search-indexing text
# (that length is tuned for embedding relevance, not for something a
# person or LLM needs to actually read and act on downstream).
MAX_HYDRATED_EXCERPTS = 15
MAX_EXCERPT_CHARS = 2000


def _label_for_status(status: ValidationStatus) -> str:
    if status in APPROVED_KNOWLEDGE_STATUSES:
        return "approved"
    if status == ValidationStatus.CONFLICTING:
        return "conflict"
    return "working"


@dataclass
class HydratedExcerpt:
    id: str
    type: str
    label: str  # "approved" | "working" | "conflict"
    validation_status: str
    text: str
    truncated: bool


@dataclass
class HydratedContextPacket:
    """The actual HTTP response shape for /context/retrieve and
    /context/troubleshoot -- packet (the original ID-only ContextPacket,
    kept for audit/citation purposes) plus excerpts (real, truncated,
    labeled content a caller can put directly in front of a person or an
    LLM)."""

    packet: ContextPacket
    excerpts: list[HydratedExcerpt] = field(default_factory=list)
    truncated_excerpt_count: int = 0  # how many ids from the packet were dropped for exceeding MAX_HYDRATED_EXCERPTS


def hydrate_context_packet(
    packet: ContextPacket,
    *,
    storage: StorageProvider,
    max_excerpts: int = MAX_HYDRATED_EXCERPTS,
    max_excerpt_chars: int = MAX_EXCERPT_CHARS,
) -> HydratedContextPacket:
    """Resolves every id in `packet`'s entities/approved_knowledge/
    evidence_excerpts/conflicts fields to real content, deduplicated
    (an id can legitimately appear in more than one field -- e.g. an
    approved Entity is also in `entities`), ordered so approved_knowledge
    ids are hydrated first (a caller truncated by max_excerpts should lose
    working/conflict material before approved material, never the other
    way around)."""
    ordered_ids: list[str] = []
    seen: set[str] = set()
    for id_list in (packet.approved_knowledge, packet.entities, packet.evidence_excerpts, packet.conflicts):
        for record_id in id_list:
            if record_id not in seen:
                seen.add(record_id)
                ordered_ids.append(record_id)

    if not ordered_ids:
        return HydratedContextPacket(packet=packet)

    selected_ids = ordered_ids[:max_excerpts]
    truncated_count = len(ordered_ids) - len(selected_ids)

    records_by_id = {r.id: r for r in storage.load_brain_context(entity_ids=ordered_ids)}
    # load_brain_context's entity_ids filter matches ANY record type by id
    # (see LocalStorageProvider's own docstring for that method), not only
    # Entity records -- correct here since evidence_excerpts/conflicts ids
    # are EvidenceUnit/Claim ids, not Entity ids.

    excerpts: list[HydratedExcerpt] = []
    for record_id in selected_ids:
        record = records_by_id.get(record_id)
        if record is None:
            continue
        excerpts.append(_hydrate_one(record, max_excerpt_chars=max_excerpt_chars))

    return HydratedContextPacket(packet=packet, excerpts=excerpts, truncated_excerpt_count=truncated_count)


def _hydrate_one(record: BrainRecordUnion, *, max_excerpt_chars: int) -> HydratedExcerpt:
    if isinstance(record, BrainReview):
        # A BrainReview has no validation_status-based approval concept of
        # its own (it's audit-trail material about OTHER records, not
        # citable knowledge) -- always "working", never "approved".
        text = record.proposed_change or record.check_name or ""
        label = "working"
        status_value = "n/a"
    else:
        text = embedding_text_for(record)
        label = _label_for_status(record.validation_status)
        status_value = record.validation_status.value

    truncated = len(text) > max_excerpt_chars
    return HydratedExcerpt(
        id=record.id,
        type=record.type.value,
        label=label,
        validation_status=status_value,
        text=text[:max_excerpt_chars],
        truncated=truncated,
    )
