
## Goals
Build a repeatable OptiSweep manual knowledge extraction agent.

The goal is to build a reusable OptiSweep knowledge extraction pipeline.

The pipeline should be capable of ingesting:

- operation and maintenance manuals
- training slide decks
- training transcripts
- incident records
- SOPs
- future SME-authored documentation

All source types should produce the same intermediate knowledge assets:

1. source artifacts
2. operational context records
3. runbook candidates
4. candidate packets (Stage 6)

These intermediate assets remain source-specific through Stage 6.

Stage 5 drafts runbook candidates. Stage 6 finalizes complete source-specific
runbooks with artifacts and context attached.

Cross-source merging is selective at Shared Stage 7 (merge clusters only).
Shared Stages 6.5–8 handle pooling, merging, and playbook linking.

This architecture allows multiple knowledge sources to contribute to the
same runbook without overwriting one another.

## Knowledge Architecture

The ingestion architecture follows a layered model:

Source Knowledge Extraction

Manual
Training Slides
Training Transcript
Incident Data
SME Documentation

        â†“

Source Artifacts

        â†“

Operational Context

        â†“

Runbook Candidates

        ↓

Stage 5 [LLM Assisted]
Draft Runbook Candidates

        ↓

Stage 6 [LLM Assisted]
Finalized Source Runbooks

        ↓

Shared Stage 6.5 [Deterministic]
Runbook Pool + Merge Clusters

        ↓

Shared Stage 7 [LLM Assisted, selective]
Merge Clusters Only

        ↓

Shared Stage 8 [LLM Assisted]
Playbook Linking + Finalization

        ↓

Relationship Linking

        ↓

Validation

Source-specific assets are preserved through Stage 6.

Stage 6 produces finalized source runbooks. Shared Stage 6.5 pools them and
identifies merge clusters. Shared Stage 7 merges only those clusters. Singleton
runbooks pass through without a Stage 7 LLM call.

No single source owns a runbook.

Each source contributes evidence that can strengthen or enrich an
existing runbook.
This should be implemented as one orchestration agent with multiple internal tools and stage-specific prompts.

Do not build multiple independent agents yet.

The user should run one CLI command:

```bash
python scripts/extract_manual_knowledge.py \
  --source-pdf "data/OptiSweep Operation and Maintenance Manual - Final 1.pdf" \
  --output-dir data/generated/manual_optisweep_om_v3 \
  --existing-runbooks data/generated/runbooks/runbook_candidates.json \
  --llm
```

Also support running without existing runbooks:

```bash
python scripts/extract_manual_knowledge.py \
  --source-pdf "data/OptiSweep Operation and Maintenance Manual - Final 1.pdf" \
  --output-dir data/generated/manual_optisweep_om_v3 \
  --llm
```

Create this file structure:

```text
scripts/
  extract_manual_knowledge.py

backend/app/agents/
  manual_knowledge_extraction_agent.py

backend/app/tools/manual_ingestion/
  source_bundle_builder.py
  source_artifact_extractor.py
  artifact_enrichment_tool.py
  operational_context_extractor.py
  runbook_candidate_extractor.py
  runbook_finalization_tool.py
  runbook_pool_builder.py
  runbook_merge_tool.py
  playbook_finalization_tool.py
  relationship_linker.py
  manual_knowledge_validator.py
  extraction_report_writer.py

backend/app/prompts/manual_ingestion/
  master_manual_knowledge_agent_prompt.md
  stage3_artifact_enrichment_prompt.md
  stage4_operational_context_extraction_prompt.md
  stage5_runbook_candidate_discovery_prompt.md
  stage6_runbook_finalization_prompt.md
  stage6_5_runbook_pool_merge_prep_prompt.md
  stage7_runbook_merge_prompt.md
  stage8_playbook_finalization_prompt.md
  stage8_relationship_linking_prompt.md
  stage9_validation_repair_prompt.md

backend/app/schemas/
  source_artifact_schema.py
  manual_reference_schema.py
  operational_context_schema.py
  runbook_schema.py
  extraction_report_schema.py
```

The agent must execute source-specific stages in this order:

