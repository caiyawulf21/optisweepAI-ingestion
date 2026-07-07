# Stage 8 — Playbook Finalization & Runbook Linking

This note defines Shared Stage 8: the relationship-linking stage that resolves
incident playbook candidates to canonical runbooks and produces reviewable
finalized playbook packets.

Read this alongside:

- [Stage 5–7 Runbook Architecture](stage_5_7_runbook_architecture.md)
- [Stage 5/6 Playbook Extraction Mode Decision Notes](stage_5_6_playbook_extraction_modes.md)
- [Runbook Candidate Pool, Merge Review, And Azure Publishing Design Notes](runbook_candidate_pool_and_azure_review_design.md)

## Problem Statement

Incident Stage 5 produces playbook candidates with plain-text
`runbook_placeholder` nodes. Shared Stages 6.5 and 7 produce a canonical
runbook catalog from operational and incident sources.

Stage 8 is the first stage where playbooks become executable orchestration
assets. It resolves every playbook node to one or more real runbook IDs, surfaces
healthy/unhealthy decision descriptors for diagnostic and branching nodes,
inherits images from linked runbooks, and emits explicit branch wiring for
runtime routing.

Stage 8 is relationship linking at the playbook layer — analogous to
operational relationship linking, but scoped to incident playbooks and the
shared canonical runbook pool.

## Pilot Scope

Initial build and validation use **two incidents only**:

- `case_228086`
- `case_228723`

Both incidents already have Stage 5 Prompt A and Prompt B playbook candidates.
Stage 8 runs both extraction-mode tracks in parallel and emits a comparison
report. Do not expand beyond these cases until pilot review passes.

## Overall Principle

```text
Stage 7 canonical_runbooks.json
Stage 6.5 runbook retrieval index
Stage 8 playbook retrieval cards (new)
Incident Stage 5 playbook candidates (Prompt A + Prompt B)

        ↓

Shared Stage 8 [LLM Assisted]
  - Retrieve candidate runbooks per node
  - Link placeholders → procedure_id(s)
  - Emit explicit branches from branch_hints + LLM
  - Surface decision KPIs from linked runbooks
  - Generate Markdown + HTML review per playbook

        ↓

stage_8_finalized_playbooks/
  prompt_a_one_per_incident/
  prompt_b_multi_flow/
  stage_8_comparison_report.json
```

## Playbook Canonicalization Model

Stage 8 outputs are **incident-specific finalized playbooks**, not a cross-incident
canonical playbook pool.

| Concept | Stage 8 behavior | Later stage (if any) |
| --- | --- | --- |
| Playbook candidate | One per incident (A) or one-or-more (B) | Input only |
| Finalized playbook | One finalized record per candidate, tied to `case_id` | `needs_sme_review` until approved |
| Canonical playbook | **Not created at Stage 8** | Future shared stage after SME review and cross-incident dedup |

Why keep playbooks incident-specific at Stage 8:

- Playbooks are extracted from historical incident evidence and may contain
  case-specific context, tentative internal patterns, and weak-confidence paths.
- Runbooks already have a cross-source canonical pool (Stages 6.5/7). Playbooks
  reference that pool; they do not replace it.
- Runtime routing will eventually select among **reviewed** playbooks by symptom
  match, not by auto-merging incident playbooks into one canonical record.
- Treating Stage 8 output as canonical would prematurely freeze extraction
  experiments (Prompt A vs B) before SME review.

Stage 8 may assign a stable `playbook_id` per finalized playbook for linking
and review, but `validation_status` defaults to `needs_sme_review`. Promotion
to a shared canonical playbook catalog is out of scope for the pilot.

## Inputs

| Input | Source | Purpose |
| --- | --- | --- |
| `canonical_runbooks.json` | Shared Stage 7 | Authoritative runbook catalog (pass-through + merged) |
| `candidate_to_procedure_mapping.json` | Shared Stage 7 | Lineage; incident-source preference |
| `retrieval_cards.json` | Shared Stage 6.5 | Runbook retrieval metadata |
| `runbook_retrieval_index.json` | Shared Stage 6.5 | Runbook embedding vectors |
| `playbook_candidates.json` | Incident Stage 5 Prompt A folder | One-per-incident candidates |
| `playbook_candidates.json` | Incident Stage 5 Prompt B folder | Multi-flow candidates |
| Incident artifacts / operational context | Incident Stage 2–4 outputs | Review images, tie-breaking, lineage |

Pilot input paths (convention):

```text
incidenceknowledgeingestion/data/output/incidents/case_<id>/stage_5_runbook_candidates/
  playbook_prompt_a_one_per_incident/playbook_candidates.json
  playbook_prompt_b_multi_flow/playbook_candidates.json

shared_pipeline_stages/data/output/shared/<tuning_run>/stage_7_merged_runbooks/
  canonical_runbooks.json
  candidate_to_procedure_mapping.json

shared_pipeline_stages/data/output/shared/<tuning_run>/stage_6_5_runbook_pool/
  retrieval_cards.json
  runbook_retrieval_index.json
```

