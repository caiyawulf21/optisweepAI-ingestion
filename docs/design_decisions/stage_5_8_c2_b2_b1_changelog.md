# Stage 5/8 capability tags & linking — change log

Progress against [stage_8_capability_tags_and_linking_plan.md](stage_8_capability_tags_and_linking_plan.md).

## Initial goal (why this exists)

Day 2 produces many L2 **SSMS / WCS DB** runbooks. Playbook nodes historically only ask for **RMS / HMI**. Stage 8 retrieval then never admits SQL peers into the candidate set, so remote diagnostics stay **orphans**.

**Do not** hardcode “SQL ≡ RMS.” **Do** tag the same **capability** on both sides (`agv_active_errors`, …), name **access surfaces** (`rms_ui` vs `wcs_sql`), and let Stage 8 **multi-link** on capability overlap.

Three tracks:

1. **Track A** — taxonomy + Stage 6 runbook tags (+ Stage 7 / 6.5 pass-through) → **A3 Stage 8 overlap boost done**
2. **Track C** — Stage 5 playbooks *ask* for the remote job via `expects_*` (no SQL text in nodes) → **C-regen done (backfill)**
3. **Track B** — SME linking quality (evidence, hard-reject, gaps, regen) → **B3–B5 next**

Ontology catalogs / Stage 6 mini-RAG (separate design: [ontology_surface_catalogs_and_stage6_rag.md](ontology_surface_catalogs_and_stage6_rag.md)) support **richer Stage 6 enrichment** so tags and runbook steps stay source-grounded — they do **not** replace A3.

---

## Status board

| Item | Status | Notes |
| --- | --- | --- |
| **A0** Taxonomy JSON | Done | `docs/ontology/taxonomy/` — now **0.4** + deep `docs/ontology/catalogs/` (SQL fields, capability cards, surface catalogs) |
| **C1** Stage 5 vocab + SQL ban rewrite | Done | Surface yes, statements no |
| **C2** Stage 5 `expects_*` | Done | Emit path live; **existing playbooks need C-regen** to gain fields |
| **B1** Attainable-evidence contract | Done | Who / tool_or_view / signal |
| **B2** Hard-reject / confidence caps | Done | Recovery-prep reject; pairing/hospital/roster → low |
| **A1** Stage 6 LLM tagging | Done | Prompts + taxonomy appendix + normalize + review MD |
| **A1b** Tag backfill | Done | ~409 Stage 6 finalized; Active AGV SQL → `agv_active_errors` + `wcs_sql` + `L2_support` |
| **A2** Stage 7 + 6.5 cards | Done | `union_runbook_tags`; retrieval cards + embed text carry tags |
| **Ontology 0.4 / mini-RAG** | Done (wired) | Surface catalogs + capability cards + `ontology_rag.py` — Stage 5 ≤2 surface/capability snippets; Stage 6 ≤3 deep model/activity snippets in packets |
| **Day 1/2 training ingest** | Day1/2 OpenAI done; shared retry | Day2 OpenAI **112/112**. Day1 OpenAI **150/150**, Stage 8 **7833** links. Shared 6.5 failed: mini chat env overwrote `AZURE_OPENAI_ENDPOINT` → embedding `DeploymentNotFound`. Retrying shared 6.5–10 with `.env` embedding endpoint (`data/output/regen_shared_65_10.log`). |
| **A3** Stage 8 capability-overlap boost | **Done** | Overlap boost + role/surface companions + prompt policy; RMS+SSMS multi-link tests |
| **C-regen** Playbook `expects_*` | **Done** | Backfill upgraded: 46/46 expects nodes; dual `rms_ui`+`wcs_sql` on remote fleet/AGV caps; L1/L2 audience |
| **B3** Gap messaging | **Done** | Capability-tagged actionable evidence-path gaps; node `catalog_gaps` for unresolved |
| **B4** Branch graph cleanup | **Done** | Drop empty/duplicate playbook branch rows; proceed/escalate convention in review |
| **B5** Full Stage 8 regen + SME pack | **Done** | 11 playbooks (4 cases × A/B); `sme_review_runbooks/stage_8_playbooks_capability_tags/`; RMS+SSMS multilink spot-checked |

