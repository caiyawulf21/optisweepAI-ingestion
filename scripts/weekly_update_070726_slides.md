# Optisweep.ai Weekly Update — July 7, 2026

---

## Slide 1 — Title

**Optisweep.ai Weekly Update**

July 7th, 2026

---

## Slide 2 — Agenda

- This Week: Data Validation
- Playbook Workflow — Prompt A vs Prompt B
- Pipeline Progress
- Post-Review Plan & Milestones
- Discussion

---

## Slide 3 — This Week: Data Validation Session

**This Week: Data Validation Session — Tuesday, July 7**

### Objective

Validate the quality, credibility, and completeness of generated knowledge assets before any prompt testing in the application.

### What we are reviewing

- Runbooks and procedures from the O&M Manual, Day 1 training video, and historical incident cases (228086, 228723)
- Incident playbooks (workflows) in both **Prompt A** and **Prompt B** variants — linked to canonical runbooks with decision branches

### What this session is not

I will not be demonstrating the troubleshooting application. This is a knowledge-asset review only.

### Pre-read

- Case 228086 example runbook: https://github.com/caiyawulf21/optisweepAI-ingestion/tree/master/sme_review_runbooks/case_228086
- All runbooks (408): https://github.com/caiyawulf21/optisweepAI-ingestion/tree/master/sme_review_runbooks
- Stage 8 playbooks: `shared_pipeline_stages/data/output/shared/stage_8_finalized_playbooks/`

---

## Slide 4 — Playbook Workflow: Why Prompt A & Prompt B

### Why test two extraction modes?

Incidents are historical records — not every case maps to a single troubleshooting path. A case may have:

- one clear resolution path
- multiple separable troubleshooting paths
- a main issue with downstream recovery steps

**Playbooks are runtime orchestration assets, not case summaries.**

At runtime, users describe symptoms ("robots not moving," "HMI shows question marks") — the assistant must route to the right workflow without knowing the diagnosis upfront.

| Risk | What happens |
|------|--------------|
| Playbooks too **broad** | Vague guidance, wrong routing, unnecessary questions |
| Playbooks too **narrow** | Too many overlapping workflows, harder to select the right path |

We run both modes in parallel so SMEs can compare quality before we lock in a default.

### Prompt A — One playbook per incident (MVP default)

- Exactly **one** playbook candidate per incident
- Simpler routing, lower review burden, cleaner symptom-to-workflow mapping
- Best when an incident has one dominant troubleshooting narrative

### Prompt B — Multi-flow when separable

- **One or more** playbook candidates per incident
- Creates multiple playbooks only when clearly separable flows exist (different entry symptoms or operational signatures)
- Best when an incident contains distinct troubleshooting paths that should not be compressed

### Pilot comparison — cases 228086 & 228723

| Variant | Playbooks | Nodes | High-confidence links |
|---------|-----------|-------|----------------------|
| Prompt A | 2 | 13 | 93% |
| Prompt B | 3 | 19 | 95% |

**Example — case 228086 (site-wide motion stop):**

- **Prompt A** → one combined recovery playbook covering the full incident narrative
- **Prompt B** → splits into:
  1. Site motion stoppage / OptiSweep recovery
  2. WCSWebApp / Ignition error investigation

**Tomorrow we need SME input:** which extraction produces more accurate, usable workflows?

**After data review** we will select a playbook extraction mode, choose representative cases, and define the prompts to test in the application during the weeks of July 13 and July 20.

---

## Slide 5 — Ingestion Pipeline Progress Tracker

### Operational Knowledge

| Deliverable | Progress |
|---|---|
| Manual Ingestion Framework | 100% |
| Multi-Source Ingestion Architecture | 95% |
| Video Ingestion Path | 90% |
| Operational Context Generation | 100% |
| Runbook Candidate Generation | 100% |
| Canonical Runbook Library | 85% |
| Knowledge Relationships | 75% |
| Validation & Quality Controls | 65% |
| Production-Ready Knowledge Assets | 55% |

**Post-Data-Review Activities**

- Incorporate SME feedback from July 7 review
- Select playbook extraction mode (Prompt A vs B) based on review
- Choose representative incident cases and demo prompts for testing
- Load validated knowledge into the troubleshooting application
- End-to-end prompt testing — weeks of July 13 & July 20

**Data Review:** July 7 | **Case & Prompt Selection:** July 7–11 | **App Testing:** Weeks of July 13 & July 20

### Incidence Knowledge

