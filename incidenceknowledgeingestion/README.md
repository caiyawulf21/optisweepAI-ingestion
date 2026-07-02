# Incidence Knowledge Ingestion

`incidenceknowledgeingestion` is the planned incident-data ingestion area for OptiSweep support evidence.

Its purpose is to convert source-grounded incident packages into reviewable knowledge assets that can support historical incident retrieval, troubleshooting, runbook creation, workflow/playbook creation, relationship linking, embeddings, and eventual Cosmos DB/vector search publishing.

## Development Status

<!-- AUTO:DEVELOPMENT_STATUS_START -->
This section is generated from `incidenceknowledgeingestion/docs/development_status.md`. Update that file whenever an incident-ingestion stage moves from planned to implemented, changes scope, or gains new review outputs.

Current position: Case 228086 is the proof case. Stages 1, 2, and 2.5 are implemented as deterministic local scripts. Stage 3 is the required LLM artifact enrichment step. Stage 4 prompts and CLI wiring are implemented for LLM-backed canonical incident record and timeline extraction. Stage 5 runbook candidate discovery is implemented and consumes Stage 4 outputs.

## Implemented Content

```text
datastructureprompts/
  Canonical Incident Record Example.md - Stage 4 canonical incident record example
  Runbook Example.md - Stage 6 candidate/shared canonical runbook structure reference
  Timeline Events.md - Stage 4 timeline event example
scripts/
  extract_incident_knowledge.py - Stages 1-5 local runner
  update_readme.py - all-stage documentation utility
src/optisweep_incidence_ingestion/
  ocr.py - Stage 2 OCR support helpers
  stage1_source_package.py - Stage 1 source package loading
  stage2_5_artifact_enrichment_packets.py - Stage 2.5 artifact enrichment packet preparation
  stage2_ocr_artifacts.py - Stage 2 OCR and evidence artifact extraction
  stage3_artifact_enrichment.py - Stage 3 LLM artifact enrichment
  stage4_canonical_incident_record.py - Stage 4 LLM canonical incident and timeline extraction
  stage5_runbook_candidates.py - Stage 5 LLM incident runbook candidate discovery
  prompts/stage3_artifact_enrichment_prompt.md - Stage 3 artifact enrichment prompt
  prompts/stage4_canonical_incident_record_prompt.md - Stage 4 canonical incident record prompt
  prompts/stage4_timeline_events_prompt.md - Stage 4 timeline event prompt
  prompts/stage5_runbook_candidate_discovery_prompt.md - Stage 5 candidate prompt
```

These files are prompt/schema examples, deterministic extraction code, and local proof outputs for Case 228086. They are contract guidance and extraction scaffolding, not source truth for every future incident.

## Stage Tracker

| Stage | Purpose | Status |
| --- | --- | --- |
| Stage 1 | Incident source package loading | Implemented |
| Stage 2 | OCR and evidence artifact extraction | Implemented |
| Stage 2.5 | Artifact enrichment packet preparation | Implemented |
| Stage 3 | Incident artifact enrichment | Ready for LLM run |
| Stage 4 | Create canonical incident records and timeline | Implemented |
| Stage 5 | Incident runbook candidate discovery | Implemented |
| Stage 6 | Draft incident-derived workflow/playbook discovery | Planned |
| Stage 7 | Candidate pool contribution | Planned |
| Stage 8 | Source-specific validation and extraction report | Planned |
| Stage 9 | Source-specific final output writing | Planned |
| Shared Stage 11 | Cross-source canonical runbook synthesis | Shared planned |
| Shared Stage 12 | Canonical workflow/playbook synthesis | Shared planned |
| Shared Stage 13 | Relationship linking | Shared planned |
| Shared Stage 14 | Embedding generation | Shared planned |
| Shared Stage 15 | Cosmos DB and vector publishing | Shared planned |

## Stage 1 And Stage 2 Notes

Stage 1 builds `incident_source_package.json` with source and page inventory.

Stage 2 renders every page for page inventory and OCR, extracts embedded PDF images as candidate artifacts, extracts nested media from Teams/chat wrapper screenshots when possible, OCRs rendered pages and extracted evidence with local Tesseract, classifies incident evidence types, and records duplicate groups. By default, Stage 2 uses a local Qwen2.5-VL artifact gate to keep attached evidence images/forms/screenshots while suppressing outer wrapper/feed text. Use `--stage2-artifact-gate none` for deterministic-only extraction without Qwen.

Full-page renders and chat-wrapper screenshots stay in page/page OCR context and are not promoted into `source_artifacts.json` when a cleaner nested image can be extracted.

After Stage 2, `incident_source_package.json` also contains `source_bundle`, which is the compact handoff object for later stages. Stage 2.5 and later should read `incident_source_package.json.source_bundle` first and only open detailed files when deeper audit context is needed.

