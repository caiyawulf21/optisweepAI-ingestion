# OptiSweep Brain

Source-agnostic OptiSweep knowledge contracts, local corpus data, Brain service
storage shapes, and tests.

The retired `newdesigndoc/` rationale has been folded into
[`DESIGN_RATIONALE.md`](DESIGN_RATIONALE.md). Use that file for the "why",
then verify current behavior against code and tests.

## Layout

```text
brain/
  schemas/
    common.py        # shared envelope: id, type, schema_version, source_refs, constraints, validation_status, timestamps
    evidence_unit.py  # EvidenceUnit: bounded, immutable source-backed content
    entity.py          # Entity: canonical OptiSweep object, payload discriminated by entity_type
    capability.py      # Capability: diagnostic/operational action (+ role_paths, sql_field_notes)
    claim.py            # Claim: a source-backed assertion with a polarity
    relationship.py      # Relationship: a typed graph edge between two stable IDs
    procedure.py         # Procedure: linear human-executable steps for one Capability
    playbook.py          # Playbook: branching graph referencing procedure/capability IDs
    review.py             # BrainReview: pending/resolved Reconciliation + audit-finding work items
    context_packet.py     # ContextPacket: LLM-call working-memory shape (schema only, no retrieval yet)
  id_generation.py    # deterministic, type-prefixed stable IDs (entity:system:wcs)
  validators.py        # cross-record checks: relationship endpoints resolve, source_refs present
  migration/            # Pass 0/1 backfill + enrich_brain_knowledge offline agent
  data/local/           # local corpus (ontology_catalogs + operational_sources)
  fixtures/             # one example JSON per record type, used by the tests
  tests/
  AGENT_DESIGN_NOTES.md # append-only implementation notes and historical decisions
  DESIGN_RATIONALE.md   # migrated architecture rationale from retired newdesigndoc/
```

## Core rules (see the architecture lock for full rationale)

- **No source owns truth.** Manuals, training video, incidents, and RCAs all
  emit the same `EvidenceUnit` → `Entity`/`Claim`/`Relationship`/`Capability`
  shapes.
- **Evidence is immutable.** A `EvidenceUnit` is never overwritten; new
  interpretations create new derived records that reference it.
- **Claims are not facts.** `Claim.polarity` (`affirmed`/`negated`/
  `uncertain`/`conflicting`) lets incident evidence disagree with operational
  evidence without deciding a winner in Part 1.
- **IDs are stable and typed**, never titles. Use `brain/id_generation.py`
  rather than constructing ID strings by hand.
- **Constraints default to global.** An empty/omitted `constraints` object
  means the record applies everywhere; scope it only when a source is
  explicit about a site, product version, or environment.
- **`Entity.payload` is discriminated by `entity_type`**, not a free-form
  dict. `system`, `database_table`, `ui_screen`, and `system_action` have
  fully specified payload fields today; other MVP entity types use an
  empty placeholder payload until real evidence defines their fields.
  `system_action` is a system/API action invoked by a call ("GetAGVStatuses",
  "OpenAllChutes") — never a human action (that's `Capability`) and never a
  persistent state (that's `Entity` state/symptom); see
  `AGENT_DESIGN_NOTES.md` §11.
- **Role policy vs steps.** `Capability.role_paths` holds per-role guidance
  text; executable SSMS/SQL sequences live on `Procedure` actions — never
  invent queries onto a Capability.
- **`validation_status` gates runtime eligibility.** Every record carries a
  `ValidationStatus` (`catalog_authoritative`/`operational_unreviewed`/
  `needs_sme_review`/`sme_approved`/`conflicting`/`deprecated`). A
  `ContextPacket.approved_knowledge` list must only ever cite records whose
  status is `catalog_authoritative` or `sme_approved` — everything else is
  Reconciliation/Curation working material, never runtime guidance. See
  `AGENT_DESIGN_NOTES.md` §14.

## Current State

The Brain now includes schemas, local corpus data, provider-backed storage,
real semantic retrieval, pipeline hooks, MCP tools, and an HTTP API surface.
It remains distinct from the Phase 0 app: this repo publishes and serves
Brain context; the app repo owns runtime scoring, UI, session state, and
playbook execution.

Current durable storage options:

- local JSON under `brain/data/local/` for development, handoff, and replay;
- Azure Cosmos `brain_*` containers when `OPTISWEEP_STORAGE_BACKEND=azure`.

Provision and sync Brain Cosmos:

```powershell
python -m providers.scripts.provision_brain_cosmos_containers --dry-run
python -m providers.scripts.provision_brain_cosmos_containers
python -m providers.scripts.sync_local_brain_to_cosmos --dry-run
python -m providers.scripts.sync_local_brain_to_cosmos
```

The Brain containers are separate from the Stage 11 app-publish containers
documented in `app_handoff_package/`. Brain containers use partition key path
`/_partition_key`; Stage 11 app-publish containers use `/publish_version_id`.

### Domain knowledge graph (next steps)

Relationship records exist and are graph-shaped, but most local edges are
evidence provenance (`supports`), not a coherent OptiSweep domain graph. The
handoff next-step plan covers separating provenance from domain edges, freezing
component/failure taxonomies, Stage 5–8 edge extraction, fixing relationship
write failures, and driving Stage 8 / Brain retrieval from approved edges only
— without requiring a graph database first:

[`docs/HANDOFF.md`](../docs/HANDOFF.md#next-steps-optisweep-domain-knowledge-graph).

## Scope

**In scope:** typed Brain schemas, deterministic IDs, validation, local corpus,
embedding backfill, local and Azure storage providers, reconciliation/review
service logic, pipeline stage hooks, MCP tools, and HTTP routes.

**Out of scope here:** Phase 0 app UI/session/runtime implementation, direct
app writes to Brain storage, secret ownership by the previous Azure account,
and any unreviewed promotion of feedback into approved knowledge.

## Enriching the local corpus

```bash
python -m brain.migration.enrich_brain_knowledge        # dry-run
python -m brain.migration.enrich_brain_knowledge --write
```

Restores ontology `role_paths`, fills `sql_field_notes.database_entity_id`,
promotes finalized runbooks into `Procedure` records, and adds role-path /
approved-query Claims. See `AGENT_DESIGN_NOTES.md` §7.

## Azure handoff

For new-owner Azure setup, use the root
[`AGENT_AZURE_HANDOFF.md`](../AGENT_AZURE_HANDOFF.md). It explains required
env vars, Brain container provisioning, Stage 11 app corpus upload, Phase 0
app wiring, and the retained output zip `HANDOFF_AZURE_BOOTSTRAP.zip`.

## Running the tests

```bash
python -m pytest brain/tests/ -v
```