---

## Week-now cut (landed): C2 + B2 + B1

| Item | What landed |
| --- | --- |
| **C2** | Diagnostic/branching/validation nodes emit `expects_capability`, `expects_surface`, `preferred_audience` (taxonomy-constrained) |
| **B2** | Recovery-prep hard-filtered from check nodes; pairing/hospital/roster gaps cap confidence to **low**; empty candidate set → no link |
| **B1** | Stage 5 prompt contract + Stage 8 `decision_outcomes` gain `observer` + `tool_or_view` (incl. WCS/SSMS when applicable) |

### Code / prompt touchpoints

**C2 — Stage 5 expects fields**

- Normalize + soft warnings: `incidenceknowledgeingestion/.../stage5_runbook_candidates.py`
- Prompts A/B: expects tags section + JSON example fields
- Stage 5 review MD: Expects column
- Retrieval cards carry expects into embed text: `shared_pipeline_stages/stage_8/playbook_retrieval.py`, `schemas.py`
- Taxonomy loader: `shared_pipeline_stages/taxonomy.py`
- Tests: `incidenceknowledgeingestion/tests/test_stage5_playbook_expects_fields.py`

**B2 — Linking guards**

- Severe gap phrases in `_cap_confidence_from_gaps` (`stage_8/normalize.py`)
- Existing hard reject in `filter_intent_compatible_matches` unchanged
- Tests: recovery-prep-only → `[]`; pairing gap → confidence `low`

**B1 — Attainable evidence**

- Stage 5 prompts: attainable-evidence on `expected_or_observed_result`
- Stage 8 outcomes: `observer`, `tool_or_view`
- Review MD/HTML show observer/tool on outcomes

---

## Operational Stage 5 follow-up (role matrix + SQL gating)

| Stage | Role matrix | SQL / DB gating | Action taken |
| --- | --- | --- | --- |
| Ops Stage 5 discovery / backfill | Inline matrix | Source-backed SSMS/Helix diagnostics **are** candidates | Clarified prompts; no invented SELECT |
| Ops Stage 5 `_role_from_title` | Was defaulting to `operator` | SQL titles → operator (matrix: **No access**) | Map sql/ssms/database → `L2_support`; Event Viewer/API/Ignition → `L1_support` |
| Ops Stage 6 | Matrix + taxonomy appendix | Capability tags | A1 |
| Incident Stage 5 **runbook** (not playbook) | Matrix present | Read-only SSMS candidates valid | Prompt note |

Playbooks name the **surface** only; operational runbooks **may include source-backed SQL** in Stage 6 steps.

---

## A1 / A1b / A2 — Stage 6 tags through the pool (landed)

| Item | What landed |
| --- | --- |
| **A1** | Structure ref + ops/incident prompts; taxonomy appendix; `normalize_runbook_tags`; SME-visible Stage 6/7 review fields |
| **A1b** | `shared_pipeline_stages/scripts/backfill_runbook_capability_tags.py` |
| **A2** | Stage 7 `union_runbook_tags`; Stage 6.5 `RetrievalCard` → `retrieval_cards.json` + `retrieval_text` |

**Code:** `shared_pipeline_stages/runbook_tags.py`, `stage_prompts.py`, `stage_6_5/schemas.py` + `retrieval_card.py`

---

## Ontology enrichment (support for Stage 6 — landed)

Machine-retrievable system docs under `docs/ontology/catalogs/` (schema 0.4):

- Shared surface catalog shape (`surface_catalog_schema.json`) + all access surfaces (RMS, SQL, API/Apidog, Ignition, Stunnel, Event Viewer, Aveva, tipper WebVisu, hospital, ACB, site_interview, physical_floor)
- Rich **capability cards** (`capability_catalog.json`) linking surfaces / DBs / APIs / activities / observables
- Deep **wcs_sql** field catalog (Day2 OCR/transcript + AGV SQL guide)
- Tipper **WebVisu/VISU** screens from OM §4.1.2.1–6
- Mini-RAG helper `shared_pipeline_stages/ontology_rag.py` wired into Stage 5/6 packets (`ontology_snippets`)

