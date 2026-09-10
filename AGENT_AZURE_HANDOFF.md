# Agent Azure Handoff

This handoff is written for an agent recreating OptiSweep ingestion resources in a new Azure subscription. Do not use the previous owner's Azure account, resource group, keys, managed identities, Key Vault, Container Apps, or storage accounts. Treat existing names in historical notes as examples only unless the new owner explicitly asks to reuse a name.

## 1. Read First

1. Read `docs/HANDOFF.md` for the repo inventory.
2. Read `docs/architecture.md` for the current pipeline and Cosmos/App boundary.
3. Read `app_handoff_package/README.md`, `app_handoff_package/COSMOS_DATA_MAP.md`, `app_handoff_package/GATE_PHRASE_TABLE_CONTRACT.md`, and `app_handoff_package/retrieval/ALGORITHMS.md` for the Phase 0 app contract.
4. Read `brain/README.md` and `brain/DESIGN_RATIONALE.md` for Brain-specific storage, schemas, and rationale.
5. Inspect `.env.mock` (agent-oriented, every key + required/optional + consumers) or `.env.example` (shorter human template) before creating `.env`. Copy variable names, never old secret values.
6. Local pipeline outputs live under the trees listed in `HANDOFF_DATA_INVENTORY.md`. A full on-disk archive is `LOCAL_PIPELINE_DATA.zip` (~1.8 GB; gitignored — keep beside the clone). `HANDOFF_AZURE_BOOTSTRAP.zip` is the smaller Cosmos/app bootstrap subset.

## 2. Prerequisites

1. Confirm the new owner has an Azure subscription and permissions to create Resource Groups, Cosmos DB for NoSQL, Storage Accounts/Blob containers, Azure OpenAI or Azure AI Foundry deployments, Azure Computer Vision, and optionally Azure Container Apps, Azure Container Registry, Key Vault, and Application Insights.
2. Install local tools on the handoff machine:
   - Python 3.11+
   - Azure CLI: `az login`
   - PowerShell
   - Git
3. Create a Python environment from the repo root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r orchestration/requirements.txt
pip install -e mcp_server
```

4. Copy `.env.mock` (preferred for agents) or `.env.example` to `.env` and fill only new-owner values:

```powershell
copy .env.mock .env
# or: copy .env.example .env
```

Required secret or configuration names include:

```text
AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_API_KEY
AZURE_OPENAI_DEPLOYMENT
AZURE_OPENAI_API_VERSION
AZURE_MINI_OPENAI_ENDPOINT
AZURE_MINI_OPENAI_API_KEY
AZURE_MINI_OPENAI_DEPLOYMENT
AZURE_MINI_OPENAI_API_VERSION
AZURE_COMPUTER_VISION_ENDPOINT
AZURE_COMPUTER_VISION_KEY
AZURE_COMPUTER_VISION_API_VERSION
AZURE_EMBEDDINGS_ENDPOINT
AZURE_EMBEDDINGS_API_KEY
AZURE_EMBEDDINGS_DEPLOYMENT
AZURE_EMBEDDINGS_API_VERSION
AZURE_STORAGE_CONNECTION_STRING
AZURE_STORAGE_ACCOUNT_URL
AZURE_CANONICAL_IMAGES_CONTAINER
COSMOS_ENDPOINT
COSMOS_KEY
COSMOS_DATABASE
COSMOS_CONTAINER_RUNBOOKS
COSMOS_CONTAINER_PLAYBOOKS_A
COSMOS_CONTAINER_PLAYBOOKS_B
COSMOS_CONTAINER_RELATIONSHIP_LINKS
COSMOS_CONTAINER_SOURCE_ARTIFACTS
COSMOS_CONTAINER_OPERATIONAL_CONTEXT
COSMOS_CONTAINER_CANONICAL_IMAGES
COSMOS_CONTAINER_GATE_PHRASE_TABLES
OPTISWEEP_LLM_PROVIDER
OPTISWEEP_VISION_PROVIDER
OPTISWEEP_EMBEDDING_PROVIDER
OPTISWEEP_STORAGE_BACKEND
BRAIN_INGESTION_ENABLED
```

Optional intake/probe variables are documented in `.env.example`: `SHAREPOINT_*`, `GRAPH_*`, and `SALESFORCE_*`.

## 3. Create Azure Resources

Use new-owner naming. The historical live names in old design notes belonged to the previous owner and must not be treated as the target.

1. Create a resource group:

```powershell
az group create --name <new-resource-group> --location eastus
```

2. Create a Cosmos DB for NoSQL account and database. The repo expects `COSMOS_ENDPOINT`, `COSMOS_KEY`, and `COSMOS_DATABASE`; `.env.example` currently uses `optisweep_knowledge_phase0` as the database name pattern.

```powershell
az cosmosdb create `
  --name <new-cosmos-account> `
  --resource-group <new-resource-group> `
  --locations regionName=eastus failoverPriority=0 `
  --capabilities EnableServerless

