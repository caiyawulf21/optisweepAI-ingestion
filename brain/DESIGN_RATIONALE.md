# Brain Design Rationale

This page preserves the useful substance from the retired `newdesigndoc/` design notes. Current behavior should still be verified against code, tests, `docs/architecture.md`, and `AGENT_AZURE_HANDOFF.md`.

## Core Architecture

The Brain is one source-agnostic OptiSweep knowledge system. Manuals, training videos, support guides, incidents, RCAs, SME notes, and future app feedback all enter the same evidence/entity/claim/relationship/capability/procedure/playbook model. No source type owns truth by itself.

The main design separation is:

```text
Source pipelines extract and package evidence.
Brain service decides how evidence changes the corpus.
Runtime apps retrieve, score, display, and collect feedback.
```

Raw evidence is immutable. A bounded `EvidenceUnit` records what a source said or showed at a location; later interpretations create or update derived records while preserving source references. Claims are deliberately separate from evidence so a single incident, LLM summary, or unreviewed feedback item does not become universal truth.

## Stable Records

Brain records use typed, deterministic IDs such as `entity:system:wcs`, `evidence:case_218550:event_007`, and `relationship:wcs:controls:agv_fleet`. Titles are never foreign keys.

The schema set is intentionally explicit:

```text
EvidenceUnit      bounded provenance
Entity            stable OptiSweep object
Claim             source-backed assertion with polarity
Relationship      typed graph edge
Capability        diagnostic/operational ability
Procedure         human-executable steps for a capability
Playbook          branching symptom-driven workflow
BrainReview       audit/reconciliation work item
ContextPacket     bounded working-memory response shape
```

Knowledge is global by default. `constraints: {}` means no site/version/environment restriction. Add constraints only when a source explicitly limits applicability.

`Entity.payload` is discriminated by `entity_type`; it is not a generic bag for unreviewed facts. Capability records describe what can be accomplished and under what support contract; executable steps live on Procedure records.

## Governance Boundary

`validation_status` is the runtime eligibility signal. `catalog_authoritative` and `sme_approved` are safe for approved guidance. `operational_unreviewed`, `needs_sme_review`, `conflicting`, and `deprecated` remain working or audit material.

Feedback and incident observations are evidence, not truth. The ingestion chain extracts, classifies, reconciles, validates, and records reviews rather than directly promoting new statements as approved guidance.

## Storage Model

Brain is graph-ready without requiring a graph database. Entities are nodes, Relationships are edges, and derived records cite stable IDs. This is enough for traversal and validation at the current scale.

Local files remain the development and handoff corpus under `brain/data/local/`. Azure Cosmos is the durable shared store when `OPTISWEEP_STORAGE_BACKEND=azure` is set.

Brain's Cosmos containers are separate from the Stage 11 app-publish containers. Brain containers are all `brain_*` and use a synthetic top-level partition key path `/_partition_key`, computed from record content by `providers/azure_cosmos_config.py`. Stage 11 app-publish containers use `/publish_version_id`.

Brain containers:

```text
brain_evidence
brain_entities
brain_claims
brain_relationships
brain_capabilities
brain_procedures
brain_playbooks
brain_reviews
brain_ingestion_runs
brain_embeddings
```

Provision and sync:

```powershell
python -m providers.scripts.provision_brain_cosmos_containers --dry-run
python -m providers.scripts.provision_brain_cosmos_containers
python -m providers.scripts.sync_local_brain_to_cosmos --dry-run
python -m providers.scripts.sync_local_brain_to_cosmos
```

The sync is idempotent and push-only. It also syncs embeddings, which are required for `query_text` retrieval.

## Provider Neutrality

Provider interfaces exist so the Brain is not tied to a single model or storage vendor:

```text
LLMProvider
VisionProvider
EmbeddingProvider
StorageProvider
```

The implemented providers are Azure-backed plus local storage:

```text
providers/azure_openai_llm.py
providers/azure_cv_vision.py
providers/azure_openai_embeddings.py
providers/azure_storage.py
providers/local_storage.py
```

Provider selection is controlled by:

```text
OPTISWEEP_LLM_PROVIDER=azure_openai
OPTISWEEP_VISION_PROVIDER=azure_cv
OPTISWEEP_EMBEDDING_PROVIDER=azure_openai
OPTISWEEP_STORAGE_BACKEND=local|azure
```

Unsupported provider names raise immediately instead of silently falling back.

## Pipeline Integration

The existing incident and operational pipelines are kept. Brain ingestion runs in tandem with selected stage outputs rather than replacing those pipelines or deleting generated artifacts.

Current hooks cover incidence stages 4/5/6/8 and operational stages 4/5/6/8. `BRAIN_INGESTION_ENABLED` defaults on and can be set to `0`, `false`, or `no` to opt out for a run.

```text
stage output
  -> ingest_stage_output(...)
  -> extract_evidence
  -> classify_candidate
  -> reconcile_candidate
  -> validate_and_prepare_for_review
  -> persistence/review
```

Generated outputs remain important for replay, SME review, and app handoff. Do not delete `data/output/`, source-specific `*/data/output/`, shared output bundles, or `brain/data/local/` during Azure transfer.

## App and Phase 0 Boundary

The Phase 0 app lives in a separate codebase. From this repo's side, the app consumes the Stage 11 published Cosmos corpus plus, optionally, the Brain HTTP API. The app owns runtime retrieval/scoring/session/UI and must not write directly to Brain `brain_*` containers.

Stage 11 app-publish containers hold runbooks, playbooks, embeddings, relationship shards, source artifact metadata, operational context, canonical image metadata, and gate phrase tables. The app loads a single `PUBLISH_VERSION_ID`, runs in-memory hybrid scoring over Cosmos-loaded embeddings, follows playbook-to-runbook links, and renders Blob-backed images.

Authoritative app contract docs:

```text
app_handoff_package/README.md
app_handoff_package/COSMOS_DATA_MAP.md
app_handoff_package/GATE_PHRASE_TABLE_CONTRACT.md
app_handoff_package/retrieval/ALGORITHMS.md
app_handoff_package/schema/record_types.md
```

## Deferred Or Human-Owned Choices

The following remain owner decisions rather than hidden assumptions:

- New Azure naming, region, networking, and cost controls.
- Whether Brain HTTP is deployed immediately or after the Stage 11 Cosmos handoff is stable.
- Human/SME review workflow for open `BrainReview` records.
- Any future graph database or vector-index service.
- Phase 0 app implementation details beyond the contracts in `app_handoff_package/`.
