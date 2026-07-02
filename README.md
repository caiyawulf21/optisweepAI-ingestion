# OptiSweep AI Ingestion

`optisweepAI-ingestion` is the local workspace for building source-grounded ingestion pipelines that turn OptiSweep operational and incident evidence into reviewable knowledge records for the troubleshooting app.

The repository is organized around two sibling ingestion areas plus shared pipeline stages:

```text
operationalknowledgeingestion/
incidenceknowledgeingestion/
shared_pipeline_stages/
```

The long-term production shape is two coordinated LangGraph pipelines that share downstream review, synthesis, embedding, and publishing stages:

1. Operational knowledge ingestion
2. Incidence knowledge ingestion

Both pipelines should preserve source lineage, create reviewable local outputs first, and only publish validated/reviewable records to Cosmos DB and vector search for use by the OptiSweep AI troubleshooting app.

## Pipeline Roles

`operationalknowledgeingestion/` handles stable operational knowledge from manuals, training slides, training recordings, transcripts, SOP-style material, and other product documentation.

It produces source artifacts, operational context records, runbook candidates, candidate pools, and planned canonical runbooks, relationships, embeddings, and graph/publishing outputs.

`incidenceknowledgeingestion/` handles incident evidence, especially PDF screenshot packages containing Salesforce case events, Teams chats, RCA/support screenshots, logs, and attachments.

It should produce source package inventories, incident artifacts, canonical incident records, timeline events, operational context, runbook candidates, workflow/playbook candidates, and candidate pool contributions. Incident-derived candidates should flow into the same shared candidate pool used by operational sources.

## Shared Knowledge Flow

The two pipelines converge after source-specific extraction:

```text
Operational/manual/training candidates
Incident-derived candidates
SOP/SME candidates
        ->
Shared candidate pool
        ->
Cross-source merging, deduplication, synthesis
        ->
Canonical runbooks and canonical workflows/playbooks
        ->
Markdown review files + structured JSON
        ->
Relationship linking and validation
        ->
Embedding records
        ->
Cosmos DB / vector search / troubleshooting app retrieval
```

Final runbooks should not be owned by a single source. Manuals describe what should be done; incidents describe what was actually done. The final canonical library should merge evidence while preserving source lineage.

## Development Status

<!-- AUTO:DEVELOPMENT_STATUS_START -->
This section is generated from `docs/development_status.md`. Update that file whenever either ingestion area advances to a new stage or changes its next milestone.

## Operational Knowledge Ingestion

Current position: source-specific operational extraction is implemented through Stage 6 as local, reviewable scripts.

Implemented today:

- Stage 1: source bundle extraction.
- Stage 2: source artifact and image extraction.
- Stage 3: Azure OpenAI source artifact enrichment.
- Stage 4: operational context extraction.
- Stage 5: runbook candidate discovery.
- Stage 6: source runbook finalization (LLM assisted).
- Stage 6.5: shared runbook pool generation over finalized runbooks.
- Training video bundle generation and preparation for Stage 4 and Stage 5.

Next milestones:

- Run and review Stage 6 finalized runbooks against Runbook Example.md.
- Shared Stage 6.5: runbook pool and merge preparation from finalized runbooks (`shared_pipeline_stages/`).
- Shared Stage 7: selective cross-source runbook merge.
- Stage 8+: relationship linking, validation, embeddings, and publishing.

Primary details live in `operationalknowledgeingestion/README.md`.

## Incidence Knowledge Ingestion

Current position: source-specific incident extraction is implemented through Stage 6 scripts; Case 228086/228723 have Stage 5 outputs and Stage 6 is ready to run with `--llm`.

Implemented today:

- Stage 1: incident source package loading and page/source inventory.
- Stage 2: OCR and evidence artifact extraction with page inventory, artifact extraction report, source artifacts, duplicate grouping, and compact `incident_source_package.json.source_bundle` handoff.
- Stage 2.5: deterministic artifact enrichment packet preparation.
- Stage 3: Azure OpenAI incident artifact enrichment.
- Stage 4: Azure OpenAI canonical incident record and timeline extraction.
- Stage 5: incident runbook candidate discovery plus playbook candidate discovery (Prompt A/B).
- Stage 6: source runbook finalization for runbook candidates only (LLM assisted).

Next milestones:

- Run and review Stage 6 finalized runbooks for Case 228086.
- Shared Stage 6.5: runbook pool and merge preparation from finalized runbooks (`shared_pipeline_stages/`).
- Shared Stage 7: selective cross-source runbook merge.
- Shared Stage 8: playbook linking and finalization.

Primary details live in `incidenceknowledgeingestion/README.md`.

## Shared Design Notes

- `docs/runbook_candidate_pool_and_azure_review_design.md` tracks the proposed
  shared candidate pool, Stage 6.5 packet finalization, Azure retrieval,
  local-first `RunbookRetriever` plan, merge-review, human approval, and
  versioned publishing model for canonical runbooks.
- `docs/design_decisions/stage_5_6_playbook_extraction_modes.md` tracks why
  Stage 5 currently runs both playbook extraction modes and how Stage 6 should
  compare them before choosing the default behavior.

## README Update Rule

When stage status changes:

1. Update this file.
2. Update any area-specific status source, such as `incidenceknowledgeingestion/docs/development_status.md`.
3. Run the relevant hook:

```bash
python scripts/update_readme.py
python incidenceknowledgeingestion/scripts/update_readme.py
```

The operational README also has its own generated development-log hook:

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
cursorprompts/
  incidence_ingestion_prompts/
    incidence_ingestion_prompt

docs/
  development_status.md

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
  data/output/shared/                  cross-source shared stage outputs
  stage_6_5/
  tests/

stage_prompts/
  stage_6/                           shared Stage 6 LLM prompts

scripts/
  update_readme.py
  stage6_5_build_runbook_pool.py
```

## Reviewing Data Outputs

Each pipeline writes local JSON, reports, and images first. Review locally before any Cosmos DB or vector publishing.

**Where outputs live**

| Area | Output root | Example |
| --- | --- | --- |
| Operational ingestion | `operationalknowledgeingestion/data/output/<source_id>/` | `manual_optisweep_om_v3/` |
| Incident ingestion | `incidenceknowledgeingestion/data/output/incidents/<case_id>/` | `case_228086/` |
| Shared pipeline stages | `shared_pipeline_stages/data/output/shared/` | `stage_6_5_runbook_pool/` |

**General review order**

1. Read the stage extraction report first (`*_report.json`, `*_extraction_report.json`, or `runbook_pool_report.json`).
2. Check counts, warnings, dropped records, and failed packets before opening large JSON payloads.
3. Open the primary stage JSON (`source_artifacts.json`, `runbook_candidates.json`, `merge_clusters.json`, etc.).
4. Trace a sample record back to source refs (page, artifact, candidate, or case evidence).
5. Confirm review status is still `needs_sme_review` unless a reviewer explicitly approved the record.

**Area-specific review guides**

- Operational stages 1–6: `operationalknowledgeingestion/README.md`
- Incident stages 1–6: `incidenceknowledgeingestion/README.md`
- Shared Stage 6.5 runbook pool and merge prep: `shared_pipeline_stages/README.md`

## Where To Start

For operational ingestion, start with:

```text
operationalknowledgeingestion/README.md
```

For incidence ingestion planning, start with:

```text
cursorprompts/incidence_ingestion_prompts/incidence_ingestion_prompt
incidenceknowledgeingestion/README.md
incidenceknowledgeingestion/datastructureprompts/
```

## README Update Hook

Run the root README update hook after meaningful stage changes:

```bash
python scripts/update_readme.py
```

The hook refreshes the marked development-status section from `docs/development_status.md` while preserving the rest of this README.
