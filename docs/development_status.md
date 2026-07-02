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
python shared_pipeline_stages/scripts/update_readme.py
python incidenceknowledgeingestion/scripts/update_readme.py
```

The operational README also has its own generated development-log hook:

```bash
python operationalknowledgeingestion/scripts/update_readme.py
```