## Playbook Retrieval Cards

Stage 8 builds **playbook-specific retrieval cards** separate from runbook
retrieval cards. These cards drive embedding search when matching node
placeholders to canonical runbooks.

Built once per finalized playbook candidate (before per-node linking):

```json
{
  "playbook_id": "",
  "playbook_candidate_id": "",
  "case_id": "",
  "extraction_mode": "one_playbook_candidate_per_incident | one_or_more_playbook_candidates_when_separable",
  "title": "",
  "user_facing_summary": "",
  "observed_entry_symptoms": [],
  "support_user_language_examples": [],
  "affected_systems_or_components": [],
  "node_retrieval_summaries": [
    {
      "node_id": "",
      "node_type": "",
      "title": "",
      "intent": "",
      "runbook_placeholder": "",
      "expected_or_observed_result": "",
      "allowed_roles": []
    }
  ],
  "validation_status": "needs_sme_review"
}
```

Embeddings:

- One vector per playbook card (symptom/entry routing use later).
- One vector per node retrieval summary (primary retrieval unit for linking).

Store alongside Stage 8 outputs:

```text
playbook_retrieval_cards.json
playbook_retrieval_index.json
```

Reuse the Stage 6.5 embedder interface; do not embed the full playbook JSON.

## Core Responsibilities

Stage 8 performs:

1. Build playbook retrieval cards and embeddings.
2. For each playbook node, retrieve top-N canonical runbooks using node summary
   embeddings + lexical search over runbook retrieval cards.
3. LLM-select `resolved_runbook_ids[]` from retrieved candidates only.
4. Prefer incident-derived canonical runbooks when scores are close.
5. Emit explicit `branches[]` on branching nodes, seeded from `branch_hints[]`.
6. Surface `decision_outcomes[]` with healthy/unhealthy/inconclusive descriptors
   from linked runbook `healthy_conditions` and step expected results.
7. Resolve inline images per node from linked runbook visual refs.
8. Write JSON, Markdown, and HTML review artifacts.
9. Emit link records, per-variant finalization reports, and A/B comparison report.

Stage 8 does NOT:

- Merge runbooks (Stage 7).
- Finalize source runbooks (Stage 6).
- Create cross-incident canonical playbooks.
- Auto-approve playbooks or links for production runtime.

## Runbook Linking Rules

### ID authority

- Every `procedure_id` must exist in `canonical_runbooks.json`.
- Never invent runbook IDs.
- Unmatched placeholders use policy **C**: link to the nearest partial match
  with `link_confidence: "low"` and document `link_rationale` + `match_gaps[]`.
- If no candidate scores above the minimum retrieval floor, emit
  `link_confidence: "unresolved"` (no ID).

### Incident-source preference

When retrieval scores are within **0.05 cosine similarity** of each other, prefer
the canonical runbook whose source lineage includes the same `case_id` as the
playbook being finalized.

Evidence order when still tied:

1. Incident-derived canonical runbook from same case
2. SME-approved / manual source
3. SOP / training
4. Other incident sources
5. Lowest merge conflict count from Stage 7 report

### Procedure type compatibility

| Node type | Allowed runbook `procedure_type` | Blocked |
| --- | --- | --- |
| `diagnostic_decision` | `diagnostic`, `reference`, `monitoring` | `recovery`, `operation` unless read-only inspection |
| `branching_condition` | `diagnostic`, `reference`, `monitoring` | `recovery` as sole link |
| `validation_gate` | `diagnostic`, `monitoring`, `reference` | — |
| `procedure_reference` | any compatible with node intent | read-only runbook for state-changing intent |
| `escalation_gate` | `reference`, `diagnostic` | — |
| `recovery_phase_marker` | `reference`, `diagnostic`, `monitoring` | — |

Compatibility violations force `link_confidence: "low"` minimum and add a
validation warning; hard blocks become `unresolved` if no compatible candidate
exists.

### Multiple runbooks per node

Allow `resolved_runbook_ids[]` (ordered) when the placeholder clearly spans
multiple distinct procedures.

Rules:

| Rule | Detail |
| --- | --- |
| Max IDs per node | 3 |
| Ordering | Primary action first; supporting checks after |
| Same-type only | All IDs must satisfy procedure type compatibility for the node |
| No duplication | Do not link two runbooks with >0.90 similarity to each other |
| Compound placeholder signal | Placeholder mentions 2+ distinct systems/screens/tools with "and", "then", "also", or numbered sub-checks |
| Single-id default | When one runbook covers the full placeholder, use one ID |
| Validation gate exception | May link one diagnostic + one monitoring runbook (max 2) |

