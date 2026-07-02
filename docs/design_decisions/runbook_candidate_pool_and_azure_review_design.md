# Runbook Candidate Pool, Merge Review, And Azure Publishing Design Notes

This note tracks design decisions and open questions for moving from
source-specific runbook candidates into shared canonical runbooks, while keeping
incident playbooks separate from runnable procedures.

For the current Stage 5–7 architecture, see
[Stage 5–7 Runbook Architecture](stage_5_7_runbook_architecture.md).

For the current Stage 5 playbook extraction-mode comparison, see
[Stage 5/6 Playbook Extraction Mode Decision Notes](stage_5_6_playbook_extraction_modes.md).

## Current Direction

Operational sources and incident sources should contribute different kinds of
knowledge:

- Operational manuals, SOPs, and training videos are the primary sources for
  reusable runbook procedures.
- Incident Stage 5 should run three LLM discovery calls: one for
  source-specific runbook candidates and two for source-specific playbook
  candidate extraction modes.
- The Stage 5 runbook call may produce zero candidates when the incident
  evidence does not support a reusable procedure.
- The Stage 5 playbook calls test two extraction modes in separate output
  folders: Prompt A forces one playbook candidate per incident, while Prompt B
  produces one or more candidates and allows multiple only when separable
  troubleshooting flows are clearly present.
- Playbook discovery should describe needed runbook capabilities, not point
  directly at specific runbook IDs during extraction.

Example from incident `228723`:

- Incident Stage 5 may correctly produce zero runbook candidates when the
  incident does not show the exact reusable controls, screens, commands,
  fields, or substeps needed for a runbook.
- The incident may still support a later playbook node such as "check for AGV
  mapping, roster, or remove/add mismatch."
- The reusable procedure likely comes from operational candidates such as manual
  or training-video AGV add/remove and hospital-flow procedures.

## Recommended Stage Shape

The current stage names differ between operational and incident ingestion. The
recommended conceptual layout is:

```text
Operational Stage 5 [LLM Assisted]
  Source-specific runbook candidate discovery from manuals, SOPs, and training.

Operational Stage 6 [LLM Assisted]
  Source-specific runbook finalization. Expands Stage 5 drafts into finalized
  runbooks with artifacts, context, sections, and lineage attached.

Incident Stage 5 [LLM Assisted]
  Runbook candidate discovery and playbook candidate discovery (Prompt A/B).

Incident Stage 6 [LLM Assisted]
  Source-specific runbook finalization for runbook candidates only.

Shared Stage 6.5 [Deterministic]
  Shared runbook pool and merge preparation. Indexes finalized runbooks,
  computes similarity, identifies merge clusters, marks singleton pass-through.

Shared Stage 7 [LLM Assisted, selective]
  Cross-source runbook merge only. Does not run on every runbook.

Shared Stage 8 [LLM Assisted]
  Playbook finalization and runbook linking using pass-through + merged runbooks.

Shared Stage 9+ [mixed]
  Relationship linking, validation, publishing.
```

## Stage 6 Source-Specific Runbook Finalization

Stage 6 runs inside each source pipeline and is LLM assisted.

Stage 5 already drafts candidates. Stage 6 finalizes complete source-specific
runbooks per Runbook Example.md.

Inputs per source:

- `runbook_candidates.json`
- `source_artifacts_enriched.json`
- operational context or incident evidence handoff from Stage 4
- source bundle / source package sections

Outputs:

- `finalized_runbooks/*.json`
- `review_markdown/runbooks/*.md`

Stage 6 must not search other sources or merge across sources.

## Stage 6.5 Shared Runbook Pool And Merge Preparation

Stage 6.5 is deterministic. It is the first shared stage.

Inputs:

- Finalized runbooks from every source-specific Stage 6 output.

Outputs:

- `runbook_pool.json`
- `retrieval_cards.json`
- `runbook_similarity.json`
- `runbook_retrieval_index.json`
- `merge_clusters.json`
- `pass_through_runbooks.json`

Stage 6.5 identifies merge clusters for Stage 7 and singleton pass-through
runbooks that skip Stage 7 LLM cost.

## Stage 7 Cross-Source Runbook Merge (Selective)

Stage 7 is LLM assisted and runs **only on merge clusters** from Stage 6.5.

It merges finalized runbooks when multiple sources describe the same procedure.
It does not re-draft every runbook Stage 6 already finalized.

Singleton runbooks pass through via `pass_through_runbooks.json`.

## Stage 8 Playbook Finalization And Runbook Linking

Shared Stage 8 links playbooks to pass-through finalized runbooks and merged
canonical runbooks from Stage 7.

## Implementation Sequence

Build and validate the pipeline locally before wiring Azure retrieval and
publishing.

Recommended order:

1. Stabilize source-specific Stage 5 draft candidates and Stage 6 finalized
   runbooks for operational and incident sources.
2. Stabilize shared Stage 6.5 pool, merge clusters, and pass-through lists.
3. Implement selective Stage 7 merge-only LLM calls.
4. Implement Shared Stage 8 playbook linking against finalized/canonical runbooks.
5. Define a `RunbookRetriever` interface for published-runbook match checks during Stage 6.5/7.
6. Add Azure retrieval and publishing after local merge and review workflows are stable.

