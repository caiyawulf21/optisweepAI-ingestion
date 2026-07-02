# OptiSweep AI Ingestion

`optisweepAI-ingestion` is the local workspace for building source-grounded ingestion pipelines that turn OptiSweep operational and incident evidence into reviewable knowledge records for the troubleshooting app.

The repository is organized around two sibling ingestion areas:

```text
operationalknowledgeingestion/
incidenceknowledgeingestion/
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
- Stage 6: candidate pool generation.
- Training video bundle generation and preparation for Stage 4 and Stage 5.

Next milestones:

- Stage 7: canonical runbook drafting and merging from candidate pools.
- Stage 8: relationship linking across artifacts, context, candidates, and runbooks.
- Stage 9 and Stage 10: validation, repair, and final local outputs.
- Stage 11 and Stage 12: vector embeddings and operational knowledge graph generation.
- Future LangGraph orchestration and Cosmos DB/vector publishing after validation gates.

Primary details live in `operationalknowledgeingestion/README.md`.

## Incidence Knowledge Ingestion

Current position: Case 228086 proof-path extraction is implemented through Stage 3 outputs, with Stage 4 prompts and scripts now implemented but not yet run.

Implemented today:

- Stage 1: incident source package loading and page/source inventory.
- Stage 2: OCR and evidence artifact extraction with page inventory, artifact extraction report, source artifacts, duplicate grouping, and compact `incident_source_package.json.source_bundle` handoff.
- Stage 2.5: deterministic artifact enrichment packet preparation.
- Stage 3: Azure OpenAI incident artifact enrichment.
- Stage 4: Azure OpenAI canonical incident record and timeline extraction prompts/scripts, pending first run and review.

Current proof output:

- `incidenceknowledgeingestion/data/output/incidents/case_228086/stage_1_source_package/incident_source_package.json`
- `incidenceknowledgeingestion/data/output/incidents/case_228086/stage_2_ocr_artifacts/page_inventory.json`
- `incidenceknowledgeingestion/data/output/incidents/case_228086/stage_2_ocr_artifacts/source_artifacts.json`
- `incidenceknowledgeingestion/data/output/incidents/case_228086/stage_2_ocr_artifacts/artifact_extraction_report.json`
- `incidenceknowledgeingestion/data/output/incidents/case_228086/stage_2_5_artifact_enrichment_packets/artifact_enrichment_packets.json`
- `incidenceknowledgeingestion/data/output/incidents/case_228086/stage_3_artifact_enrichment/source_artifacts_enriched.json`

Next milestones:

- Run and review Stage 4 for Case 228086.
- Stage 5 through Stage 8: operational context, runbook candidates, playbook candidates, and candidate pool contribution.
- Stage 9 and Stage 10: source-specific validation and final local outputs.
- Stage 11 through Stage 15: shared canonical synthesis, relationship linking, embeddings, and publishing alignment with the operational pipeline.

Primary details live in `incidenceknowledgeingestion/README.md`.

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
  docs/
    development_status.md
  datastructureprompts/
    Canonical Incident Record Example.md
    Timeline Events.md

operationalknowledgeingestion/
  README.md
  docs/
  scripts/
  src/
  tests/

scripts/
  update_readme.py
```

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