Design: [ontology_surface_catalogs_and_stage6_rag.md](ontology_surface_catalogs_and_stage6_rag.md)

---

## Still next (back to linking goal)

1. Optional SME gap runbooks for thin catalog areas (Event Viewer, dedicated pairing/hospital remote confirm)
2. **Training quality regen** — Stage 2 prepare → 5 → 6 → 8 (+ shared) for Day1/2 after packet/linker hygiene (as needed)


---

## Ops log (2026-08-03) — B5

| Item | Result |
| --- | --- |
| **Stage 8 finalize** | `--llm` cases 218550/223554/228086/228723 → **11 playbooks**; ~10 min (`data/output/regen_stage8_b5.log`) |
| **SME export** | `sme_review_runbooks/stage_8_playbooks_capability_tags/` (+ refreshed `stage_8_playbooks_linking_guards/`) |
| **Spot-check** | ≥5 RMS+SSMS multi-link nodes (L1 `rms_ui` + L2 `wcs_sql`); 228723 B branch graph clean; Event Viewer playbook stays unresolved with catalog gaps |

## Ops log (2026-08-03) — B3 + B4

| Item | Result |
| --- | --- |
| **B3 gap messaging** | `capability_corroboration_gaps` / `unresolved_catalog_gaps`; review shows catalog gaps; confidence caps updated for new phrases |
| **B4 branch cleanup** | `sanitize_playbook_branch_graph` + review `_branch_rows` dedupe; procedure/escalation “proceed / escalate” convention |
| **Tests** | Stage 8 suite 31 passed |

## Ops log (2026-08-03) — C-regen + A3

| Item | Result |
| --- | --- |
| **C-regen upgrade** | `scripts/backfill_playbook_expects.py`: dual `rms_ui`+`wcs_sql` on remote-attainable caps; fill missing capability; L1/L2 audience. 8 files, 23 nodes changed; **46/46** expects nodes complete |
| **A3** | `link_scoring.capability_overlap_adjustment`; retrieval rescoring in `search_for_node`; capability×surface/role companions in `normalize.py`; role/surface policy in Stage 8 prompt. Tests: 29 passed |

## Ops log (2025-07-31)

| Item | Result |
| --- | --- |
| **Stage 6 image dedupe / strip rule** | Shipped; `test_stage6_runbook_finalization.py` — 8 passed |
| **C-regen (`expects_*` backfill)** | 8 playbook files; 46 nodes touched/changed (no `--force`) |
| **Day1/Day2 regen** | Failed twice (2025-07-31): --max-workers 1 + 3m cooldown; Day1 Stage5 5 then 2 candidates (80x429); Stage6 0; stopped at Day1 Stage8. Restored Day1 stage5/6 from HEAD (182). Day2 not in git. |
| **Code fix** | `stage5_runbook_candidates.py`: `lineage` in `repair_missing_sections_with_llm` |

## Do not regress

- No SQL statements in playbook nodes (surface name only)
- No hardcoded WCS↔RMS peer lists
- `operator` ≠ FORTNA; soft stop ≠ E-stop; AVEVA = site only
- Constrained taxonomy IDs only for tags / `expects_*`; catalogs are reference-only

---

## Ops — 2026-07-31 regen switch (DeepSeek → OpenAI)

- Killed `regen_day1_day2_stage5_6.py` (PID 63160 + Stage 6 child 58288) after Day1 Stage 6 wipe + 429 backoff.
- Restored **Day1 stage_6 only** from HEAD (182 finalized runbooks); kept DeepSeek Stage 5 until OpenAI overwrote it.
- Added `scripts/regen_day1_openai.py` (mirror of `regen_day2_openai.py`; runs shared 6.5–10 when Day2 Stage 8 is complete).
- **Day2 OpenAI** (`data/output/regen_day2_openai.log`): Stage 5 112 / Stage 6 112 / Stage 8 26619 links.
- **Day1 OpenAI** (`data/output/regen_day1_openai.log`): Stage 5 **150 candidates, 0 failed**; Stage 6+8 in flight (PID via background shell).