az cosmosdb sql database create `
  --account-name <new-cosmos-account> `
  --resource-group <new-resource-group> `
  --name optisweep_knowledge_phase0
```

3. Create the Stage 11 app-publish containers. These containers are consumed by the Phase 0 app. They are defined in `shared_pipeline_stages/stage_11/container_config.py` and all documents use partition key `/publish_version_id`.

```text
runbooks
playbooks_prompt_a
playbooks_prompt_b
relationship_links
publish_source_artifacts
operational_context
publish_canonical_images
gate_phrase_tables
```

4. Create the Brain containers with the repo script after `COSMOS_*` is set in `.env`. These containers are separate from the Stage 11 app-publish containers and all use partition key `/_partition_key`.

```powershell
python -m providers.scripts.provision_brain_cosmos_containers --dry-run
python -m providers.scripts.provision_brain_cosmos_containers
```

Brain container roles:

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

5. Create a Storage Account and Blob container for canonical images. Stage 11 expects `AZURE_STORAGE_CONNECTION_STRING`, `AZURE_STORAGE_ACCOUNT_URL`, and `AZURE_CANONICAL_IMAGES_CONTAINER` (default `canonical-images`). Do not publish image docs to Cosmos unless `storage_uri` values point at HTTPS Blob locations.

6. Create Azure OpenAI or Azure AI Foundry deployments for chat and embeddings. The query embedding deployment used by the Phase 0 app must match the Stage 10 `embedding_model` in `data/output/cosmos_publish/publish_manifest.json`.

7. Create Azure Computer Vision for Stage 2/3 image analysis if new ingestion will run.

8. If deploying the Brain HTTP API, provision Container Apps/ACR/Key Vault under the new subscription. Store secrets in the new Key Vault and grant only the new container app managed identity access. The API entrypoint is:

```powershell
uvicorn http_server.app:app --host 0.0.0.0 --port 8000
```

The deployed `BRAIN_HTTP_BASE_URL` belongs in the Phase 0 app configuration only after it points to the new owner's Container App. The API exposes `/brain/v1/context/retrieve`, `/brain/v1/context/troubleshoot`, `/brain/v1/feedback`, and `/brain/v1/reviews/{id}/resolve`.

## 4. Configure Local Repo

1. Set provider choices in `.env`:

```env
OPTISWEEP_LLM_PROVIDER=azure_openai
OPTISWEEP_VISION_PROVIDER=azure_cv
OPTISWEEP_EMBEDDING_PROVIDER=azure_openai
OPTISWEEP_STORAGE_BACKEND=azure
BRAIN_INGESTION_ENABLED=1
```

Use `OPTISWEEP_STORAGE_BACKEND=local` only when testing against `brain/data/local/`.

2. Keep generated outputs. Do not delete `data/output/`, `incidenceknowledgeingestion/data/output/`, `operationalknowledgeingestion/data/output/`, `shared_pipeline_stages/data/output/`, `sme_review_runbooks/`, or `brain/data/local/`. They are retained for handoff, replay, SME review, and Azure bootstrap.