The local implementation should still be designed with Azure in mind. The goal
is to avoid cloud plumbing while the contracts are still moving, without
painting the backend into a local-only shape.

## Azure Retrieval Need

When canonical runbooks are stored in Azure, the backend ingestion pipeline will
need a retrieval function, similar to RAG, to decide which published runbooks
should be compared to a new finalized runbook or merge cluster.

The ingestion pipeline should not send the full published runbook corpus to the
LLM.

Recommended retrieval shape:

```text
candidate packet retrieval card
  -> lexical search over published runbook cards
  -> vector search over published runbook cards
  -> metadata filters
  -> top N possible published matches
  -> deterministic compatibility scoring in Stage 6.5
  -> merge hints for Stage 7
  -> Stage 7 LLM comparison/draft/update only for selected matches
```

Published runbooks should have compact retrieval cards alongside the full
canonical runbook body:

```json
{
  "runbook_id": "",
  "title": "",
  "summary": "",
  "when_to_use": "",
  "procedure_type": "",
  "role_required": "",
  "systems": [],
  "components": [],
  "tools": [],
  "action_verbs": [],
  "step_summaries": [],
  "success_criteria": [],
  "failure_conditions": [],
  "source_candidate_ids": [],
  "validation_status": "",
  "version": 1
}
```

The retrieval card is what gets embedded and searched. The full runbook is only
loaded when a retrieved match passes the initial gates.

## Merge Decision Logic

Candidate packets and published runbooks should be considered merge-compatible
when they share:

- Same procedure goal.
- Same system, screen, component, or operational target.
- Same general user intent.
- Compatible procedure type.
- Compatible role and risk profile.
- Compatible expected outcome.
- No conflicting safety requirements.

They should not merge when:

- One is diagnostic and the other is recovery, unless the diagnostic is clearly
  just a validation substep for the recovery.
- One changes system state and the other is read-only.
- The components or screens differ materially.
- The expected outcomes differ.
- Safety or access requirements differ materially.
- The candidate is only incident context and not a reusable procedure.
- The only similarity is broad vocabulary such as AGV, RMS, HMI, hospital, or
  OptiSweep.

Evidence priority when sources conflict:

1. SME-approved canonical runbook.
2. Official manual.
3. SOP.
4. Training slide.
5. Training transcript.
6. Incident record.
7. Chat-derived evidence.

Incident evidence can enrich failure modes, validation checks, and escalation
notes, but should not override official procedure steps unless an
SME-approved source confirms the change.

Stage 6.5 may compute similarity and emit merge hints. Only Stage 7 may decide
that two packets become one canonical runbook.

## Published Runbook Update Model

Published runbooks in Azure should be treated as versioned records, not
destructively edited in place without review.

Recommended model:

- Keep immutable published versions.
- Create proposed replacement versions during Stage 7.
- Preserve lineage from all source candidates and previous canonical versions.
- Mark superseded versions as inactive or deprecated after approval.
- Do not hard-delete old runbooks during normal ingestion.
- Maintain redirects or replacement links from old runbook IDs to the approved
  current version.

Possible record statuses:

- `draft_generated`
- `pending_human_review`
- `approved_for_publish`
- `published_current`
- `published_superseded`
- `rejected`
- `deprecated`

## Human Review And Notification Gate

Before Azure records are changed, the pipeline should create a review package
and notify a human reviewer.

The review package should show:

- The existing published runbook version.
- The newly generated merged runbook version.
- A diff or side-by-side comparison of changed sections.
- The seed candidate packet and retrieved packets that triggered the update.
- Retrieved published-runbook matches and match scores.
- Source evidence used for each new or changed instruction.
- Images/artifacts added or removed.
- Safety, role, or access changes.
- Known gaps and low-confidence claims.
- Proposed Azure action:
  - create new runbook
  - publish new version of existing runbook
  - mark old version superseded
  - no action
  - reject/defer

No production Azure runbook should be overwritten, removed, or superseded until
this review package is approved.

## Azure Publishing Workflow

Proposed future workflow:

```text
1. Build source-specific Stage 5 draft candidates.
2. Build source-specific Stage 6 finalized runbooks.
3. Build shared Stage 6.5 runbook pool and merge clusters.
4. Run Stage 7 only on merge clusters.
5. Run Stage 8 to link playbooks to finalized/canonical runbooks.
```

## Open Questions

- Should Stage 6.5 live in a shared package, operational ingestion, or a backend
  service that has Azure access?
- What is the minimal local `RunbookRetriever` interface needed before Azure is
  introduced?
- Similarity thresholds for Stage 6.5 merge hints versus `needs_human_review`.
- Should a low-confidence LLM merge ever be auto-created as a draft, or only
  logged as a review suggestion?
- How should reviewers approve changes: local markdown review files, web UI,
  Teams notification, Git PR, or Azure-native approval workflow?
- Should old runbook IDs remain stable forever with version pointers, or should
  procedure IDs represent logical procedures while version IDs represent
  immutable published artifacts?
