# OptiSweepAI Ingestion Handoff

Use this as the first-stop inventory for a new owner. The repo has three active tracks: the ingestion pipelines, the shared publish path, and the newer Brain service work.

## Read These First

1. `AGENT_AZURE_HANDOFF.md` - step-by-step new-owner Azure recreation for an agent.
2. `HANDOFF_AZURE_BOOTSTRAP.zip` - curated portable publish bundle and Cosmos shape docs at repo root.
3. `README.md` - repo start page and current run commands.
4. `docs/architecture.md` - current architecture and why the publish path works this way.
5. `orchestration/README.md` - easiest end-to-end entrypoint for inbox/watch/SharePoint flows.
6. `shared_pipeline_stages/README.md` - Shared Stages 6.5-11, including cumulative Cosmos publish.
7. `app_handoff_package/README.md` - Phase 0 app-side Cosmos loading, scoring, and gate phrase contract.
8. `brain/README.md` and `brain/DESIGN_RATIONALE.md` - source-agnostic Brain schemas, service boundary, and migrated design rationale.

## Active Areas

| Area | Status | Purpose |
| --- | --- | --- |
| `orchestration/` | Active | LangGraph entrypoints over local inbox and optional SharePoint intake. |
| `incidenceknowledgeingestion/` | Active | Incident PDF evidence Stages 1-6 and per-source Stage 8 links. |
| `operationalknowledgeingestion/` | Active | Manual/training/support-guide Stages 1-8. |
| `shared_pipeline_stages/` | Active | Shared runbook pool, merge, playbooks, validation, embeddings, cumulative Cosmos publish. |
| `app_handoff_package/` | Active docs only | App implementation contract for Cosmos records, retrieval, and gate phrases. |
| `brain/`, `brain_service/`, `http_server/`, `mcp_server/`, `providers/` | Active | Source-agnostic Brain records, service logic, HTTP/MCP surfaces, and provider wrappers. |
| `connectors/` | Active probes | Salesforce and Microsoft Graph dev probes/adapters. |
| `data/inbox/` | Active drop zone | Local files to ingest; real source files are ignored after placement. |
| `data/output/` | Active handoff output | Assembled SME review and Cosmos publish outputs. |
| `docs/ontology/` and `stage_prompts/` | Active contracts | Taxonomy, prompt, and ontology guidance consumed by stages. |

## Near-Term Agent Posture

For a new owner working inside Cursor, start MCP-first: `mcp_server/` exposes the Brain curation, retrieval, validation, review, and direct source-ingest tools that an agent can call interactively. Keep `orchestration/` as an optional automation path for one-shot local files, local inbox watching, SharePoint intake, shared publish, and Cosmos upload. Do not require LangGraph just to use the MCP tools or inspect/update the Brain corpus.

LangGraph can later become the automated intake layer around MCP/Brain service calls, but today it runs a separate graph over the existing pipeline CLIs rather than wrapping the MCP server.

## Generated Or Review Outputs

These are useful for audit and SME review, but they are not the canonical source of code behavior:

- `incidenceknowledgeingestion/data/output/`
- `operationalknowledgeingestion/data/output/`
- `shared_pipeline_stages/data/output/`
- `sme_review_runbooks/`
- `data/output/baseline_publishes/`
- `brain/data/local/`

Keep these outputs for tests, replay, SME review, Azure bootstrap, and app handoff. Do not delete `data/output/` or `brain/data/local/` during ownership transfer. `HANDOFF_DATA_INVENTORY.md` lists retained output trees that may need separate transfer if the root zip is not enough.

## Azure And Phase 0 Handoff

The previous owner's Azure resources are not the target. Recreate resources in
the new owner's subscription using `AGENT_AZURE_HANDOFF.md`, then upload the
retained `data/output/cosmos_publish/` bundle to the new Stage 11 app-publish
containers.

The OptiSweep Phase 0 app is a separate codebase. From this repo it consumes:

- Stage 11 Cosmos containers for runbooks, playbooks, embeddings, relationship
  shards, operational context, source artifacts, canonical images, and gate
  phrases.
- `PUBLISH_VERSION_ID` from `data/output/cosmos_publish/publish_manifest.json`.
- Blob image URIs produced during Stage 11 publish.
- Optional `BRAIN_HTTP_BASE_URL` if the Brain HTTP API is redeployed under the
  new subscription.

Authoritative app integration docs live under `app_handoff_package/`. The app
retrieves/scores/renders; this repo ingests/publishes/serves Brain contracts.

## What To Ignore

- Top-level scratch files, temporary checkout folders, and root-level PDF/PPTX dumps are not handoff material.
- `app_handoff_package/sample_data/` and its generator/smoke scripts were removed; the app must load Cosmos, not local sample files.
- Historical design notes under `docs/design_decisions/` may explain why decisions were made, but current behavior should be verified against `docs/architecture.md`, area READMEs, and code. The retired `newdesigndoc/` content was migrated into `brain/DESIGN_RATIONALE.md`, `brain/README.md`, `docs/architecture.md`, and this handoff.

