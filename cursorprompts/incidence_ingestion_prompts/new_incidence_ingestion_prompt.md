<!--
Incidence pipeline stage-contract planning prompt.
Defines source-specific Stages 1-11, shared finalization stages, downstream
input contracts, and the file-header convention for scripts, src, and prompts.
-->

# OptiSweep Incidence Ingestion Pipeline Planning Prompt

We are designing the OptiSweep incidence ingestion pipeline from scratch.

This is not a Codex implementation prompt yet. This is a planning prompt to help us reason through the correct architecture, stage boundaries, outputs, dependencies, and build sequence before creating implementation tasks.

## Project Context

The OptiSweep AI Support Assistant has two sibling ingestion pipelines:

1. Operational knowledge ingestion
   Sources include manuals, training videos, training transcripts, SOPs, slides, and stable documentation.

2. Incidence knowledge ingestion
   Sources include Salesforce cases, Teams chats, RCA PDFs, support screenshots, logs, attachments, and incident evidence packages.

These two pipelines should be separate during source-specific extraction but should converge later into shared finalization stages.

Operational sources generally tell us:

```text
What should be done.
```

Incident sources generally tell us:

```text
What was actually done.
```

The long-term goal is to combine both into reusable, source-grounded, reviewable support knowledge for RAG, runbooks, workflows/playbooks, escalation, and future knowledge graph relationships.

## Core Architecture Principle

Do not treat raw source evidence as final truth.

Do not treat one incident as a validated universal workflow.

However, for the current MVP/demo stage, we may create a draft workflow/playbook from one incident so we can test guided troubleshooting, runtime UX, evidence display, and escalation behavior.

The distinction is:

```text
Current state:
One incident -> draft incident-derived workflow/playbook candidate

Future state:
Multiple incidents + manuals + SOPs + SME review -> canonical workflow/playbook
```

A single-incident workflow is allowed right now, but it must be clearly marked as:

```text
draft
needs_sme_review
single_incident_case
demo_or_review_only
not_canonical
not approved for general runtime use
```

## Current Operational Pipeline Pattern

The operational knowledge pipeline follows this pattern:

```text
Stage 1: Source bundle extraction
Stage 2: Source artifact and image extraction
Stage 3: Source artifact enrichment
Stage 4: Operational context extraction
Stage 5: Runbook candidate discovery
Stage 6: Candidate pool generation
Stage 7: Canonical runbook drafting and merging
Stage 8: Relationship linking
Stage 9: Validation and repair
Stage 10: Final output writing
Stage 11: Vector embedding generation
Stage 12: LangGraph orchestration / publishing later
```

The incident pipeline should reuse this pattern where it makes sense, especially:

```text
source lineage
source refs
deterministic JSON reading/writing
stable ID generation
artifact records and image refs
artifact enrichment patterns
operational context extraction packet patterns
runbook candidate schema shape
candidate pool format
canonical runbook Markdown + JSON review pattern
relationship linking patterns
validation and extraction report patterns
```

However, the incident pipeline must not copy manual-specific assumptions such as manual sections, figure numbers, manual-only source types, or manual priority checks.

## Incidence Pipeline Purpose

The incidence pipeline converts incident evidence packages into structured, reviewable knowledge assets.

The first seed incident is Case 228086.

Case 228086 includes evidence such as:

```text
Teams chat screenshots
Salesforce or RCA-style case evidence
HMI / web application fault screenshots
memory trend screenshots
RMS screenshots
Ignition restart command screenshots
Ignition status/performance screenshots
API client / API Dog screenshots
Windows Services screenshots
support discussion around restart, validation, and escalation
```

The pipeline must preserve exact source evidence and avoid inventing details.

It should extract what is actually supported by the incident packet.

## Important Case 228086 Grounding

Case 228086 should be treated as the first seed case for proving the incident pipeline can extract detailed recovery procedures from original case evidence instead of relying only on compressed normalized summaries.

The incident evidence appears to support the following kinds of information:

```text
AGVs not moving
heartbeat issue mentioned in chat
question marks on HMI
possible Ignition crash discussion
RDP / remote access discussion
24-hour Ignition Server memory snapshot request
memory trend screenshot
CPU trend / uptime check suggestion
Ignition restart using gwcmd -r
waiting for Ignition to come back up
verifying OptiSweep service/API response after restart
restarting OptiSweep Windows service if no response
confirming by sending another request
releasing E-stop after confirmation
RMS or AGV state correction evidence if source-supported
infrastructure follow-up for memory/log sizing if source-supported
```

Do not infer unsupported details such as:

```text
hostnames
server names
URLs
service names beyond what appears in source evidence
commands beyond what appears in source evidence
API endpoints beyond what appears in source evidence
root cause beyond what is explicitly supported
access paths not shown in the incident
exact downtime unless calculable from source timestamps
```

## Duplicate Image Strategy

Do not delete duplicate or blown-up images from the raw source package.

