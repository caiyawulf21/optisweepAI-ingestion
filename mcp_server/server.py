"""MCP stdio server entrypoint. Registers all seven ingestion/Brain tools,
draft_procedure and draft_playbook (Tools 8-9, draft FROM Brain instead of
the static ontology catalog), plus get_brain_context, validate_brain_records,
prepare_sme_review, get_ingestion_run, and the two pipeline orchestration
tools (ingest_incident_pdf, ingest_operational_source).

Run with: python -m mcp_server.server
(or via the `optisweep-brain-mcp` console script once installed --
see mcp_server/pyproject.toml)
"""

from __future__ import annotations

from typing import Any

from mcp.server import MCPServer

from mcp_server import tools

server = MCPServer(
    "optisweep-brain",
    instructions=(
        "Tools for ingesting OptiSweep operational sources and incidents into "
        "the Brain knowledge corpus, and for auditing/reconciling/migrating "
        "that corpus. Does not serve runtime context to an end user or "
        "capture app feedback -- that belongs to the separate appcode "
        "repository. See newdesigndoc/BRAIN_AGENT_HANDOFF.md for the full "
        "contract."
    ),
)


@server.tool()
def extract_evidence(source_packet: dict[str, Any]) -> dict[str, Any]:
    """Turn one bounded raw source packet into EvidenceUnit candidates and
    raw claim candidates. Never judges truth, never resolves an entity id,
    never decides anything is a duplicate."""
    return tools.tool_extract_evidence(source_packet)


@server.tool()
def classify_candidate(
    candidate_text: str, evidence_id: str, likely_entity_ids: list[str] | None = None
) -> dict[str, Any]:
    """Classify one raw claim candidate as an Entity, Capability, Claim, or
    Relationship, per the locked entity/claim boundary test."""
    return tools.tool_classify_candidate(candidate_text, evidence_id, likely_entity_ids)


@server.tool()
def reconcile_candidate(classified: dict[str, Any]) -> dict[str, Any]:
    """Decide REINFORCE/PATCH/CONFLICT/GAP/NEW_CANDIDATE for one classified
    candidate against the existing Brain corpus, running the mandatory
    duplicate check for NEW_CANDIDATE outcomes."""
    return tools.tool_reconcile_candidate(classified)


@server.tool()
def validate_and_prepare_for_review(reconciled: dict[str, Any]) -> dict[str, Any]:
    """Mechanically validate a reconciled candidate and draft a plain-language
    BrainReview for human approval. Never self-approves."""
    return tools.tool_validate_and_prepare_for_review(reconciled)


@server.tool()
def find_audit_candidates(record_ids: list[str] | None = None) -> dict[str, Any]:
    """Read-only corpus scan for duplicates, mis-typed records, and dangling
    references. Deliberately over-reports; never resolves anything."""
    return tools.tool_find_audit_candidates(record_ids)


@server.tool()
def resolve_audit_candidate(review: dict[str, Any]) -> dict[str, Any]:
    """Propose MERGE/RETYPE/RECLASSIFY/NOT_A_DUPLICATE/NEEDS_HUMAN for one
    audit finding. Proposes only -- does not write the resolution to the
    corpus."""
    return tools.tool_resolve_audit_candidate(review)