Each ID in the array gets its own `link_confidence`, `link_rationale`, and
inherited image set on the node.

## Branch Wiring

Stage 8 uses **both** Stage 5 `branch_hints[]` and LLM-emitted explicit
branches.

Process:

1. Start from playbook-level `branch_hints[]` as seed edges
   (`from_node_id`, `condition_or_signal`, `suggested_next_node_id`).
2. LLM emits finalized `branches[]` on each `branching_condition` node and
   enriches diagnostic nodes that gate flow:

```json
{
  "branch_id": "",
  "condition_label": "",
  "condition_descriptor": "",
  "outcome": "healthy | unhealthy | inconclusive | escalate",
  "next_node_id": "",
  "source_branch_hint_ids": [],
  "linked_runbook_step_ref": "",
  "source_refs": []
}
```

3. Validate every `next_node_id` references an existing node in the same playbook.
4. Flag `needs_graph_repair: true` when branch_hints suggest an edge the LLM
   did not confirm.

## Decision Outcomes And KPIs

For `diagnostic_decision`, `branching_condition`, and `validation_gate` nodes,
Stage 8 must emit `decision_outcomes[]`:

```json
{
  "outcome_label": "healthy | unhealthy | inconclusive | escalate",
  "descriptor": "",
  "observable_signal": "",
  "source": "runbook_healthy_condition | runbook_step | playbook_expected_result",
  "linked_runbook_id": "",
  "linked_step_number": null,
  "next_node_id": ""
}
```

Rules:

- Pull descriptors from linked runbook `healthy_conditions[]` and step
  `expected_result` / `healthy_condition` fields when available.
- Fall back to playbook `expected_or_observed_result` only when runbook KPIs
  are missing; mark `source: "playbook_expected_result"` and
  `link_confidence` penalty on the node.
- Diagnostic nodes without at least one `healthy` and one `unhealthy` or
  `inconclusive` outcome generate a validation warning.

## Image Inheritance

Images are embedded with linked runbook steps, not as separate reference-only blocks.

Per node in review output:

1. Embed the full linked runbook body (summary, steps, healthy conditions, success/failure criteria).
2. Copy assets into `review_markdown/playbooks/assets/` using the Stage 7 artifact image resolver.
3. Render runbook header images and per-step images inline under each linked runbook within the node section.
4. Store full runbook payloads on `linked_runbooks[]` in finalized playbook JSON (not just IDs).

If image file missing, render artifact ID + caption text; do not drop the node
image slot silently.

## Outputs

```text
shared_pipeline_stages/data/output/shared/stage_8_finalized_playbooks/
  prompt_a_one_per_incident/
    canonical_playbooks.json
    playbook_runbook_links.json
    playbook_retrieval_cards.json
    playbook_retrieval_index.json
    playbook_finalization_report.json
    review_markdown/
      playbooks/*.md
      playbooks/*.html
      playbooks/assets/*
  prompt_b_multi_flow/
    (same structure)
  stage_8_comparison_report.json
```

### `canonical_playbooks.json`

Despite the filename (consistent with Stage 7 naming), records are
**incident-specific finalized playbooks**:

```json
{
  "playbooks": [
    {
      "playbook_id": "",
      "playbook_candidate_id": "",
      "case_id": "",
      "extraction_mode": "",
      "title": "",
      "validation_status": "needs_sme_review",
      "nodes": [
        {
          "node_id": "",
          "node_type": "",
          "resolved_runbook_ids": [],
          "runbook_links": [
            {
              "procedure_id": "",
              "link_confidence": "high | medium | low | unresolved",
              "link_rationale": "",
              "match_gaps": [],
              "preferred_incident_source": true
            }
          ],
          "decision_outcomes": [],
          "branches": [],
          "inherited_image_refs": []
        }
      ],
      "branches": [],
      "branch_hints": []
    }
  ]
}
```

### `playbook_runbook_links.json`

Flat link index for audit:

```json
{
  "links": [
    {
      "case_id": "",
      "playbook_id": "",
      "node_id": "",
      "procedure_id": "",
      "link_confidence": "",
      "link_rank": 1,
      "extraction_mode": ""
    }
  ]
}
```

### Review artifacts

Each playbook produces paired Markdown and HTML review files:

- Markdown: `review_markdown/playbooks/<playbook_id>.md`
- HTML: `review_markdown/playbooks/<playbook_id>.html`

HTML uses the same content as Markdown with embedded asset paths suitable for
browser review (follow operational Stage 6 HTML review conventions).

Review layout per playbook:

1. Playbook header (case, mode, confidence, validation status)
2. Entry symptoms and affected systems
3. Per-node sections with:
   - Node type, intent, linked runbook ID(s) + confidence
   - Decision outcomes / branches (if applicable)
   - Inline images from linked runbooks
   - Unresolved or low-confidence warnings
