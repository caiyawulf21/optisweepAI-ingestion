# Stage 8 Capability Tags & Linking Quality Plan

Vetting notes and implementation plan for Stage 8 playbook–runbook linking:
capability / surface / role tags (Track A) and the SME-quality audit list (Track B).

Read alongside:

- [Stage 8 — Playbook Finalization](stage_8_playbook_finalization.md) (especially P1→P3 / knowledge-graph enrichment)
- [Stage 8 Link Scoring And Confidence](stage_8_link_scoring_and_confidence.md)
- [Stage 5–7 Runbook Architecture](stage_5_7_runbook_architecture.md)
- [Support Roles, Components, and Runbook Adjacency](../ontology/support_roles_components_and_adjacency.md) — locked org model: `operator` = site/customer (not FORTNA); L1/L2/L3/L4 all remote
- [SME Component Access Matrix](sme_component_access_matrix.md) / canonical prompt `[role_component_access_matrix.md](../../stage_prompts/shared/role_component_access_matrix.md)`

## Bottom line

Three related problems, three tracks:

1. **Tag model (capability / surface / role)** — fixes *why* remote SQL never competes with RMS UI in Stage 8 scoring.
2. **Stage 5 playbook shape** — fixes *why playbooks never ask* for SSMS/WCS DB checks (today SQL is banned/escalation-only).
3. **Audit list (#1–#5)** — fixes *what* Stage 8 ships to SMEs when linking is weak or wrong.

Day 2 training will produce many L2 SSMS runbooks. Tags alone are not enough if Stage 5 nodes still only name RMS/HMI. Do **not** hardcode “SQL ≡ RMS.” Do **not** build a separate adjacency agent. Keep playbook↔procedure separation (no SQL text in nodes), but **name the remote diagnostic j ob + surface** so Stage 8 can multi-link.

### Roles / access matrix (landed)

Org model and prompt wiring for **who may execute** is already in the repo (separate from Stage 8 linking):


| Artifact                        | Path                                                                                                                 |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Fuller roles + adjacency design | `[docs/ontology/support_roles_components_and_adjacency.md](../ontology/support_roles_components_and_adjacency.md)`   |
| SME Teams sheet                 | `[docs/design_decisions/sme_component_access_matrix.md](sme_component_access_matrix.md)`                             |
| Canonical prompt snippet        | `[stage_prompts/shared/role_component_access_matrix.md](../../stage_prompts/shared/role_component_access_matrix.md)` |


**Locked rules:** `operator` = customer/client (not FORTNA); L1/L2/L3/L4 all remote on Zscaler; physical E-stop = operator only; RMS soft stop = L2/L3 only (not E-stop); AVEVA = site only. Stage 6/7 append the matrix at runtime; incident/ops Stage 5 have inline matrix + role guidance. **Stage 8 does not emit roles** (no role output fields) — it should later *consume* `role_required` / `allowed_roles` for match/block once tags exist.

**Open SME:** Building/ACB L1/L2 access?; confirm Zscaler + soft-stop wording with CSE.

---

## How Stage 8 works today (simple)

Stage 8 is **retrieval-first, then LLM** — not retrieval alone.

1. Embed each playbook node placeholder → search the full Stage 7 runbook pool.
2. Deterministic filters/boosts in `link_scoring.py` / `normalize.py` (RMS-heavy today).
3. LLM gets only those candidates + `stage_prompts/stage_8/stage8_playbook_linking_prompt.md`.
4. Prompt already has advisory component/symptom tables — but they treat RMS as the AGV-status surface and never describe remote WCS SQL as equivalent.

So: changing the prompt helps selection among retrieved candidates. It **cannot** attach a SQL runbook if scoring never admits it into the candidate set. Hardcoded “WCS ↔ RMS” peer rules would paper over that; **tags are the right lever**.

---

## Recommended model (no adjacency hardcoding)

Encode **capability + surface + role**, not “this runbook is adjacent to that one.”


| Tag dimension         | Examples                                                     | Purpose                            |
| --------------------- | ------------------------------------------------------------ | ---------------------------------- |
| `capability` / checks | `agv_active_errors`, `device_roster_state`, `service_health` | Same job across tools              |
| `access_surface`      | `rms_ui`, `wcs_sql`, `hospital_hmi`, `event_viewer`          | How you do the job                 |
| `audience_role`       | `operator`, `L2_support`, `on_site`, `remote`                | Who can execute                    |
| `failure_pattern`     | `site_stoppage`, `hospital_diversion`, `pairing_failure`     | When it’s relevant                 |
| `procedure_intent`    | `observe`, `diagnose`, `recover`, `validate`                 | Already partly in `procedure_type` |


Stage 8 links when:

- `node.expects_capability ∩ runbook.capability`
- Optionally prefers runbooks whose `audience_role` matches the support context (remote triage → prefer remote/L2 surfaces; site walkthrough → prefer `rms_ui`).

Example: the AGV SQL runbook and `proc_check_overall_system_rms_…` share `agv_active_errors`; they differ on surface/role. That is the equivalence — learned from tags, not a hardcoded peer list.

This is the design doc’s **P1→P3** path, with role/surface made first-class.

### Where to put the “agent that knows remote vs operator”

Do not invent a separate costly “adjacency agent” later in the graph. Put a structured enrichment step where runbooks are born:


| Stage                                               | Emit                                                                                                                |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Operational/training Stage 6 (and incident Stage 6) | `capability_tags`, `access_surface`, `audience_roles`, `failure_pattern_tags` on each runbook                       |
| Incident Stage 5 playbook nodes                     | `expects_capability`, `expects_surface` (or “any surface for this capability”), `preferred_audience`                |
| Shared Stage 7                                      | Preserve tags on canonical records (merge-safe)                                                                     |
| Shared Stage 8                                      | Retrieval boost on capability overlap; prompt uses tags + a short role/surface policy (not a giant component table) |


One controlled LLM pass at Stage 6 scales with new training video: every new DB/remote procedure gets tags once, then Stage 8 stays cheaper (retrieval + light linking).

### Stage 8 prompt policy (not giant tables)

- Same capability + different `access_surface` ⇒ valid multi-link (remote + on-site)
- Prefer `audience_role` compatible with how the node will be executed
- Do not substitute a different capability just because text is similar (HMI bump screen ≠ active-error roster)

### ML vs LLM for tagging


| Approach                                     | When it wins                                                                                         | Cost / risk                                                           |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **LLM tagging at Stage 6 (recommended now)** | Taxonomy is small (~15–30 capabilities, ~10 surfaces, few roles); need explainability for SME review | Tokens per runbook once; cheap vs Stage 8 re-link of whole corpus     |
| Separate “adjacency subagent”                | Only if you refuse tags and want free-form “what’s equivalent?”                                      | Expensive, unstable, hard to test; recreates hardcoding in prose      |
| Classic ML classifier                        | After hundreds of SME-approved tagged runbooks                                                       | Needs labeled data you don’t have yet; worse cold-start for new video |


**Practical path:**

1. **Now:** frozen taxonomy JSON + Stage 6 LLM fills tags (constrained to the vocab) + SME-visible fields in review MD
2. **Stage 8:** capability-overlap retrieval boost + slim role/surface policy; dial back regex RMS-only companion logic over time
3. **Later (optional):** train a small classifier (or embedding→tag head) on approved tags to cut Stage 6 token cost — same schema, swap the producer

Role matching is not a separate ML app: it’s `audience_roles` + node `preferred_audience`, with `support_safe` / `role_required` already as seeds.

### Ahead of the next training video

Tag enrichment should land **before or with** that ingest, otherwise Stage 8 will keep preferring RMS UI runbooks for AGV status nodes.

For DB/remote procedures in the video, Stage 6 prompts should ask explicitly:

- What capability does this check/change?
- What surface (SQL, API, RMS, HMI, …)?
- Who can run it (remote L2 vs on-site operator)?
- What failure patterns is it for?

Then AGV SQL and future tipper/WCS queries attach by shared capability, not by special-casing one document.

### What not to do

- Hardcode “SQL ≡ RMS” pairs in `normalize.py`
- Rely on Stage 8 prompt tables alone (they’re already large and still RMS-centric)
- Build a full KG store or custom ML model before the taxonomy + Stage 6 tags exist
- Expect embeddings alone to learn “remote equivalent of operator view” without tags — they optimize lexical/semantic similarity to placeholders that say “RMS”

### Suggested sequence (tags track)

1. Define the taxonomy (capabilities / surfaces / roles / failure patterns) as **data**, not code constants sprinkled in scorers
2. Stage 6 (+ backfill script for existing canonical runbooks, including `active_agv_error_query_1`)
3. Stage 5 node `expects`_* on next playbook regen (or light backfill)
4. Stage 8: overlap boost + role/surface policy in prompt; shrink regex guards
5. Re-run Stage 8 after the training video lands so new remote/DB runbooks participate

---

## Track A — taxonomy + Stage 6 tags (vetting)


|                          |                                                                                                                                                                                                                                                                                                                                                                                                           |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Verdict**              | Strong yes. Matches P1→P3; surface/role make remote≡operator learnable.                                                                                                                                                                                                                                                                                                                                   |
| **Opportunity**          | New DB/video procedures attach by shared job (`agv_active_errors`), not title similarity to “RMS”. Stage 8 stays cheaper than a linking/adjacency agent.                                                                                                                                                                                                                                                  |
| **Risk**                 | Taxonomy drift; bad LLM tags; Stage 7 merge must preserve tags; backfill of old runbooks is mandatory or new tags only help new docs.                                                                                                                                                                                                                                                                     |
| **Expected outcome**     | Multi-link remote + on-site for same capability; fewer silent wrong-domain “nearest AGV” links; SME can audit tags in review MD.                                                                                                                                                                                                                                                                          |
| **Architecture / tools** | New `taxonomy/*.json` (data, not scorer constants); Stage 5/6 schemas + prompts; Stage 6.5 cards include tags; Stage 7 merge-safe fields; Stage 8 retrieval boost + slim role/surface policy in prompt; optional backfill script for existing canonicals (incl. `active_agv_error_query_1`). Review MD/HTML show tags. Dial down RMS-only companion regex over time — don’t delete all guards on day one. |


**Defer:** classic ML classifier, KG store, adjacency subagent. Role *matching* is just `audience_roles` ∩ node `preferred_audience` (+ existing `support_safe` / `role_required`) — not a new ML app.

---

## Track B — linking quality audit (order 1→5)

Focused change list from playbook SME/audit review. Role linking is deferred as a note only.

### 1. Decision outcomes → attainable evidence (do first)

**Goal:** Every `diagnostic_decision`, `branching_condition`, and `validation_gate` outcome states how a tech decides healthy / unhealthy / inconclusive.

For each outcome, require:

- Who observes (remote vs site)
- Tool/view (RMS page, Event Viewer, HMI, API, site interview)
- Concrete healthy / unhealthy signal
- What makes it inconclusive

**Where:**

- Stage 5 playbook candidate prompt (outcome/evidence contract)
- Stage 8 outcome normalization / review markdown (don’t emit label-only descriptors)
- Re-render affected SME review playbooks after regen

**Acceptance:** No outcome like “matches the target pattern” without a named observable. Missing outcome blocks (e.g. 228723 B N4/N6) filled or explicitly marked N/A for procedure/escalation-only nodes.


|                 |                                                                                                                |
| --------------- | -------------------------------------------------------------------------------------------------------------- |
| **Verdict**     | Do first for SME trust. Schema already has `observable_signal`; enforcement is soft.                           |
| **Opportunity** | Tech can decide healthy/unhealthy/inconclusive from named views, not vague “matches pattern.”                  |
| **Risk**        | Prompt alone won’t fill catalog gaps; some nodes stay N/A (procedure/escalation-only) — that’s OK if explicit. |
| **Outcome**     | Review MDs usable for walkthrough; fewer empty outcome blocks.                                                 |
| **Pipeline**    | Stage 5 playbook prompt + Stage 8 normalize/review; regenerate affected playbooks. No Cosmos change yet.       |


### 2. Stop attaching known-wrong runbooks as “how to”

**Goal:** Gaps stay gaps; don’t ship misleading primary links.

- Keep / enforce hard reject of recovery-prep for check/symptom nodes that don’t mention grid entry (already in code; baseline artifacts are stale)
- If no corroborating runbook survives filters → no link (or explicit gap placeholder), not nearest AGV neighbor
- Cap confidence when gaps include pairing/hospital/roster misses so “high” can’t stick on a soft mismatch

**Acceptance:** Node 1 on 228723 does not link `proc_gather_required_fault_information_before_entering_the_grid`_*. Same for other check nodes currently stuck on that procedure.


|                 |                                                                                                                                              |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Verdict**     | Do next; code already has recovery-prep reject — baselines/artifacts look stale.                                                             |
| **Opportunity** | Gaps stay honest; Node 1 on 228723 stops linking grid-entry prep.                                                                            |
| **Risk**        | More `unresolved` / empty links → SMEs may think “pipeline broke”; communicate as intentional. Cap “high” when pairing/hospital gaps remain. |
| **Outcome**     | No misleading primary how-to; confidence honest.                                                                                             |
| **Pipeline**    | Tighten `filter_intent_compatible_matches` / confidence caps; refresh Stage 8 outputs; tests on known bad pairs.                             |


### 3. Symptom-confirm & validation nodes need real corroboration capability

**Goal:** Catalog or honest gap for what’s actually missing.

- Prefer fleet/RMS status checks only when they can corroborate the node’s observables
- If catalog can’t show pairing failure or hospital diversion → surface a specific gap (questions to site + RMS/DB views), don’t substitute BUMP codes or szonestaging
- Optionally draft SME-authored gap runbooks for: remote pairing/hospital pattern confirm; on-site grid entry (separate from pattern confirm)

**Acceptance:** Gaps name the missing evidence path; linked runbooks that remain are at least same diagnostic domain.


|                 |                                                                                                   |
| --------------- | ------------------------------------------------------------------------------------------------- |
| **Verdict**     | Right goal; **needs tags (Track A) or you’ll keep regex-guessing**. Short-term: gap messaging.    |
| **Opportunity** | Named missing paths (pairing/hospital remote confirm) instead of BUMP / szonestaging substitutes. |
| **Risk**        | Without catalog content (or SME draft gap runbooks), links stay sparse — correct but incomplete.  |
| **Outcome**     | Remaining links same diagnostic domain; gaps actionable.                                          |
| **Pipeline**    | Stage 8 gap strings + optional SME gap runbooks; full fix after capability tags.                  |


### 4. Clean up branch graph / outcome completeness

- Fix duplicate / empty `from_node` rows in branch graphs (seen on 228723 B)
- Procedure-reference / escalation nodes: either real Decision Outcomes or a clear “no branch outcomes — proceed / escalate” convention so review isn’t inconsistent


|                 |                                                                                    |
| --------------- | ---------------------------------------------------------------------------------- |
| **Verdict**     | Hygiene; do with regen, not as a big design.                                       |
| **Opportunity** | Cleaner review; consistent convention for escalation-only nodes.                   |
| **Risk**        | Low if scoped to known bad graphs (e.g. 228723 B).                                 |
| **Outcome**     | No duplicate/empty `from_node` rows; clear “no branch outcomes” where appropriate. |
| **Pipeline**    | Stage 8 branch validation + Stage 5 branch_hints quality.                          |


### 5. Re-run & refresh review artifacts

- Regenerate Stage 8 for the playbook set after 1–4
- Diff baseline `stage_8_playbooks` vs linking-guards behavior; publish the guarded/regenerated set for SME review
- Spot-check all five playbooks against the attainable-evidence bar


|                 |                                                                         |
| --------------- | ----------------------------------------------------------------------- |
| **Verdict**     | Mandatory after 1–4 (and after tags once they exist).                   |
| **Opportunity** | Diff vs baseline; publish guarded set for SME.                          |
| **Risk**        | Re-running without tag backfill still RMS-biases new video DB runbooks. |
| **Outcome**     | SME review pack that matches current guards.                            |
| **Pipeline**    | Shared Stage 8 over playbook set; spot-check five playbooks.            |


### Later (once role linking exists)

Prefer/require intersection of node `allowed_roles` and runbook `role_required`, and block physical grid-entry / on-floor procedures from remote diagnostic nodes unless the node explicitly needs grid entry. That reinforces #2 for this failure mode; it does **not** replace #1 (evidence text) or missing catalog content.

**Suggested order:** 1 → 2 → 3 → 4 → 5. Role linking after the role model exists.

---

## Day 2 training vs Stage 5 (why orphans get worse)

Day 2 hits this harder than the single AGV SQL guide. The OM manual has almost no database/SQL content and produced **no** DB runbooks. Day 1 filled playbooks with RMS/API UI checks; Day 2 is the remote SSMS layer those playbooks never ask for.

### Corpus today


| Source               | What it teaches                    | What playbooks ask for today                     | Link outcome                  |
| -------------------- | ---------------------------------- | ------------------------------------------------ | ----------------------------- |
| Day 1 video          | RMS / Aveva API / overview screens | “Inspect RMS / fleet status / active AGV faults” | Links well                    |
| OM manual            | Operator HMI / API screens         | Same UI wording                                  | Links well                    |
| Active AGV SQL guide | WCS `SystemActiveErrorModel`       | Same UI wording                                  | Orphan (pool only)            |
| Day 2 (projected)    | Many SSMS/table/state diagnostics  | Still UI wording                                 | Same orphans, at larger scale |


Day 2 will not “fix” linking by volume. Playbook nodes still say RMS/HMI; Day 2 runbooks will say Robotics DB / dwell / shutdown staging / item models. Retrieval + RMS-only companion rules keep preferring Day 1/OM UI procedures. Worse: Day 2 invents more true remote peers of RMS fleet views — exactly the RMS↔WCS equivalence gap.

The training itself split UI day vs DB day (“tomorrow’s like the database message flow”); the pipeline only absorbed Day 1 into playbook wording.

**Ingest note:** prefer a `.vtt` / transcript for Day 2 before a clean ingest (Day 1 has one; Day 2 sample had none).

### Stage 5 is structured against DB diagnostics

Scanned playbook nodes (cases × A/B): “database” appears almost only as **escalation** (“unsupported database intervention”) or Event Viewer / EF `Database.Command` — never “query WCS/SSMS for AGV state.”

Prompt steering today:

- Shared playbook prompt lists `run SQL query` and `change database value` as examples that must **not** become detailed playbook nodes.
- Prompt A/B: do not include exact commands, SQL, service restart steps.
- Component vocabulary: RMS, HMIs, Ignition, OptiSweep/WCS **API**, Event Viewer — **no** SSMS / WCS database row.
- Domain examples to name in placeholders: Event Viewer, Ignition, OptiSweep, Windows Services, RMS, AGV status — again no DB.

So Stage 5 is not missing a soft hint — it treats SQL as procedure detail or unsafe change. That is why even 228086 web/DB fault evidence did not produce “query AGV errors in WCS DB” nodes, and why Day 2 SSMS runbooks will not attach without **prompt + linking** changes.

---

## Track C — Stage 5: name the remote job, keep procedure detail out

### The tradeoff (playbook vs procedure)


| Keep (do not put in playbook nodes)                  | Allow / require in playbook nodes                                  |
| ---------------------------------------------------- | ------------------------------------------------------------------ |
| `SELECT …`, table schemas, column lists              | Intent: “confirm active AGV errors via WCS/SSMS (L2 remote)”       |
| Click-by-click SSMS navigation                       | Named **surface class**: `wcs_sql` / SSMS read-only                |
| Mutating DB / config changes as playbook steps       | `allowed_roles` includes `L2_support` for remote-attainable checks |
| Inventing SQL the case never supported as a *change* | `expects_capability` shared with RMS fleet/error checks            |


**Rule of thumb:** Playbook says *what to confirm and which tool class*. Runbook says *which DB, which query, how to interpret rows*.

Rewrite the ban from “never mention SQL/DB” to:

> Do not include SQL statements, schemas, or mutating database/config steps in playbook nodes.  
> Do name **WCS database / SSMS** as a remote diagnostic surface when the check is L2-attainable and read-only.  
> Link detail to runbooks via `procedure_reference` / Stage 8.

### Brainstormed options


| Option                                               | Idea                                                                                                     | Pros                                                     | Cons                                            | Verdict                             |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- | ----------------------------------------------- | ----------------------------------- |
| **C1 — Vocab + rewrite ban**                         | Add “WCS database / SSMS (read-only)” to component vocabulary; split ban (no SQL text, yes surface name) | Small prompt change; restores Day 2 attach surface       | Alone, case evidence still RMS-skewed           | **DONE**                            |
| **C2 — Capability on node + any surface**            | Status/error/roster nodes emit `expects_capability` + `expects_surface: any` (or `[rms_ui, wcs_sql]`)    | One node, multi-link remote+site; matches tag model      | Needs Stage 8 overlap boost                     | **Required with Track A**           |
| **C3 — Explicit remote companion node**              | When node is AGV fleet/errors, also emit L2 “remote corroborate via SSMS/WCS DB” sibling                 | Very visible for SME; mirrors Day 1/Day 2 training split | More nodes; risk of duplicate graph noise       | Optional for remote-heavy playbooks |
| **C4 — Hardcoded Stage 8 WCS↔RMS peers**             | Regex/peer list for SSMS AGV diagnostics ≡ RMS status                                                    | Fast for Day 2 demo                                      | Paper over; breaks on tipper/dwell/new tables   | **Avoid as primary**                |
| **C5 — Adjacency agent at Stage 8**                  | Extra LLM invents remote peers                                                                           | Feels flexible                                           | Unstable, costly, recreates hardcoding in prose | **Avoid**                           |
| **C6 — Only tag Day 2 runbooks, skip Stage 5 regen** | Hope Stage 8 finds SSMS from RMS placeholders                                                            | Cheap ingest                                             | Embeddings won’t bridge “RMS” ↔ “Robotics DB”   | **Insufficient**                    |


**Recommended combo:** **C1 + C2** (prompt boundary rewrite + capability/surface fields), Stage 6 tags on Day 2 ingest (Track A), Stage 8 overlap multi-link (A3). Use **C3** only if SMEs want an explicit “remote path” branch in review, not as the only fix.

### Example placeholders (good vs bad)

**Bad (today-shaped, too UI-locked):**

```text
Procedure needed to inspect overall system RMS / AGV status for active faults
```

**Bad (too detailed — bleeds into procedure):**

```text
Procedure needed to run SELECT * FROM SystemActiveErrorModel in Helix2x_1Prod_Robotics
```

**Good (job + surface class, detail stays in runbook):**

```text
Procedure needed to confirm active AGV errors via RMS fleet status and/or WCS/SSMS read-only query (L2 remote)
```

With fields:

```json
{
  "expects_capability": ["agv_active_errors"],
  "expects_surface": ["rms_ui", "wcs_sql"],
  "preferred_audience": ["operator", "L2_support"],
  "allowed_roles": ["operator", "L1_support", "L2_support"]
}
```

Stage 8 then multi-links Day 1 RMS check + Day 2 / AGV SQL guide without peer hardcoding.

### Policy for case evidence that only shows HMI

Incident history often never mentions SSMS. Still:

- If the **capability** is remotely attainable (active errors, robot/roster state, dwell/shutdown staging), Stage 5 should **allow** `wcs_sql` / L2 on that node even when the ticket only screenshotted RMS.
- Do **not** invent mutating DB fixes as playbook steps.
- Escalation stays for unsupported backend *changes*; read-only corroboration is a diagnostic surface, not escalation.

---

## Plan tied to next uploads


| Upload                               | What it adds                             | What it needs from the pipeline                                                                                         |
| ------------------------------------ | ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Training video day 2 (databases)** | Many L2 SSMS / table / state procedures  | `**.vtt` if possible**; Stage 6 tags; Stage 5 C1+C2 so playbooks *ask* for remote DB checks; Stage 8 overlap multi-link |
| **Finish Ekram’s file**              | More operational runbooks into Stage 6→7 | Same tag schema + merge-safe Stage 7                                                                                    |
| **More incident cases**              | More Stage 5 playbooks → Stage 8         | **Guards #2 + evidence #1** + Stage 5 remote-surface policy or wrong links / orphans multiply                           |


### Recommended sequence (practical)

```text
Week-now (before / with video day 2)
  A0  DONE — Freeze taxonomy JSON — docs/ontology/taxonomy/runbook_capability_taxonomy.json (includes wcs_sql / ssms)
  C1  DONE — Stage 5 prompt: vocab row + rewrite SQL ban (surface yes, statements no)
  C2  DONE — Stage 5: expects_capability / expects_surface / preferred_audience on diagnostic nodes
  B2  DONE — Enforce hard-reject + no-link / confidence caps (pairing/hospital/roster → low)
  B1  DONE — Attainable-evidence contract (who/tool/signal) including remote SSMS when applicable

  Changelog: docs/design_decisions/stage_5_8_c2_b2_b1_changelog.md

With video day 2 + Ekram finish
  A1  DONE — Stage 6 LLM tagging (+ taxonomy appendix + SME-visible review fields)
  A1b DONE — Backfill tags on existing Stage 6 finalized runbooks (incl. active_agv_error_query_1); script: shared_pipeline_stages/scripts/backfill_runbook_capability_tags.py
  A2  DONE — Stage 7 preserve/union tags; Stage 6.5 retrieval cards + embed text carry capability/surface/audience/failure tags
  C-regen  DONE — Re-extract Stage 5 playbooks (or light backfill expects_*) so nodes can attach Day 2

After new runbooks are in the pool
  A3  DONE — Stage 8: capability-overlap retrieval boost + short role/surface policy in prompt
  B3  DONE — Gap messaging for missing corroboration — improved once tags + Stage 5 exist
  B4  DONE — Branch graph cleanup on regen
  B5  DONE — Full Stage 8 re-run + SME review pack; spot-check playbooks (incl. multi-link RMS + SSMS)

Ontology / Stage 6 enrichment (support, not a substitute for A3)
  DONE — catalogs 0.4 + capability cards + ontology_rag stub (see ontology_surface_catalogs_and_stage6_rag.md)
  DONE — catalogs 0.4 + capability cards + ontology_rag wired into Stage 5/6 packets (option B budgets)

After role model is stable
  Role match boost/block (deferred) — not blocking Day 2 ingest
```

### Why this order (plain English)

1. **Stop the bleeding (#2)** so new cases don’t attach “how to enter the grid” as a status check.
2. **Unlock Stage 5 language (C1/C2)** so playbooks can *ask* for remote DB checks without dumping SQL into nodes.
3. **Make outcomes readable (#1)** including remote tool/signal when L2 path exists.
4. **Label every Day 2 procedure at birth (Stage 6 tags)** as capability + `wcs_sql` + L2.
5. **Re-extract / backfill playbook expects_*** so nodes and new runbooks share vocabulary.
6. **Stage 8 overlap multi-link** once both sides are tagged — then Day 2 stops being an orphan factory.
7. **Re-link once** after Day 2 + Ekram land.

---

## Architecture delta (what changes where)


| Layer                      | Change                                                                                                                                                       |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Data**                   | Taxonomy JSON; optional fields on runbooks + playbook nodes                                                                                                  |
| **Ops / training Stage 6** | Prompt: capability / surface / who / failure pattern; schema + review MD (critical for Day 2)                                                                |
| **Incident Stage 5**       | Vocab: WCS DB/SSMS read-only; rewrite SQL ban; `expects_capability` / `expects_surface` / `preferred_audience`; evidence contract on outcomes                |
| **Shared 6.5 / 7**         | Pass tags through cards + merge                                                                                                                              |
| **Shared Stage 8**         | Overlap boost; multi-link same capability × different surface; role/surface policy; keep intent rejects; shrink RMS-only companion logic gradually           |
| **Tools**                  | Backfill script for old canonicals; Stage 5 regen after prompt change; Stage 8 regen + baseline diff; tests for reject + tag overlap + no-SQL-in-placeholder |
| **Not needed now**         | Adjacency agent; hardcoded WCS↔RMS peer list; KG DB; ML training pipeline                                                                                    |


---

## Expected outcomes if followed

- Day 2 SSMS runbooks multi-link beside RMS checks for the **same capability**.
- Playbooks name remote diagnostic *jobs* without embedding SQL procedures.
- Escalation still means unsupported *changes*, not “DB exists.”
- Ekram + more cases don’t explode wrong primary links if #2 is live.
- SME review gets: honest gaps, attainable evidence (incl. remote), visible tags.
- Stay on the design-doc path without papering over retrieval with peer hardcoding.

---

## Next implementation cut

Week-now A0/C1/C2/B2/B1 and A1/A1b/A2 are done — see [stage_5_8_c2_b2_b1_changelog.md](stage_5_8_c2_b2_b1_changelog.md) (includes ontology 0.4 / mini-RAG stub as Stage 6 support).

**Back to the linking goal — next:**

Optional SME follow-up: draft gap runbooks for thin catalog areas (Event Viewer, dedicated pairing confirm). Track A–C and B1–B5 are complete for the pilot set.

SME pack: `sme_review_runbooks/stage_8_playbooks_capability_tags/`.