@server.tool()
def run_migration_batch(items: list[str], source_packets: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Pure orchestration: loop the Create-path chain over a batch of
    source/case identifiers, each mapped to its already-loaded source
    packet in `source_packets`."""
    return tools.tool_run_migration_batch(items, source_packets)


@server.tool()
def draft_procedure(
    capability_id: str,
    distinguishing_token: str,
    scope: str,
    extra_source_evidence_ids: list[str] | None = None,
    write: bool = False,
) -> dict[str, Any]:
    """Draft a Procedure for `capability_id`, grounded in that Capability's
    own fields (observables/sql_field_notes/support_contract/when_to_use/
    role_paths) plus retrieved Brain context -- not the static
    docs/ontology/catalogs snippets the old Stage 5/6 pipeline drafts from.
    Returns the constructed Procedure plus any drafting `gaps` without
    writing unless `write=True`."""
    return tools.tool_draft_procedure(capability_id, distinguishing_token, scope, extra_source_evidence_ids, write)


@server.tool()
def draft_playbook(
    entry_symptom_entity_ids: list[str],
    distinguishing_token: str,
    scope: str,
    write: bool = False,
) -> dict[str, Any]:
    """Draft a Playbook routing from `entry_symptom_entity_ids` to
    already-existing Procedures, grounded in the symptom graph
    (MAY_INDICATE/VERIFIES/CAUSES/CONTRIBUTES_TO) plus each reachable
    Capability's own already-drafted Procedures -- never embeds Procedure
    steps directly, only references procedure_id. Returns the constructed
    Playbook plus any drafting `gaps` without writing unless `write=True`."""
    return tools.tool_draft_playbook(entry_symptom_entity_ids, distinguishing_token, scope, write)


@server.tool()
def get_brain_context(
    task: dict[str, Any],
    entity_ids: list[str] | None = None,
    relationship_types: list[str] | None = None,
    hops: int = 1,
    query_text: str | None = None,
) -> dict[str, Any]:
    """ID lookup + relationship-type traversal + ValidationStatus
    filtering, optionally seeded/expanded by real semantic search when
    `query_text` is given (embeds the query, finds the closest-matching
    Entities/Claims/EvidenceUnits by cosine similarity over the corpus'
    stored embeddings). Returns a ContextPacket (record IDs only, never
    inlined content)."""
    return tools.tool_get_brain_context(task, entity_ids, relationship_types, hops, query_text)


@server.tool()
def validate_brain_records(records_by_type: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    """Bare schema + cross-reference validation for a batch of records,
    keyed by type (evidence_units/entities/claims/relationships/
    capabilities/procedures/playbooks/reviews)."""
    return tools.tool_validate_brain_records(records_by_type)


@server.tool()
def prepare_sme_review(candidate_record_ids: list[str], kind: str, proposed_change: str) -> dict[str, Any]:
    """Persist a BrainReview for human approval. Does not call an LLM to
    draft the explanation -- proposed_change is caller-supplied text."""
    return tools.tool_prepare_sme_review(candidate_record_ids, kind, proposed_change)


@server.tool()
def get_ingestion_run(run_id: str) -> dict[str, Any] | None:
    """Load previously saved run state for one ingestion job."""
    return tools.tool_get_ingestion_run(run_id)


@server.tool()
def ingest_incident_pdf(
    source_pdf_path: str,
    case_id: str,
    site_code: str = "ups_haslet_tx",
    output_dir: str | None = None,
    stages: str = "1,2,2.5,3,4,5,6,8",
) -> dict[str, Any]:
    """Run the existing incidenceknowledgeingestion pipeline (stages 1-8)
    with BRAIN_INGESTION_ENABLED=1, so each stage's own Brain hook fires in
    tandem as it runs. Does not duplicate any pipeline logic -- calls the
    same CLI script a human would run."""
    return tools.tool_ingest_incident_pdf(source_pdf_path, case_id, site_code, output_dir, stages)


@server.tool()
def ingest_operational_source(
    source_pdf_path: str,
    source_id: str,
    source_type: str = "manual",
    output_dir: str | None = None,
    stages: str = "1,2,3,4,5,6,8",
) -> dict[str, Any]:
    """Run the existing operationalknowledgeingestion pipeline with
    BRAIN_INGESTION_ENABLED=1, same shape as ingest_incident_pdf."""
    return tools.tool_ingest_operational_source(source_pdf_path, source_id, source_type, output_dir, stages)


def main() -> None:
    server.run()


if __name__ == "__main__":
    main()