Raw source evidence must remain untouched for auditability.

However, extracted source artifacts should deduplicate or group near-duplicate images.

For example, the same memory trend may appear:

```text
inline in a Teams message
as a zoomed image
inside a longer instruction post
```

The pipeline should:

```text
keep all raw evidence
extract meaningful images as artifacts
detect duplicate or near-duplicate screenshots
choose the clearest / highest-OCR-confidence version as the primary artifact
retain duplicate references for lineage
send only the primary artifact to the LLM unless duplicates contain unique surrounding context
record duplicate grouping in source_artifacts.json or artifact_enrichment_report.json
```

The goal is to reduce LLM noise without losing traceability.

## High-Level Source-Specific Incident Pipeline

The incidence pipeline should be source-specific through its first set of stages.

Recommended source-specific stages:

```text
Stage 1: Incident source package loading
Stage 2: OCR and evidence artifact extraction
Stage 2.5: Artifact enrichment packet preparation
Stage 3: Incident artifact enrichment
Stage 4: Create canonical incident records and timeline
Stage 5: Incident operational context extraction
Stage 6: Incident runbook candidate discovery
Stage 7: Draft incident-derived workflow/playbook discovery
Stage 8: Candidate pool contribution
Stage 9: Source-specific validation and extraction report
Stage 10: Source-specific final output writing
```

For v1, we may build only the core subset first:

```text
Stage 1: Incident source package loading
Stage 2: OCR and evidence artifact extraction
Stage 2.5: Artifact enrichment packet preparation
Stage 3: Incident artifact enrichment
Stage 4: Create canonical incident records and timeline
Stage 5: Incident operational context extraction
Stage 6: Incident runbook candidate discovery
Stage 7: Draft incident-derived workflow/playbook creation
Stage 9: Source-specific validation and extraction report
```

This lets us create a usable draft workflow from Case 228086 now without pretending it is canonical.

## Shared Finalization Pipeline

After source-specific operational and incident extraction, both pipelines feed shared finalization.

Recommended shared stages:

```text
Shared Stage 6: Unified candidate pool generation
Shared Stage 7: Canonical runbook drafting and merging
Shared Stage 8: Canonical workflow/playbook synthesis
Shared Stage 9: Relationship linking
Shared Stage 10: Validation and repair
Shared Stage 11: Final reviewed output writing
Shared Stage 12: Embedding generation / publishing later
Shared Stage 13: Knowledge graph relationship generation later
```

The exact numbering can be refined later, but the dependency order matters.

## Critical Dependency Rule

There are two workflow types in this system:

```text
Draft incident-derived workflow/playbook
= created from one incident for demo, review, and runtime prototyping

Canonical workflow/playbook
= created after shared runbook merging, broader evidence review, and SME approval
```

Draft incident-derived workflows may temporarily reference runbook candidate IDs.

Canonical workflows should reference stable canonical procedure IDs.

Correct current-state dependency chain:

```text
Case 228086
        ↓
canonical incident record
        ↓
timeline events
        ↓
incident runbook candidates
        ↓
draft incident-derived workflow/playbook
        ↓
demo/review workflow
```

Correct future-state dependency chain:

```text
Operational runbook candidates
Incident runbook candidates
        ↓
Shared candidate pool
        ↓
Canonical runbook drafting / merging
        ↓
Canonical procedure library
        ↓
Canonical workflow/playbook synthesis
        ↓
Workflow nodes reference canonical procedure IDs
```

The draft workflow is useful now for UX testing, demo validation, and stakeholder review.

It must not be promoted as canonical until later.

## Runbook Candidate vs Canonical Runbook

A runbook candidate is a source-specific extraction output.

It says:

```text
This source appears to contain a reusable procedure.
```

A canonical runbook is a finalized, merged, reviewable procedure.

It says:

```text
This is the reusable procedure we want the support assistant to reference, display, and eventually use inside workflows.
```

Runbook candidates can come from:

```text
manuals
training videos
training transcripts
incident cases
SOPs
SME-authored notes
```

Canonical runbooks are created after cross-source review and merging.

No single source owns a canonical runbook.

Each source contributes evidence.

## Incident Runbook Candidate Rules

Incident-derived runbook candidates should answer:

```text
What reusable diagnostic, recovery, verification, or evidence-gathering procedure was actually performed or clearly recommended in the incident?
```

They should not create polished final runbooks.

They should not include trigger conditions.

They should not include routing logic.

They should not include ML labels.

They should not infer root cause unless explicitly supported.

They should not infer that an action resolved the issue unless the incident clearly supports that sequence.

Every incident-derived runbook candidate should default to:

```text
candidate_status: needs_review
source_quality: incident_case
confidence: medium or low unless evidence is very clear
```

Allowed procedure types:

```text
operation
diagnostic
recovery
reference
```

Allowed roles:

```text
operator
L1_support
L2_support
L3_support
```

