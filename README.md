# OptiSweep AI Ingestion

`optisweepAI-ingestion` turns OptiSweep manuals, training videos, support guides, and incident evidence into reviewable knowledge assets and a **cumulative Cosmos corpus** for the troubleshooting app.

**Start here for handoff:** [AGENT_AZURE_HANDOFF.md](AGENT_AZURE_HANDOFF.md) for new-owner Azure recreation, then [docs/HANDOFF.md](docs/HANDOFF.md).  
**Bootstrap zip:** [HANDOFF_AZURE_BOOTSTRAP.zip](HANDOFF_AZURE_BOOTSTRAP.zip) (created at repo root after handoff packaging).  
**Architecture:** [docs/architecture.md](docs/architecture.md).  
**README/status update rule:** [docs/README_UPDATE.md](docs/README_UPDATE.md).

```text
operationalknowledgeingestion/   # manuals / training -> Stages 1-8
incidenceknowledgeingestion/     # case PDFs -> Stages 1-6, 8
shared_pipeline_stages/          # Shared 6.5-11: pool, merge, playbooks, validate, embed, publish
orchestration/                   # LangGraph agent + local/SharePoint intake
data/inbox/                      # drop incidents/, manuals/, or videos/ here
data/output/                     # sme_review/ + cosmos_publish/ handoff
app_handoff_package/             # app Cosmos + gate phrase contracts
brain*/ http_server/ providers/  # Brain schemas, service/API, and provider wrappers
connectors/                      # Salesforce and Microsoft Graph probes/adapters
```

## Azure And Phase 0 Handoff

This repo publishes the Cosmos corpus and Brain service contracts; the separate
OptiSweep Phase 0 app consumes them for retrieval, scoring, session state, and
UI. To migrate away from the previous owner's Azure account, recreate Cosmos,
Blob, Azure OpenAI/embeddings, Computer Vision, and optional Brain HTTP hosting
from `AGENT_AZURE_HANDOFF.md`, then point the Phase 0 app at the new
`PUBLISH_VERSION_ID` and Cosmos containers documented in `app_handoff_package/`.

## Current Happy Path

1. Drop a source in `data/inbox/` or a SharePoint library synced via `SHAREPOINT_SYNC_ROOT`.
2. Source lanes extract reviewable local JSON with source lineage and `needs_sme_review` defaults.
3. Shared Stages 6.5-10 build the pool, merge runbooks, finalize playbooks, link, validate, and embed.
4. Stage 11 merges prior published corpus + new work, gates, smokes, emits `gate_phrase_table`, and uploads `scope=all`.
5. The app loads the newest Cosmos publish and gate phrases.

```powershell
copy .env.example .env   # Azure OpenAI, embeddings, Cosmos, blob (+ optional SharePoint)
pip install -r orchestration/requirements.txt
python orchestration/scripts/watch_inbox.py --publish-to-cosmos
```

Details: [orchestration/README.md](orchestration/README.md), [shared_pipeline_stages/README.md](shared_pipeline_stages/README.md), [docs/architecture.md](docs/architecture.md).

## Active vs Generated

Active code and contracts live in `orchestration/`, `incidenceknowledgeingestion/`, `operationalknowledgeingestion/`, `shared_pipeline_stages/`, `app_handoff_package/`, `brain/`, `brain_service/`, `http_server/`, `mcp_server/`, `providers/`, `connectors/`, `docs/ontology/`, and `stage_prompts/`.

Generated and review outputs live under `data/output/`, `*/data/output/`, `shared_pipeline_stages/data/output/`, `sme_review_runbooks/`, and `brain/data/local/`. Keep them for replay/SME review when useful, but verify behavior against code and the authority docs.

## Pipeline Roles

`operationalknowledgeingestion/` handles stable operational knowledge from manuals, training slides, training recordings, transcripts, SOP-style material, and other product documentation.

`incidenceknowledgeingestion/` handles incident evidence, especially PDF screenshot packages containing Salesforce case events, Teams chats, RCA/support screenshots, logs, and attachments.

The two pipelines converge in the shared stages. Final runbooks should not be owned by a single source: manuals describe intended behavior, while incidents describe what happened in practice. The shared publish path merges evidence while preserving source lineage.

## Shared Knowledge Flow

```text
Operational/manual/training candidates
Incident-derived candidates
SOP/SME candidates
        ->
Shared candidate pool
        ->
Cross-source merging, deduplication, synthesis
        ->
Canonical runbooks and finalized playbooks
        ->
Markdown review files + structured JSON
        ->
Relationship linking and validation
        ->
Embedding records
        ->
Cosmos DB / vector search / troubleshooting app retrieval
```

## Development Status

<!-- AUTO:DEVELOPMENT_STATUS_START -->
This section is generated from `docs/development_status.md`. Update that file whenever either ingestion area advances to a new stage or changes its next milestone. See `docs/README_UPDATE.md` and `docs/architecture.md`.

