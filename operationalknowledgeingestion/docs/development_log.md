# Development Log

## Unreleased

### Changed (2026-08-07)
- Training video Stage 1 OCR default switched from local Tesseract to Azure
  AI Vision Image Analysis 4.0 ("Read" feature, synchronous
  `imageanalysis:analyze?features=read`), via new `AzureComputerVisionOCRClient`
  in `stage1_training_video_builder.py`. Select with `--ocr-backend azure_cv`
  (now default), `tesseract`, or `none`. Requires
  `AZURE_COMPUTER_VISION_ENDPOINT` / `AZURE_COMPUTER_VISION_KEY` (see
  `.env.example`); paced to the Azure free tier's 20 calls/min via
  `AZURE_COMPUTER_VISION_MIN_INTERVAL_SEC` (default 3.5s/call). Motivation:
  Tesseract-OCR'd video frames lost exact SQL column names, enum values, and
  table structure from on-screen SSMS/slide content (see
  `docs/design_decisions/day2_ontology_backend_evidence_deep_dive.md`), which
  Azure AI Vision's line/word-level Read result preserves more reliably.
  `scripts/backfill_training_video_ocr_azure_cv.py` mirrors the existing
  Tesseract backfill script for re-OCR'ing already-captured Stage 1 frames
  without re-touching the source video. This uses Azure AI Vision's Image
  Analysis "Read" feature, not Azure Document Intelligence — the 2026-08-05
  and earlier "do not use Azure Document Intelligence for this path" decision
  below was about the layout/table-extraction Document Intelligence product,
  not this OCR-only Computer Vision Read call; that decision is unchanged and
  not being revisited here.

### Changed
- Training packet enrichment: Stage 2 section `text` + stronger artifact short_description/retrieval_text; Stage 5/6 packets pass `nearby_text`/`ocr_text` and longer section text (Stage 6 also hydrates empty section text from pages). Artifact linker prefers same `section_id`, penalizes Q&A/lunch slides. Stage 5/6 prompts require named fields/outcomes and ban Q&A slide evidence. Re-prepare Stage 2 then regen Stage 5–6 (+ shared 6.5–10) for Day 1/2 to apply.
- Stage 5/6 prompts: ban training-study fluff (“from the training material,” “record that the source says,” expected_result = “documented intent captured”). Require live surface naming (SSMS / Helix DB / Robotics module / API Dog), observable expected results; prefer `diagnostic` + `L2_support` for DB/API interpretation. Existing Day 2 outputs need Stage 5–6 regen to pick this up.
- Stage 6 finalization emits taxonomy-constrained `capability_tags` / `access_surface` / `audience_roles` / `failure_pattern_tags` (prompts + normalize + SME review MD/HTML). Runtime appends taxonomy IDs via `shared_pipeline_stages/stage_prompts.py`.
- Backfill: `shared_pipeline_stages/scripts/backfill_runbook_capability_tags.py` tagged existing Stage 6 finalized runbooks (incl. `active_agv_error_query_1`) and regenerated reviews.
- Stage 5 discovery/backfill: clarify that **source-backed WCS/SSMS/DB diagnostics are valid candidates** (do not invent SQL; operator has no DB access — use L1/L2). Deterministic placeholder backfill `_role_from_title` now maps SQL/SSMS/database/query titles to `L2_support` (and Event Viewer/API/Ignition to `L1_support`) instead of defaulting to `operator`.
- Aligns operational placeholder creation with the locked role/component access matrix and Day 2 SSMS training content. See `docs/design_decisions/stage_8_capability_tags_and_linking_plan.md` and `docs/design_decisions/stage_5_8_c2_b2_b1_changelog.md`.

### Added
- Stage 1 source bundle extraction for the OptiSweep Operation and Maintenance Manual.
- Stage 2 source artifact and image extraction with artifact reports and priority figure checks.
- Stage 3 Azure AI Foundry source artifact enrichment with descriptions, tags, what-to-look-at guidance, and retrieval text.
- Stage 4 operational context extraction scaffolding for reusable context records.
- V1 training video bundle builder for video plus external VTT transcript inputs.
- Training video slide-segment normalization with cropped frame artifacts and timestamped transcript alignment.
- CLI entrypoint for building local training video source artifacts and slide segment records.
- Training video extraction preparation stage that emits a source-bundle-compatible shape for shared Stage 4 and Stage 5 reuse.
- Local Tesseract OCR-assisted training video segmentation with inspection outputs and quality gates.

### Changed
- README current-stage guidance now reflects the implemented ingestion stages.

### Decisions
- Keep this repo focused on local ingestion and data quality before database writes.
- Use one future LangGraph pipeline with multiple stage nodes.
- Keep source artifact enrichment separate from operational context, runbooks, workflows, and relationship linking.
- Training video ingestion should normalize video evidence first; Stage 4 context extraction and Stage 5 runbook candidate discovery should run afterward through the main pipeline.
- Avoid separate semantic extractors for video unless the shared Stage 4/5 packet model proves insufficient.
- Use local Tesseract OCR for training video slide-change assistance; do not use Azure Document Intelligence for this path.