Stage 2.5 builds `artifact_enrichment_packets.json` by joining clean artifact images/OCR with page-level OCR context. It does not enrich artifacts or turn OCR into English. Stage 3 reads those packets and requires `--llm`; fake enrichment is not supported. Stage 4 reads page OCR and Stage 3 enriched artifacts, builds compact `stage4_evidence_chunks.json`, then uses separate prompts to create the concise canonical incident record and detailed timeline events.

Stage 5 reads the Stage 4 incident package, canonical incident record, timeline events, `stage4_evidence_chunks.json`, and Stage 3 enriched artifacts. It builds `stage5_runbook_candidate_packet.json`, calls the Stage 5 runbook candidate prompt, normalizes returned candidates, validates page/artifact/event/chunk references, drops invalid candidates, and writes reviewable candidate outputs. Stage 5 creates runbook candidates only: reusable procedure blocks a person can follow. It does not create canonical runbooks, playbooks, workflows, trigger conditions, routing logic, issue categories, decision trees, or ML labels. Image-supported steps must include inline `[Image support needed: ...]` notes that correspond to related artifact IDs. Generic post-processing folds API/endpoint/status-response validation diagnostics into the associated recovery runbook candidate when appropriate, instead of leaving validation as a standalone runbook. All incident-derived candidates remain `needs_review` and must flow through later shared candidate-pool and canonical runbook stages before production use.

## Current Proof Output

```text
data/output/incidents/case_228086/
  stage_1_source_package/
    incident_source_package.json
    stage1_source_package_report.json
    raw_source/
  stage_2_ocr_artifacts/
    artifact_contact_sheet.jpg
    artifact_extraction_report.json
    incident_source_package.json
    page_inventory.json
    source_artifacts.json
    images/
  stage_2_5_artifact_enrichment_packets/
    artifact_enrichment_packets.json
    artifact_enrichment_packet_report.json
    incident_source_package.json
  stage_3_artifact_enrichment/
    incident_source_package.json
    artifact_enrichment_report.json
    source_artifacts_enriched.json
  stage_4_canonical_incident_record/
    stage4_evidence_chunks.json
    canonical_incident_record.json
    canonical_incident_record_extraction_report.json
    timeline_events.json
    timeline_event_extraction_report.json
    incident_source_package.json
  stage_5_runbook_candidates/
    stage5_runbook_candidate_packet.json
    runbook_candidates.json
    runbook_candidate_extraction_report.json
    runbook_candidate_review.md
    incident_source_package.json
```

## Run Current Implemented Stages

```powershell
python incidenceknowledgeingestion\scripts\extract_incident_knowledge.py `
  --source-pdf "incidenceknowledgeingestion\data\input\incidents\Case 228086 Data.pdf" `
  --case-id 228086 `
  --source-title "Case 228086 - UPS Haslet OptiSweep Incident Evidence" `
  --output-dir incidenceknowledgeingestion\data\output\incidents\case_228086 `
  --stages 1,2,2.5 `
  --ocr-backend tesseract `
  --tesseract-command "$env:LOCALAPPDATA\Programs\Tesseract-OCR\tesseract.exe" `
  --copy-source
```

Stage 2 defaults to `--stage2-artifact-gate qwen` and resolves the cached local `Qwen/Qwen2.5-VL-3B-Instruct` snapshot when present. To bypass Qwen for a faster deterministic-only run, add:

```powershell
  --stage2-artifact-gate none
```

Run Stage 3 after Azure OpenAI environment variables are configured:

```powershell
python incidenceknowledgeingestion\scripts\extract_incident_knowledge.py `
  --source-pdf "incidenceknowledgeingestion\data\input\incidents\Case 228086 Data.pdf" `
  --case-id 228086 `
  --output-dir incidenceknowledgeingestion\data\output\incidents\case_228086 `
  --stages 3 `
  --llm
```

Run Stage 4 after Stage 3 completes:

```powershell
python incidenceknowledgeingestion\scripts\extract_incident_knowledge.py `
  --source-pdf "incidenceknowledgeingestion\data\input\incidents\Case 228086 Data.pdf" `
  --case-id 228086 `
  --output-dir incidenceknowledgeingestion\data\output\incidents\case_228086 `
  --stages 4 `
  --stage4-page-chunk-chars 7000 `
  --stage4-artifact-chunk-size 8 `
  --llm
```

Run Stage 5 after Stage 4 completes:

```powershell
python incidenceknowledgeingestion\scripts\extract_incident_knowledge.py `
  --source-pdf "incidenceknowledgeingestion\data\input\incidents\Case 228086 Data.pdf" `
  --case-id 228086 `
  --output-dir incidenceknowledgeingestion\data\output\incidents\case_228086 `
  --stages 5 `
  --llm
