# OptiSweep AI Demo Test Plan

**Version:** July 7, 2026  
**Status:** Pre-Round 1 (app testing week of July 13)

---

## Table of Contents

1. [Overview](#overview)
2. [Demo Session Format](#demo-session-format)
3. [User Interaction Flow](#user-interaction-flow)
4. [Prompt A vs Prompt B Toggle](#prompt-a-vs-prompt-b-toggle)
5. [Test Prompts](#test-prompts)
6. [Success Criteria](#success-criteria)
7. [Scoring Rubric](#scoring-rubric)
8. [Coverage & Expectations by Prompt](#coverage--expectations-by-prompt)
9. [Timeline](#timeline)

---

## Overview

The OptiSweep AI troubleshooting assistant takes **symptom descriptions** (as heard on a support call) and routes operators to guided procedures — diagnostic checks, step-by-step runbooks, and escalation gates when manual recovery is not enough.

**What we are testing:** Whether the assistant would get an L1/L2 support engineer to the right troubleshooting path on a live call.

**What we are not testing:** Whether the tester already knows the correct resolution.

### Knowledge assets in scope

| Asset | Count | Role at runtime |
|-------|-------|-----------------|
| Canonical runbooks | 399 | Step-by-step procedures surfaced inline |
| Incident playbooks (Prompt A) | 2 | Orchestration for cases 228086, 228723 |
| Incident playbooks (Prompt B) | 3 | Split flows where separable paths exist |
| Operational runbooks | 225 manual + 182 training | RAG retrieval for prompts without incident playbooks |

### Architecture (runtime)

```text
User symptom input
  → Intake (collect symptoms / impact)
  → Router / classifier (select playbook or procedure set)
  → Playbook nodes (diagnostic_decision | procedure_reference | escalation_gate | validation_gate)
  → Linked canonical runbooks (numbered steps, role gates, safety notes, images)
  → Validation / escalation
```

---

## Demo Session Format

| Field | Detail |
|-------|--------|
| **Round 1** | Week of July 13, 2026 |
| **Round 2** | Week of July 20, 2026 (refined scenarios + KPI review) |
| **Where** | Shared app link (to be distributed before sessions) |
| **Duration** | 45–60 minutes per session |
| **Participants** | L1/L2 support SMEs; 2–3 testers per session preferred |

### Session steps

1. Open the app and select **Prompt A** or **Prompt B** (playbook library toggle).
2. Enter a test prompt in natural language (copy/paste or paraphrase as on a support call).
3. Walk through the assistant's responses — answer clarifying questions, follow branches.
4. Score and take notes using the [scoring rubric](#scoring-rubric).

### Recommended pairing

- **Driver:** Operates the app, enters prompts, answers branch questions.
- **Scorer:** Records scores and notes without steering the interaction.

Run **each prompt under both A and B** where incident playbooks exist so we can compare extraction modes before locking a default.

---

## User Interaction Flow

```text
1. Open app link → select Prompt A or Prompt B (playbook library toggle)
2. Paste or type the test prompt (natural language, as on a support call)
3. Assistant responds with:
   - Symptom acknowledgment
   - 1–3 clarifying questions (if needed)
   - First diagnostic check OR linked procedure steps
4. Tester answers branch questions ("yes, AGVs are stopped" / "no alarms showing")
5. Assistant advances through playbook nodes → surfaces runbook steps
6. At escalation gates: assistant either continues L1 steps or surfaces escalation criteria
7. Tester records: routing correct? steps correct? escalation appropriate? A vs B preference?
```

### How prompts vs runbooks surface

| Layer | What it is | What the user sees |
|-------|------------|-------------------|
| **Prompt** | Symptom description entered by the tester | Natural language input only |
| **Playbook** | Orchestration graph (decision nodes, branches) | Not shown as a raw document; drives conversation flow |
| **Runbook** | Canonical procedure linked from a playbook node | Numbered steps, role, safety notes, HMI screenshots |

The user never selects a playbook or runbook directly. The router matches symptoms to the right workflow; playbook nodes pull in linked procedures as needed.

---

## Prompt A vs Prompt B Toggle

The toggle switches the **playbook orchestration layer**, not the underlying procedure library. Both modes use the same ~399 canonical runbooks.

| Mode | Behavior | Best when |
|------|----------|-----------|
| **Prompt A** | Exactly one playbook per incident | Incident has one dominant troubleshooting narrative |
| **Prompt B** | One or more playbooks when separable flows exist | Distinct entry symptoms or operational signatures should not be compressed |

### Pilot comparison (cases 228086 & 228723)

| Variant | Playbooks | Nodes | High-confidence links |
|---------|-----------|-------|----------------------|
| Prompt A | 2 | 13 | 93% |
| Prompt B | 3 | 19 | 95% |

### Example — Case 228086 (site-wide motion stop)

| Mode | Playbook structure |
|------|-------------------|
| **Prompt A** | One combined recovery playbook covering the full incident narrative |
| **Prompt B** | Split into: (1) Site motion stoppage / OptiSweep recovery, (2) WCSWebApp / Ignition error investigation |

### What to compare across A and B

- Routing clarity — simpler combined flow vs more precise split routing
- Question burden — fewer unnecessary clarifying questions
- Wrong-path rate — how often the same prompt sends the user down the wrong branch
- SME trust — which mode would you use on a live call?

---

## Test Prompts

Use these as written or paraphrase naturally. Reference case IDs are for traceability — testers do not need to mention them in the app.

---

### Prompt 1 — AGVs stopped, no alarms showing

**Category:** CAT-1 entry (symptom-based routing without explicit error code)

**Scenario:**
> AGVs are not moving. No faults on RMS. System shows normal operation mode.

**Symptoms:**
- AGVs halted mid-sort
- RMS showing no active alarms
- Normal operation mode displayed

**Reference cases:** 229488, 228086

**What this tests:** The most common P1 entry point. Validates symptom-based routing into CAT-1 without an explicit error code.

---

### Prompt 2 — Zone can't get a pair, robots routing to hospital

**Category:** Zone-specific / roster issue

**Scenario:**
> Zone 5 unable to get a pair. Every robot is routing to hospital after AMR swap.

**Symptoms:**
- Single zone affected
- AGV replacement preceded the issue
- All robots routing to hospital

**Reference case:** 228723

**What this tests:** Whether the tool correctly identifies an unmapped robot as the cause rather than a broader system failure.

---

### Prompt 3 — System stuck in bag-out, won't advance to shutdown

**Category:** State disambiguation

**Scenario:**
> System is stuck in bag-out after sort. Cannot proceed to shutdown.

**Symptoms:**
- Sort completed
- Bag-out state will not advance
- No service crash indicated

**Reference cases:** 229589, 218550, 219684

**What this tests:** Disambiguation between a bag-out state issue and a service failure — same surface symptom, different resolution path.

---

### Prompt 4 — Tote still showing in RMS after removal

**Category:** CAT-3 (restrained escalation)

**Scenario:**
> Tote was removed from the hospital screen but is still showing in RMS. Cannot reinduct to that spot.

**Symptoms:**
- Physical tote removed
- RMS record persists
- Spot blocked for new induction

**Reference cases:** 220884, 230250

**What this tests:** The CAT-3 path. Whether the tool surfaces Task Management cancellation steps without over-escalating.

---

### Prompt 5 — Tipper heartbeat timeout, AGVs holding totes

**Category:** CAT-1 (highest fidelity; escalation gating)

**Scenario:**
> AGVs lined up at tippers but not completing deliveries. Tippers showing heartbeat timeout. Hospital tote removal not executing.

**Symptoms:**
- AGVs holding totes at tipper stations
- Heartbeat timeout on all tippers
- Manual tote removal commands not executing

**Reference cases:** 229374, 229716, 229777

**What this tests:** The highest-fidelity CAT-1 case. Validates that the tool correctly gates on engineer remote access as the escalation condition.

---

## Success Criteria

Evaluate across four layers. A prompt passes only when all applicable layers meet the bar.

### Layer 1 — Intake & routing (symptom → right path)

| Criterion | Pass | Fail |
|-----------|------|------|
| **Symptom recognition** | Assistant acknowledges reported symptoms without requiring an error code or diagnosis | Asks for diagnosis first, or ignores key symptoms |
| **Playbook selection** | Routes to the correct incident playbook or operational procedure set | Wrong workflow, or generic response with no next step |
| **Disambiguation** (Prompt 3) | Distinguishes bag-out state stall from service failure; asks targeted clarifying questions | Treats all "stuck" symptoms as one path |
| **Scope accuracy** (Prompt 2) | Identifies zone-specific / roster cause, not site-wide failure | Over-escalates to full system restart |

### Layer 2 — Procedure surfacing (runbook quality)

| Criterion | Pass | Fail |
|-----------|------|------|
| **Step relevance** | Steps match the symptom context (e.g., hospital tote removal vs Ignition restart) | Steps from unrelated procedures |
| **Role gating** | L1 vs L2 steps labeled; unsafe L2 actions not pushed to L1 | Missing role context or unsafe guidance |
| **Evidence display** | Screenshots / HMI references shown where linked | Text-only with no visual anchors |
| **Source grounding** | Procedures traceable to manual, training, or incident evidence | Invented steps with no source |

### Layer 3 — Branching & escalation

| Criterion | Pass | Fail |
|-----------|------|------|
| **Decision branches** | After a check, offers healthy / unhealthy / inconclusive paths | Linear script with no branching |
| **Escalation gating** (Prompt 5) | Engineer remote access surfaced only when manual steps fail | Escalates too early, or never escalates |
| **CAT-3 restraint** (Prompt 4) | Task Management cancellation steps surfaced without over-escalation | Jumps to L2/engineer when L1 steps suffice |
| **Validation** | Confirms recovery criteria before closing (zone pairing restored, bag-out advanced, etc.) | Declares "fixed" without verification steps |

### Layer 4 — Prompt A vs Prompt B comparison

| Criterion | What to compare |
|-----------|-----------------|
| **Routing clarity** | Does A (one combined playbook) feel simpler? Does B (split flows) route more precisely? |
| **Question burden** | Fewer unnecessary clarifying questions in A vs B |
| **Wrong-path rate** | How often does each mode send the user down the wrong branch on the same prompt? |
| **SME preference** | Which mode would you trust on a live call? |

---

## Scoring Rubric

For each prompt (and A/B where applicable), record a score and notes. Notes are as important as the score — capture what worked, what didn't, and anything missing or unsafe.

### Score scale (1–5)

| Score | Meaning |
|-------|---------|
| **5** | Would use on a live support call today |
| **4** | Correct path; minor gaps (wording, missing image, extra question) |
| **3** | Right general area; wrong branch or missing key step |
| **2** | Wrong workflow selected |
| **1** | No actionable guidance |

### What to capture per prompt

| Field | Values / guidance |
|-------|-------------------|
| Prompt # | 1–5 |
| Playbook mode | A / B / N/A |
| Tester | Name |
| Routing | Score 1–5 |
| Procedures | Score 1–5 |
| Escalation | Score 1–5 |
| Usability | Score 1–5 |
| A vs B preference | A / B / No difference |
| **Notes** | What was right, what was wrong, missing steps, wrong HMI references, unsafe guidance, or anything you'd want fixed before trusting this on a call |

---

## Coverage & Expectations by Prompt

| Prompt | Playbook status (July 7) | Round 1 expectation | Round 2 expectation |
|--------|--------------------------|---------------------|-------------------|
| 1 — AGVs stopped | **228086** has A+B playbooks; 229488 reference only | Full playbook path; primary test | Re-test after SME corrections |
| 2 — Zone can't pair | **228723** has A+B playbooks | Full playbook path; primary test | Re-test after SME corrections |
| 3 — Bag-out stuck | No incident playbook yet | RAG retrieval + disambiguation from operational runbooks | Re-test with incident playbook if built |
| 4 — Tote in RMS | No incident playbook yet | CAT-3 restraint; Task Management steps from runbooks | Re-test with incident playbook if built |
| 5 — Tipper heartbeat | No incident playbook yet | Escalation gating from operational runbooks | Re-test with incident playbook if built |

**Round 1 focus:** Prompts 1–2 (full playbook orchestration).  
**Round 1 exploratory:** Prompts 3–5 (retrieval path).  
**Round 2:** All prompts; add playbooks for 3–5 if available.

---

## Timeline

| Date | Milestone |
|------|-----------|
| July 7, 2026 | Data validation session (runbooks + playbooks) |
| July 7–11 | SME corrections; finalize app link and scoring sheet |
| **Week of July 13** | **Round 1 prompt testing** |
| **Week of July 20** | **Round 2 prompt testing + KPI review** |
| Late July | Handoff to Ravi Mareddy & team |

---

## Related resources

- [SME review runbooks (408)](../sme_review_runbooks/)
- [Stage 8 playbooks — Prompt A](../sme_review_runbooks/stage_8_playbooks/prompt_a_one_per_incident/)
- [Stage 8 playbooks — Prompt B](../sme_review_runbooks/stage_8_playbooks/prompt_b_multi_flow/)