Incident evidence involving remote access, services, logs, server checks, APIs, RMS correction, Ignition gateway restart, or Windows Services should usually be L2_support or L3_support unless the source clearly shows it is safe for lower support.

## Draft Incident-Derived Workflow Rules

Right now, we are creating workflows from one incident.

That is allowed for MVP/demo purposes.

However, these workflows must be treated as draft incident-derived workflows, not canonical workflows.

A draft incident-derived workflow says:

```text
This incident appears to contain a reusable troubleshooting sequence that may be useful for demo, review, and future canonical workflow synthesis.
```

It does not say:

```text
This is an approved workflow.
```

Draft incident-derived workflows may reference:

```text
timeline_event_ids
runbook_candidate_ids
artifact_ids
source_refs
canonical_incident_record_id
```

They should include guardrails such as:

```json
{
  "workflow_status": "draft",
  "validation_status": "needs_sme_review",
  "source_quality": "single_incident_case",
  "source_case_ids": ["228086"],
  "execution_scope": "demo_or_review_only",
  "canonicalization_status": "not_canonical",
  "requires_sme_approval_before_runtime": true,
  "observed_sequence_only": true,
  "do_not_treat_as_validated_workflow": true,
  "requires_canonical_runbook_mapping": true
}
```

A draft workflow node may temporarily reference a runbook candidate:

```json
{
  "node_id": "restart_ignition_gateway",
  "node_type": "procedure_candidate",
  "title": "Restart Ignition Gateway",
  "runbook_candidate_ref": "candidate_incident_228086_restart_ignition_gateway",
  "procedure_ref": null,
  "mapping_status": "candidate_only",
  "status": "draft"
}
```

Later, after shared canonical runbook drafting and merging, that node should be remapped:

```json
{
  "node_id": "restart_ignition_gateway",
  "node_type": "procedure",
  "title": "Restart Ignition Gateway",
  "runbook_candidate_ref": "candidate_incident_228086_restart_ignition_gateway",
  "procedure_ref": "proc_restart_ignition_gateway_v1",
  "mapping_status": "mapped_to_canonical",
  "status": "draft_needs_review"
}
```

The workflow schema should support both temporary candidate refs and future canonical procedure refs.

## Final Canonical Workflow/Playbook Rules

Final canonical workflows/playbooks should be created only after shared canonical runbook drafting and merging.

Final workflow/playbook nodes should reference:

```text
canonical procedure IDs
canonical operational context IDs
approved source artifacts
validated evidence refs
```

They should not directly reference raw incident runbook candidates as executable steps.

A final workflow node may look like:

```json
{
  "node_id": "verify_optisweep_api_response",
  "node_type": "procedure",
  "procedure_ref": "proc_verify_optisweep_api_response_v1"
}
```

A final workflow may still preserve lineage back to incident candidates through metadata:

```json
{
  "source_playbook_candidate_refs": [
    "playbook_candidate_incident_228086_service_recovery_sequence"
  ],
  "source_runbook_candidate_refs": [
    "candidate_incident_228086_verify_optisweep_api_response"
  ],
  "source_refs": [
    "case_228086:page_17",
    "case_228086:page_18"
  ]
}
```

## Canonical Incident Record Role

The canonical incident record is the incident-level summary.

It is not a runbook, workflow, or timeline.

It should summarize one incident in a concise, searchable, source-grounded way.

It should include:

```text
incident_id
source_case_id
title
customer
site
status
validation_status
reported_at
resolved_at
resolution_time or downtime_minutes
kpi_confidence
people or roles involved
symptoms
incident_description
customer_operational_impact
systems_involved
what_resolved_it
follow_up_required
support_boundary
source_refs
retrieval_text
```

It must include either a real resolution_time value or downtime_minutes.

If exact timestamps are unavailable, use a source-grounded fallback such as same_day and record a warning in the extraction report.

Do not include:

```text
issue category
ML labels
routing confidence
workflow branches
detailed step-by-step instructions
full timeline events
invented timestamps
invented people
invented service names
invented commands
invented RMS screens
```

## Timeline Event Role

Timeline events preserve incident sequence.

They are one of the most important sources for later workflow/playbook creation.

Timeline events should capture:

```text
what happened
when it happened if source timestamp is visible
who or what role acted if visible
what symptoms were observed
what diagnostic checks were performed
what actions were taken
what outcome followed
what evidence supports the event
what artifact IDs are related
```

Timeline events are not runbooks.

They are historical evidence.

They help us understand ordering, causality, uncertainty, and recovery sequence.

## Artifact Extraction Requirements

Incident PDFs are image-heavy and chat-heavy.

Stage 2 must be stronger than the manual pipeline.

It should not rely only on parsed PDF text.

It should use OCR and visual extraction heavily.

Stage 2 should produce:

```text
page inventory
full-page render references
cropped meaningful screenshots
OCR text
detected Teams chat pages
detected Salesforce/case pages
detected HMI screenshots
detected RMS screenshots
detected command window screenshots
detected Ignition screenshots
detected API client screenshots
detected Windows Services screenshots
duplicate/near-duplicate image groups
artifact extraction report
```

Every page should be inventoried, but not every page should become a meaningful source artifact.

Only meaningful screenshots, cropped evidence regions, charts, logs, command windows, tables, and reusable support evidence should become artifact records.

## Artifact Enrichment Packet Requirements

Stage 2.5 prepares artifact enrichment packets. It does not perform artifact enrichment.

Stage 2.5 must not consume `source_artifacts.json` by itself.

Before LLM enrichment, build a deterministic joined enrichment packet from:

```text
source_artifacts.json: clean artifact images, artifact OCR, artifact IDs
page_inventory.json: full-page OCR, Teams/Salesforce surrounding text, page refs
incident_source_package.json: source/package metadata and page-to-artifact links
```

The cropped or nested image is the visual artifact.

The Teams/Salesforce surrounding text is page evidence and context, not part of the image file.

Do not bake surrounding context into the cropped image.

Do preserve surrounding context in page OCR.

Do join image + page OCR in Stage 2.5 enrichment packets.

Do preserve `source_refs` linking every later claim back to page and artifact evidence.

Recommended Stage 2.5 packet shape:

```json
{
  "artifact_id": "artifact_incident_228086_page_007_nested_image_01",
  "image_path": "images/embedded/artifact_incident_228086_page_007_nested_image_01.png",
  "artifact_ocr_text": "Memory Trend ...",
  "artifact_image_type": "memory_trend_screenshot",
  "page_number": 7,
  "page_ocr_text": "Zane Bubb 2/20 9:17 AM ... Michael Langley ... No indication here that memory caused a crash ...",
  "context_role": "surrounding_teams_chat",
  "source_refs": [],
  "instruction": "Enrich the image using the image plus page OCR context, but do not describe surrounding chat as part of the image."
}
```

Stage 2.5 should write these deterministic packets to:

```text
artifact_enrichment_packets.json
```

## Artifact Enrichment Requirements

Incident artifact enrichment should not merely describe the image.

Stage 3 should read `artifact_enrichment_packets.json`, not infer context from image files alone.

Stage 3 should use an explicit artifact enrichment prompt and an LLM/image-capable model when available.

It should identify the artifact’s role in the incident.

Artifact enrichment should answer:

```text
What does this artifact show?
What incident evidence does it provide?
Is it symptom evidence, diagnostic evidence, action evidence, validation evidence, escalation evidence, duplicate context, or unknown?
Does it support a runbook candidate?
Does it support a timeline event?
Does it support the canonical incident record?
Is it a primary artifact or duplicate artifact?
What should a reviewer look at?
What OCR text or visible UI text is important?
```

Artifact enrichment should preserve raw OCR text and source refs.

Do not invent visual details.

If OCR is uncertain, record uncertainty.

## Source Lineage Rules

Every output record must preserve source lineage.

This includes:

```text
source_id
source_type
source_case_id
source_title
ingestion_batch_id
source_refs
evidence_source_refs
related_artifact_ids
page numbers where available
timestamps where visible
OCR confidence where applicable
duplicate group IDs where applicable
```

Source lineage must never be removed during later stages.

## Downstream Structured Knowledge Input Contracts

Stages 4 and later must build structured datasets from the joined source bundle, not from one file in isolation.

The required upstream inputs are:

```text
incident_source_package.json.source_bundle: compact handoff with source metadata, page OCR, artifact manifest, wrapper context, duplicate groups, and detail file refs
page_inventory.json: authoritative full-page OCR and surrounding Teams/Salesforce/case context
source_artifacts.json: clean visual artifact records, artifact OCR, artifact IDs, image paths, duplicate roles
artifact_enrichment_packets.json: joined artifact + page OCR context packets from Stage 2.5
artifact_enrichment_packet_report.json: Stage 2.5 packet quality warnings and duplicate context
source_artifacts_enriched.json: Stage 3 image-specific enriched evidence, separated into visual observations and contextual interpretation
artifact_extraction_report.json / artifact_enrichment_report.json: quality warnings, uncertainty, duplicate notes, validation hints
```

Later stages should apply these precedence rules:

```text
Canonical incident record:
  Primary input: incident_source_package.source_bundle and page_inventory OCR.
  Supporting input: source_artifacts_enriched for evidence support.
  Do not derive incident facts only from image captions when page OCR has richer case/chat context.

Timeline events:
  Primary input: page_inventory OCR, especially Teams timestamps, Salesforce comments, and visible case status updates.
  Supporting input: source_artifacts_enriched when a message includes, requests, or discusses a screenshot.
  Every event should keep page refs and artifact refs when available.

Incident operational context:
  Primary input: page OCR plus enriched artifacts.
  Extract systems, tools, roles, commands, symptoms, validation checks, and uncertainty only when source-supported.

Runbook candidates:
  Primary input: page OCR plus source_artifacts_enriched.
  A candidate step needs source support from text, image, or both.
  Preserve whether the support came from surrounding context, visual artifact, or both.

Draft incident-derived workflow/playbook:
  Primary input: timeline events and runbook candidates.
  Supporting input: canonical incident record and enriched artifacts.
  Must remain draft, single-incident, review-only, and not canonical.

Candidate pool contribution:
  Primary input: runbook_candidates.json.
  Supporting input: enriched artifacts, timeline links, and source refs.
  Must preserve incident provenance and review status.

Validation/reporting:
  Validate every claim against source_refs, page refs, artifact refs, OCR confidence, duplicate metadata, and uncertainty notes.
```

Each structured record should include enough lineage to reconstruct why it exists:

```text
source_refs
page_refs
related_artifact_ids
related_enriched_artifact_ids
timeline_event_ids where applicable
runbook_candidate_ids where applicable
evidence_support_type: page_ocr | artifact_visual | artifact_ocr | joined_context | mixed
confidence or uncertainty fields
unsupported_or_missing_detail_notes
```

## Expected Source-Specific Incident Outputs

For each incident package, the pipeline should eventually produce:

```text
incident_source_package.json
source_artifacts.json
artifact_enrichment_packets.json
source_artifacts_enriched.json
canonical_incident_record.json
timeline_events.json
operational_context.json
runbook_candidates.json
draft_incident_workflow.json
candidate_pool_contribution.json
extraction_report.json
images/
```

For v1, it is acceptable to produce:

```text
incident_source_package.json
source_artifacts.json
artifact_enrichment_packets.json
source_artifacts_enriched.json
canonical_incident_record.json
timeline_events.json
runbook_candidates.json
draft_incident_workflow.json
extraction_report.json
images/
```

## Draft Incident Workflow Schema Direction

The draft incident workflow schema should support temporary runbook candidate references now and canonical procedure references later.

Recommended shape:

```json
{
  "workflow_id": "draft_workflow_incident_228086_service_recovery_v1",
  "title": "Draft OptiSweep Service Recovery Workflow From Case 228086",
  "workflow_type": "draft_incident_derived_playbook",
  "source_case_ids": ["228086"],
  "source_quality": "single_incident_case",
  "workflow_status": "draft",
  "validation_status": "needs_sme_review",
  "execution_scope": "demo_or_review_only",
  "canonicalization_status": "not_canonical",
  "requires_sme_approval_before_runtime": true,
  "observed_sequence_only": true,
  "do_not_treat_as_validated_workflow": true,
  "requires_canonical_runbook_mapping": true,
  "nodes": [
    {
      "node_id": "",
      "node_type": "question | procedure_candidate | validation | escalation | terminal",
      "title": "",
      "instruction": "",
      "runbook_candidate_ref": "",
      "procedure_ref": null,
      "mapping_status": "candidate_only | mapped_to_canonical | unmapped",
      "role_required": "operator | L1_support | L2_support | L3_support",
      "timeline_event_refs": [],
      "artifact_refs": [],
      "source_refs": [],
      "next_node_rules": [],
      "escalation_conditions": [],
      "notes": ""
    }
  ],
  "source_runbook_candidate_refs": [],
  "timeline_event_refs": [],
  "artifact_refs": [],
  "source_refs": [],
  "metadata": {
    "created_by": "incident_workflow_candidate_discovery_agent",
    "created_from": "single_incident_case",
    "future_required_step": "remap_nodes_to_canonical_procedure_ids_after_shared_stage_7"
  }
}
```

## Build Strategy

Start with deterministic scripts and local JSON outputs.

Do not start with full LangGraph orchestration.

Do not start with Cosmos publishing.

Do not start with embeddings.

Do not start with knowledge graph generation.

Build the local pipeline first, then wrap stages as LangGraph nodes after the stage contracts are stable.

Recommended first CLI shape:

```bash
python scripts/extract_incident_knowledge.py \
  --source-pdf "data/input/incidents/Case 228086.pdf" \
  --case-id 228086 \
  --source-title "Case 228086 - UPS Haslet OptiSweep Incident" \
  --output-dir data/output/incidents/case_228086 \
  --llm
```

The script should be able to run stage-by-stage as the pipeline matures.

## Stage Numbering And File Header Convention

From this point forward, every incidence pipeline script, source module, and prompt file should declare its stage ownership near the top of the file.

Stage-owned files should include:

```text
Stage number
Stage name
Brief file purpose
Primary inputs and outputs when practical
```

Shared helper files should not pretend to belong to one stage. Instead, they should declare:

```text
Stage support scope, such as "Stages 1-2 support" or "All incident stages support"
Brief file purpose
Main records or utilities they affect
```

Prompt files should include stage numbers in their prompt title or opening note.

