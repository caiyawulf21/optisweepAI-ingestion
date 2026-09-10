"""Route handler logic for the four appcode-facing endpoints -- thin
functions, no FastAPI/HTTP framework imports here, so every handler is
directly unit-testable with fake providers (mirroring mcp_server/tools.py's
own separation from mcp_server/server.py's transport wiring). app.py wires
these into actual FastAPI routes.
"""

from __future__ import annotations

from brain.schemas.common import RecordType
from brain.schemas.review import BrainReview, ReviewResolution
from brain_service.audit import resolve_audit_candidate
from brain_service.audit_execution import apply_audit_resolution
from brain_service.context import get_brain_context
from brain_service.create_chain import run_create_chain
from brain_service.hydration import hydrate_context_packet
from providers.embeddings import EmbeddingProvider
from providers.llm import LLMProvider
from providers.storage import StorageProvider

from http_server.models import (
    ContextResponse,
    ContextRetrieveRequest,
    FeedbackEvent,
    FeedbackResponse,
    HydratedExcerptResponse,
    ReviewListResponse,
    ReviewResolveRequest,
    ReviewResolveResponse,
    ReviewSummary,
    TroubleshootRequest,
)


class ReviewNotFoundError(ValueError):
    def __init__(self, review_id: str) -> None:
        super().__init__(f"review id {review_id!r} does not exist")


def _context_response(hydrated) -> ContextResponse:
    return ContextResponse(
        task=hydrated.packet.task,
        excerpts=[
            HydratedExcerptResponse(
                id=e.id, type=e.type, label=e.label,
                validation_status=e.validation_status, text=e.text, truncated=e.truncated,
            )
            for e in hydrated.excerpts
        ],
        excerpt_count=len(hydrated.excerpts),
        truncated_excerpt_count=hydrated.truncated_excerpt_count,
        entity_ids=hydrated.packet.entities,
        approved_knowledge_ids=hydrated.packet.approved_knowledge,
    )


def handle_context_retrieve(
    request: ContextRetrieveRequest,
    *,
    storage: StorageProvider,
    embeddings: EmbeddingProvider,
) -> ContextResponse:
    packet = get_brain_context(
        storage,
        task={"route": "context/retrieve", "query_text": request.query_text},
        entity_ids=request.entity_ids or None,
        relationship_types=request.relationship_types,
        hops=request.hops,
        query_text=request.query_text,
        embeddings=embeddings,
    )
    hydrated = hydrate_context_packet(packet, storage=storage)
    return _context_response(hydrated)


def handle_troubleshoot(
    request: TroubleshootRequest,
    *,
    storage: StorageProvider,
    embeddings: EmbeddingProvider,
) -> ContextResponse:
    # A troubleshooting session's query text is synthesized from whatever
    # session state the app has -- there is no single free-text query the
    # way /retrieve has one, so observed_signals + the current node id
    # stand in for it, folded into query_text the same way any other
    # semantic search call would use it. Node/playbook ids resolve to real
    # Entity ids that seed the graph traversal only when they happen to
    # already look like well-formed entity ids (a raw node_id like "node_3"
    # is a Playbook-internal id, not a Brain entity id, and is intentionally
    # NOT passed to entity_ids -- only entity_ids the caller explicitly
    # supplies, or the query text itself, ground this call).
    query_text = " ".join(
        part for part in [request.current_node_id, *request.observed_signals] if part
    ).strip()
    packet = get_brain_context(
        storage,
        task={
            "route": "context/troubleshoot",
            "session_id": request.session_id,
            "playbook_id": request.playbook_id,
            "current_node_id": request.current_node_id,
        },
        entity_ids=request.entity_ids or None,
        hops=request.hops,
        query_text=query_text or None,
        embeddings=embeddings,
    )
    hydrated = hydrate_context_packet(packet, storage=storage)
    return _context_response(hydrated)