```text
1. Build source bundle
2. Extract source artifacts / images / tables
3. Enrich source artifacts
4. Extract operational context
5. Discover runbook candidates
6. Finalize source runbooks
```

Shared finalization runs after every source completes Stage 6:

```text
6.5. Build shared runbook pool and merge clusters [Deterministic]
7. Merge cross-source runbook clusters only [LLM Assisted, selective]
8. Link runbooks to playbooks and finalize playbooks [LLM Assisted]
9. Link artifacts ↔ context ↔ runbooks
10. Validate and repair
11. Write final outputs
```

Stages 1–6 are source-specific. Stages 6.5–8 are shared.

Stage 7 must not run on every runbook. Stage 5 drafts candidates; Stage 6
finalizes them. Stage 7 merges only when Stage 6.5 identifies a merge cluster.

## Important design rules:

Source Traceability Rules

All extracted records must preserve source lineage.

Artifacts, operational context records, runbook candidates, runbooks,
and relationships must include:

- source_id
- source_type
- ingestion_batch_id
- source_refs

Example source types:

- manual
- training_slide
- training_transcript
- incident
- sop
- sme_authored

Source lineage must never be removed during later stages.

This allows multiple sources to contribute evidence to the same
canonical runbook while preserving traceability.

* Images/source artifacts must be extracted before operational context and runbooks.
* linked_context_ids and linked_runbook_ids must remain empty during artifact extraction and enrichment.
* linked_context_ids and linked_runbook_ids should be populated near the end by the relationship linker.
* Runbooks are reusable procedure/instruction records, not workflows or decision trees.
* Do not add trigger conditions, routing logic, ML labels, workflow branches, or signal fields to runbooks.
* Operational context explains what something means.
* Runbooks tell a human what to check, click, inspect, scan, reset, start, stop, or escalate.
* Source artifacts/images visually support screens, fields, faults, metrics, controls, buttons, alarms, or physical inspection targets.
* The script should be deterministic where possible.
* The LLM should only be used for semantic extraction, summarization, candidate discovery, drafting, and repair.
* Do not invent commands, hostnames, service names, SQL, API endpoints, screenshots, page refs, section refs, or access paths.
* Preserve source traceability everywhere.

Use this simple decision rule:

```text
If it explains what something means â†’ operational context.
If it tells a human what to check/do â†’ runbook.
If it visually supports a screen, metric, fault, status, action, or component â†’ source artifact.
If it connects records together â†’ final relationship linking stage.
```

The heartbeat diagnostic is the canonical example.

The manual states that the Operator Station HMI Data screen includes Heartbeat Stats. Last is the most recent signal time between the tipper and WCS. Max is the longest signal time between the tipper and WCS. Min is the shortest signal time. A heartbeat signal longer than 10 seconds can cause tipper operation issues due to mis-synchronization.

That information should produce:

1. A source artifact for the Heartbeat Stats screenshot.
2. An operational context record explaining the heartbeat metrics.
3. A diagnostic runbook telling a user how to check heartbeat stats.
4. Final links connecting the artifact, context, and runbook.

The source artifact should include longer summary and retrieval text, for example:

```json
{
  "artifact_id": "artifact_manual_fig_4_22_heartbeat_stats",
  "artifact_type": "manual_figure",
  "image_type": "hmi_screenshot",
  "title": "Operator Station HMI Data Screen â€” Heartbeat Stats",
  "figure_number": "Figure 4-22",
  "section_id": "manual_4_1_2_2",
  "page": 36,
  "short_description": "Heartbeat statistics section on the Operator Station HMI Data screen.",
  "summary": "This screenshot shows the Heartbeat Stats section of the Operator Station HMI Data screen. It supports checking heartbeat timing between the tipper and WCS. The Last, Max, and Min values represent the most recent, longest, and shortest signal timing values. The Max value is important because heartbeat signals longer than 10 seconds can cause tipper operational issues due to mis-synchronization.",
  "retrieval_text": "Operator Station HMI Data screen heartbeat stats. Use this image when checking heartbeat communication between the tipper and WCS. Fields include Last, Max, Min, and Reset. Max heartbeat over 10 seconds may indicate tipper-to-WCS mis-synchronization risk and possible tipper operational issues.",
  "what_to_look_at": [
    "Heartbeat Stats section",
    "Last value",
    "Max value",
    "Min value",
    "RESET button"
  ],
  "linked_context_ids": [],
  "linked_runbook_ids": [],
  "validation_status": "needs_sme_review"
}
```