Script and source comments/docstrings should be brief but explicit, so a reader can tell which stage a file belongs to before reading implementation details.

## Recommended Plan Of Attack

### Step 1 — Define folder structure and output contracts

Decide final local folder structure for incidenceknowledgeingestion.

Define JSON schemas for:

```text
incident_source_package
incident_source_artifact
canonical_incident_record
timeline_event
incident_operational_context
incident_runbook_candidate
draft_incident_workflow
incident_extraction_report
```

Keep schemas simple.

Avoid overengineering.

### Step 2 — Build Stage 1 source package loader

Goal:

```text
Load the incident PDF and create a stable source package inventory.
```

Output:

```text
incident_source_package.json
```

Include:

```text
case_id
source title
source file path
page count
source type
ingestion batch ID
page records
page refs
basic parsed text if available
rendered page image refs if produced
```

### Step 3 — Build Stage 2 OCR and artifact extraction

Goal:

```text
Extract page images, OCR text, meaningful cropped evidence artifacts, and duplicate groups.
```

Output:

```text
source_artifacts.json
artifact_extraction_report.json
images/
```

Initial implementation can be simple:

```text
render each page
OCR each page
save full-page artifact for review
detect embedded image regions where possible
crop large visual regions
mark likely artifact type with rules
dedupe near-identical images
```

For Case 228086, make sure Stage 2 can identify:

```text
Teams chat pages
HMI question-mark screenshots
memory trend charts
RMS screenshot
Ignition command prompt screenshot
Ignition status/performance screenshot
API client screenshot
Windows Services OptiSweep screenshot
```

### Step 4 — Build Stage 2.5 artifact enrichment packet preparation

Goal:

```text
Build deterministic joined packets for Stage 3 artifact enrichment.
```

Output:

```text
artifact_enrichment_packets.json
artifact_enrichment_packet_report.json
```

Stage 2.5 should join:

```text
source_artifacts.json
page_inventory.json
incident_source_package.json
```

into `artifact_enrichment_packets.json`.

Each packet should include:

```text
artifact_id
image_path
artifact_ocr_text
artifact_image_type
artifact summary/type/role hints from Stage 2
page_number
page_ref
page_ocr_text
context_role, such as surrounding_teams_chat, surrounding_salesforce_case, same_page_context, or no_page_context
source_refs
duplicate group metadata
instruction telling the LLM to use page OCR as context without treating surrounding chat/case text as part of the image
```

### Step 5 - Build Stage 3 artifact enrichment

Goal:

```text
Use the LLM to enrich artifact packets into reviewable incident evidence artifacts.
```

Output:

```text
source_artifacts_enriched.json
artifact_enrichment_report.json
```

Stage 3 should enrich artifacts from `artifact_enrichment_packets.json` using the Stage 3 artifact enrichment prompt.

The enriched artifact should distinguish:

```text
visual_observations: what is actually visible in the cropped image
contextual_interpretation: what surrounding page OCR says about the image or incident
source_supported_claims: claims tied to source_refs
uncertainties: OCR/visual/context uncertainty
```

Later stages should consume different parts of the bundle:

```text
Artifact enrichment: image-specific output plus page OCR context
Canonical incident record: page_inventory and incident_source_package first, enriched artifacts as evidence support
Timeline events: page OCR first, especially Teams timestamps/messages, with linked artifacts when a message includes or discusses a screenshot
Runbook candidates: page OCR plus enriched artifacts, so steps are grounded in both text around screenshots and screenshots themselves
```

The enrichment should produce:

```text
artifact summary
evidence role
retrieval text
what_to_look_at
OCR highlights
duplicate grouping notes
review uncertainty
candidate support hints
```

### Step 6 — Build Stage 4 create canonical incident records and timeline

Goal:

```text
Create one concise incident record and source-grounded timeline for Case 228086.
```

Output:

```text
canonical_incident_record.json
canonical_incident_record_extraction_report.json
timeline_events.json
timeline_event_extraction_report.json
```

Use the already-created canonical incident record prompt as the planning baseline.

Inputs:

```text
incident_source_package.json.source_bundle
page_inventory.json
source_artifacts_enriched.json
artifact_enrichment_report.json
```

Use page OCR and source bundle text as the primary source of incident facts.

Use enriched artifacts as supporting evidence, not as the only source of incident facts.

The canonical incident record should preserve:

```text
source_refs
page_refs
supporting_artifact_ids
supporting_timeline_event_ids when available
evidence_support_type
uncertainty notes
unsupported or missing detail notes
```

The record should include resolution_time or downtime_minutes.

If exact timing cannot be calculated, use a source-grounded fallback and write a warning.

Stage 4 timeline extraction should:

Goal:

```text
Extract the incident sequence from Teams chat, screenshots, and case evidence.
```

Output:

```text
timeline_events.json
timeline_event_extraction_report.json
```

Inputs:

```text
incident_source_package.json.source_bundle
page_inventory.json
source_artifacts_enriched.json
```

