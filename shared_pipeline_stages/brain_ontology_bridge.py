"""Drop-in, Brain-backed replacements for the two ontology_rag.py functions
shared_pipeline_stages/stage_8/playbook_builder.py calls
(ontology_contracts_for_capabilities, ontology_snippets_for_stage5_playbook).

Not wired into playbook_builder.py yet -- that file is under active,
uncommitted development on this branch (2026-09-09), so this module is
built and tested standalone. Swapping it in later is a two-line import
change per call site (see each function's docstring below for the exact
signature match), once the in-flight Stage 8 work lands.

Why this exists: playbook_builder.py's grounding today comes from the
static docs/ontology/catalogs/*.json files via ontology_rag.py. Brain
(brain/, brain_service/) now holds the same kind of knowledge --
Capability records with their own support_contract/sql_field_notes, plus
Entity/Claim/EvidenceUnit records reachable via semantic search -- as a
live, versioned corpus rather than a static file. This module reads FROM
Brain instead, without changing anything about how playbook_builder.py
uses the results: both functions here match their ontology_rag.py
counterparts' exact call signature and return shape, verified against the
real consumer (action_synthesis.py::_selected_ontology_entities, which
reads only `id`/`title`/`score`/`source_refs`/`text` keys from each
snippet dict -- confirmed by reading that function, not assumed).
"""

from __future__ import annotations

from typing import Any

from brain.schemas.capability import Capability
from brain_service.embedding_text import embedding_text_for
from brain_service.retrieval import find_similar_records
from providers.embeddings import EmbeddingProvider
from providers.storage import StorageProvider


def brain_contracts_for_capabilities(
    capability_ids: list[str] | set[str] | None,
    *,
    storage: StorageProvider,
) -> list[dict[str, Any]]:
    """Matches ontology_rag.ontology_contracts_for_capabilities's signature
    and return shape: given capability ids (bare names like
    "confirm_agv_active_error_state", OR already-prefixed
    "capability:confirm_agv_active_error_state" -- both accepted, matching
    the original function's own normalization), returns
    [{"id": "capability:<name>", "support_contract": {...}, "backend_mappings": [...]}]
    per matched Capability found in Brain.

    Brain's Capability schema (brain/schemas/capability.py) already carries
    `support_contract` (SupportContract: diagnostic_surface_entity_ids,
    control_surface_entity_ids, required_evidence_capability_ids,
    forbidden_capability_ids, preferred_surface_entity_id) as a first-class
    field -- no reshaping needed there. `backend_mappings` has no direct
    Brain equivalent field; it's derived here from `sql_field_notes`
    (database_entity_id/table_entity_id/field/purpose), grouped by table,
    mirroring the shape ontology_rag.py synthesizes from
    primary_models/field_highlights for the same downstream consumer.
    """
    requested = {
        str(value).split(":", 1)[1] if str(value).startswith("capability:") else str(value)
        for value in capability_ids or []
        if str(value).strip()
    }
    if not requested:
        return []

    contracts: list[dict[str, Any]] = []
    for record in storage.load_brain_context():
        if not isinstance(record, Capability):
            continue
        bare_name = record.id.split(":", 1)[-1]
        if bare_name not in requested:
            continue

        support_contract = record.support_contract.model_dump(mode="json") if record.support_contract else {}

        fields_by_table: dict[str, list[str]] = {}
        for note in record.sql_field_notes:
            table_key = note.table_entity_id or note.database_entity_id or ""
            if table_key:
                fields_by_table.setdefault(table_key, []).append(note.field)
        backend_mappings = [
            {
                "operational_concept": bare_name,
                "preferred_support_surface": "wcs_sql",
                "support_read_sources": [
                    {
                        "surface": "wcs_sql",
                        "database": table_key,
                        "model": table_key,
                        "fields": fields[:8],
                    }
                ],
            }
            for table_key, fields in list(fields_by_table.items())[:3]
        ]

        contracts.append(
            {
                "id": f"capability:{bare_name}",
                "support_contract": support_contract,
                "backend_mappings": backend_mappings,
            }
        )
    return contracts


def brain_snippets_for_stage5_playbook(
    text: str,
    *,
    embeddings: EmbeddingProvider,
    storage: StorageProvider,
    artifacts: list[dict[str, Any]] | None = None,
    max_snippets: int = 6,
    min_score: float = 0.7,
) -> list[dict[str, Any]]:
    """Matches ontology_rag.ontology_snippets_for_stage5_playbook's
    signature (`artifacts` accepted but unused here, same as the original
    -- it's part of the shared call signature across ontology_rag.py's
    sibling functions, not actually read by this one either) and return
    shape: ranked snippet dicts with `id`/`title`/`score`/`source_refs`/
    `text` keys, the only keys action_synthesis.py's
    _selected_ontology_entities() reads.

    Where ontology_snippets_for_stage5_playbook ranks by snippet KIND
    first (model > capability > db > surface > activity) and score
    second, this ranks by real cosine similarity alone across
    Capability/Entity/EvidenceUnit records -- Brain has no equivalent
    "kind" taxonomy to rank by, and semantic score is the more direct
    relevance signal now that real embeddings exist over the whole corpus
    (brain_service/retrieval.py). `STAGE5_PLAYBOOK_MAX_SNIPPETS` (6) and a
    0.7 min-score floor are carried over as sane defaults matching
    get_brain_context's own existing semantic-search defaults, not
    re-derived from the original's char-budget-based cutoff (Brain
    snippets are short structured dicts, not char-budgeted prose blocks).
    """
    del artifacts  # accepted for signature parity; unused by the original too
    if not text.strip():
        return []

    from brain.schemas.entity import Entity

    matches = find_similar_records(
        embeddings,
        storage,
        query_text=text,
        top_k=max_snippets,
        min_score=min_score,
    )
    if not matches:
        return []

    records_by_id = {record.id: record for record in storage.load_brain_context()}
    snippets: list[dict[str, Any]] = []
    for match in matches:
        record = records_by_id.get(match.record_id)
        if record is None:
            continue
        title = record.name if isinstance(record, (Capability, Entity)) else record.id
        snippets.append(
            {
                "id": record.id,
                "title": title,
                "score": round(match.score, 4),
                "source_refs": list(record.source_refs),
                "text": embedding_text_for(record)[:500],
            }
        )
    return snippets
