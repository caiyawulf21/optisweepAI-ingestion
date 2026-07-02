# Stage 5/6 Playbook Extraction Mode Decision Notes

This note tracks why Stage 5 currently runs two playbook candidate extraction
modes and how the result affects shared Stage 6.5 candidate pooling, later
canonical playbooks, and runtime orchestration.

Read this alongside
[Stage 5–7 Runbook Architecture](stage_5_7_runbook_architecture.md) and
[Runbook Candidate Pool, Merge Review, And Azure Publishing Design Notes](runbook_candidate_pool_and_azure_review_design.md).

## Why We Are Testing Both Extraction Modes

We are testing two playbook extraction strategies because incidents do not
always map cleanly to troubleshooting workflows.

An incident is a historical record of what happened. It may contain one clear
resolution path, multiple partially related troubleshooting paths, or a main
issue with downstream recovery steps. The extraction logic needs to learn the
difference between:

- one incident with one reusable troubleshooting path
- one incident containing multiple separable troubleshooting paths

This matters because playbooks are not case summaries. Playbooks are runtime
orchestration assets that guide the assistant through technical resolution.

Testing both approaches lets us compare whether the extraction model:

- over-compresses complex incidents into one vague playbook
- over-splits one incident into too many narrow playbooks
- correctly keeps runbook-level actions out of playbook nodes
- preserves symptom-based entry logic
- produces candidates that can later merge into canonical playbooks

The goal is not to decide permanently that every incident produces one playbook
or many playbooks. The goal is to discover which extraction strategy produces
better candidate quality for downstream review and runtime orchestration.

## Downstream Impact On The App And Runtime Orchestration

This decision directly affects how the assistant behaves at runtime.

At runtime, the user will not usually know the technical diagnosis. They will
describe symptoms such as:

- robots are not moving
- HMI has question marks
- hospital tote removal is stuck
- RMS does not show failed AGVs
- system looks frozen

The orchestration layer must translate those symptoms into the correct
troubleshooting path.

If playbooks are too broad, the assistant may choose the right general area but
give vague guidance, ask too many unnecessary questions, or fail to route to the
correct procedure.

If playbooks are too narrow, the assistant may struggle to choose between many
similar playbooks, route incorrectly, or require the user to know the root cause
before help can begin.

The right balance gives us:

```text
symptom input
  -> routing/classification
  -> selected playbook
  -> playbook node
  -> referenced runbook/procedure
  -> validation or escalation
```

This is why we are keeping playbook nodes lightweight. The playbook should
control the path, while the runbook contains the exact operational
instructions.

## What This Means For Runtime Design

The runtime assistant should not execute a playbook as a long static checklist.
It should use the playbook as an orchestration guide.

A good runtime flow looks like this:

1. Intake collects enough symptoms and impact to route.
2. Router selects a likely playbook based on observable symptoms.
3. Playbook determines the next diagnostic direction.
4. A node references a runbook when exact action is needed.
5. Role and risk gates decide whether the user can proceed.
6. Validation gates confirm whether the issue is resolved.
7. Escalation gates stop unsafe or uncertain paths.

So the extraction strategy affects all of these runtime components:

| Component | Why playbook quality matters |
| --- | --- |
| Router/classifier | Needs symptom-driven playbooks, not case-specific names |
| RAG layer | Needs source-traceable candidates and evidence summaries |
| LangGraph orchestration | Needs clean nodes with predictable types |
| Runbook execution/display | Needs playbook nodes to reference runbooks instead of embedding steps |
| Escalation logic | Needs clear role/risk gates |
| UI/UX | Needs user-facing names that match how support describes issues |
| Validation | Needs recovery checks that confirm the system is actually working |
| Knowledge graph later | Needs clean relationships between incident, symptom, playbook, runbook, component, and resolution |

## Why This Is Important For MVP

For Phase 0, we should avoid overengineering, but we also need clean boundaries
now. Bad extraction structure will create expensive cleanup later.

If we allow one incident to create too many playbooks, the system will become
noisy:

- too many overlapping candidates
- harder routing
- higher SME review burden
- duplicate workflows
- lower confidence at runtime

If we force every incident into exactly one playbook, we may lose important
reusable patterns:

- complex incidents become vague
- secondary recovery flows get buried
- distinct troubleshooting paths are harder to reuse

Testing both prompts gives us evidence before choosing the final Stage 5
behavior.

The expected long-term rule is:

> Default to one playbook candidate per incident, but allow multiple only when
> the incident contains clearly separable troubleshooting flows with different
> entry symptoms or reusable operational signatures.

That gives us a simple MVP default while still allowing the extraction pipeline
to handle real-world complexity.

## Current Stage 5 Test Setup

Stage 5 runs both candidate playbook extraction modes every time:

- Prompt A: one incident produces exactly one playbook candidate.
- Prompt B: one incident produces one or more candidates, but creates multiple
  candidates only when separable troubleshooting flows are clearly present.

The outputs are written to separate folders under the Stage 5 output directory:

```text
stage_5_runbook_candidates/
  runbook_candidates.json
  runbook_candidate_extraction_report.json
  runbook_candidate_review.md
  playbook_prompt_a_one_per_incident/
    playbook_candidates.json
    playbook_candidate_extraction_report.json
    playbook_candidate_review.md
  playbook_prompt_b_multi_flow/
    playbook_candidates.json
    playbook_candidate_extraction_report.json
    playbook_candidate_review.md
```

Stage 6 source-specific packet enrichment applies to **runbook candidates only**.
Playbook Prompt A/B outputs are not part of Stage 6 or Stage 6.5 runbook pooling.

Compare both playbook candidate outputs during review before choosing the default
extraction behavior. Shared Stage 8 links playbooks to finalized/canonical runbooks
after Stages 6–7.