The operational context should explain the metric:

```json
{
  "context_id": "ctx_manual_operator_station_heartbeat_stats_v1",
  "record_type": "operational_context",
  "context_type": "hmi_metric_reference",
  "title": "Operator Station Heartbeat Stats",
  "summary": "The Operator Station HMI Data screen includes Heartbeat Stats for signals between the tipper and WCS. Last shows the most recent signal time, Max shows the longest signal time, and Min shows the shortest signal time. A heartbeat longer than 10 seconds can cause tipper operational issues due to mis-synchronization.",
  "retrieval_text": "Heartbeat Stats on the Operator Station HMI Data screen show communication timing between the tipper and WCS. Last is the most recent signal time. Max is the longest signal time. Min is the shortest signal time. A Max heartbeat longer than 10 seconds can indicate mis-synchronization risk and may cause tipper operational issues.",
  "components": ["operator_station", "tipper", "WCS"],
  "systems": ["OptiSweep", "Operator Station HMI", "WCS"],
  "source_refs": [],
  "image_refs": ["artifact_manual_fig_4_22_heartbeat_stats"],
  "related_runbook_ids": [],
  "validation_status": "needs_sme_review"
}
```

The runbook should tell a user how to check it:

```json
{
  "procedure_id": "proc_check_operator_station_heartbeat_stats_v1",
  "title": "Check Operator Station Heartbeat Stats",
  "procedure_type": "diagnostic",
  "summary": "Check heartbeat signal timing between the tipper and WCS on the Operator Station HMI Data screen.",
  "role_required": "operator",
  "support_safe": true,
  "estimated_time_minutes": 3,
  "when_to_use": "Use this when checking whether tipper-to-WCS heartbeat timing may be contributing to tipper operational issues.",
  "access_or_tools_needed": ["Operator Station HMI access"],
  "steps": [
    {
      "step_number": 1,
      "title": "Open the Operator Station Data screen",
      "instruction": "At the Operator Station HMI, press F5 or navigate to the Visu_Data screen.",
      "expected_result": "The Operator Station HMI Data screen is visible.",
      "healthy_condition": "The screen loads and displays data sections including Heartbeat Stats.",
      "failure_condition": "The screen does not load or the heartbeat section is not visible.",
      "actions": [
        {
          "action_type": "hmi_navigation",
          "label": "Open Visu_Data screen",
          "exact_action": "Press F5 on the Operator Station HMI to open the Visu_Data screen.",
          "parameters": [],
          "role_required": "operator",
          "source_refs": []
        }
      ],
      "commands": [],
      "screens_or_images": [
        {
          "artifact_id": "artifact_manual_fig_4_20_operator_station_data_screen",
          "required_for_step": true,
          "what_to_look_at": ["Operator Station HMI Data screen"]
        }
      ],
      "source_refs": []
    },
    {
      "step_number": 2,
      "title": "Review Heartbeat Stats",
      "instruction": "Locate the Heartbeat Stats section and review the Last, Max, and Min values.",
      "expected_result": "Heartbeat timing values are visible in milliseconds.",
      "healthy_condition": "Heartbeat values are updating and Max is not showing a signal longer than 10 seconds.",
      "failure_condition": "Heartbeat values are frozen, missing, or Max indicates a heartbeat signal longer than 10 seconds.",
      "actions": [
        {
          "action_type": "inspection_action",
          "label": "Review heartbeat values",
          "exact_action": "Record the Last, Max, and Min heartbeat timing values shown on the screen.",
          "parameters": ["Last", "Max", "Min"],
          "role_required": "operator",
          "source_refs": []
        }
      ],
      "commands": [],
      "screens_or_images": [
        {
          "artifact_id": "artifact_manual_fig_4_22_heartbeat_stats",
          "required_for_step": true,
          "what_to_look_at": ["Last value", "Max value", "Min value"]
        }
      ],
      "source_refs": []
    }
  ],
  "success_criteria": [
    "Heartbeat Stats are visible.",
    "Last, Max, and Min values can be recorded.",
    "No heartbeat signal longer than 10 seconds is observed."
  ],
  "escalation_guidance": [
    "Escalate if heartbeat values are missing, frozen, or Max shows a signal longer than 10 seconds.",
    "Escalate if the tipper has operational issues and heartbeat timing suggests possible tipper-to-WCS mis-synchronization."
  ],
  "source_refs": [],
  "image_refs": [
    "artifact_manual_fig_4_20_operator_station_data_screen",
    "artifact_manual_fig_4_22_heartbeat_stats"
  ],
  "linked_context_ids": [],
  "validation_status": "needs_sme_review"
}
```

