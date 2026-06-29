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

Current position: Case 228086 proof-path extraction is implemented through Stage 2 as deterministic local scripts.

Implemented today:

- Stage 1: incident source package loading and page/source inventory.
- Stage 2: OCR and evidence artifact extraction with page inventory, artifact extraction report, source artifacts, duplicate grouping, and compact `incident_source_package.json.source_bundle` handoff.

Current proof output:

- `incidenceknowledgeingestion/data/output/incidents/case_228086/incident_source_package.json`
- `incidenceknowledgeingestion/data/output/incidents/case_228086/page_inventory.json`
- `incidenceknowledgeingestion/data/output/incidents/case_228086/source_artifacts.json`
- `incidenceknowledgeingestion/data/output/incidents/case_228086/artifact_extraction_report.json`

Next milestones:

- Stage 3: incident normalization from the Stage 2 source bundle.
- Stage 4: timeline event extraction.
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