Use page OCR as the primary timeline source.

Use enriched artifacts when a page message includes, requests, discusses, validates, or depends on a screenshot.

This should preserve visible timestamps, action ordering, artifact refs, and uncertainty.

### Step 7 - Build Stage 5 incident operational context extraction

Goal:

```text
Extract structured operational context from the incident without turning it into a runbook.
```

Output:

```text
operational_context.json
operational_context_extraction_report.json
```

Inputs:

```text
incident_source_package.json.source_bundle
page_inventory.json
source_artifacts_enriched.json
timeline_events.json
canonical_incident_record.json
```

The operational context should capture source-supported:

```text
systems and tools mentioned
symptoms and observed states
commands and exact command evidence
services and applications mentioned
roles or actors when visible
validation checks
remote access or escalation context
uncertainty and missing details
source_refs, page_refs, and artifact_refs
```

Do not infer hostnames, URLs, service names, root cause, access paths, or responsibilities unless the source explicitly supports them.

### Step 8 - Build Stage 6 incident runbook candidate discovery

Goal:

```text
Extract source-grounded reusable procedure candidates from the incident.
```

Possible Case 228086 candidates if supported by evidence:

```text
Check Ignition memory trend
Check CPU trend or uptime after suspected Ignition crash
Restart Ignition Gateway using source-backed command evidence
Wait for Ignition Gateway to become available after restart
Verify OptiSweep service/API response after Ignition restart
Restart OptiSweep Windows service if API response is unavailable
Confirm recovery by sending another request
Release E-stop after service response is confirmed
Correct AGV state in RMS if the source provides enough detail
```

Output:

```text
runbook_candidates.json
runbook_candidate_extraction_report.json
```

Inputs:

```text
incident_source_package.json.source_bundle
page_inventory.json
source_artifacts_enriched.json
timeline_events.json
canonical_incident_record.json
operational_context.json
```

Each runbook candidate and step must identify whether its support came from:

```text
page OCR
artifact visual evidence
artifact OCR
joined page+artifact context
timeline ordering
```

Do not turn a single incident into a final general procedure.

Do not create final canonical runbooks here.

### Step 9 - Build Stage 7 draft incident-derived workflow creation

Goal:

```text
Create a draft workflow/playbook from Case 228086 for demo, review, and runtime prototyping.
```

Output:

```text
draft_incident_workflow.json
draft_incident_workflow_extraction_report.json
```

Inputs:

```text
canonical_incident_record.json
timeline_events.json
runbook_candidates.json
operational_context.json
source_artifacts_enriched.json
incident_source_package.json.source_bundle
```

This workflow may reference runbook candidate IDs temporarily.

It must include:

```text
workflow_status: draft
validation_status: needs_sme_review
source_quality: single_incident_case
execution_scope: demo_or_review_only
canonicalization_status: not_canonical
requires_sme_approval_before_runtime: true
observed_sequence_only: true
do_not_treat_as_validated_workflow: true
requires_canonical_runbook_mapping: true
```

It should preserve:

```text
timeline_event_refs
runbook_candidate_refs
artifact_refs
source_refs
role_required
escalation conditions
validation nodes
uncertainty notes
```

### Step 10 - Build candidate pool contribution

Goal:

```text
Prepare incident runbook candidates to enter the shared candidate pool.
```

Output:

```text
candidate_pool_contribution.json
```

This should be compatible with the operational pipeline’s candidate pool format.

Inputs:

```text
runbook_candidates.json
source_artifacts_enriched.json
timeline_events.json
canonical_incident_record.json
operational_context.json
```

For v1, this can be deferred until runbook candidates are stable.

### Step 11 - Build validation and quality reporting

Goal:

```text
Catch missing source refs, missing OCR, duplicate artifacts, unsupported claims, weak timestamps, invalid schema fields, and workflow status errors.
```

Validation should check structured downstream records against:

```text
incident_source_package.json.source_bundle
page_inventory.json
source_artifacts.json
artifact_enrichment_packets.json
source_artifacts_enriched.json
artifact_extraction_report.json
artifact_enrichment_report.json
```

Output:

```text
extraction_report.json
validation_report.json
```

The report should include warnings such as:

```text
exact downtime could not be calculated
artifact OCR confidence low
duplicate screenshot group detected
runbook candidate references unsupported artifact
timeline event missing timestamp
source text says restart service but exact service name missing
LLM output attempted to infer root cause
draft workflow missing needs_sme_review status
draft workflow node references missing runbook candidate
draft workflow incorrectly marked canonical
```

## Shared Finalization Plan After Source-Specific Extraction

After both operational and incidence pipelines produce runbook candidates:

### Shared Stage 6 — Unified Candidate Pool

Inputs:

```text
operational runbook_candidates.json
incident runbook_candidates.json
SOP runbook_candidates.json later
SME-authored candidates later
```

Output:

```text
candidate_pool.json
```

