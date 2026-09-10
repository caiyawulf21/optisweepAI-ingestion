This section is generated from `incidenceknowledgeingestion/docs/development_status.md`. Update that file whenever an incident-ingestion stage moves from planned to implemented, changes scope, or gains new review outputs. Architecture rationale: `docs/architecture.md`. Update process: `docs/README_UPDATE.md`.

Current position: Cases `218550`, `223554`, `228086`, and `228723` run through Stages 1–6 + 8 into shared publish. Stage 2 uses Azure Computer Vision gating (`--stage2-artifact-gate azure_cv`) plus automatic page/OpenCV fallback when embedded wrappers yield no nested crops (fix for 218550 empty artifacts). Stage 5 playbook candidates must carry short `support_user_language_examples`; Shared Stage 8 enriches them further before cumulative Stage 11 publish. Stage 5 playbook discovery is source-grounded: nodes separate observed and historical surfaces with provenance from required evidence concepts, while ontology surfaces are not injected and Stage 8 selects the current diagnostic surface. Incident **runbook** Stage 5/6 still mirrors operational live-surface rules (`allowed_access_surfaces`, `ontology_snippets`, eligibility, tag emit/infer). Shared Stage 8 caps confidence on pairing/hospital/roster gaps and hard-rejects recovery-prep on check-only nodes.

## Implemented Content

```text
datastructureprompts/
  Canonical Incident Record Example.md - Stage 4 canonical incident record example
  Runbook Example.md - Stage 6 candidate/shared canonical runbook structure reference
  Timeline Events.md - Stage 4 timeline event example
scripts/
  extract_incident_knowledge.py - Stages 1-8 local runner
  stage8_link_relationships.py - Stage 8 relationship linking CLI
  update_readme.py - all-stage documentation utility
src/optisweep_incidence_ingestion/
  ocr.py - Stage 2 OCR support helpers
  stage1_source_package.py - Stage 1 source package loading
  stage2_5_artifact_enrichment_packets.py - Stage 2.5 artifact enrichment packet preparation
  stage2_ocr_artifacts.py - Stage 2 OCR and evidence artifact extraction
  stage3_artifact_enrichment.py - Stage 3 LLM artifact enrichment
  stage4_canonical_incident_record.py - Stage 4 LLM canonical incident and timeline extraction
  stage5_runbook_candidates.py - Stage 5 LLM incident runbook and playbook candidate discovery
  stage6_runbook_finalization.py - Stage 6 LLM incident source runbook finalization
  stage8_relationship_linking.py - Stage 8 deterministic incident relationship linking
  tools/incident_relationship_linker.py - Stage 8 link graph builder
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
| Stage 5 | Incident runbook and playbook candidate discovery | Implemented — source-grounded playbook surfaces/evidence; runbook packets include allowed_access_surfaces + ontology_snippets |
| Stage 6 | Source runbook finalization | Implemented — access_surface/capability tag emit + ontology packet alignment |
| Stage 8 | Per-source relationship linking (artifact ↔ incident record ↔ runbook) | Implemented |
| Shared Stage 6.5 | Runbook pool and merge preparation | Shared implemented |
| Shared Stage 7 | Cross-source canonical runbook synthesis | Shared implemented |
| Shared Stage 8 | Playbook finalization, runbook linking, operator-language enrichment | Shared implemented |
| Shared Stage 8.5 | Corpus relationship linking | Shared implemented |
| Shared Stage 9 | Corpus validation | Shared implemented |
| Shared Stage 10 | Embedding generation | Shared implemented |
| Shared Stage 11 | Cumulative Cosmos publish + gate + smoke + gate_phrase_table | Shared implemented |

## Stage 1 And Stage 2 Notes

Stage 1 builds `incident_source_package.json` with source and page inventory.

Stage 2 renders every page for page inventory and OCR, extracts embedded PDF images as candidate artifacts, extracts nested media from Teams/chat wrapper screenshots when possible, OCRs rendered pages and extracted evidence with local Tesseract, classifies incident evidence types, and records duplicate groups. By default, Stage 2 uses a local Qwen2.5-VL artifact gate to keep attached evidence images/forms/screenshots while suppressing outer wrapper/feed text. Use `--stage2-artifact-gate none` for deterministic-only extraction without Qwen.

When an embedded wrapper yields **no** nested crops, Stage 2 automatically falls back to the rendered page and may promote OpenCV crops (`detected_crop_mode: fallback_only`). Use `--include-detected-crops` to force broader crop promotion when a PDF exposes no useful embedded images. Without this fallback, cases like 218550 produced zero `source_artifacts`, empty runbook `image_refs`, and weak playbook evidence.

Full-page renders and chat-wrapper screenshots stay in page/page OCR context and are not promoted into `source_artifacts.json` when a cleaner nested image can be extracted.

After Stage 2, `incident_source_package.json` also contains `source_bundle`, which is the compact handoff object for later stages. Stage 2.5 and later should read `incident_source_package.json.source_bundle` first and only open detailed files when deeper audit context is needed.

Stage 2.5 builds `artifact_enrichment_packets.json` by joining clean artifact images/OCR with page-level OCR context. It does not enrich artifacts or turn OCR into English. Stage 3 reads those packets and requires `--llm`; fake enrichment is not supported. Stage 4 reads page OCR and Stage 3 enriched artifacts, builds compact `stage4_evidence_chunks.json`, then uses separate prompts to create the concise canonical incident record and detailed timeline events.

Per-source Stage 8 relationship linking runs after Stage 6. It connects incident artifacts to `canonical_incident_record.json`, `timeline_events.json`, and finalized runbooks. Playbook candidates remain for Shared Stage 8 playbook→runbook linking; Shared Stage 8.5 aggregates per-source graphs into one corpus-wide link export.

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
canonical runbooks or playbooks. Playbook component vocabulary includes
**WCS database / SSMS (read-only)**; prompts ban SQL statements in nodes but
allow naming that surface for remote corroboration. Diagnostic nodes should
emit `expects_capability` / `expects_surface` / `preferred_audience` from
`docs/ontology/taxonomy/runbook_capability_taxonomy.json` (see
`docs/design_decisions/stage_5_8_c2_b2_b1_changelog.md`).

Stage 2 defaults to `--stage2-artifact-gate none` (no gate; embedded/nested image heuristics and OpenCV crop fallback only). Company policy requires Azure Computer Vision to be the only vision model used anywhere in this repo, so the only optional gate is Azure CV-backed:

```powershell
  --stage2-artifact-gate azure_cv
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

Default crop mode is `fallback_only` (automatic when wrappers yield no nested media). Pass `--include-detected-crops` only when you need forced OpenCV crops across pages; that can pull more surrounding chat/UI text into artifact images.

## Next Development Target

Keep operator-language examples and remote-support procedure wording aligned with demo findings (`docs/demo_testing_report.md`). Every new case must survive Shared Stage 8 enrichment + Stage 11 cumulative gate/smoke so `AUTO_PUBLISH_VERSION=true` stays safe.
