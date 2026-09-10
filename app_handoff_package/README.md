# OptiSweep App Handoff Package

Import these docs into the separate OptiSweep Phase 0 app repo to wire the app
around the **Cosmos-published ingestion corpus**.

Architecture rationale: `docs/architecture.md`. New-owner Azure handoff:
`AGENT_AZURE_HANDOFF.md`. Gate phrase contract: `GATE_PHRASE_TABLE_CONTRACT.md`.

## Start Here

1. `APP_AGENT_SCORING_HANDOFF.md` - current publish version, `AGVs stopped` results, scoring notes.
2. `GATE_PHRASE_TABLE_CONTRACT.md` - versioned keyword phrases in `gate_phrase_tables`.
3. `CURSOR_PROMPT.md` - staged app implementation brief and legacy delete list.
4. `COSMOS_DATA_MAP.md` - Cosmos containers, document shapes, and queries.
5. `config/feature_flags.env.example` - required env vars.

## Data Is In Cosmos

The app must not read local sample files from this repo. The published corpus is uploaded by ingestion Shared Stage 11 cumulative publish (`--publish-to-cosmos`).

Copy `PUBLISH_VERSION_ID` and container names from:

```text
data/output/cosmos_publish/publish_manifest.json
```

| Container | Env var |
| --- | --- |
| Runbooks + runbook embeddings | `COSMOS_CONTAINER_RUNBOOKS` |
| Prompt A playbooks + embeddings | `COSMOS_CONTAINER_PLAYBOOKS_A` |
| Prompt B playbooks + embeddings | `COSMOS_CONTAINER_PLAYBOOKS_B` |
| Relationship graph shards | `COSMOS_CONTAINER_RELATIONSHIP_LINKS` |
| Source artifacts (screenshots) | `COSMOS_CONTAINER_SOURCE_ARTIFACTS` |
| Operational context | `COSMOS_CONTAINER_OPERATIONAL_CONTEXT` |
| Gate phrase table | `COSMOS_CONTAINER_GATE_PHRASE_TABLES` |

See `COSMOS_DATA_MAP.md` for partition key (`publish_version_id`), schemas, and SQL queries.

## Phase 0 Boundary

This ingestion repo publishes and documents the contract. The Phase 0 app owns
runtime retrieval, scoring, session state, UI, and playbook/runbook execution.
After Azure migration, point the app to the new owner's `COSMOS_ENDPOINT`,
`COSMOS_DATABASE`, container names, Blob settings, embedding deployment, and
`PUBLISH_VERSION_ID`; do not keep references to the previous owner's Azure
resources.

The app consumes:

- runbooks and Prompt A/B playbooks from Stage 11 Cosmos containers;
- precomputed embeddings for playbook/runbook/context/artifact retrieval;
- relationship graph shards for playbook-to-runbook and artifact links;
- canonical image metadata plus Blob `storage_uri` values;
- `gate_phrases` for the same `publish_version_id`;
- optional `BRAIN_HTTP_BASE_URL` if Brain HTTP is redeployed.

App-side env names are listed in `config/feature_flags.env.example`; values
must come from the new Azure account and current `publish_manifest.json`.

## Gate Phrases At Runtime

On corpus load for a `publish_version_id`:

1. Read doc `id=gate_phrases` / `doc_type=gate_phrase_table` from `gate_phrase_tables`.
2. If present, initialize `KeywordSignalExtractor.from_phrases(...)`.
3. If absent, use local YAML only as a dev/test fallback.

Phrases are published with the same version as playbooks. Details: `GATE_PHRASE_TABLE_CONTRACT.md`.

## Package Contents

| Path | Purpose |
| --- | --- |
| `CURSOR_PROMPT.md` | Implementation brief: delete legacy local corpus paths and wire Cosmos. |
| `GATE_PHRASE_TABLE_CONTRACT.md` | App load contract for versioned keyword phrases. |
| `COSMOS_DATA_MAP.md` | Authoritative Cosmos storage reference. |
| `APP_AGENT_SCORING_HANDOFF.md` | Scoring and smoke handoff notes. |
| `retrieval/ALGORITHMS.md` | Hybrid retrieval over Cosmos-loaded vectors. |
| `retrieval/local_hybrid_retriever.py` | Scoring reference to port; not a data source. |
| `retrieval/cosmos_corpus_queries.md` | Query cheat sheet. |
| `schema/record_types.md` | Cosmos `payload` field mapping. |
| `config/feature_flags.env.example` | Cosmos-only env template. |

Deprecated local `sample_data/` and scripts that generated/tested it were removed during handoff cleanup. The app should use Cosmos and the scoring reference above.

## App Agent Instructions

1. Delete filesystem corpus loaders: root cause, CAT-1, YAML workflows, procedure dictionaries, `LOCAL_CORPUS_PATH`, Azure AI Search, and local sample data.
2. Load embedding index and relationship graph from Cosmos at startup.
3. Load `gate_phrases` for that version into keyword extraction.
4. Retrieve turn 1 via in-memory hybrid search over Cosmos embeddings.
5. Execute turn 2+ via playbook/runbook ID lookups and the link graph.
6. Keep a single `playbook_graph.py`; do not reintroduce a case triage graph or `HybridWorkflowRouter`.

## Retrieval Without Azure AI Search

Cosmos stores precomputed vectors from Stage 10. The app loads them into memory and runs brute-force hybrid scoring. Playbook cards are entry-scoped: title, `observed_entry_symptoms`, and `support_user_language_examples`. Details: `retrieval/ALGORITHMS.md`.

## Ingestion Repo Reference

- Architecture: `docs/architecture.md`
- Handoff: `docs/HANDOFF.md`
- Publisher: `shared_pipeline_stages/stage_11/cosmos_publisher.py`
- Cumulative path: `shared_pipeline_stages/stage_11/cumulative_publish.py`
- Containers: `shared_pipeline_stages/stage_11/container_config.py`
- Demo findings: `docs/demo_testing_report.md`
