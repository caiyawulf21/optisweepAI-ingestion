# Cosmos Phase-1 container cleanup (2026-09-16)

Account: `optisweepsupportdev`  
Database: `optisweep_knowledge_phase0`  
Resource group: `optisweepai`

## Action required — appcode (optisweepAI-phase0)

Please confirm whether the empty legacy Cosmos container **`source_artifacts`** (partition key `/incident_id`) may be deleted.

| Fact | Detail |
|------|--------|
| Live Stage 11 publish target | **`publish_source_artifacts`** (`/publish_version_id`, ~3.5k items) |
| Env used by ingestion | `COSMOS_CONTAINER_SOURCE_ARTIFACTS=publish_source_artifacts` |
| Leftover container | `source_artifacts` — empty, PK `/incident_id` (Phase-1 shape) |
| Why not deleted yet | Hard stop: do not delete `source_artifacts` without appcode sign-off |

Reply in this PR (or ticket) with **approve delete** or **keep** and a short reason. If approved, ingestion will run:

```text
az cosmosdb sql container delete \
  --account-name optisweepsupportdev \
  --database-name optisweep_knowledge_phase0 \
  --resource-group optisweepai \
  --name source_artifacts --yes
```

Also confirm app `.env` / `container_config.py` maps source artifacts to **`publish_source_artifacts`**, not `source_artifacts`.

---

## What was deleted (empty; unused by Stage 11 / Brain)

All had item count `0`. No backup copy (nothing to copy).

| Container | Former partition key | Replaced by |
|-----------|----------------------|-------------|
| `canonical_images` | `/category` | `publish_canonical_images` |
| `workflow_definitions` | `/issue_category` | `playbooks_prompt_a` / `playbooks_prompt_b` |
| `canonical_workflow_definitions` | `/issue_category` | same |
| `procedure_dictionary` | `/procedure_type` | `runbooks` |
| `canonical_procedure_dictionary` | `/procedure_type` | `runbooks` |
| `knowledge_relationships` | `/from_id` | `relationship_links` |
| `context_reference` | `/context_type` | unused by playbook hot path |
| `incident_records` | `/issue_category` | unused by playbook hot path |
| `timeline_events` | `/incident_id` | unused by playbook hot path |
| `workflow_candidates` | `/candidate_type` | unused by playbook hot path |
| `raw_evidence_chunks` | `/incident_id` | unused by playbook hot path |
| `escalation_summaries` | `/incident_id` | unused by playbook hot path |
| `retrieval_vectors` | `/record_type` | embeddings live in publish / `brain_embeddings` |

Command pattern:

```text
az cosmosdb sql container delete \
  --account-name optisweepsupportdev \
  --database-name optisweep_knowledge_phase0 \
  --resource-group optisweepai \
  --name <container> --yes
```

Ingestion repo grep: no Stage 11 or Brain create/upsert/query targeted those Cosmos names (local JSON field names only).

## Kept

### Stage 11 publish (`/publish_version_id`)

| Container | Notes |
|-----------|--------|
| `runbooks` | live |
| `playbooks_prompt_a` | live |
| `playbooks_prompt_b` | live |
| `operational_context` | live |
| `relationship_links` | live |
| `publish_source_artifacts` | live publish corpus (dataset key `source_artifacts`) |
| `publish_canonical_images` | live (dataset key `canonical_images`) |
| `gate_phrase_tables` | live |

### App runtime (`/session_id`) — do not delete without appcode

- `workflow_sessions`
- `interaction_logs`
- `feedback_events`

### Brain (`/_partition_key`) — do not delete without Brain sign-off

- `brain_evidence`, `brain_entities`, `brain_claims`, `brain_relationships`
- `brain_capabilities`, `brain_procedures`, `brain_playbooks`, `brain_reviews`
- `brain_ingestion_runs`, `brain_embeddings`

### Skipped pending appcode

- `source_artifacts` — empty Phase-1 leftover (`/incident_id`)

## Not found in Cosmos

- `incidence_workflow_definitions`
- `procedure_refinement_candidates`

## Stage 11 env (already correct; no code change required)

```env
COSMOS_CONTAINER_RUNBOOKS=runbooks
COSMOS_CONTAINER_PLAYBOOKS_A=playbooks_prompt_a
COSMOS_CONTAINER_PLAYBOOKS_B=playbooks_prompt_b
COSMOS_CONTAINER_RELATIONSHIP_LINKS=relationship_links
COSMOS_CONTAINER_SOURCE_ARTIFACTS=publish_source_artifacts
COSMOS_CONTAINER_OPERATIONAL_CONTEXT=operational_context
COSMOS_CONTAINER_CANONICAL_IMAGES=publish_canonical_images
COSMOS_CONTAINER_GATE_PHRASE_TABLES=gate_phrase_tables
```

`publish_manifest.json` `containers` map must use only the KEEP publish names above (never Phase-1 names).
