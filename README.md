# OptiSweep Ingestion

## Project Name

`optisweep-ingestion`

## Purpose

This repo is focused only on local OptiSweep data ingestion and data quality. It will eventually turn source material into clean local JSON outputs that can be reviewed before any production system or database is involved.

The first target source is the OptiSweep Operation and Maintenance Manual. The first proof case will be the heartbeat diagnostic example.

## Current Scope

- Organize source material for local ingestion.
- Define the planned output records.
- Prepare a clean Python project structure.
- Track the intended ingestion stages.
- Keep the README current as the project evolves.

## Current Stage: Stage 5 — LLM Runbook Candidate Discovery

Stage 5 uses the source bundle, enriched source artifacts, and operational context records to identify reusable runbook/procedure candidates.

A runbook candidate is not a final runbook. It is a lightweight record that identifies a reusable procedure opportunity, rough steps, likely role, likely procedure type, source refs, related context, and related artifacts.

This stage does not create workflows, routing rules, trigger conditions, or final approved runbooks.

Inputs:

```text
data/output/manual_optisweep_om_v3/source_bundle.json
data/output/manual_optisweep_om_v3/source_artifacts_enriched.json
data/output/manual_optisweep_om_v3/operational_context.json
```

Outputs:

```text
data/output/manual_optisweep_om_v3/runbook_candidates.json
data/output/manual_optisweep_om_v3/runbook_candidate_extraction_report.json
```

Run:

```bash
python scripts/extract_runbook_candidates.py \
  --source-bundle data/output/manual_optisweep_om_v3/source_bundle.json \
  --source-artifacts data/output/manual_optisweep_om_v3/source_artifacts_enriched.json \
  --operational-context data/output/manual_optisweep_om_v3/operational_context.json \
  --output-dir data/output/manual_optisweep_om_v3 \
  --llm
```

## Previous Stage: Stage 4 — LLM Operational Context Extraction

Stage 4 uses the source bundle and enriched source artifacts to extract reusable operational context records.

Operational context explains systems, components, screens, metrics, alarms, statuses, and stable operating concepts.

It does not create runbooks, procedures, workflows, routing rules, or trigger conditions.

Inputs:

```text
data/output/manual_optisweep_om_v3/source_bundle.json
data/output/manual_optisweep_om_v3/source_artifacts_enriched.json
```

Outputs:

```text
data/output/manual_optisweep_om_v3/operational_context.json
data/output/manual_optisweep_om_v3/operational_context_extraction_report.json
```

Run:

```bash
python scripts/extract_operational_context.py \
  --source-bundle data/output/manual_optisweep_om_v3/source_bundle.json \
  --source-artifacts data/output/manual_optisweep_om_v3/source_artifacts_enriched.json \
  --output-dir data/output/manual_optisweep_om_v3 \
  --llm
```

## Previous Stage: Stage 3 — LLM Source Artifact Enrichment

Stage 3 uses an LLM to enrich extracted source artifact records with descriptions, what-to-look-at guidance, tags, and retrieval text.

Inputs:

```text
data/output/manual_optisweep_om_v3/source_artifacts.json
data/output/manual_optisweep_om_v3/artifact_extraction_report.json
```

Outputs:

```text
data/output/manual_optisweep_om_v3/source_artifacts_enriched.json
data/output/manual_optisweep_om_v3/artifact_enrichment_report.json
```

Run:

```bash
python scripts/enrich_source_artifacts.py \
  --source-artifacts data/output/manual_optisweep_om_v3/source_artifacts.json \
  --artifact-report data/output/manual_optisweep_om_v3/artifact_extraction_report.json \
  --output-dir data/output/manual_optisweep_om_v3 \
  --llm
```

This stage does not create operational context, runbooks, workflows, or relationship links.

## Previous Stage: Stage 2 - Source Artifact / Image Extraction

