"""get_brain_context — the shared retrieval call used internally by
classify_candidate/reconcile_candidate and exposed directly via MCP.

Two query paths, composable: direct ID lookup + relationship-type
traversal + ValidationStatus filtering (the original MVP shape), and now
real semantic search (brain_service/retrieval.py) via `query_text` +
`embeddings` -- AGENT_DESIGN_NOTES.md §14.4 explicitly deferred "embeddings,
ranking" as retrieval-engine work; this is that engine, built once the
corpus had real stored vectors to search (brain_service/scripts/
backfill_embeddings.py) rather than before there was anything to search.
"""

from __future__ import annotations

from typing import Any

from brain.schemas.claim import Claim
from brain.schemas.common import RecordType
from brain.schemas.context_packet import APPROVED_KNOWLEDGE_STATUSES, ContextPacket
from brain.schemas.entity import Entity
from brain.schemas.relationship import Relationship, RelationshipType
from providers.embeddings import EmbeddingProvider
from providers.storage import StorageProvider


def get_brain_context(
    storage: StorageProvider,
    *,
    task: dict[str, Any],
    entity_ids: list[str] | None = None,
    relationship_types: list[RelationshipType] | None = None,
    hops: int = 1,
    include_unapproved: bool = False,
    query_text: str | None = None,
    embeddings: EmbeddingProvider | None = None,
    semantic_top_k: int = 10,
    semantic_min_score: float = 0.75,
) -> ContextPacket:
    """Direct ID lookup + relationship-type traversal + ValidationStatus
    filtering. `hops` defaults to 1 (bounded, safe default); a traversal
    like the §14.4 worked example (symptom -MAY_INDICATE-> capability
    -USES<- procedure) needs hops=2, passed explicitly by the caller.

    If `query_text` and `embeddings` are both given, semantic search finds
    the closest-matching Entities (merged into the traversal frontier
    alongside any explicit `entity_ids`) and the closest-matching Claims/
    EvidenceUnits (cited directly into the returned packet, since a claim
    or evidence match doesn't need graph traversal to be relevant -- it
    already IS the relevant thing). `entity_ids` and `query_text` may be
    used together or alone; passing neither returns an empty packet, same
    as before this capability existed.

    `include_unapproved` is accepted but has no effect on approved_knowledge
    in this MVP -- ContextPacket has no field for "relevant but unreviewed"
    beyond `conflicts` (which is specifically for BrainReview(kind=CONFLICT)
    records). It is reserved for a future extension, not silently dropped.
    """
    del include_unapproved  # reserved; no ContextPacket field to populate yet

    seed_entity_ids = set(entity_ids or [])
    semantic_claim_ids: set[str] = set()
    semantic_evidence_ids: set[str] = set()

    if query_text and embeddings is not None:
        from brain_service.retrieval import find_similar_records

        # Embed the query ONCE and reuse the vector for all three searches
        # below -- embedding is a real Azure OpenAI/Foundry network call,
        # and calling find_similar_records with query_text 3x here
        # previously re-embedded the identical text 3 times per request, a
        # real, measured cost in production (2026-09-10: found via direct
        # latency testing against the deployed HTTP API, not assumed).
        query_vector = embeddings.embed_texts([query_text])[0]

        entity_matches = find_similar_records(
            embeddings, storage, query_vector=query_vector, record_type=RecordType.ENTITY,
            top_k=semantic_top_k, min_score=semantic_min_score,
        )
        seed_entity_ids |= {match.record_id for match in entity_matches}

        claim_matches = find_similar_records(
            embeddings, storage, query_vector=query_vector, record_type=RecordType.CLAIM,
            top_k=semantic_top_k, min_score=semantic_min_score,
        )
        semantic_claim_ids = {match.record_id for match in claim_matches}

        evidence_matches = find_similar_records(
            embeddings, storage, query_vector=query_vector, record_type=RecordType.EVIDENCE_UNIT,
            top_k=semantic_top_k, min_score=semantic_min_score,
        )
        semantic_evidence_ids = {match.record_id for match in evidence_matches}

    frontier = seed_entity_ids
    visited_entities: set[str] = set()
    all_entities: dict[str, Entity] = {}
    all_relationships: dict[str, Relationship] = {}

    def _load_entities(ids: set[str]) -> None:
        if not ids:
            return
        for record in storage.load_brain_context(entity_ids=list(ids), record_type=RecordType.ENTITY):
            if isinstance(record, Entity):
                all_entities[record.id] = record

    _load_entities(frontier)
    for _ in range(max(0, hops)):
        if not frontier:
            break
        visited_entities |= frontier

        relationships = [
            record
            for record in storage.load_brain_context(record_type=RecordType.RELATIONSHIP)
            if isinstance(record, Relationship)
            and (record.from_id in frontier or record.to_id in frontier)
            and (relationship_types is None or record.relationship_type in relationship_types)
        ]
        next_frontier: set[str] = set()
        for relationship in relationships:
            all_relationships[relationship.id] = relationship
            next_frontier.add(relationship.from_id)
            next_frontier.add(relationship.to_id)
        frontier = next_frontier - visited_entities
        # The newly-discovered frontier's own Entity records must be loaded
        # here, at the end of this hop, not deferred to the next iteration's
        # start -- on the LAST hop there is no next iteration, so an entity
        # discovered only via a relationship endpoint on the final hop was
        # previously never loaded at all (found via test coverage: hops=1
        # returned only the seed entity, never the one hop away from it).
        _load_entities(frontier)

    claims = [
        record
        for record in storage.load_brain_context(record_type=RecordType.CLAIM)
        if isinstance(record, Claim)
        and (record.subject_entity_id in all_entities or record.id in semantic_claim_ids)
    ]

    approved_ids: list[str] = []
    evidence_ids: set[str] = set(semantic_evidence_ids)
    for record in [*all_entities.values(), *all_relationships.values(), *claims]:
        evidence_ids.update(record.source_refs)
        if record.validation_status in APPROVED_KNOWLEDGE_STATUSES:
            approved_ids.append(record.id)

    return ContextPacket(
        task=task,
        entities=list(all_entities.keys()),
        approved_knowledge=approved_ids,
        evidence_excerpts=sorted(evidence_ids),
    )