4. Branch graph summary table
5. Unlinked placeholder summary

## A/B Comparison Report

`stage_8_comparison_report.json` compares Prompt A vs Prompt B across **all**
pilot metrics:

| Metric | Description |
| --- | --- |
| `high_confidence_link_rate` | % node links with `link_confidence: high` |
| `unresolved_link_count` | Nodes with no resolvable runbook |
| `low_confidence_link_count` | Nodes linked under policy C |
| `duplicate_runbook_refs` | Same `procedure_id` linked by multiple nodes in one playbook |
| `diagnostic_outcome_coverage` | % diagnostic/branching nodes with healthy + unhealthy/inconclusive outcomes |
| `branch_graph_completeness` | % branch_hints confirmed in explicit `branches[]` |
| `incident_source_preference_applied_count` | Times incident-derived runbook won tie-break |
| `multi_runbook_node_count` | Nodes with >1 resolved ID |
| `sme_review_flags` | Aggregated warnings for human review queue |

Report is per case and rolled up across cases 228086 and 228723.

## Validation Rules (Deterministic)

Post-LLM gates:

1. Every `procedure_id` exists in canonical catalog.
2. `resolved_runbook_ids.length` ≤ 3 per node.
3. All branch `next_node_id` values exist in playbook nodes.
4. No invented procedure IDs.
5. `diagnostic_decision` nodes must not link only to `recovery` runbooks.
6. Playbook `validation_status` remains `needs_sme_review` unless explicitly
   overridden by SME tooling later.
7. Low-confidence links must include non-empty `match_gaps[]`.
8. HTML and Markdown review files exist for every playbook in output.

## Mode

**LLM Assisted** — one LLM call per playbook (or per playbook batch) for link
selection and branch emission. Retrieval and validation are deterministic.

## Relationship To Operational Stage 8

Operational ingestion uses Stage 8 for **source artifact and runbook relationship
linking** within a manual/video pipeline. Shared Stage 8 is **playbook-to-runbook
relationship linking** across the canonical pool. Both are relationship-linking
stages at different layers. Shared stage numbering stays at **Stage 8** per
[Stage 5–7 Runbook Architecture](stage_5_7_runbook_architecture.md).

## Implementation Status

| Component | Status |
| --- | --- |
| Design doc | Current |
| Playbook retrieval cards + embeddings | Implemented |
| Linking LLM prompt (`stage_prompts/stage_8/`) | Implemented |
| `shared_pipeline_stages/stage_8/` module | Implemented |
| Pilot CLI (228086, 228723) | Implemented |
| Markdown + HTML review writer | Implemented |
| A/B comparison report | Implemented |

## Risks

| Risk | Severity | Mitigation |
| --- | --- | --- |
| Runbook pool lacks coverage for playbook placeholders (228723) | High | Policy C low-confidence links + unresolved counts in report; do not invent runbooks |
| False-positive runbook match (similar titles, different screens) | High | Procedure type gate + component/screen metadata check + incident tie-break only within 0.05 |
| LLM invents procedure IDs | High | Deterministic catalog validation |
| Diagnostic node linked to recovery runbook | High | Procedure type compatibility matrix |
| Missing healthy/unhealthy KPIs on branches | Medium | Require `decision_outcomes[]`; warn when sourced only from playbook text |
| Low-confidence links treated as production-ready | Medium | Default `needs_sme_review`; low-confidence explicitly labeled in HTML |
| Branch graph incomplete | Medium | Seed from branch_hints; flag `needs_graph_repair` |
| Multi-runbook nodes confuse runtime ordering | Medium | Max 3 IDs; ordered array with link_rank |
| Image missing from runbook asset copy | Low | Fallback caption; warn in finalization report |
| Pilot N=2 overfits A/B comparison | Low | Treat comparison as directional only |

## Open Questions (Resolved For Pilot)

| Question | Decision |
| --- | --- |
| Pilot scope | Cases 228086 and 228723 only |
| Unresolved placeholder policy | C — low-confidence partial match; unresolved if below floor |
| Multiple runbooks per node | B — allowed with rules (max 3, compatibility, dedup) |
| Branch wiring | branch_hints seed + LLM explicit branches |
| Incident runbook preference | Procedure-reference nodes only; 0.02 margin (see [link scoring note](stage_8_link_scoring_and_confidence.md)) |
| Playbook canonicalization | Incident-specific finalized playbooks; no cross-incident merge at Stage 8 |
| A/B metrics | All metrics in comparison report |
| Stage numbering | Shared Stage 8 |
| Retrieval | Playbook-specific retrieval cards + embeddings |
| Review format | Inline images per node; Markdown + HTML |