3. The root bootstrap zip is `HANDOFF_AZURE_BOOTSTRAP.zip`. It contains the current curated `data/output/cosmos_publish/` bundle, Cosmos/App contract docs, Brain schemas/config scripts, and an internal README. If a target transfer cannot include the whole repo, use the zip first and then copy the full output trees listed in `HANDOFF_DATA_INVENTORY.md`.

4. For the first Cursor-based handoff phase, prefer MCP-first operation. Install `mcp_server/` so agents can call Brain retrieval, review, validation, drafting, audit, and source-ingest tools directly. Treat `orchestration/` LangGraph commands as optional automation for local inbox, SharePoint, shared publish, and Cosmos upload rather than a prerequisite for using the Brain tools.

## 5. Publish Existing Outputs To New Cosmos

The fastest recreation path is to upload the retained Stage 11 bundle already assembled under `data/output/cosmos_publish/`.

1. Confirm `data/output/cosmos_publish/publish_manifest.json` and `data/output/cosmos_publish/publish_bundle/` exist.
2. Confirm `.env` points at the new Cosmos account, database, and containers.
3. Upload the assembled bundle:

```powershell
python orchestration/scripts/publish_cosmos_from_output.py --publish-scope all
```

4. If you need to rebuild the Stage 11 bundle before upload, run:

```powershell
python shared_pipeline_stages/scripts/stage11_publish_cosmos.py --publish --publish-version-id <new_publish_version_id>
```

Do not use a scoped publish unless intentionally patching an existing version. The code refuses thin uploads by default because Phase 0 can load the newest `publish_version_id` automatically.

## 6. Load Brain Corpus To New Cosmos

The Brain local corpus is retained under `brain/data/local/`. After the Brain containers are provisioned:

```powershell
python -m providers.scripts.sync_local_brain_to_cosmos --dry-run
python -m providers.scripts.sync_local_brain_to_cosmos
```

If a long sync is interrupted or embeddings are incomplete:

```powershell
python -m providers.scripts.sync_local_brain_to_cosmos --missing-embeddings
```

The sync is push-only and idempotent. It upserts records and embeddings; it does not delete remote records.

## 7. Verify

1. Validate the retained publish manifest:

```powershell
python orchestration/scripts/assemble_output.py
```

2. Upload smoke is reflected in `data/output/cosmos_publish/cosmos_upload_report.json` after upload. Confirm `uploaded: true`, `publish_scope: all`, and nonzero counts.

3. Check Stage 11 retrieval/gate reports:

```text
data/output/cosmos_publish/retrieval_smoke_report.json
data/output/cosmos_publish/gate_phrase_smoke_report.json
data/output/cosmos_publish/publish_manifest.json
```

4. Verify Brain provider selection by loading from the new Cosmos account:

```powershell
python -m providers.scripts.provision_brain_cosmos_containers --dry-run
python -m providers.scripts.sync_local_brain_to_cosmos --dry-run
```

5. Run focused tests before new ingestion work:

```powershell
python -m pytest brain/tests providers/tests brain_service/tests mcp_server/tests -q
```

6. For an end-to-end new ingest and publish:

```powershell
python orchestration/scripts/run_ingestion_agent.py `
  --source "data/inbox/incidents/<case pdf>.pdf" `
  --with-publish `
  --publish-to-cosmos `
  --publish-scope all
```

## 8. Phase 0 App Integration

The Phase 0 app codebase is separate from this ingestion repo. This repo owns ingestion, reviewable outputs, Cosmos publishing, and Brain service contracts. The Phase 0 app owns runtime retrieval, scoring, session state, UI, and answer/playbook execution.

What Phase 0 consumes from this repo:

```text
Stage 11 app-publish Cosmos containers:
  runbooks                    doc_type=runbook and canonical_runbook embeddings
  playbooks_prompt_a          doc_type=playbook and playbook_prompt_a embeddings
  playbooks_prompt_b          doc_type=playbook and playbook_prompt_b embeddings
  relationship_links          doc_type=relationship_graph shards
  publish_source_artifacts    artifact RAG records and embeddings
  operational_context         operational RAG records and embeddings
  publish_canonical_images    image metadata with Blob storage_uri
  gate_phrase_tables          doc_type=gate_phrase_table, id=gate_phrases

Brain HTTP API, if deployed:
  BRAIN_HTTP_BASE_URL
  /brain/v1/context/retrieve
  /brain/v1/context/troubleshoot
  /brain/v1/feedback
  /brain/v1/reviews/{id}/resolve
```

To wire Phase 0 after migration:

1. In the app repo, point Cosmos env vars at the new owner's Cosmos account and containers. Use names from `app_handoff_package/config/feature_flags.env.example`.
2. Set `PUBLISH_VERSION_ID` from `data/output/cosmos_publish/publish_manifest.json` after the new upload.
3. Ensure the app query embedding deployment matches the manifest `embedding_model`.
4. Configure Blob image env vars so image `storage_uri` values are renderable.
5. Load `gate_phrases` from `gate_phrase_tables` for the same `PUBLISH_VERSION_ID`; local YAML is fallback only.
6. Load embeddings and relationship graph from Cosmos at startup, then run in-memory hybrid scoring as described in `app_handoff_package/retrieval/ALGORITHMS.md`.
7. Do not reintroduce local filesystem corpus loaders, Azure AI Search, YAML workflow loaders, CAT-1/root-cause datasets, or old sample data paths.

App-side env names to provide, without secret values:

```text
COSMOS_ENDPOINT
COSMOS_KEY
COSMOS_DATABASE
COSMOS_CONTAINER_RUNBOOKS
COSMOS_CONTAINER_PLAYBOOKS_A
COSMOS_CONTAINER_PLAYBOOKS_B
COSMOS_CONTAINER_RELATIONSHIP_LINKS
COSMOS_CONTAINER_SOURCE_ARTIFACTS
COSMOS_CONTAINER_OPERATIONAL_CONTEXT
COSMOS_CONTAINER_CANONICAL_IMAGES
COSMOS_CONTAINER_GATE_PHRASE_TABLES
AZURE_STORAGE_CONNECTION_STRING
AZURE_CANONICAL_IMAGES_CONTAINER
AZURE_STORAGE_ACCOUNT_URL
PUBLISH_VERSION_ID
AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_API_KEY
AZURE_EMBEDDINGS_DEPLOYMENT
AZURE_OPENAI_API_VERSION
RETRIEVAL_BACKEND
USE_PLAYBOOK_ORCHESTRATION
ENABLE_CANONICAL_WORKFLOW_RUNTIME
SKIP_PLAYBOOK_CONFIRMATION
PLAYBOOK_MATCH_THRESHOLD
PLAYBOOK_HIGH_CONFIDENCE_THRESHOLD
DEFAULT_PLAYBOOK_VARIANT
BRAIN_HTTP_BASE_URL
```

Authoritative app contract docs live in `app_handoff_package/`; this repo does not contain the Phase 0 app implementation.

## 9. Known Human Decisions

1. Choose new Azure names, region, SKU/serverless choices, and budget controls.
2. Decide whether to deploy the Brain HTTP API immediately or start with Stage 11 Cosmos publish only.
3. Rotate all secrets into the new owner's Key Vault or secret store.
4. Confirm whether the Phase 0 app should auto-load newest publish or pin a specific `PUBLISH_VERSION_ID`.
5. Confirm any organization-specific RBAC, private networking, App Insights, and logging requirements before production use.
6. Domain knowledge graph work is a product/engineering next step, not an Azure provisioning blocker. Brain relationship rows are mostly provenance today; the plan to turn them into an OptiSweep domain KG (taxonomy, semantic edges, Stage 5–8 extraction, approved-only traversal) lives in `docs/HANDOFF.md` § Next Steps: OptiSweep Domain Knowledge Graph. Do not provision Neo4j/Gremlin for this until that semantic subgraph exists and is consumed.