```

Stage 5 outputs:

- `stage_5_runbook_candidates/stage5_runbook_candidate_packet.json`
- `stage_5_runbook_candidates/runbook_candidates.json`
- `stage_5_runbook_candidates/runbook_candidate_extraction_report.json`
- `stage_5_runbook_candidates/runbook_candidate_review.md`
- `stage_5_runbook_candidates/incident_source_package.json`

Use `--include-detected-crops` only when a PDF does not expose useful embedded images and OpenCV fallback crops are needed. The default keeps artifact images focused on the actual embedded screenshots/photos and avoids surrounding document or chat text in the image file.

## Next Development Target

Stage 5 should be reviewed for Case 228086 and Case 228723. The first quality gate is whether each candidate is source-grounded, preserves valid page/artifact/event refs, remains a `needs_review` candidate, and reads like a runbook procedure rather than a playbook, workflow, passive evidence card, or canonical runbook.
<!-- AUTO:DEVELOPMENT_STATUS_END -->

## Source Shape

The initial v1 input shape is expected to be incident evidence packages, especially:

- PDFs containing screenshots of Salesforce case events
- PDFs containing screenshots of Teams chats related to an incident
- optional RCA/support screenshots or documents
- optional logs and attachments

The pipeline should not assume native Salesforce export JSON or native Teams export JSON exists in v1.

PDF pages are source evidence containers, not automatic artifacts. Every page should be inventoried for lineage, OCR, and review, but only meaningful screenshots, cropped evidence regions, attached images, tables, logs, or reusable support evidence should become source artifact records.

## Planned Pipeline

```text
Stage 1: Incident source package loading
Stage 2: OCR and evidence artifact extraction
Stage 2.5: Artifact enrichment packet preparation
Stage 3: Incident artifact enrichment
Stage 4: Create canonical incident records and timeline
Stage 5: Incident runbook candidate discovery
Stage 6: Draft incident-derived workflow/playbook discovery
Stage 7: Candidate pool contribution
Stage 8: Source-specific validation and extraction report
Stage 9: Source-specific final output writing
Shared Stage 11: Cross-source canonical runbook synthesis
Shared Stage 12: Canonical workflow/playbook synthesis
Shared Stage 13: Relationship linking
Shared Stage 14: Embedding generation
Shared Stage 15: Cosmos DB and vector publishing
```

Stages 1 through 11 are incident-source extraction stages. Shared stages are finalization stages that should align with the operational knowledge pipeline.

## Planned Outputs

Source-specific incident extraction should produce:

```text
source_artifacts.json
canonical_incident_record.json
timeline_events.json
runbook_candidates.json
playbook_candidates.json
candidate_pool_contribution.json
extraction_report.json
```

Shared finalization should produce:

```text
canonical_runbooks.json
canonical_workflows.json
review_markdown/runbooks/*.md
review_markdown/workflows/*.md
relationship_links.json
embedding_records.json
cosmos_publish_report.json
```

## Relationship To Operational Ingestion

The incidence pipeline should reuse structure from `operationalknowledgeingestion` where it is clean and low-risk:

- source lineage and source refs
- deterministic JSON reading/writing
- stable ID generation
- artifact records and image refs
- operational context extraction packet patterns
- runbook candidate schema shape
- shared candidate pool format and clustering
- canonical runbook Markdown + JSON review pattern
- relationship linking and validation report patterns
- embedding and publishing report patterns

It should not copy manual-specific assumptions such as manual sections, figure numbers, manual-only source types, or manual priority checks.

If a shared utility would require risky changes to operational ingestion, copy/adapt the pattern into this folder first and record the future refactor opportunity.

## Case 228086

Case 228086 is the gold-standard planning case for proving the incidence pipeline can extract detailed recovery procedures from original case evidence instead of relying only on compressed normalized summaries.

The extractor should preserve:

- exact engineer actions
- Windows service restart steps
- service names if explicitly present
- VPN/RDP/remote access steps if explicitly present
- RMS navigation and AGV correction steps
- Ignition or web application recovery steps
- screenshots or attachment references
- validation checks
- log collection steps
- escalation notes
- unresolved follow-up items, such as infrastructure/log sizing

If the source only says "restart the service," preserve that as a source-grounded action and record missing details in the extraction report. Do not invent service names, hostnames, commands, URLs, RMS screens, Ignition screens, or access paths.

## Review And Publishing Rules

- Incident-derived records default to `needs_sme_review`.
- Incident-derived runbook candidates feed the shared candidate pool.
- Final runbooks come from the finalized canonical runbook library after pooling, merging, deduplication, synthesis, validation, and SME review.
- Final workflows/playbooks should reference finalized canonical runbooks as reusable procedure blocks where possible.
- Markdown files are for SME/product review.
- Structured JSON records are for validation, embeddings, Cosmos DB publishing, graph relationships, and runtime use.
- Cosmos/vector publishing should happen only after validation gates pass.