Implement the following outputs:

```text
data/generated/manual_optisweep_om_v3/stage_2_source_artifacts/source_artifacts.json
data/generated/manual_optisweep_om_v3/stage_10_final_outputs/manual_references.json
data/generated/manual_optisweep_om_v3/stage_4_operational_context/operational_context.json
data/generated/manual_optisweep_om_v3/stage_5_runbook_candidates/runbook_candidates.json
data/generated/manual_optisweep_om_v3/stage_10_final_outputs/extraction_report.json
```

Do not write directly to Cosmos yet.

Do not write directly to retrieval tables yet.

This is still a local extraction and validation layer.

Stage details:

## Stage 1: Build Source Bundle

Tool: source_bundle_builder.py

Responsibilities:

* Parse the PDF.
* Extract document metadata.
* Extract table of contents if possible.
* Create section IDs.
* Create page records.
* Extract page text.
* Extract table records.
* Extract figure references/captions.
* Preserve page numbers.
* Preserve section titles.
* Write source_bundle.json.

No LLM required.

Output:

```text
data/processed/manual_optisweep_om_v3/source_bundle.json
```
### Additional Responsibilities

Create source metadata:

{
  "source_id": "",
  "source_type": "",
  "source_title": "",
  "source_version": "",
  "ingestion_batch_id": ""
}

All downstream records should inherit source metadata.

## Stage 2: Extract Source Artifacts

Tool: source_artifact_extractor.py

Responsibilities:

* Extract figures/images from the PDF.
* Assign stable artifact IDs.
* Extract figure number, title, page, section ID.
* Save image files.
* Create initial source_artifacts.json.
* Create manual_references.json.
* Leave linked_context_ids and linked_runbook_ids empty.

No LLM required unless OCR/caption cleanup is needed.

## Stage 3: Enrich Source Artifacts

Tool: artifact_enrichment_tool.py

Prompt: stage3_artifact_enrichment_prompt.md

Responsibilities:

* Add short_description.
* Add longer summary.
* Add retrieval_text.
* Add what_to_look_at.
* Add image_type.
* Add component/system tags if obvious.
* Do not populate linked_context_ids or linked_runbook_ids.
* Do not invent what is not visible or supported by nearby source text.

Input packet should include one artifact, nearby section text, figure caption, OCR text if available, table text if nearby.

## Stage 4: Extract Operational Context

Tool: operational_context_extractor.py

Prompt: stage4_operational_context_extraction_prompt.md

Responsibilities:

* Extract context records that explain systems, screens, metrics, fields, statuses, alarms, components, safety references, and operational concepts.
* Include retrieval_text.
* Include source_refs.
* Include image_refs when supporting artifacts exist.
* Do not create runbooks in this stage.
* Do not create workflow logic.
* Do not create trigger conditions.
* Do not create ML labels.

Context types should stay simple:

```text
system_overview
component_reference
hmi_screen_reference
hmi_metric_reference
alarm_reference
status_reference
safety_reference
glossary
troubleshooting_reference
maintenance_reference
```

## Stage 5: Discover Runbook Candidates [LLM Assisted]