def handle_feedback(
    event: FeedbackEvent,
    *,
    llm: LLMProvider,
    storage: StorageProvider,
) -> FeedbackResponse:
    """Routes app-sourced feedback through the SAME Create-path chain
    pipeline ingestion uses (2026-09-09 write model: writes immediately as
    operational_unreviewed/conflicting, never gated on SME review --
    confirmed with appcode as the intended policy for app feedback too,
    not a special case)."""
    source_packet = {
        "source_type": "app_feedback",
        "session_id": event.session_id,
        "interaction_id": event.interaction_id,
        "sentiment": event.sentiment,
        "text": event.text,
        "targets": event.targets,
        "image_summaries": event.image_summaries,
    }
    result = run_create_chain(
        llm,
        storage,
        source_packet=source_packet,
        evidence_id_prefix=f"app_feedback:{event.session_id}:{event.interaction_id}",
        scope=f"operational_sources/app_feedback_{event.session_id}",
    )
    return FeedbackResponse(
        status=result.status,
        detail=result.detail,
        review_ids=result.review_ids,
        written_record_ids=result.written_record_ids,
    )


def _get_review(storage: StorageProvider, review_id: str) -> BrainReview:
    for record in storage.load_brain_context(record_type=RecordType.REVIEW):
        if record.id == review_id and isinstance(record, BrainReview):
            return record
    raise ReviewNotFoundError(review_id)


def handle_list_reviews(*, storage: StorageProvider, status: str | None = "open") -> ReviewListResponse:
    all_reviews = [
        r for r in storage.load_brain_context(record_type=RecordType.REVIEW) if isinstance(r, BrainReview)
    ]
    # open_count always reflects the TOTAL open count, independent of
    # `status` filtering the returned `reviews` list below -- it's the app
    # nav badge's number (per the appcode SME-review-page design), which
    # must stay meaningful even when a caller lists status="resolved".
    open_count = sum(1 for r in all_reviews if r.status == "open")
    reviews = [r for r in all_reviews if status is None or r.status == status]
    return ReviewListResponse(
        reviews=[
            ReviewSummary(
                id=r.id, kind=r.kind.value, check_name=r.check_name,
                affected_record_ids=r.affected_record_ids, proposed_change=r.proposed_change,
                status=r.status, resolution=r.resolution.value if r.resolution else None,
                resolved_by=r.resolved_by,
            )
            for r in reviews
        ],
        open_count=open_count,
    )


def handle_resolve_review(
    review_id: str,
    request: ReviewResolveRequest,
    *,
    llm: LLMProvider,
    storage: StorageProvider,
) -> ReviewResolveResponse:
    """SME resolves one BrainReview. If `request.resolution` is not given,
    runs resolve_audit_candidate (Tool 6) to get the agent's own proposed
    resolution first (matching find_audit_candidates -> resolve_audit_candidate's
    existing two-step contract); an explicit `resolution` always overrides
    whatever the agent proposed, since an SME's direct judgment call
    outranks a proposal. MERGE/RETYPE are then actually applied
    (apply_audit_resolution); any other resolution is recorded on the
    review but not applied to the corpus (see audit_execution.py's own
    docstring for why)."""
    review = _get_review(storage, review_id)

    if request.resolution is not None:
        resolved_review = review.model_copy(
            update={
                "status": "resolved",
                "resolution": ReviewResolution(request.resolution),
                "resolved_by": "human",
                # An SME's own new_entity_type always overrides whatever
                # the review already carried (e.g. from a prior agent
                # proposal) -- same "human judgment outranks a proposal"
                # rule as `resolution` itself, just for this one extra field.
                "fields_to_rewrite": (
                    {**review.fields_to_rewrite, "entity_type": request.new_entity_type}
                    if request.new_entity_type
                    else review.fields_to_rewrite
                ),
            }
        )
    else:
        resolved_review = resolve_audit_candidate(llm, storage, review)

    new_entity_type = request.new_entity_type or resolved_review.fields_to_rewrite.get("entity_type")
    execution = apply_audit_resolution(
        storage, resolved_review, winner_record_id=request.winner_record_id, new_entity_type=new_entity_type
    )

    scope = storage.find_scope_for_record(review.id) or "reviews/resolved"
    storage.save_brain_records([resolved_review], scope=scope)

    return ReviewResolveResponse(
        review_id=review_id,
        resolution=execution.resolution.value,
        applied=execution.applied,
        mutated_record_ids=execution.mutated_record_ids,
        detail=execution.detail,
    )