| Phase | Progress |
|---|---|
| Architecture & Design | 100% |
| Shared Pipeline Components Available | 90% |
| Incident Source Package + OCR Extraction | 100% |
| Incident Artifact Enrichment | 100% |
| Canonical Incident + Timeline Development | 40% |
| Runbook + Playbook Generation | 85% |
| Overall Incident Pipeline | 70% |

---

## Slide 6 — Recent Changes & Post-Review Plan

### Recent pipeline changes

**Shared synthesis stages (6.5 → 8) now operational across all three source types:**

- **Stage 6.5:** Cross-source runbook pool — 403 candidates embedded and clustered (manual + training + incident)
- **Stage 7:** Canonical runbook merge — 399 canonical runbooks with SME review Markdown; LLM merge only on approved clusters
- **Stage 8:** Playbook-to-runbook linking — finalized playbooks with decision branches, linked procedures, and HTML review outputs

**Other changes since last update:**

- Video ingestion path added — training recordings feed the same pipeline as manuals
- Human-reviewable Markdown + HTML outputs for runbooks and playbooks (not just JSON)
- Dual Prompt A/B tracks run end-to-end through Stage 5 extraction and Stage 8 linking with comparison metrics
- 408 SME-reviewable runbooks published to GitHub (225 manual, 182 training, 1 incident)

### After data review (July 7–11)

1. Incorporate SME corrections into knowledge assets
2. Decide Prompt A vs Prompt B as the default extraction mode (or case-by-case rules)
3. **Select a small set of representative incident cases and demonstration prompts for application testing**
4. Load validated knowledge into the troubleshooting app
5. Prompt testing sessions — weeks of July 13 and July 20 (retrieval, workflow selection, troubleshooting guidance, UX)

### Discussion

- Biweekly meeting cadence during transition
- Handoff target: Ravi Mareddy & team
- Please bring operational corrections, gap notes, and preference on playbook extraction quality

---

## Slide 7 — Project Schedule & Near-Term Milestones

| Timeline | Milestone | Key Deliverables |
|---|---|---|
| Week of 7/7 | Data Validation Session | Review runbooks & playbooks (Prompt A + B); collect SME feedback on quality and extraction mode |
| 7/7 – 7/11 | Case & Prompt Selection | Apply SME corrections; choose extraction mode, incident cases, and demo prompts for app testing |
| Week of 7/13 | Prompt Testing — Round 1 | Selected cases + prompts in app: retrieval quality, workflow routing, troubleshooting guidance |
| Week of 7/20 | Prompt Testing — Round 2 | Refined scenarios based on Round 1; KPI discussion; gap analysis |
| Late July | Handoff Preparation | Documentation, training, transfer to Ravi Mareddy & team |
| End of effort | Final Deliverables | Reusable ingestion pipeline, app codebase, validated knowledge assets |

---

## Slide 8 — Pipeline Stages Reference

→ Stage 1: Source bundle extraction (Deterministic, PyMuPDF)
→ Stage 2: Source artifact and image extraction (Deterministic, PyMuPDF)
→ Stage 3: Source artifact enrichment (LLM Assisted)
→ Stage 4: Operational context extraction (LLM Assisted)
→ Stage 5: Runbook candidate discovery (LLM Assisted)
→ Stage 6: Candidate pool generation (Deterministic)
→ Stage 7: Canonical runbook drafting and merging (LLM Assisted)
→ **Stage 8: Playbook finalization & runbook linking (LLM Assisted)** — links incident playbook nodes to canonical runbooks; runs Prompt A and Prompt B in parallel
→ Stage 9: Validation and repair
→ Stage 10: Vector embedding generation
→ Stage 11: Cosmos DB publishing and manifest
→ Stage 12: LangGraph orchestration and Cosmos DB publishing
→ Stage 13: RAG retrieval in the OptiSweep AI troubleshooting app

**Inputs:** PDFs, slides (as PDFs) with transcripts, videos

---

## Slide 9 — Project Codebases

**Data Ingestion Pipeline** — 2 LangGraph pipelines (Operational + Incidence)

**Optisweep Troubleshooting App** — backend orchestration agent + UI

**Optisweep Ingestion Pipeline:** https://github.com/caiyawulf21/optisweepAI-ingestion

**Why:** Original data sources are not directly usable by a RAG assistant unless broken into reliable, source-linked records. A standardized repeatable ingestion pipeline allows Optisweep knowledge to expand as the product matures.

**What it produces:** Stable operational information chunks, enriched visual artifacts, runbooks, and incident playbooks.
