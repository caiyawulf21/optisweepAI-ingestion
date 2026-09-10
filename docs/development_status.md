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