Responsibilities:

```text
pool candidates
group likely similar candidates
preserve source lineage
do not lose candidate IDs
do not fully merge yet if uncertain
```

### Shared Stage 7 — Canonical Runbook Drafting and Merging

Inputs:

```text
candidate_pool.json
source_artifacts_enriched.json from relevant sources
operational_context.json from relevant sources
existing canonical runbook library if present
```

Outputs:

```text
canonical_runbooks.json
review_markdown/runbooks/*.md
runbook_merge_report.json
candidate_to_procedure_mapping.json
```

Responsibilities:

```text
select best candidates
merge duplicate or complementary candidates
draft canonical runbooks
preserve all source refs
map candidate IDs to canonical procedure IDs
mark review status
```

### Shared Stage 8 — Canonical Workflow/Playbook Synthesis

Inputs:

```text
canonical_runbooks.json
candidate_to_procedure_mapping.json
draft_incident_workflow.json
timeline_events.json
canonical incident records
operational context
source artifacts
existing approved workflow library if present
```

Outputs:

```text
canonical_workflows.json
review_markdown/workflows/*.md
workflow_synthesis_report.json
workflow_candidate_to_canonical_mapping.json
```

Responsibilities:

```text
create draft canonical workflows/playbooks
reference canonical procedure IDs in workflow nodes
remap draft incident workflow nodes from runbook candidate IDs to canonical procedure IDs
preserve source workflow candidate refs
preserve source runbook candidate refs
preserve timeline and incident evidence
do not approve until SME-reviewed
```

### Shared Stage 9 — Relationship Linking

Link:

```text
artifacts ↔ operational context
artifacts ↔ canonical runbooks
canonical runbooks ↔ workflows
incidents ↔ runbooks
incidents ↔ workflows
timeline events ↔ artifacts
timeline events ↔ runbook candidates
components ↔ incidents
systems ↔ procedures
```

### Shared Stage 10 — Validation and Repair

Validate:

```text
schema correctness
source refs
artifact refs
procedure refs
workflow node refs
candidate-to-canonical mappings
unsupported claims
review status
role validity
procedure type validity
workflow canonicalization status
```

### Shared Stage 11 — Final Output Writing

Write:

```text
final canonical runbooks
final canonical workflows/playbooks
review markdown
relationship links
validation reports
runtime-ready datasets later
```

## Design Decisions To Confirm Before Implementation

Before writing Codex prompts, we need to decide:

1. What exact folder structure should incidenceknowledgeingestion use?
2. Should incident stages mirror operational stage numbering or have their own numbering?
3. What minimum JSON schemas do we need for v1?
4. Should Stage 2 create full-page artifacts for every page or only inventory every page and create artifact records only for meaningful regions?
5. What OCR approach should be used locally for v1?
6. How aggressive should image duplicate detection be?
7. Should canonical incident record extraction happen before or after timeline extraction?
8. Should incident operational context be required for v1 or deferred?
9. Should draft workflow creation be included in v1? Current answer: yes, for Case 228086 demo/review only.
10. What exact compatibility contract should candidate_pool_contribution.json follow?
11. What exact workflow node schema should support temporary runbook candidate refs now and canonical procedure refs later?

## Recommended MVP Decision

For the first implementation pass, focus on Case 228086 and build the stages needed to prove the source evidence can become high-quality structured records and a draft review workflow.

Recommended v1 build:

```text
1. Incident source package loader
2. OCR + artifact extraction with duplicate grouping
2.5. Artifact enrichment packet preparation
3. Artifact enrichment
4. Create canonical incident records and timeline
5. Incident runbook candidate discovery
6. Draft incident-derived workflow creation
7. Validation/extraction report
```

Defer:

```text
incident operational context extraction
candidate pool contribution
shared canonical workflow synthesis
relationship linking
embeddings
Cosmos publishing
LangGraph orchestration
```

Reason:

```text
If OCR and artifact enrichment are poor, every later stage will be noisy.
```

The first quality gate should be:

```text
Can we accurately extract the evidence from Case 228086?
Can we identify the useful screenshots?
Can we group duplicates?
Can we create a concise canonical incident record?
Can we create a trustworthy timeline?
Can we extract source-grounded runbook candidates without inventing details?
Can we create a draft incident-derived workflow that is clearly marked as demo/review-only?
```

## Final Architectural Rule

The incidence pipeline produces evidence and draft review workflows.

The operational pipeline produces evidence and runbook candidates.

The shared finalization pipeline produces canonical runbooks and canonical workflows/playbooks.

Single-incident workflows are allowed now for demo and review, but they are not canonical.

Final workflows/playbooks must eventually reference canonical procedure IDs, not raw runbook candidate IDs.

Draft incident-derived workflows may temporarily reference runbook candidate IDs, but they must be remapped after shared canonical runbook drafting and merging.

This keeps the system useful now while preserving the path to a traceable, reviewable, stable architecture later.