## Main Entrypoints

```powershell
# Watch local inbox and publish to Cosmos
python orchestration/scripts/watch_inbox.py --publish-to-cosmos

# Run one source through ingestion and shared publish
python orchestration/scripts/run_ingestion_agent.py `
  --source "data/inbox/incidents/Case 228086 Data.pdf" `
  --with-publish `
  --publish-to-cosmos `
  --publish-scope all

# Assemble current outputs without new ingest
python orchestration/scripts/assemble_output.py
```

Use source-specific scripts only when debugging a stage directly:

- `incidenceknowledgeingestion/scripts/extract_incident_knowledge.py`
- `operationalknowledgeingestion/scripts/extract_operational_knowledge.py`
- `shared_pipeline_stages/scripts/stage11_publish_cosmos.py`

## Next Steps: OptiSweep Domain Knowledge Graph

Brain already has a relationship *table* (typed `from_id` / `relationship_type` /
`to_id` records, local JSON + `brain_relationships` Cosmos). That is **not** yet
a useful OptiSweep domain knowledge graph.

**Current reality (local corpus inspection):**

- ~11.6k relationship rows exist, but ~79% touch an `evidence:` endpoint and
  most are `supports` — provenance / citation links, not domain structure.
- The curated ontology subgraph is thin: ~545 non-evidence edges over ~225
  endpoints; only ~197 of ~2.2k ontology entities appear on any ontology edge.
- Incident scopes barely contribute (tens of edges). Case `233681` has no
  `relationships.json`; many relationship reviews failed with
  `WRITE FAILED: 'from_id'`.
- Shared Stage 12 “operational knowledge graph” and a native graph DB remain
  future; do not wait on them to fix semantic edge quality.

**Goal:** a closed OptiSweep domain graph that Stage 8 linking and Brain
retrieval can traverse — systems/components, failure patterns, capabilities,
procedures, and playbook nodes — with provenance kept on `source_refs`, not as
traversable edges.

### Recommended sequence

1. **Separate provenance from domain edges**
   - Keep `source_refs` on every domain relationship (already required).
   - Exclude `evidence:` endpoints from graph traversal / ContextPacket paths
     (or demote them to a non-traversable citation index).
   - Stop treating bulk `supports` and most generic `applies_to`
     (component→system) as the KG; keep only SME-approved structural edges.

2. **Freeze a small closed node taxonomy**
   - System / Component (RMS, Hospital HMI, Ignition, WCS API, AGV fleet, …)
   - Symptom / FailurePattern (`pairing_failure`, `bump_fault`, …)
   - State / Metric / Alarm where needed
   - Capability, Procedure, Playbook / playbook node
   - New nodes only via catalog IDs + remap/merge — not one-off incident strings.
   - Seed from Stage 8 component vocabulary and
     [Stage 8 KG enrichment plan](design_decisions/stage_8_playbook_finalization.md#future-design-considerations-knowledge-graph-component-enrichment).

3. **Allow only high-signal edge types**
   - symptom `may_indicate` → capability
   - procedure `uses` / `checks_component` / `acts_on_component` → component
   - procedure `addresses_failure` → failure pattern
   - component `contains` / `controls` / `communicates_with` → component
   - playbook_node `expects_check` → component / `addresses_failure` → pattern

4. **Extract edges at the right stages**
   - Ontology catalogs + SME pairings: seed symptom↔capability and topology.
   - Stage 6/7 runbook finalization: structured component / failure fields.
   - Stage 5/8 playbooks: per-node `expects_check` / `addresses_failure`.
   - Stage 4 incidents: `exhibited` / `observed_at` as **candidates** only.
   - Manuals/videos: candidates → review queue, not auto-global truth.
   - **Fix relationship persistence** so validated `from_id`/`to_id` writes
     succeed (unblock incident graph growth).

5. **Govern promotion with `validation_status`**
   - Incidents → `operational_unreviewed` / `needs_sme_review`.
   - Only `catalog_authoritative` / `sme_approved` edges in runtime retrieval
     and Stage 8 linking.

6. **Make consumers use the graph**
   - Brain context: bounded hops (1–2) over approved edge types.
   - Stage 8: boost / guard runbook links on component and failure overlap;
     emit honest gaps (`no_runbook_for_component:…`).

7. **Defer a graph database**
   - Stay on document Cosmos + in-process traversal until the approved
     semantic subgraph is dense and used.
   - Consider Gremlin/Neo4j only if multi-hop / path analytics outgrow that.

### Pointers

- Brain schemas and storage: `brain/README.md`, `brain/DESIGN_RATIONALE.md`
- Future Stage 8 component enrichment:
  `docs/design_decisions/stage_8_playbook_finalization.md`
- Architecture note: `docs/architecture.md` (Brain domain graph direction)

## Cleanup Notes

During handoff cleanup, deprecated app-local corpus samples and temporary checkout artifacts had already been removed. The former `newdesigndoc/` tree was migrated into active Brain and handoff docs, then deleted.