Tool: runbook_candidate_extractor.py

Prompt: stage5_runbook_candidate_discovery_prompt.md

Purpose:

Discover and draft reusable runbook candidates from a single source.

Responsibilities:

* Identify reusable runbook/procedure candidates from the manual.
* Include operation, diagnostic, recovery, and reference procedures.
* Include metric-check procedures like heartbeat stats, operator stats, process status, IO diagnostics, alarms, AGV status, tote task, hospital status fields, etc.
* Draft candidate content: title, goal, rough steps, procedure type, role, source refs.
* Preserve source lineage.
* Do not merge or normalize candidates.
* Do not attach full artifact payloads yet (Stage 6 does that).
* Do not finalize full runbooks yet (Stage 6 does that).
* Do not create workflow logic.
* Do not create trigger conditions.

Output:

```text
runbook_candidates.json
```

Candidate output should include:

```json
{
  "candidate_id": "",
  "candidate_title": "",
  "candidate_goal": "",
  "likely_procedure_type": "",
  "likely_role_required": "",

  "source_id": "",
  "source_type": "",

  "source_section_ids": [],
  "artifact_ids": [],
  "related_context_ids": [],

  "rough_steps": [],
  "source_grounded_values": [],

  "evidence_source_refs": [],

  "confidence": ""
}
```

## Stage 6: Source Runbook Finalization [LLM Assisted]

Tool:
runbook_finalization_tool.py

Prompt:
stage6_runbook_finalization_prompt.md

This stage runs independently inside each source ingestion pipeline.

Purpose:

Turn each Stage 5 candidate draft into a finalized source-specific runbook with
all supporting evidence attached.

Responsibilities:

* Expand Stage 5 drafts into full runbook structure per Runbook Example.md.
* Attach relevant source artifacts and image refs.
* Attach operational context records.
* Attach relevant source sections and OCR text.
* Attach nearby figures/tables.
* Attach source lineage and metadata.
* Generate Markdown + JSON review outputs per candidate.

Do NOT:

* Search other sources.
* Merge candidates across sources.
* Make cross-source merge decisions.

Output:

```text
finalized_runbooks/*.json
review_markdown/runbooks/*.md
runbook_finalization_report.json
```

## Shared Stage 6.5: Runbook Pool & Merge Preparation [Deterministic]

Tool:
runbook_pool_builder.py

Prompt:
stage6_5_runbook_pool_merge_prep_prompt.md

Inputs:

* Finalized runbooks from every source-specific Stage 6 output.

Purpose:

Index all finalized runbooks, compute cross-source similarity, identify merge
clusters, and mark singleton runbooks for pass-through without Stage 7 LLM cost.

Responsibilities:

* Build the shared runbook pool.
* Create retrieval cards for every finalized runbook.
* Generate normalized searchable metadata and embedding hooks.
* Build a runbook retrieval index.
* Compute cross-source similarity scores.
* Generate merge clusters for Shared Stage 7.
* Generate pass-through list for singletons (no Stage 7 LLM).

Important:

Stage 6.5 does NOT merge runbooks.

Outputs:

```text
runbook_pool.json
retrieval_cards.json
runbook_similarity.json
runbook_retrieval_index.json
merge_clusters.json
pass_through_runbooks.json
```

## Shared Stage 7: Cross-Source Runbook Merge [LLM Assisted, Selective]

Tool:
runbook_merge_tool.py

Prompt:
stage7_runbook_merge_prompt.md

Purpose:

Merge finalized runbooks from different sources when they represent the same
reusable procedure.

Cost rule:

Stage 7 must NOT run on every runbook. Run only on merge clusters from Stage 6.5.
Singleton finalized runbooks pass through without a Stage 7 LLM call.

Input (per merge cluster only):

* Finalized runbooks in the cluster.
* Similarity evidence and merge hints from Stage 6.5.
* Existing canonical runbook (if applicable).

Responsibilities:

* Confirm cluster members represent the same reusable procedure.
* Merge cross-source evidence when appropriate.
* Produce one merged canonical runbook (Markdown + JSON).
* Preserve source lineage from every contributing source.
* Record merge history, conflicts, and gaps.