## Operational Knowledge Ingestion

Current position: source-specific operational extraction is implemented through Stage 6; outputs feed shared Stages 6.5–11.

Implemented today:

- Stage 1: source bundle extraction (including document-level section fallback for short guides).
- Stage 2: source artifact and image extraction.
- Stage 3: Azure OpenAI source artifact enrichment.
- Stage 4: operational context extraction.
- Stage 5: runbook candidate discovery.
- Stage 6: source runbook finalization (LLM assisted).
- Per-source Stage 8 relationship linking.
- Training video bundle generation and preparation for Stage 4 and Stage 5.
- Ingested remote-support guide `active_agv_error_query_1` → singular WCS `SystemActiveErrorModel` diagnostic runbook (catalog now carries gold `select_template`).
- Capability catalog `fleet_system_status` has `sql_model_links`; deferred roster/hospital SQL runbook gen plan in `docs/plan_catalog_sql_runbooks_roster_hospital.md`.

Next milestones:

- Continue SME review of finalized runbooks against `Runbook Example.md`.
- Keep operational sources in every cumulative Stage 11 publish (no thin pilots).
- Publish `active_agv_error_query_1` via cumulative Stage 11 when Cosmos env is configured.

Primary details live in `operationalknowledgeingestion/README.md`.

## Incidence Knowledge Ingestion

Current position: Cases `218550`, `223554`, `228086`, `228723` flow through Stages 1–6 + 8 into the shared corpus. Stage 2 promotes nested evidence with automatic page/OpenCV fallback when wrappers yield no crops.

Implemented today:

- Stage 1: incident source package loading and page/source inventory.
- Stage 2: OCR and evidence artifact extraction (Qwen gate + wrapper fallback).
- Stage 2.5: deterministic artifact enrichment packet preparation.
- Stage 3: Azure OpenAI incident artifact enrichment.
- Stage 4: Azure OpenAI canonical incident record and timeline extraction.
- Stage 5: incident runbook candidate discovery (live-surface rules aligned with operational: `allowed_access_surfaces` + `ontology_snippets` + eligibility) plus playbook candidate discovery (Prompt A/B) with short `support_user_language_examples` and active-error → `agv_active_errors` expects disambiguation.
- Stage 6: source runbook finalization for runbook candidates only (LLM assisted; taxonomy tags + ontology packet wiring).
- Stage 8: per-source relationship linking.

Next milestones:

- Improve remote-support-aware procedures and role-aware wording (see `docs/demo_testing_report.md`).
- Keep operator-language coverage high as new cases land (Stage 8 enrichment + Stage 11 gate).
- Stage 5 `expects_*` + Stage 6 tags + Stage 6.5 cards + Stage 8 capability-overlap multi-link (A3) + playbook expects backfill (C-regen) + gap messaging (B3) + branch cleanup (B4) + Stage 8 SME pack (B5) landed — see `docs/design_decisions/stage_5_8_c2_b2_b1_changelog.md` and `sme_review_runbooks/stage_8_playbooks_capability_tags/`.

Primary details live in `incidenceknowledgeingestion/README.md`.

## Shared Publish Path (6.5–11)

Implemented today:

- Shared Stage 6.5: runbook pool and merge preparation.
- Shared Stage 7: selective cross-source runbook merge.
- Shared Stage 8: playbook finalization, runbook linking, operator-language enrichment.
- Shared Stage 8.5: corpus relationship linking.
- Shared Stage 9: corpus validation (publish gate).
- Shared Stage 10: full-corpus embedding generation.
- Shared Stage 11: **cumulative** Cosmos publish + pre-publish gate + retrieval smoke + `gate_phrase_table`.
- Auto shared refresh after Day1/Day2 OpenAI Stage 6 regen (`scripts/shared_after_source_regen.py` → Stages 6.5/7/8 by default; disable with `REGEN_REFRESH_SHARED=0`).

LangGraph orchestration (`orchestration/`) routes inbox uploads, runs shared stages, and forces `publish_scope=all` for new partitions so `AUTO_PUBLISH_VERSION=true` never lands on a thin corpus.

## OptiSweep Brain

Current position: Brain schemas, local corpus, provider-backed storage, semantic retrieval, pipeline hooks, MCP tools, HTTP routes, and real Azure Cosmos container support are implemented. Brain generated/local data is retained for handoff and replay under `brain/data/local/`.

Implemented today:

- `brain/schemas/`: pydantic models for `EvidenceUnit`, `Entity`, `Capability`, `Claim`, `Relationship`, `Procedure`, `Playbook`, `BrainReview`, and `ContextPacket`.
- `providers/`: Azure OpenAI, Azure Computer Vision, Azure embeddings, Azure Cosmos storage, and local storage provider wrappers.
- Brain Cosmos containers are provisioned by `providers/scripts/provision_brain_cosmos_containers.py` and synced from `brain/data/local/` by `providers/scripts/sync_local_brain_to_cosmos.py`.
- `brain_service/`, `mcp_server/`, and `http_server/` expose extraction/reconciliation/review/context workflows and app-facing Brain HTTP routes.
- Incidence and operational stage hooks feed Brain in tandem, gated by `BRAIN_INGESTION_ENABLED` (default on; set to `0`/`false`/`no` to opt out).

Next milestones:

- Recreate Azure resources under the new owner's subscription using `AGENT_AZURE_HANDOFF.md` and `HANDOFF_AZURE_BOOTSTRAP.zip`; do not use the previous owner's Azure account.
- Decide whether to redeploy Brain HTTP immediately or start with Stage 11 Cosmos publish plus local Brain sync.
- Continue SME review workflow design for open `BrainReview` records and Phase 0 app feedback handling.

Primary details live in `brain/README.md` and `brain/DESIGN_RATIONALE.md`.

## Shared Design Notes

- Architecture and rationale: `docs/architecture.md`.
- README update process: `docs/README_UPDATE.md`.
- Demo validation log: `docs/demo_testing_report.md`.
- Gate phrase app contract: `app_handoff_package/GATE_PHRASE_TABLE_CONTRACT.md`.
- `docs/design_decisions/stage_5_6_playbook_extraction_modes.md` tracks Prompt A/B playbook modes.

## README Update Rule

When stage status or architecture changes:

1. Update `docs/architecture.md` if behavior or rationale changed.
2. Update this file (`docs/development_status.md`) and any area-specific status source.
3. Update the owning area README.
4. Run the relevant hooks:

```bash
python shared_pipeline_stages/scripts/update_readme.py
python incidenceknowledgeingestion/scripts/update_readme.py
```

Operational README hook when that area changes:

```bash
python operationalknowledgeingestion/scripts/update_readme.py
```
<!-- AUTO:DEVELOPMENT_STATUS_END -->

## Key Rules

- Preserve source lineage on every extracted record.
- Do not treat raw incident evidence as final truth automatically.
- Do not create final runbooks directly from a single incident.
- Do not invent commands, service names, hostnames, SQL, API endpoints, screenshots, access paths, timestamps, root causes, or approval status.
- Keep observed signals separate from inferred causes.
- Default review status should be `needs_sme_review`.
- Publish to Cosmos/vector search only after validation gates pass.

## Main Folders

```text
docs/
  HANDOFF.md
  architecture.md
  development_status.md

orchestration/
  scripts/watch_inbox.py
  scripts/run_ingestion_agent.py

incidenceknowledgeingestion/
  README.md
  data/output/incidents/<case_id>/   source-specific incident outputs
  docs/
  scripts/
  src/
  tests/

operationalknowledgeingestion/
  README.md
  data/output/<source_id>/           source-specific operational outputs
  docs/
  scripts/
  src/
  tests/

shared_pipeline_stages/
  README.md                          shared stage code and review guide
  scripts/                           shared stage entrypoints
  data/output/shared/                cross-source shared stage outputs

app_handoff_package/
  README.md                          app-side Cosmos and gate phrase contract

brain/
brain_service/
http_server/
mcp_server/
providers/
  Brain records, service/API surfaces, and provider wrappers

connectors/
  Salesforce and Microsoft Graph probes/adapters

sme_review_runbooks/
  SME-friendly copies of runbook markdown by source

stage_prompts/
  shared prompt contracts
```

## Reviewing Data Outputs

Each pipeline writes local JSON, reports, and images first. Review locally before any Cosmos DB or vector publishing.

| Area | Output root |
| --- | --- |
| Operational ingestion | `operationalknowledgeingestion/data/output/<source_id>/` |
| Incident ingestion | `incidenceknowledgeingestion/data/output/incidents/<case_id>/` |
| Shared pipeline stages | `shared_pipeline_stages/data/output/shared/` |
| SME runbook review copies | `sme_review_runbooks/<source_id>/` |
| Assembled handoff | `data/output/sme_review/` and `data/output/cosmos_publish/` |

Review order: report JSON first, then primary stage JSON, then source refs/images, then validation status. Area-specific review details live in the owning README.

## Where To Start

For handoff, read `docs/HANDOFF.md`, then `docs/architecture.md`, then `orchestration/README.md`. For stage-specific debugging, read the owning area README before opening generated outputs.

## README Update Hook

After architecture or stage-status changes, follow [docs/README_UPDATE.md](docs/README_UPDATE.md). Do not hand-edit generated blocks between `<!-- AUTO:*_START -->` and `<!-- AUTO:*_END -->`; edit the source status doc and run the matching update script.