Stage 2 reads the Stage 1 `source_bundle.json` and the original PDF manual, extracts available embedded images, and creates traceable source artifact records.
If a figure cannot be extracted as a standalone embedded image, Stage 2 renders the full PDF page under `images/fallback_pages/` and marks the artifact for crop/visual review.

Outputs:

```text
data/output/manual_optisweep_om_v3/source_bundle.json
data/output/manual_optisweep_om_v3/source_artifacts.json
data/output/manual_optisweep_om_v3/artifact_extraction_report.json
data/output/manual_optisweep_om_v3/images/
```

Run:

```bash
python scripts/extract_manual_artifacts.py \
  --source-bundle data/output/manual_optisweep_om_v3/source_bundle.json \
  --source-pdf "data/input/manuals/OptiSweep Operation and Maintenance Manual - Final 1.pdf" \
  --output-dir data/output/manual_optisweep_om_v3
```

This stage is deterministic. It does not call an LLM and does not populate linked context or runbook IDs yet.

Stage 1 source bundle generation remains available:

```bash
python scripts/extract_manual.py \
  --source-pdf "data/input/manuals/OptiSweep Operation and Maintenance Manual - Final 1.pdf" \
  --output-dir data/output/manual_optisweep_om_v3
```

Stage 1 now includes quality checks for:
- conservative section heading detection
- front matter filtering
- canonical figure/table reference selection
- heartbeat detectability smoke checks

## Out of Scope For Now

- Running the production assistant.
- Writing to Cosmos or PostgreSQL.
- Connecting to Teams, SharePoint, Salesforce, Azure storage, or other runtime services.
- Implementing LLM calls, operational context extraction, runbook extraction, database writes, or LangGraph runtime orchestration.

## Target Outputs

- Source artifacts, images, and manual references.
- Operational context records for retrieval.
- Reusable runbooks and procedures.
- Extraction reports.

## Planned Pipeline

LangGraph will be used later to orchestrate ingestion stages, but the graph is not implemented yet.

Detailed stage planning lives in `cursorprompts/manual_ingestion_prompts/manual_ingestion_plan.md`.
Future architecture decisions live in `docs/operational_knowledge_pipeline_architecture.md`.

## Folder Structure

```text
.
  README.md
  pyproject.toml
  .env.example
  .gitignore
  data/
    input/
    processed/
    output/
    review/
  docs/
  scripts/
  src/
    optisweep_ingestion/
  tests/
```

## Development Workflow

1. Add source files under `data/input/`.
2. Keep planned contracts and decisions in `docs/`.
3. Add ingestion code under `src/optisweep_ingestion/` only when the design is ready.
4. Write local JSON outputs under `data/output/`.
5. Review samples and validation reports under `data/review/`.

## README Update Hook

Run the README update hook after meaningful project changes:

```bash
python scripts/update_readme.py
```

The hook refreshes the marked development log section while preserving the rest of this README.

## Current Status

Stages 1–4 are implemented. Stage 4 (operational context extraction) produces `operational_context.json` from the source bundle and enriched artifacts using an LLM. Later ingestion stages remain placeholders.

<!-- AUTO:DEVELOPMENT_LOG_START -->
# Development Log

## Unreleased

### Added
- Stage 1 source bundle extraction for the OptiSweep Operation and Maintenance Manual.
- Stage 2 source artifact and image extraction with artifact reports and priority figure checks.
- Stage 3 Azure AI Foundry source artifact enrichment with descriptions, tags, what-to-look-at guidance, and retrieval text.
- Stage 4 operational context extraction scaffolding for reusable context records.

### Changed
- README current-stage guidance now reflects the implemented ingestion stages.

### Decisions
- Keep this repo focused on local ingestion and data quality before database writes.
- Use one future LangGraph pipeline with multiple stage nodes.
- Keep source artifact enrichment separate from operational context, runbooks, workflows, and relationship linking.
<!-- AUTO:DEVELOPMENT_LOG_END -->