Important:

* Stage 7 owns cross-source merge decisions only.
* Stage 7 does not re-draft runbooks Stage 6 already finalized unless merging.
* Stage 6 and Stage 6.5 must never merge runbook content.

Outputs:

```text
canonical_runbooks.json
review_markdown/runbooks/*.md
runbook_merge_report.json
candidate_to_procedure_mapping.json
```

## Shared Stage 8: Playbook Finalization & Runbook Linking [LLM Assisted]

Tool:
playbook_finalization_tool.py

Prompt:
stage8_playbook_finalization_prompt.md

Purpose:

Link finalized/canonical runbooks to playbooks and finalize playbooks.

Inputs:

* Pass-through finalized runbooks from Stage 6.5.
* Merged canonical runbooks from Stage 7.
* Playbook candidates from incident Stage 5.

Responsibilities:

* Resolve playbook runbook_placeholder nodes to runbook IDs.
* Finalize playbook structure for review.
* Preserve symptom-driven entry logic and source lineage.

Outputs:

```text
canonical_playbooks.json
review_markdown/playbooks/*.md
playbook_runbook_links.json
playbook_finalization_report.json
```

## Stage 9: Link Relationships

Tool: relationship_linker.py

Prompt: stage8_relationship_linking_prompt.md only if deterministic matching is not enough.

Responsibilities:

* Populate linked_context_ids and linked_runbook_ids after all records exist.
* Link artifacts to context records.
* Link artifacts to runbooks.
* Link context records to related runbooks.
* Keep this conservative.
* Prefer links based on shared section IDs, source refs, artifact refs, title similarity, and component/screen tags.
* Do not create workflow links yet.

Example final relationship:

```text
artifact_manual_fig_4_22_heartbeat_stats
  linked_context_ids:
    ctx_manual_operator_station_heartbeat_stats_v1
  linked_runbook_ids:
    proc_check_operator_station_heartbeat_stats_v1
```

## Stage 10: Validate and Repair

Tool: manual_knowledge_validator.py

Prompt: stage9_validation_repair_prompt.md

Responsibilities:

* Validate schemas.
* Validate required fields.
* Validate enum values.
* Validate source refs exist.
* Validate image refs exist.
* Validate linked IDs exist.
* Validate no forbidden fields exist.
* Validate action/command separation.
* Validate no invented commands/access paths.
* Validate linked_context_ids and linked_runbook_ids are only populated after the linking stage.
* Send failed records to LLM repair only for formatting or wording issues.
* Do not let repair invent missing facts.

## Stage 11: Write Outputs

Tool: extraction_report_writer.py

Responsibilities:

* Write final JSON files.
* Write extraction_report.json.
* Include counts.
* Include missing images.
* Include missing command details.
* Include missing access details.
* Include possible duplicates.
* Include conflicts.
* Include warnings.
* Include validation errors that could not be repaired.

Create these prompt files:

1. master_manual_knowledge_agent_prompt.md
2. stage3_artifact_enrichment_prompt.md
3. stage4_operational_context_extraction_prompt.md
4. stage5_runbook_candidate_discovery_prompt.md
5. stage6_runbook_finalization_prompt.md
6. stage6_5_runbook_pool_merge_prep_prompt.md
7. stage7_runbook_merge_prompt.md
8. stage8_playbook_finalization_prompt.md
9. stage9_relationship_linking_prompt.md
10. stage10_validation_repair_prompt.md

The master prompt should tell the agent to run source-specific stages 1–6 in
order, then invoke shared stages 6.5–8. Stage 7 runs only on merge clusters.
Never skip directly to cross-source merging before Stage 6 finalizes runbooks.

## Master prompt content:

