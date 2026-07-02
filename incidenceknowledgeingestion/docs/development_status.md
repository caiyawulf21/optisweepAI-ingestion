This section is generated from `incidenceknowledgeingestion/docs/development_status.md`. Update that file whenever an incident-ingestion stage moves from planned to implemented, changes scope, or gains new review outputs.

Current position: Case 228086 is the proof case. Stages 1, 2, and 2.5 are implemented as deterministic local scripts. Stage 3 is the required LLM artifact enrichment step. Stage 4 prompts and CLI wiring are implemented for LLM-backed canonical incident record and timeline extraction. Stage 5 runbook and playbook candidate discovery is implemented and consumes Stage 4 outputs.

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
  stage5_runbook_candidates.py - Stage 5 LLM incident runbook and playbook candidate discovery
  prompts/stage3_artifact_enrichment_prompt.md - Stage 3 artifact enrichment prompt
  prompts/stage4_canonical_incident_record_prompt.md - Stage 4 canonical incident record prompt
  prompts/stage4_timeline_events_prompt.md - Stage 4 timeline event prompt
  prompts/stage5_runbook_candidate_discovery_prompt.md - Stage 5 runbook candidate prompt
  prompts/stage5_playbook_candidate_discovery_prompt.md - Stage 5 playbook candidate prompt
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
| Stage 5 | Incident runbook and playbook candidate discovery | Implemented |
| Stage 6 | Candidate pool contribution | Planned |
| Stage 7 | Source-specific validation and extraction report | Planned |
| Stage 8 | Source-specific final output writing | Planned |
| Stage 9 | Reserved for source-specific handoff packaging | Planned |
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

Stage 5 runs three Azure OpenAI calls in the same stage: one for
incident-derived runbook candidates and two for incident-derived playbook
candidate extraction modes. Runbook discovery may return zero candidates when
the incident evidence does not support a reusable procedure. Playbook Prompt A
forces one incident to one playbook candidate. Playbook Prompt B produces one
or more candidates, but creates multiple only when separable troubleshooting
flows are clearly present. Playbook discovery describes incident response logic and
needed runbook capabilities without binding nodes to canonical runbook IDs. All
candidates are needs-review source-specific discoveries, not finalized
canonical runbooks or playbooks.

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

Use `--include-detected-crops` only when a PDF does not expose useful embedded images and OpenCV fallback crops are needed. The default keeps artifact images focused on the actual embedded screenshots/photos and avoids surrounding document or chat text in the image file.

## Next Development Target

Stage 4 should be run and reviewed for Case 228086. The first quality gate is whether it preserves source refs, handles Haslet/Alliance location ambiguity, keeps exact downtime warnings when needed, and avoids promoting restart guidance or case comments into canonical root cause.