```text
You are the OptiSweep Manual Knowledge Extraction Agent.

Your job is to orchestrate a repeatable ingestion pipeline for OptiSweep source manuals.

You produce source-specific knowledge outputs through Stage 6:
1. source artifacts / images / manual references
2. operational context records
3. draft runbook candidates (Stage 5)
4. finalized source runbooks (Stage 6)

Shared finalization then runs:
6.5. Build shared runbook pool and merge clusters
7. Merge cross-source runbook clusters only (not every runbook)
8. Link runbooks to playbooks and finalize playbooks
9. Link artifacts, context, and runbooks
10. Validate and repair
11. Write outputs

Do not skip stages.

Stage 5 drafts candidates. Stage 6 finalizes source runbooks with artifacts attached.
Stage 7 merges only when Stage 6.5 identifies a merge cluster.

Do not run Stage 7 LLM on singleton runbooks.

Do not populate linked_context_ids or linked_runbook_ids until the relationship linking stage.

Use deterministic tools for parsing, IDs, file writing, validation, source refs, image refs, and relationship checks.

Use LLM prompts only for semantic extraction, summaries, candidate discovery, drafting, merge reasoning, relationship suggestions, and repair.

Keep the schemas simple and human-reviewable.

Runbooks/procedures are reusable instructional assets.
They are not workflows, decision trees, ML labels, or routing logic.

Operational context explains what something means.
Runbooks tell a human what to check or do.
Source artifacts/images visually support screens, fields, faults, metrics, controls, buttons, alarms, or inspection targets.

Do not invent:
- commands
- service names
- hostnames
- SQL table names
- API endpoints
- access paths
- screenshots
- page numbers
- section IDs
- approval status
- exact thresholds not present in the source

Forbidden runbook fields:
- trigger_conditions
- candidate_input_signals
- produces_signals
- resolved_signals
- next_step_on_success
- next_step_on_failure
- workflow_branch
- decision_node
- ml_label
- routing_key

Use only these runbook role values:
- operator
- L1_support
- L2_support
- L3_support

Use only these runbook procedure types:
- operation
- diagnostic
- recovery
- reference

Default validation_status:
- needs_sme_review

Final outputs:
- source_artifacts.json
- manual_references.json
- operational_context.json
- runbook_candidates.json
- extraction_report.json
```

### Canonical Runbook Rule

Source-derived candidates are not canonical runbooks.

Manuals, training materials, transcripts, incident records, and
SME-authored documentation are evidence sources.

Multiple candidates from different sources may represent the same
procedure.

Canonical runbooks are created only after cross-source normalization,
candidate consolidation, and evidence merging.

The goal is to create a single reusable runbook library supported by
many evidence sources rather than separate runbook libraries for each
source type.

Implement tests or smoke checks for:

1. The heartbeat example produces:

   * one source artifact
   * one operational context record
   * one diagnostic runbook
   * final linked IDs between them

2. The System Startup procedure produces a runbook.

3. The Operator Station Data Screen produces operational context records for metrics.

4. The Operator Station Alarm screen produces operational context and possible diagnostic runbook candidates.

5. No runbook contains forbidden workflow/routing/ML fields.

6. No linked_context_ids or linked_runbook_ids are populated before the relationship linking stage.

7. All image_refs and source_refs point to existing records.

8. Missing images or unresolved refs are captured in extraction_report.json.

Do not write to Cosmos or PostgreSQL vector tables yet.
This stage only creates local reviewed extraction outputs.

## Future LangGraph Orchestration

Future LangGraph orchestration should mirror the source-specific versus shared
boundary:

```text
Source-specific subgraph (per manual, video, incident, SOP, SME doc)
  Stage 1  [Deterministic]
  Stage 2  [Deterministic]
  Stage 3  [LLM Assisted]
  Stage 4  [LLM Assisted]
  Stage 5  [LLM Assisted]
  Stage 6  [LLM Assisted]

Shared finalization subgraph
  Stage 6.5  [Deterministic]  pool + merge clusters + pass-through
  Stage 7    [LLM Assisted]    merge clusters only
  Stage 8    [LLM Assisted]    playbook linking + finalization
  Stage 9+   [mixed]            links, validation, publish
```

- Stages 1–6 are source-specific nodes.
- Stages 6.5–8 are shared nodes.
- Stage 7 must not run on every finalized runbook.

Canonical runbook JSON/Markdown structure: `incidenceknowledgeingestion/datastructureprompts/Runbook Example.md`

