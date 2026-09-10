# Design notes for the future LLM-based Brain agent

This is a running log of architectural decisions relevant to the production
ingestion agent described in `brain/DESIGN_RATIONALE.md`, migrated from the
retired `newdesigndoc/` notes and the earlier Brain design document. That
agent spans Extraction / Operational model / Incident intelligence /
Reconciliation / Procedure / Playbook / Validation / Curation / Runtime
orchestration responsibilities.
None of that agent exists yet — per the architecture lock §11.4, building it
is explicitly deferred until the schema foundation is proven. This document
exists so that when that work starts, it is built on the decisions and
findings below instead of rediscovering them.

`brain/migration/BRAIN_BUILD_PROCESS.md` documents the one-time backfill of
existing pipeline output into Brain records — a different, already-finished
piece of work. This document is about the target *production* architecture:
how new material gets ingested going forward, once an LLM (not a
deterministic script parsing specific stage-4/5/6 JSON shapes) is doing the
extraction.

---

## 1. The production/backfill distinction

**What exists today (`brain/migration/`) is a one-time backfill, not the
production path.** Every script there (`migrate_ontology_catalogs.py`,
`migrate_operational_source.py`, `consolidate_entities.py`,
`reclassify_ambiguous_entities.py`, `cleanup_entity_descriptions.py`) is a
deterministic parser tied to the exact JSON shape of
`operationalknowledgeingestion`/`incidenceknowledgeingestion`'s existing
stage outputs. That was the right approach for migrating already-existing
data — see `BRAIN_BUILD_PROCESS.md` for the full account, including every
bug the deterministic approach surfaced (entity-name collapse, self-
referential relationships, catalog cross-reference duplicates, the entity-
vs-claim category error, the Pass 0 Claim gap, the state-vs-action identity
mismatch across all 28 capabilities).

**Explicit direction from the user (2026-09-02): stop investing further in
migration-script precision.** Production ingestion of new material will most
likely be LLM-driven, and its output does not need to structurally tie back
to a specific upstream stage-output shape the way today's scripts assume.
Schema and architecture decisions from here should be designed around *"what
would an LLM extraction/reconciliation call produce"*, not *"what does this
specific JSON field look like."*

**What this means concretely for schema design**: the five Part 1 schemas
(`EvidenceUnit`, `Entity`, `Claim`, `Relationship`, `Capability`) and the
generic merge machinery (`brain/migration/merge.py`) were built to be
source-shape-agnostic already — an LLM extraction call producing a `Claim`
or `Entity` dict goes through the exact same pydantic validation and
`merge_record()` reconciliation as a migration script's output does. The
schemas do not need to change for an LLM producer; what needs to be
designed is the **contract** (tool input/output shapes, the reconciliation
decision the agent makes) around them, and the **judgment calls** the
deterministic scripts couldn't safely make (see §3).

**Explicit direction, sharpened further (2026-09-08): incidence migration
will be agent-executed, not a hand-written deterministic script — and this
is now the standing rule for all future Brain ingestion, not just
incidents.** Concretely:

- **`migrate_incident_case.py` will not be written.** Every place this
  document (and `BRAIN_BUILD_PROCESS.md`) previously said "Pass 2, planned"
  meant a deterministic parser in the shape of `migrate_ontology_catalogs.py`/
  `migrate_operational_source.py`. That plan is superseded. Incident case
  migration is the first real production job for the ingestion agent
  described in §4, not a sixth backfill script.
- **The existing `brain/migration/` scripts (Pass 0/1 and every fix script
  built through §6.13) are NOT retroactively deprecated.** They already did
  their job — the operational-source backfill is finished, validated, and
  stands as documented history (`BRAIN_BUILD_PROCESS.md`). They stay as-is
  and remain re-runnable for that already-migrated data. The boundary is
  forward-looking: no NEW hand-written, source-shape-specific migration
  script gets added to this codebase going forward, for incidents or for
  any future operational source. If existing operational data needs a
  correction after this point, that correction should also go through the
  agent path where practical, not a new one-off script in
  `brain/migration/`.
- **§7 (the offline knowledge enrichment agent, executed 2026-09-03) is the
  working precedent for how this looks in practice before real runtime
  tools exist**: a documented algorithm (§7.3, "Agent algorithm — replicate
  exactly") that a human or coding agent executes by reading ontology +
  evidence and writing only schema-valid, evidence-grounded records — never
  inventing SQL, steps, or role policy — validated via `validate_batch()`
  before anything is written. This already proved the pattern works for
  capability/procedure enrichment (289 Procedures, 101 role-path Claims, 0
  validation errors). Incident migration should follow the same shape: a
  documented algorithm an agent executes, not code that parses a specific
  JSON key path.
- **"Called in the necessary ingestion phases"** — the user's own framing —
  means the eventual target is not a standalone offline pass at all, but
  the Brain agent invoked directly from within
  `incidenceknowledgeingestion`'s (and `operationalknowledgeingestion`'s)
  own pipeline stages, the same way §11.1's Foundry ingestion agent design
  already describes ("Source arrives → agent opens/continues ingestion run
  → ... → tool: extract or reconcile bounded evidence packet → ..."). §7's
  offline script is a stepping stone toward that, run by a human/coding
  agent today because the real runtime tools (§11.3) don't exist yet — not
  the intended permanent shape.

---

## 2. The Entity / Capability / EvidenceUnit / Claim boundary (locked)

This is the definition an extraction/reconciliation agent needs to apply
consistently. Established across two review passes (see
`BRAIN_BUILD_PROCESS.md` §6.7 for the Entity-vs-Claim category-error fix,
§6.9 for the state-vs-action capability fix):

- **EvidenceUnit**: a bounded quote from a source. No judgment. Never
  asserts anything.
- **Entity**: a thing, OR a **state of a thing**, that exists whether or not
  anyone is checking it right now. Structural things (WCS, a database table,
  a role) and conditions/symptoms ("an AGV has an active error", "a tote is
  stuck at bag-out") are both entities. The test: *is this a name someone
  would look up, independent of any specific claim about it?*
- **Capability**: something a **human** (operator/L1/L2/L3) does to
  diagnose, verify, or act on a state. The test: *put a person's name in
  front of the label — does it read as an instruction?* "Operator, confirm
  the AGV active error state" works; "Operator, the AGV active error" does
  not. A Capability never replaces the state entity it's about — it
  `VERIFIES` it (a `Relationship`, not a merge).
- **Claim**: the Brain's current belief about exactly one subject Entity,
  always carrying `polarity` (affirmed/negated/uncertain/conflicting) so it
  can be provisional or contested without deleting the evidence it came
  from.

**Known-wrong pattern, found systemically in the existing catalog data and
now fixed in the Brain corpus (`BRAIN_BUILD_PROCESS.md` §6.10)**: all 28
real top-level capabilities in `docs/ontology/catalogs/capability_catalog.json`
were named after the STATE they check (`agv_active_errors`,
`tote_lifecycle_state`, `hospital_diversion`), not the action of checking
it — even though each record's own `job` field was already correctly
action-shaped ("Confirm whether..."). The paired state/symptom entity was
almost always missing entirely. Fixed by hand-judging all 28 pairings
(`brain/migration/capability_state_pairings.py`) and applying them
(`apply_capability_state_pairings.py`): each capability now has a verb-first
id/label (`capability:confirm_agv_active_error_state`, not
`capability:agv_active_errors`) and a `VERIFIES`/`CONTROLS` Relationship to
its own paired `Entity(state)`/`Entity(symptom)` record. **The underlying
source catalog (`docs/ontology/catalogs/capability_catalog.json`) itself was
NOT changed** — its ids are still state-shaped, and Pass 0
(`migrate_ontology_catalogs.py`) still assigns `capability_kind` via the
`CAPABILITY_KIND_BY_PREFIX` keyword heuristic on every fresh rebuild, so
`apply_capability_state_pairings.py --write` is now a required, permanent
step of the rebuild order, not one-time cleanup — see
`BRAIN_BUILD_PROCESS.md` §9. An extraction agent should default to creating
BOTH records for any "check X" capability candidate going forward: the
state/symptom entity, and the action capability, connected by `VERIFIES` —
not one record trying to be both. See the published State vs. Action
Boundary Audit artifact (2026-09-02 session) for the original worked
example and the 28/28 finding.

**A third shape exists and is neither of the above**: a system/API action
("GetAGVStatuses", "OpenAllChutes") is something *the system* does when
called, not a human action and not a persistent state. **Promoted to its
own `EntityType.SYSTEM_ACTION` (2026-09-08, user-directed) — no longer a
sub-case of `component`.** See §11 for the full migration; the short
version: `component` was only "correct" in the weak sense of being a
catch-all for "a named, look-up-able thing," the same weak-correctness
problem the state-vs-action Capability fix (§6.10 of
`BRAIN_BUILD_PROCESS.md`) already found and fixed for Capabilities. A
`SystemActionPayload` (`invocation_kind`, `access_surface_entity_ids`,
`mutates_state`) now gives this shape the same first-class, evidence-
grounded treatment `system`/`database_table`/`ui_screen` already have.

**A fourth known-wrong pattern, found in the second operational-source
audit** (`BRAIN_BUILD_PROCESS.md` §6.13): `symptom` and `state` were both
being used as a catch-all for "anything diagnostic-adjacent," not held to
the actual boundary test. Refined here with concrete negative examples,
since the positive definition above ("an anomaly/problem condition" /
"a checkable condition") wasn't specific enough on its own to catch these
20 real miscategorizations on the first two audit passes:
- A `symptom`/`state` entity's OWN description must assert the
  condition/anomaly ITSELF, not describe something adjacent to it.
  Failing this test: a pointer to documentation
  ("References to external documentation for..."), a description of a
  database table's stored contents ("The System Active Error model shows
  errors that are currently active"), a description of normal/non-anomalous
  behavior ("API interactions are described primarily as..."), or a
  description of the RESPONSE to a condition rather than the condition
  ("The procedure involves stopping the RMS, removing the faulted AGV...").
  All four read as informative and diagnostic-adjacent, which is exactly
  what made them slip past two prior review passes that were checking for
  narrower, more obviously-wrong shapes (claim-shaped names, state-shaped
  capability ids) — this is not a keyword pattern (no single word marks
  these as wrong) and needs the same "read it and ask what it actually
  asserts" test as the entity/claim boundary itself.
- Database table content specifically belongs on `Entity(database_table)`
  (with a `DatabaseTablePayload` — `database_name`, `key_fields`, etc.),
  never on `state`/`symptom` even when the training material frames it as
  "the status this table shows," because the checkable fact is the state
  the table's LIVE DATA holds, not the table's schema — the schema is a
  `database_table` fact, permanent and structural; a query against it
  produces the actual `state`/`symptom` observation, which is what a
  Capability's `sql_field_notes`/observation step should cite, not a
  second entity describing the table itself under a different type.
- A recovery-procedure description belongs on `component` (or, once
  Procedure records are populated in production, on an actual `Procedure`)
  — never on the `symptom`/`state` it responds to. The underlying
  condition is a SEPARATE fact that may already have its own bare entity
  elsewhere in the corpus (e.g. `entity:symptom:object_blocking_agv`
  already existed as a bare, correctly-typed stub while
  `obstruction_parcel_on_floor_troubleshooting` separately described the
  response to it under the wrong type) — an extraction agent encountering
  a "how to fix X" passage should look for or create the state/symptom
  entity for X specifically, and file the fix-it content as a Capability
  or Procedure connected to it, not conflate the two into one record.

---

## 3. Judgment calls a deterministic script could not safely make

Each of these was attempted with keyword/regex heuristics during the
backfill, found to produce real false positives or false negatives, and is
now explicitly named as something the future LLM-based extraction/
reconciliation agent should own instead:

- **Semantic tag/description → Capability matching.** A vision-enrichment
  tag ("tipper") and a capability slug (`tipper_station_fault`) sharing a
  word is not evidence the artifact supports that capability specifically —
  requires understanding what the artifact actually depicts relative to the
  capability's real diagnostic scope. (`BRAIN_BUILD_PROCESS.md` §4, the
  removed tag→capability keyword-matching pass.)
- **Free-text sentence → structured Claim.** `stage4_evidence_chunks.json`'s
  `source_supported_claims[].claim` values are plain sentences ("The case
  status shown is New"), not subject/predicate/object triples — turning
  these into well-formed Claims needs entity resolution against free text,
  a genuine extraction task. This is exactly why incident migration was
  redirected to be agent-executed rather than a deterministic script
  (§1, 2026-09-08 direction) — this specific gap is the concrete example of
  the judgment a script structurally cannot do safely, that motivated the
  redirection.
- **Catalog evidence → target catalog matching.** The alias-overlap
  matching used for the operational→catalog backfill (`BRAIN_BUILD_PROCESS.md`
  §6.6) needed a hand-curated exception list and cross-surface exclusion
  rules after the first pass produced real misplacements (tipper_hmi_catalog.json
  absorbing hospital/ACB content via shared generic vocabulary). Confirmed
  this does not scale past a one-time human-reviewed pass.
- **Entity name → duplicate detection.** "Identical source_refs" is a weak
  duplicate signal on this corpus (catalog files attach one shared evidence
  pool to every record derived from them, so unrelated entities routinely
  share citations) and word-overlap is equally unreliable in the opposite
  direction ("AGVs with totes" / "AGVs without totes" share every word but
  one and are opposite states). The one true-positive pattern found in
  Pass 0 (`BRAIN_BUILD_PROCESS.md` §6.8) was structural — two catalog arrays
  cross-referencing the same catalog-internal `id` — not a text-similarity
  rule. A second true-positive pattern, found in the operational lane and
  now fixed (`BRAIN_BUILD_PROCESS.md` §6.11): a `component` entity built
  from a context record's own subject, plus a bare, empty-description
  `system` entity built from that SAME record's `applies_to`
  self-reference — confirmed per-pair by reading the loser's relationships
  and finding no independent fact, only a self-referential `applies_to`
  link back to the very component it was extracted alongside. 7 reported
  pairs (8 entities) were resolved this way by direct evidence/relationship
  inspection, not by trusting the report's signal alone. One further pair
  was explicitly identified and left unresolved
  (`entity:component:tote_exchange_thresholds` vs.
  `entity:component:tote_exchange_threshold_categories`) because it's a
  genuinely different kind of duplicate — two independently-sourced,
  populated records describing the same real screen from two different
  sources, not a bare echo — and needs its own dedicated judgment call
  rather than being folded into the bare-echo fix.

  **A third true-positive pattern, mechanically distinct from the other
  two**, found in a sample-based full-corpus read
  (`BRAIN_BUILD_PROCESS.md` §6.12): casing/spacing collisions. Two
  mentions of the same real thing under different capitalization
  conventions ("GeekAgv" vs. "geek_agv") produce two different entity ids,
  since `entity_id()` slugifies `name` without normalizing case or
  word-boundary style. Found not by the evidence/name-overlap signal at
  all, but by grouping same-`entity_type` entities on a fully-normalized
  name (lowercase, alphanumeric-only) — a check the original duplicate
  report never ran. 7 pairs found; unlike the bare-echo pattern, there was
  no reliable "richer side wins" shortcut — which side of a casing pair
  ended up with the real relationships was arbitrary (depended on which
  spelling the source material happened to favor), so all 7 needed
  individual relationship inspection, and 3 turned out to be the
  independently-real-record case (not a collision duplicate at all) once
  read closely.

  **A fourth true-positive pattern, found during the second operational-
  source audit** (`BRAIN_BUILD_PROCESS.md` §6.13): same-name,
  different-`entity_type` collisions. Two entities with the IDENTICAL name
  but different `entity_type` don't collide as ids at all under normal
  operation (`entity_id()` is type-prefixed), so no name-based duplicate
  check — including the casing-collision one above, which groups by
  `entity_type` first — can ever see them; they only become detectable
  (and become a real id collision) after something else changes one
  side's `entity_type` to match the other's, at which point they land on
  the identical id and MUST merge, not silently overwrite. Found while
  fixing a `symptom`-vs-`component` category-confusion issue: retyping
  `entity:symptom:agv_fault_during_exchange_recovery_concept` to
  `component` produced exactly the id of an already-existing, already-
  correct `entity:component:agv_fault_during_exchange_recovery_concept`.
  This is a structural consequence of type-prefixed ids, not a rare fluke
  — any future entity_type correction (by a migration script or a
  Reconciliation agent) must check the *new* id against the existing
  registry before writing, the same way `apply_entity_type_corrections.py`
  was fixed to do only after it first silently overwrote a real record
  this way (see the standalone lesson on this bug below, in this section's
  discussion of the reference-rewrite gap).

  **Pattern for the future agent, now confirmed across four different
  duplicate mechanisms** (structural cross-reference, `applies_to`
  self-echo, casing collision, retype-induced same-name collision):
  "identical evidence" and "name/token overlap" are both good *candidate
  finders*, never safe auto-merge signals on their own. Every true positive
  found across all four mechanisms needed a structural or relationship-shape
  confirmation before merging — reading what the entity is actually
  connected to, not just comparing its text to another entity's text. An
  extraction/reconciliation agent should treat "two entities might be the
  same" as a hypothesis to verify against relationships and evidence
  content, never as a decision the name-similarity score itself is allowed
  to make. It's also worth running MULTIPLE independent candidate-finding
  heuristics (not just one) before considering a duplicate sweep complete —
  the casing-collision pattern was invisible to every check used earlier in
  this backfill and only surfaced once an orthogonal method (normalized-name
  grouping) was tried; the fourth mechanism above was invisible to ALL
  name-based checks and only surfaced as a side effect of an unrelated
  fix (retyping for a different reason entirely).
- **Claim-shaped vs. entity-shaped record titles.** `is_claim_shaped()`
  (`brain/migration/entity_shape.py`) catches the unambiguous cases
  (verb-first names, claim-verb constructions, 9+ word sentences) by
  design, leaving genuinely ambiguous entities that needed direct human
  review (`BRAIN_BUILD_PROCESS.md` §6.7, §6.12) — tightening the heuristic
  to catch that ambiguous class automatically was tested and produced 80
  false positives against real entity names. This is the clearest evidence
  in the whole backfill that the entity/claim boundary needs real language
  understanding past a certain precision, not a bigger rule set. Also
  worth noting: the original review scoped itself to names matching a
  claim-shaped *pattern*; 2 more genuinely claim-shaped records
  (`crash_example`, `repeat_incident_avoidance_as_a_training_concept`)
  were missed entirely because they were typed `symptom`, outside where
  the pattern-based review was looking — found only by reading `symptom`
  entities directly during the §6.12 full-corpus sample, not by any
  refinement of the original pattern check. A type filter and a
  name-pattern filter both narrow what gets reviewed; neither alone is a
  substitute for reading a representative sample with no filter at all.
- **A single hardcoded heuristic bug recurred three separate times before
  being fully found** (`CAPABILITY_KIND_BY_PREFIX` in
  `migrate_ontology_catalogs.py` — §6.10, §6.12): first on the 2 capabilities
  the original state-vs-action audit was built to catch
  (`rms_soft_stop`, `agv_physical_recovery`); then, during the §6.12
  re-judge, on a 3rd capability (`rms_map_reposition`) in a code path
  (auto-created "referenced only" stubs) that the original fix didn't even
  look at, because it isn't one of the 27 capabilities `job`/`description`
  fields were read from. **Lesson**: fixing every instance of a bug found
  by reading N records does not mean the bug is fixed everywhere that
  record-creation code path runs — a keyword/heuristic function used in
  multiple call sites (a normal capability, AND a stub capability, in this
  case) needs its callers enumerated, not just its known-bad outputs
  patched one at a time.

---

## 4. The reconciliation model (design doc §10, not yet built)

From the design doc, the production update path when new material is
ingested is NOT "re-run a migration script." It is:

1. **Extraction agent**: raw bounded source packet → `EvidenceUnit`s,
   artifacts, raw claims. Never approves anything on its own.
2. **Operational model agent** / **Incident intelligence agent**: evidence +
   existing ontology context → Entity/Capability/Constraint candidates (or,
   for incidents, an observed episode with evidence-backed resolution/
   failed-step candidates). Never invents missing SQL or commands — must
   ground every candidate in the evidence it was given.
3. **Reconciliation agent**: new claims + existing Brain context → one of
   **reinforce** (matches/strengthens something already approved),
   **patch** (proposes a specific, scoped change to an existing record),
   **conflict** (disagrees with something already approved — becomes a
   `Claim(polarity=conflicting)`, does not silently overwrite),
   **gap** (identifies something the Brain has no record of at all), or
   **new-candidate** (a genuinely new Entity/Capability/Relationship,
   pending review). This is the step `brain/migration/merge.py`'s
   `merge_record()` mechanically approximates today for the backfill's
   "grow richer, never regress" behavior — but `merge_record()` has no
   concept of *conflict* (it only ever unions/fills, never flags
   disagreement), which is a real gap between what exists today and what
   the design calls for.
4. **Validation agent**: draft + policy/configuration → pass/fail/repair
   (provenance, role, SQL, restart order, duplication checks).
5. **Curation agent**: candidate diff + impact data → an SME-ready review
   explanation and approval request. This is where a human actually
   approves a change before it's promotable — nothing before this step
   should be treated as production-eligible knowledge.

**Concrete gap this reveals in the current schemas**: there is no
`validation_status` or `review_status` field on any Part 1 record — every
record migrated so far (whether from a hand-curated catalog or an
unreviewed LLM extraction pass) is stored identically, with no way to
distinguish "SME-approved" from "reconciliation agent proposed, unreviewed."
This was deliberately deferred in Part 1 (§8/§14 of both design docs) but is
a hard prerequisite for the Curation/approval step above to mean anything —
worth flagging now so the field's design isn't rushed later. See also §2.1
of `BRAIN_BUILD_PROCESS.md` ("catalog-derived" vs. "operational-lane-
unreviewed" content is currently indistinguishable at the record level; the
same gap, described from the data-quality angle instead of the
agent-design angle).

**Second concrete gap, found doing the capability re-identification
(`BRAIN_BUILD_PROCESS.md` §6.10), and closed 2026-09-03**:
`brain/validators.py`'s `validate_batch()` originally only checked
`Relationship.from_id`/`to_id` against known record ids — it did not check
id-list fields embedded inside a record's own payload (e.g.
`Capability.support_contract.required_evidence_capability_ids`/
`forbidden_capability_ids`, or `Claim.subject_entity_id`/
`Claim.object.entity_id`). Re-identifying all 28 capabilities silently
produced 27 dangling `support_contract` references that `validate_batch()`
reported as 0 errors on.

**This same class of bug then recurred TWICE MORE in the very next
session** (`BRAIN_BUILD_PROCESS.md` §6.13) before being closed generically
— worth recording as its own lesson because "we already found this once"
did not prevent it happening again, twice, in new code written with full
knowledge of the first occurrence:
1. A newly-written `apply_entity_type_corrections.py` rewrote
   `Relationship` references on an entity retype but not `Claim.subject_entity_id`
   references — 22 claims would have gone dangling.
2. `apply_entity_duplicate_merges.py` (in production use since an EARLIER
   session, §6.11) had the identical gap the whole time, undetected — 5
   claims were already silently dangling in the live corpus, discovered
   only because this session explicitly went looking, not because
   anything flagged it.

Both were fixed by rewriting Claims too, but the generic fix is what
actually closes this permanently: `validate_batch()` now includes
`validate_claim_references()` (subject_entity_id / object.entity_id) and
`validate_capability_support_contract_references()` (finally generalizing
the §6.10 finding instead of leaving it as a documented-but-open gap only
checked by a one-off migration script). Any future id-rename/merge
operation — migration script, or eventually a Reconciliation/Curation
agent — can now trust `validate_batch() == 0 errors` as real evidence
nothing dangles, for these two reference kinds specifically. `Procedure`/
`Playbook`'s own payload-embedded ids were covered from day one
(`validate_procedure_playbook_references()`, §5.3) precisely because this
lesson was already learned once by the time they were built — the pattern
is finally holding.

**The generalizable lesson, restated because it needed re-learning twice**:
a schema field whose value is an id string pointing at another record is a
foreign key, full stop, regardless of whether it lives inside a
`Relationship` or inside some other record's own payload. `validate_batch()`
checking only `Relationship` endpoints was always an incomplete
implementation of "check that ids resolve," not a deliberate scope
boundary — every new record type or new id-shaped field should be assumed
to need this check by default, with the checker added in the SAME change
that introduces the field, not discovered later by an engineer manually
grepping after data has already gone stale. A Reconciliation agent that
performs corpus-wide id operations (§4.1) inherits this responsibility
directly: it must not treat "the record I edited still passes schema
validation" as proof nothing elsewhere references the id it changed.

### 4.1. Continual learning: what happens on every new ingest (2026-09-02)

Directed by the user: document, concretely, what the Brain does every time
new material shows up — new operational source, new incident, or a
correction to something already ingested. This is the actual production
loop §4's five agents exist to run, made specific rather than left as five
abstract pipeline stages.

**The trigger.** Every ingest — whether it's a new operational source
(a manual, a training video, a support ticket, a live query result) or a
new incident case — starts the same way: raw source material goes through
Extraction (§4 step 1) into a bounded packet of new `EvidenceUnit`s and raw
claim candidates, scoped to *only* what that source actually contains. No
new material is ever merged into Brain directly; it always passes through
Reconciliation first.

**Reconciliation's actual decision, per candidate, is a five-way branch —
here is what happens to the corpus under each branch:**

1. **Reinforce.** The new evidence supports something Brain already has
   (an existing Claim, Entity, or Capability field) without adding new
   information. Action: append the new `EvidenceUnit` to that record's
   `source_refs` via `merge_record()`'s existing "grow richer, never
   regress" behavior. No new record created. Example shape: a second
   operational source independently confirms "OptiSweep is a Windows
   service" — the existing Claim gets one more citation, nothing else
   changes.
2. **Patch (refine an existing entry).** The new evidence adds real detail
   to something Brain already has, but doesn't contradict it — a thinner
   record gets richer. Action: `merge_record()` on the existing record,
   filling previously-empty fields (a `Capability.sql_field_notes` entry
   that was empty gets its first real `SqlFieldNote`; an `Entity.description`
   that was thin gets extended) or unioning list fields (a new alias, a new
   `when_to_use` scenario). **This is the mechanism §5.1 describes for
   filling `sql_field_notes`/`observables`/`support_contract` over time** —
   not a one-time backfill action, but the steady-state behavior every time
   relevant new evidence arrives. A record is never "done"; it accumulates.
3. **Conflict.** The new evidence disagrees with something Brain already
   holds as established. Action: create a new `Claim(polarity=conflicting)`
   citing the new evidence, explicitly linked (by shared `subject_entity_id`
   or a `Relationship`) to the claim it conflicts with — the existing claim
   is NOT deleted, edited, or silently overwritten. Both stand, flagged as
   contested, until a human (Curation, step 5) resolves which is current —
   e.g. a firmware update changes a threshold value the manual documented
   as fixed; the manual's claim doesn't get silently edited, a new
   conflicting claim is added and a person decides which is now correct
   (or whether both are correct under different `constraints`).
4. **Gap.** The new evidence is about something Brain has no record of at
   all — not a refinement of anything existing. Action: flagged as a true
   gap, not silently created as a new record either; surfaced to Curation
   as "this needs a decision," since only a human (or, later, an approved
   Reconciliation policy) should decide whether a gap becomes a
   new-candidate or is genuinely out of scope.
5. **New-candidate.** The new evidence describes a genuinely new
   Entity/Capability/Relationship that should exist, per the same
   Entity/Capability/Claim boundary test in §2 — not a refinement of
   anything existing, and judged worth creating (as opposed to a Gap that's
   flagged but not yet actioned). Action: create the new record via the
   existing `EntityRegistry`-style resolve-or-create pattern (§1's
   migration scripts already do exactly this at backfill time — the same
   resolve-by-type-and-name-or-create logic generalizes directly to
   production ingest), THEN immediately run the near-duplicate check
   below before the record is considered final.

**Merging is not a sixth branch — it's a check every New-candidate passes
through before being accepted**, because a "new" candidate is often not
actually new; it's the same real-world thing already in Brain, named or
scoped slightly differently by a new source. This project's own corpus
work found this pattern repeatedly and by three DIFFERENT mechanisms
(`BRAIN_BUILD_PROCESS.md` §6.8, §6.11, §6.12 — structural cross-reference,
`applies_to` self-echo, casing/spacing collision), which is itself the
strongest evidence that duplicate-checking must be a standing step in the
production loop, not a one-time backfill cleanup:

- Before a New-candidate is finalized, check it against existing records of
  the same `entity_type`/`RecordType` for (a) an identical or
  near-identical normalized name, (b) significant alias overlap, (c) the
  same `applies_to`/`VERIFIES`/`CONTROLS` relationship target already
  claimed by another record. Any hit is a MERGE candidate, not an automatic
  merge — per AGENT_DESIGN_NOTES.md §3's confirmed lesson across all three
  duplicate mechanisms found so far, "identical evidence" and "name/token
  overlap" are candidate finders, never safe auto-merge signals. A
  structural or relationship-shape confirmation is required before two
  records are actually merged (read what each is connected to, not just
  what its text says) — and per the deliberately-deferred pairs in
  `entity_duplicate_merges.py` (`tote_exchange_thresholds` vs.
  `tote_exchange_threshold_categories`, etc.), it is entirely correct
  outcome for this check to conclude "these are similar but genuinely
  different, do not merge" — a merge candidate flagged and left alone is a
  success of this check, not a failure to resolve it.
- A confirmed merge uses the exact same `merge_record()` +
  reference-rewrite pattern `apply_entity_duplicate_merges.py` and
  `apply_capability_state_pairings.py` already implement for the backfill:
  fold content into the winner, rewrite every `Relationship`/payload-
  embedded reference to the loser's id, retire the loser. This is not new
  machinery to design — the backfill scripts already ARE a working
  reference implementation of "detect candidate → judge → merge safely
  without dangling references," just currently triggered by a human running
  a script instead of automatically by new-candidate ingest.

**The loop, stated once concretely** (extends §5.2's diagram with what
actually happens at each arrow):

```
new source material
        │
        ▼
  Extraction (bounded EvidenceUnits + raw claims, no judgment)
        │
        ▼
  Reconciliation ── per candidate, one of:
        │
        ├── Reinforce  → append source_ref to existing record
        ├── Patch      → merge_record() fills existing record's empty fields
        ├── Conflict   → new Claim(polarity=conflicting), old claim untouched
        ├── Gap        → surfaced to Curation, no record created yet
        └── New-candidate → duplicate-check → merge into existing, OR
                                              → create genuinely new record
        │
        ▼
  Validation (schema + validate_batch() + policy checks)
        │
        ▼
  Curation (SME reviews the diff, approves/rejects)
        │
        ▼
  Promoted into the queryable Brain corpus
        │
        └──→ available as grounding context for the NEXT ingest's
             Reconciliation step, AND for Procedure/Playbook generation
             (§5) — this is the actual "learning" in continual learning:
             each promoted change makes the next Reconciliation decision
             better-informed, and the next Procedure/Playbook generation
             cite richer, more-refined Capability fields.
```

**What this requires that doesn't exist yet** (concrete blockers to note,
not just abstract gaps): (1) the `validation_status`/`review_status` field
named above — without it, nothing distinguishes "Curation-approved" from
"Reconciliation proposed, sitting in the Gap/New-candidate queue
unreviewed," so the corpus can't actually separate current knowledge from
pending proposals; (2) `merge_record()` genuinely has no conflict
detection — it will silently union two contradictory list entries rather
than flagging them, so today, running it on conflicting content produces
neither a clean merge nor a flagged conflict, just quietly-combined data;
extending it (or building the Reconciliation agent's own separate
conflict-detection reasoning ahead of ever calling `merge_record()`) is a
hard prerequisite before Reconciliation can run unattended; (3) the
duplicate-check step above has no callable implementation yet — the
backfill's `entity_duplicate_merges.py`/`apply_capability_state_pairings.py`
are one-off scripts with hand-typed judgment dicts, not a callable
"check this new candidate against the corpus" function a Reconciliation
agent could invoke per-candidate at ingest time.

### 4.2. Prompting language and role decomposition for the Reconciliation agent

Directed by the user: write the actual prompting language for this agent,
and decide whether it should be one agent/prompt or several tools/prompts
split apart. This section is deliberately concrete/literal (prompt
language, tool signatures) rather than abstract design prose, since that
was the explicit ask.

**Decision: split into four narrow tools/prompts behind one calling agent,
not one large prompt.** Reasoning: §4's five conceptual steps
(Extraction → Operational-model/Incident-intelligence → Reconciliation →
Validation → Curation) already ARE a natural tool boundary — each has a
genuinely different input shape, a different failure mode, and a different
blast radius if it goes wrong. Collapsing them into one mega-prompt means
one bad generation can simultaneously misjudge extraction AND
classification AND merge-safety, with no seam to catch it. Four SEPARATE,
narrow calls (below) means each step's output is independently checkable
before the next step runs, mirroring how this project's own migration
scripts are already separated (`migrate_operational_source.py` doesn't try
to also do consolidation; `consolidate_entities.py` doesn't try to also do
description cleanup) — that separation is exactly why individual bugs in
this corpus were findable and fixable in isolation rather than needing a
full-pipeline rewrite each time.

**Tool 1 — `extract_evidence`** (Extraction agent, §4 step 1)

*Role*: Turn one bounded raw source packet into `EvidenceUnit` records and
raw claim candidates. Never judges truth, never resolves an entity id,
never decides anything is a duplicate.

*Prompting language*:

> You are extracting evidence from a single bounded source packet for the
> OptiSweep Brain. Your ONLY job is to identify bounded, quotable spans of
> text or structured data (screenshots, OCR text, transcript segments,
> query results) and package each as an EvidenceUnit candidate with an
> honest `is_verbatim` flag and a locator (page/timestamp/section).
>
> You do NOT decide whether something is true. You do NOT resolve which
> existing Entity or Capability a claim is about — that is a later step's
> job and it has context you don't have here. You do NOT merge anything.
> You do NOT skip content because it seems unimportant or already-known —
> a later step decides relevance, not you.
>
> For each bounded span, also propose a RAW claim candidate: a plain-
> language sentence stating what the span asserts, with no attempt to
> structure it into subject/predicate/object yet, and no polarity
> judgment — just "here is what this text says." If the same fact appears
> twice in this packet, extract it twice; deduplication is not your job.
>
> Output: a list of {evidence_unit: {...}, raw_claim_candidates: [...]}.
> Reject nothing for being mundane. Reject nothing for contradicting
> something you believe you already know from elsewhere — you do not have
> corpus context in this step by design.

**Tool 2 — `classify_candidate`** (Operational-model/Incident-intelligence
agent, §4 step 2)

*Role*: Given one raw claim candidate + surrounding Brain context (nearby
Entities/Capabilities the tool call retrieves, NOT the whole corpus),
decide what kind of Brain record this candidate should become, per the
locked §2 boundary. Grounds every candidate in the evidence it was given —
never invents missing SQL/commands/thresholds not present in the source.

*Prompting language*:

> You are classifying one raw claim candidate against the OptiSweep Brain's
> locked record types. You have been given the candidate, its source
> evidence, and a retrieved set of Brain records that might be relevant
> (entities/capabilities near this candidate's likely subject) — you do
> NOT have the whole corpus, only what was retrieved for you, so do not
> assume a record doesn't exist just because it isn't in what you see; flag
> uncertainty instead of asserting non-existence.
>
> Apply this test, in order:
> — Is this a bounded quote with no interpretation? → It's already an
>   EvidenceUnit from the prior step; do not re-emit it as anything else.
> — Is this naming a THING or a STATE OF A THING that exists whether or
>   not anyone is checking it right now (a system, a database table, a
>   role, a symptom, a state)? → Entity candidate. Give it entity_type and
>   a name that is the thing/state itself, NOT the action of checking it
>   (put a person's name in front of the candidate's name — "Operator,
>   confirm the AGV active error" reads as an instruction, meaning the
>   underlying thing "AGV active error" is the Entity and "confirm" names
>   a separate Capability).
> — Is this something a HUMAN does (operator/L1/L2/L3) to diagnose,
>   verify, or act on a state? → Capability candidate, connected to its
>   target state/symptom Entity by a VERIFIES (checking) or CONTROLS
>   (changing) relationship — never both merged into one record.
> — Is this the Brain's current belief about one specific subject Entity,
>   provisional and citable? → Claim candidate, with subject_entity_id,
>   predicate, object, and a polarity you must actually judge (AFFIRMED
>   only if the evidence states it directly and without hedging;
>   UNCERTAIN if the evidence hedges, is secondhand, or is a training
>   aside rather than a documented fact; CONFLICTING only if you were
>   given a conflicting prior claim in your retrieved context).
> — Is this two things that relate to each other in a specific,
>   nameable way? → Relationship candidate, choosing the MOST SPECIFIC
>   relevant type from the fixed vocabulary, not a generic fallback (do
>   not default to `affects` when `verifies`/`controls`/`contains` is
>   actually correct).
>
> Never invent a SQL field, API name, command, or threshold that is not
> present in the evidence you were given, even if it seems like the
> obviously-correct value based on similar systems — ground everything
> or mark it as a gap you could not fill from this evidence.
>
> Output: one classified candidate with its proposed record shape, plus
> a confidence level and a one-sentence rationale citing which part of the
> evidence text drove the classification.

**Tool 3 — `reconcile_candidate`** (Reconciliation agent, §4 step 3, folds
in the duplicate-check from §4.1)

*Role*: Given one classified candidate + retrieved existing Brain records
of the same type, decide Reinforce / Patch / Conflict / Gap /
New-candidate, and for New-candidate, run the duplicate check before
finalizing.

*Prompting language*:

> You are reconciling one classified candidate against the OptiSweep
> Brain's existing records. You have been given the candidate and a
> retrieved set of existing records that might already cover it — this set
> was chosen by similarity search and may be incomplete or may include
> irrelevant results; use your judgment on what's actually related, do not
> assume every retrieved record is relevant just because it was retrieved,
> and do not assume nothing else exists just because nothing else was
> retrieved.
>
> Decide exactly one of:
> — REINFORCE if an existing record already states this and the candidate
>   adds no new information beyond another citation.
> — PATCH if an existing record covers this subject but the candidate adds
>   real new detail (a previously-empty field, a new alias, a new
>   scenario) without contradicting what's there. Specify exactly which
>   field(s) change and with what value — do not describe this vaguely as
>   "update the record."
> — CONFLICT if the candidate disagrees with something an existing record
>   already asserts. Name exactly which existing claim it conflicts with
>   and why. Never propose overwriting or deleting the existing claim —
>   conflicts are additive (both stand, flagged) until a human resolves
>   them.
> — GAP if this is about a real subject the retrieved context suggests
>   Brain doesn't cover, but you are not confident enough it should become
>   a permanent record to propose New-candidate outright. Say what's
>   missing and why you're not proposing creation yet.
> — NEW-CANDIDATE only if you are confident this is a genuinely new,
>   real, distinct thing per the §2 boundary test, AND it survives the
>   duplicate check below.
>
> If NEW-CANDIDATE: before finalizing, explicitly check it against every
> retrieved existing record of the same type for (a) near-identical name,
> (b) significant alias overlap, (c) the same relationship target already
> claimed by another record (e.g. another Capability already VERIFIES the
> same state entity this one would). A name or evidence-pool match ALONE
> is never sufficient grounds to merge — you must also find a structural
> or relationship-shape reason two records are the same real thing (what
> is each one actually connected to?), not just that their text looks
> similar. It is a correct, complete answer to conclude "this resembles
> record X but is genuinely different" and proceed as new — do not force
> a merge to avoid growing the corpus, and do not skip the check to save
> time.
>
> Output: your decision, the specific record(s) affected, the specific
> field-level change if PATCH, and your reasoning citing what in the
> retrieved context drove the decision.

**Tool 4 — `validate_and_prepare_for_review`** (Validation + Curation prep,
§4 steps 4-5 combined into one tool call, since both consume the same
reconciled-candidate-diff shape and neither should be an open-ended LLM
judgment call — Validation is closer to a deterministic gate,
Curation-prep is drafting an explanation for a human, not making the
approval decision itself)

*Role*: Run schema + `validate_batch()` + policy checks on the reconciled
candidate; if it passes, draft a short SME-facing explanation of the
proposed change for the actual human approval step. This tool never
approves anything — approval is a human action outside the agent
entirely, matching §4's "nothing before Curation should be treated as
production-eligible knowledge."

*Prompting language*:

> You are preparing one reconciled candidate for human review. First,
> mechanically verify: does it validate against its pydantic schema? Does
> it pass validate_batch() including payload-embedded id-reference checks
> (not just Relationship endpoints — see the support_contract gap in
> AGENT_DESIGN_NOTES.md §4)? Does every derived record (Claim, Relationship,
> Capability, Procedure, Playbook) carry non-empty source_refs? If any
> mechanical check fails, stop and report the failure — do not attempt to
> silently fix it yourself.
>
> If mechanical checks pass, write a short explanation for the SME who
> will approve or reject this change: what is changing, which existing
> record(s) are affected, what evidence supports it, and — if this is a
> CONFLICT — what it disagrees with and why both readings are being kept
> rather than one being silently chosen. Do not use hedged or vague
> language ("this might improve accuracy") — state plainly what the
> concrete before/after difference is, the same way a code-review diff
> summary would, so the SME can approve or reject in seconds without
> having to re-derive what changed.
>
> You do not approve or reject. You prepare the case for a human to do so.

**Why this split, restated plainly**: an agent that extracts AND classifies
AND reconciles AND validates in one call has no internal seam where a
wrong step can be caught before it contaminates the next one — exactly the
"do not use hardcoded heuristics as a stand-in for real judgment" lesson
from the corpus audit (`BRAIN_BUILD_PROCESS.md` §6.10/§6.12) applies here
in the opposite direction too: real judgment calls need to be isolated and
checkable, not buried inside one large inference no one can independently
verify a piece of. Each tool above has a narrow, single-sentence job
description on purpose.

---

## 5. How runbooks/playbooks actually get produced (design doc §10)

Not templated directly from raw Brain records. The **Procedure agent**
drafts a procedure from a candidate + relevant operational/incident context,
referencing Capability/Entity/evidence IDs rather than inventing steps —
its raw material is a Capability's `required_role_ids`/`support_contract`/
`observables`/`sql_field_notes`/`api_checks` fields plus cited evidence. The
**Playbook agent** then drafts symptom-driven branching logic from incident
patterns (symptom entities, Claims about what happened) + already-approved
Procedures, referencing Procedure IDs only.

**Why the state-vs-action fix (§2 above) matters concretely for this**: a
playbook branch needs to express *"if `entity:symptom:agv_active_error` is
true, invoke `capability:confirm_agv_active_error_state`"* as two separate,
addressable facts. With today's shape — only the capability exists, the
state is implicit in its name — a playbook-generation agent has no clean
record to branch ON, only a record describing the check to run. Fixing the
entity/capability pairing is not just an ontology-cleanliness exercise; it's
a load-bearing prerequisite for playbook generation to work as designed.

### 5.1. Where those Capability fields themselves come from (2026-09-02)

The paragraph above assumes a Capability's `required_role_ids`/
`observables`/`sql_field_notes`/`api_checks`/`support_contract` are already
populated by the time a Procedure agent reads them. **They are frequently
not** — checked directly against the current corpus: of 31 capabilities,
`sql_field_notes` is populated on only 19, `api_checks` on 15, and
`support_contract` on 16 (`required_role_ids`/`observables`/`when_to_use`/
`not_for` are populated on 28/31, missing only on the 3 "referenced only"
stub capabilities from `BRAIN_BUILD_PROCESS.md` §6.12). These fields were
never hand-authored beyond what `docs/ontology/catalogs/capability_catalog.json`
happened to specify — nobody has gone back and filled the gaps, because
until now nothing consumed them.

**User-directed correction to the design (2026-09-02)**: these fields are
not meant to be a one-time hand-authored blank a migration script leaves
empty when the source catalog didn't specify one. They are themselves an
**LLM-generation target, grounded in Brain, using the exact same
reconciliation machinery as everything else** — not invented from the
capability's name/description alone:

- **`required_role_ids`**: filled by looking at which `entity:role:*`
  records, Claims, and prior Capability/Relationship history already
  associate a role with this capability's surface/kind — not guessed from
  the capability's label.
- **`observables` (healthy/degraded/escalate)**: filled from the paired
  state/symptom Entity's own Claims and the evidence cited by the
  VERIFIES/CONTROLS relationship (§2) — what does the evidence actually say
  a healthy vs. degraded vs. escalate-worthy reading looks like, not a
  generic template.
- **`sql_field_notes`**: filled by having the LLM query Brain for the
  relevant `entity:database`/`entity:database_table` records (real ones —
  e.g. `entity:database:sorter_sweeper`, `entity:database_table:sortermodel`,
  the ones consolidated in `BRAIN_BUILD_PROCESS.md` §6.11–§6.12) and their
  known fields, then draft a plausible field reference/query *grounded in
  that evidence* — each `SqlFieldNote.database_entity_id`/`table_entity_id`
  is a real foreign key into the Entity corpus, not a free-text guess. This
  is the same shape as `technical_field_mapping` in the pre-Brain pipeline
  (audit artifact "Runbook Pipeline Audit," 2026-09-02) — the fix is making
  it draw from Brain's curated database/table entities instead of being
  regenerated fresh, ungrounded, per playbook node every time.
- **`support_contract`**: filled the same way — required-evidence and
  forbidden-capability lists drafted from what other Capabilities/Claims in
  Brain already establish about this capability's surface and conflicts,
  not hand-typed.

**A capability's own record is therefore not "done" once created — it gets
richer over time as more evidence accumulates**, the same "grow richer,
never regress" principle `brain/migration/merge.py`'s `merge_record()`
already applies to entities during backfill, now extended to apply to
LLM-*drafted* field content during production use, not just migration-time
merges of already-known facts.

### 5.2. Runbooks/playbooks are not incident-only — and the loop closes

**Explicit correction, also from user direction (2026-09-02)**: runbooks
come from BOTH incident sources and operational sources — this document's
phrasing above ("incident patterns... symptom entities") undersold that.
The existing pre-Brain pipeline already reflects this correctly (Stage 5/6
runs once per source, and `BRAIN_BUILD_PROCESS.md`'s Pass 1 already
migrates 5 operational sources, only 1 of which — `active_agv_error_query_1`
— is incident-flavored; the other 4 are manual/training-video operational
material). Any future Procedure/Playbook agent must draw Capability/Entity
context from Brain's full corpus (ontology catalogs + all operational
sources + incident cases), not just incident-derived Claims.

**The larger point this corrects**: Brain is not a one-way backfill target
that runbooks/playbooks get generated *from* once and never touch again.
It is a **learning mechanism** — a closed loop:

```
operational sources ─┐
incident cases       ─┼─→  Brain (Entity/Claim/Capability/Relationship)
new ingested material ┘         │
                                 │  Procedure/Playbook agents draft FROM
                                 │  Brain context (§5.1), grounded in real
                                 │  entity/evidence IDs, not invented
                                 ▼
                    generated runbooks & playbooks
                                 │
                                 │  used in the field; new incidents,
                                 │  corrections, and SME review happen
                                 ▼
                    flows back into Brain as new Claims/Evidence,
                    refining the next generation's Capability fields
```

Every generation cycle should make the next one better-grounded — a
playbook drafted this month cites the SQL fields Brain knew about this
month; if next month's incident work adds a new `database_table` entity or
corrects a `sql_field_note`, next month's playbook generation should
reflect that automatically because it reads live from Brain, not from a
copy frozen at generation time. This is the concrete reason `sql_field_notes`
et al. must be Entity-ID-backed (§5.1) rather than free text: a free-text
SQL note can't be refined by a later Claim the way an ID-referenced one can.

### 5.3. Schema built (2026-09-02)

The Procedure/Playbook schema itself is now built —
`brain/schemas/procedure.py` (`Procedure`, `ProcedureStep`,
`ProcedureAction`) and `brain/schemas/playbook.py` (`Playbook`,
`PlaybookNode`, `PlaybookBranch`, `PlaybookNodeType`, `BranchOutcome`),
following §5.1/§5.2's design directly:

- **`Procedure`** is a linear step sequence carrying out ONE `capability_id`
  (Part 1 does not model runtime branch evaluation — branching stays a
  Playbook concept). It does NOT duplicate the Capability's own
  `observables`/`sql_field_notes`/`support_contract` — a Procedure step
  cites the specific evidence that grounds its concrete action
  (`source_refs`, required per step, matching the pipeline's own per-step
  citation granularity found in the "Runbook Pipeline Audit"), while the
  reusable diagnostic contract stays owned by the Capability per §5.1.
  `procedure_type` reuses `CapabilityKind` directly rather than a parallel
  enum, since a Procedure exists to carry out a Capability and the two
  should share one kind vocabulary.
- **`Playbook`** is the branching graph — `PlaybookNode.capability_id`/
  `procedure_id`/`symptom_entity_id` are the addressable facts a branch
  routes on (the exact "two separate addressable facts" gap named earlier
  in this section), `PlaybookBranch.outcome` uses the real vocabulary
  confirmed against `shared_pipeline_stages`' actual finalized playbook
  output (`healthy`/`unhealthy`/`inconclusive`/`escalate`), and a node
  never embeds a Procedure's steps — only `procedure_id`, matching the
  pre-Brain pipeline's own deliberate choice.
- **Role references are entity IDs, not free strings** —
  `responsible_role_entity_id`/`allowed_role_entity_ids` point at real
  `entity:role:*` records (the same ones audited/consolidated in
  `BRAIN_BUILD_PROCESS.md` §6), not a bare "L2_support" string the way the
  pre-Brain pipeline stores it — consistent with §5.1's "grounded in a real
  ID, not free text" principle applied to every reference field, not just
  `sql_field_notes`.
- **Structural integrity is enforced at the schema level**: steps must be
  numbered sequentially (no gaps, no branch-shaped step lists), every
  branch's `next_node_id` must resolve to a real node in the same playbook,
  node ids must be unique within a playbook, and a `procedure_reference`
  node must carry a `procedure_id`. These catch a malformed playbook graph
  before it ever reaches `validate_batch()`.
- **`validate_batch()` extended** with `validate_procedure_playbook_references()`
  — checks every payload-embedded id reference a Procedure/Playbook carries
  (`capability_id`, `procedure_id`, `symptom_entity_id`,
  `allowed_role_entity_ids`, per-step role ids) against the batch's known
  ids, closing the exact gap named earlier in this section rather than
  repeating it: `Capability.support_contract`'s dangling-reference problem
  (found in `BRAIN_BUILD_PROCESS.md` §6.10) went undetected because nothing
  walked that field; Procedure/Playbook's own id-reference fields are
  covered from the moment they were introduced, not retrofitted later.

Not yet built: the Procedure agent and Playbook agent themselves (still
explicitly deferred per architecture lock §11.4 — schema first, agent
later), the §5.1 mechanism for LLM-filling a Capability's own fields from
Brain context (still an open question in §6 below — the schema doesn't
change based on how a field gets filled, only that it CAN be filled and
checked once it is), and any migration path from the pre-Brain pipeline's
existing 268 canonical runbooks / 9 playbooks into these new record types
(a real, sizeable backfill once the agent exists, out of scope for the
schema itself). See the "Runbook Pipeline Audit" artifact (2026-09-02) for
the full comparison this schema was built against, including the concrete
finding that motivated it: `technical_field_mapping` (the `sql_field_notes`
analog) was being regenerated per-playbook-node with no reuse or grounding
in a curated entity.

---

## 6. Open questions for when this work actually starts

Carried forward from the review sessions, not yet decided:

- What's the LLM tool contract for `get_brain_context` /
  `resolve_entities` / `validate_brain_records` / `persist_brain_records`
  (architecture lock §11.3's candidate tool list)? None of these exist as
  callable functions yet — `brain/validators.py`'s `validate_batch()` is the
  closest thing to `validate_brain_records`, but it's a pure function over
  an in-memory batch, not a tool with Cosmos-backed state. §4.2's four
  prompts (`extract_evidence`/`classify_candidate`/`reconcile_candidate`/
  `validate_and_prepare_for_review`) each assume a "retrieval" step feeds
  them relevant existing Brain records — that retrieval mechanism (likely
  `get_brain_context`) is exactly this same undesigned tool, now with four
  concrete callers instead of an abstract one.
- **How does anyone gain confidence the §4.2 prompts actually work before
  trusting them on live corpus writes?** No eval/test harness exists yet
  for prompt-driven classification/reconciliation decisions the way
  `brain/tests/` exists for schema correctness. A reasonable starting point:
  replay the backfill's own already-known-correct judgment calls (the 28
  capability pairings, the 37 reclassified entities, the 12 duplicate
  merges — all hand-judged and documented with reasoning in
  `capability_state_pairings.py`/`reclassify_ambiguous_entities.py`/
  `entity_duplicate_merges.py`) as a held-out test set: does
  `classify_candidate`/`reconcile_candidate` reach the same verdict a human
  already reached and justified? This wouldn't prove the prompts handle
  genuinely novel cases, but a prompt that can't reproduce already-solved,
  already-documented judgment calls shouldn't be trusted on new ones
  either.
- Does `merge_record()` get extended with real conflict detection (§4
  above), or does conflict-detection live entirely in the Reconciliation
  agent's own reasoning, with `merge_record()` staying a dumb "apply this
  agreed patch" primitive?
- Where does `validation_status`/`review_status` actually live — a new field
  on `BrainRecord` (touches every schema), or a separate `reviews` container/
  record type that references what it's reviewing (matches the original
  design doc §7's `reviews` Cosmos container, keyed by `/status`)?
- The 7-pair near-duplicate list, the 35-entity claim-shape review, and the
  capability state-vs-action problem are all now resolved
  (`BRAIN_BUILD_PROCESS.md` §6.10, §6.11, §6.12), via the same "hand-judge,
  then apply mechanically" shape throughout: a human/LLM makes each
  individual judgment call once (recorded in a static, reviewable mapping —
  `entity_duplicate_merges.py`/`capability_state_pairings.py`/
  `reclassify_ambiguous_entities.py`), a plain script applies it and
  rewrites every reference. The §6.12 re-judge pass reused this same
  machinery for newly-found records with zero code changes (only new
  dict/list entries), which is evidence the shape generalizes at least
  within "the same kind of defect, found later." Open question narrows to:
  does it also generalize as the standard shape for a *genuinely new*
  defect category (not yet true — §6.12's casing-collision and
  stub-capability-kind findings each needed a few lines of new script logic,
  not just new entries), or does all of this get replaced once the
  Reconciliation agent exists and can own corpus-wide decisions directly
  against live Cosmos state instead of a static file?
- ~~Should `validate_batch()` be extended to check payload-embedded
  id-reference fields...~~ **Done (2026-09-03)** — see §4's full account:
  `validate_claim_references()` and
  `validate_capability_support_contract_references()` now cover this. Open
  question narrows to: are there OTHER payload-embedded id-reference fields
  in the current schemas not yet covered by any check? A quick audit of
  every `str`/`list[str]` field across all 7 record types that is
  semantically an id (by naming convention — `*_id`, `*_ids`) but isn't yet
  walked by a validator would close this properly rather than waiting for
  the next one to be found the hard way, a third and fourth time.
- **The systemic `supports` over-attachment pattern** (found, reported, NOT
  fixed — `BRAIN_BUILD_PROCESS.md` §6.13): entities `supports` a broad,
  loosely-related sprawl of `runbook_proc` evidence stubs from the same
  source document, not just evidence specifically about that entity — seen
  even on entities that are otherwise correctly typed and well-formed (e.g.
  `entity:symptom:operator_station_chute_debris` supports 13 largely
  unrelated maintenance/replacement procedure stubs). This looks like a
  Pass 1 migration-time pattern where evidence attachment is scoped
  per-document-section rather than per-fact. Not yet root-caused or scoped
  — worth a dedicated investigation before assuming it's either a
  cosmetic/harmless graph-density artifact or a real precision problem
  that would mislead a future agent asking "what evidence supports this
  fact" and getting a wall of unrelated procedures back.
- 3 entity pairs were explicitly found and deliberately left unmerged
  during the duplicate-resolution passes, each needing its own dedicated
  review rather than a blanket rule (documented in
  `entity_duplicate_merges.py`'s docstring): `tote_exchange_thresholds` vs.
  `tote_exchange_threshold_categories`, `exchangesortersidezone` vs.
  `exchange_sorter_side_zone`, and `initializetote` vs. `initialize_tote`
  — all three are cases where BOTH sides are independently-sourced, real,
  populated records describing the same underlying thing from two
  different sources/systems, not a bare echo of one another. Also open:
  `entity:ui_screen:overall_system_agv_status_page` vs.
  `entity:state:overall_system_agv_status_page` (a duplicate AND a type
  mismatch layered together), and `entity:system:close_out` vs.
  `entity:system:closeout` (a naming collision sitting on an unresolved
  question of whether "closeout" is more correctly a `system`, `state`, or
  something else entirely). None of these are urgent — they don't fail
  validation and don't block runbook generation — but they're real,
  specific, already-diagnosed work items for whoever does the next
  duplicate-resolution pass, human or agent.
- **What is the actual tool/prompt contract for "LLM fills a Capability's
  `sql_field_notes`/`observables`/`support_contract`/`required_role_ids`
  from Brain context" (§5.1)?** Directed by the user (2026-09-02) as the
  correct design, but the concrete mechanism isn't specified yet: does the
  LLM call something like `get_brain_context(capability_id)` that returns
  the capability's own evidence plus nearby `entity:database`/
  `entity:database_table`/`entity:role` records for it to draft from, or
  does it get a raw retrieval query over the whole corpus and have to find
  relevant entities itself? This is the same undesigned tool contract named
  at the top of this section (`get_brain_context`/`resolve_entities`), now
  with a concrete first caller (Capability field-filling) rather than an
  abstract one.
- **Should Capability field-filling be validated/reviewed before a
  Procedure/Playbook agent is allowed to read it?** §5.1 describes an LLM
  drafting `sql_field_notes` grounded in real entity IDs — but "grounded in
  a real ID" only proves the entity exists, not that the drafted SQL
  field/query is actually correct. This is the same `validation_status`
  gap already named earlier in this section, now sharpened: a
  Procedure agent building a runbook step directly off an unreviewed,
  LLM-drafted `sql_field_note` could propagate a wrong query into a
  human-facing recovery instruction. Needs the Curation/approval step (§4)
  to sit between "LLM drafted this Capability field" and "a Procedure was
  generated citing it," not just between "Procedure drafted" and
  "published."
- **How does operational-source-derived runbook generation differ from
  incident-derived, concretely?** §5.2 corrects the framing that runbooks
  are incident-only, but doesn't yet specify whether the Procedure agent
  reads operational-source Capabilities/Claims differently than
  incident-source ones (e.g. an incident's Claims are about one specific
  observed episode; an operational source's Claims are closer to reference
  documentation) — this distinction likely matters for how much weight
  each contributes when drafting a step, but isn't designed yet.

---

## 7. Offline knowledge enrichment agent (executed 2026-09-03)

Runtime agent tools (`get_brain_context`, etc.) remain deferred. Until they
exist, a human/coding agent must enrich the local Brain the same way a future
ingestion agent will: **read ontology + operational evidence, write only
schema-valid records, never invent SQL/steps/role policy.**

### 7.1. Why this pass existed

The Pass 0/1 backfill preserved volume but dropped or stalled product-detail
the design doc requires for OptiSweep knowledge:

| Gap | Where it lived | Brain before enrichment |
|---|---|---|
| Per-role guidance ("operator: no SSMS", L2 SQL path, …) | `capability_catalog.role_paths` | Only `required_role_ids` |
| `SqlFieldNote.database_entity_id` | Catalog `database` slug + table payload | Always `null` |
| Executable SSMS/SQL step sequences | Stage 6 finalized runbooks | Only `EvidenceUnit.structured_payload` |
| Exact SELECT text as a citeable fact | Runbook `actions[].exact_action` | Not a Claim / not on Capability |
| Procedure records | Schema existed (§5.3) | Zero instances |

### 7.2. Schema addition (locked for this pass)

`Capability.role_paths: list[RolePathGuidance]` where each entry is
`{role_entity_id, guidance}`.

- `required_role_ids` = *who may* touch the capability.
- `role_paths` = *how each role is expected to act* (policy sentence).
- Executable queries/click-paths stay on `Procedure.steps[].actions[].exact_action`
  (never invent a query onto Capability).

Pass 0 (`migrate_ontology_catalogs.py`) now writes `role_paths` and fills
`database_entity_id` on fresh rebuilds. Existing local corpora are repaired
by the enrichment script below without a full rebuild.

### 7.3. Agent algorithm (replicate exactly)

Script: `python -m brain.migration.enrich_brain_knowledge [--write]`

**Inputs (read-only):**

- `docs/ontology/catalogs/capability_catalog.json`
- `brain/data/local/ontology_catalogs/{entities,capabilities,claims,relationships,evidence_units}.json`
- `brain/data/local/operational_sources/<source>/{evidence_units,claims,relationships}.json`
- `brain/migration/capability_state_pairings.PAIRINGS` (old catalog slug → renamed capability id)

**Rules the agent must obey:**

1. **No invention.** Every `role_paths` string, SELECT, and procedure step
   must come from catalog text or runbook evidence. If a runbook has no
   resolvable capability tag / USES edge, skip it (do not invent a
   capability).
2. **Grow richer, never regress.** Use `merge_record` / `merge_list_field`
   so enrichment never blanks populated fields.
3. **IDs stay typed and stable.** Capability tags resolve via PAIRINGS then
   exact id match; roles resolve to existing `entity:role:*` records;
   procedures use `procedure_id(capability_suffix, source_procedure_token)`.
4. **Provenance.** Every Claim/Procedure/Relationship carries
   `source_refs` to the EvidenceUnit (or catalog evidence) it came from.
   Every Procedure step carries per-step `source_refs`.
5. **Validate before write.** `validate_batch(...)` across the full corpus
   (including new Procedures) must return 0 errors; refuse `--write` otherwise.
6. **Procedures stay SME-gated.** New Procedures set
   `validation_status="needs_sme_review"` — enrichment is not approval.

**Steps:**

1. **Capability enrichment from ontology**
   - For each catalog capability card, map old slug → live
     `capability:confirm_*` (or action) id via PAIRINGS.
   - Restore `role_paths` from catalog `role_paths` map.
   - Emit Claim(`predicate=role_path_guidance`, `condition=<capability_id>`,
     subject=`entity:role:*`, object=literal guidance).
   - Rebuild/merge `sql_field_notes` from `sql_model_links` +
     `field_highlights`, setting `database_entity_id` from the database
     slug (`robotics` → `entity:database:robotics`) and
     `table_entity_id` from the model name.
   - For any remaining notes with null `database_entity_id`, fill from the
     linked table entity's `payload.database_name`.

2. **Procedure promotion from each operational source**
   - Walk EvidenceUnits whose `structured_payload` has `steps` and a
     runbook/`procedure_id` identity.
   - Resolve capability ids from `capability_tags` in catalog order
     (primary first); if none, fall back to Relationship(USES) edges.
     Multi-tagged runbooks produce one Procedure per resolvable capability
     (same steps, distinct procedure ids) — a Procedure still carries out
     exactly one capability_id.
   - Build `Procedure` + `ProcedureStep` + `ProcedureAction` (including
     exact SQL text when present in `exact_action`).
   - Map responsible/supporting roles to `entity:role:*`.
   - Add Relationship(`procedure` USES `capability`).
   - When an action contains `SELECT … FROM …`, also emit Claim
     (`predicate=approved_ssms_query`, subject=`entity:system:wcs_sql` or
     the matched table entity, `condition=<procedure_id>`, object=query
     text) and, if the FROM table matches a known
     `entity:database_table:*`, append a grounded `SqlFieldNote` on the
     capability.

3. **Persist layout**
   - Updated capabilities + ontology role-path claims →
     `brain/data/local/ontology_catalogs/`
   - Per-source `procedures.json`, appended claims, appended relationships →
     `brain/data/local/operational_sources/<source>/`

### 7.4. Results of the 2026-09-03 run

- 28/31 capabilities with `role_paths` (3 stubs have no catalog card)
- 101 role-path Claims
- 520/520 `sql_field_notes` with `database_entity_id`
- 289 Procedures promoted (63 containing SQL actions; multi-tagged runbooks
  yield one Procedure per resolvable capability); 11 runbooks skipped
  (`no_capability`)
- 84 `approved_ssms_query` Claims
- `validate_batch` = 0 errors; `pytest brain/tests/` = 41 passed

### 7.5. Still open after this pass

- 11 runbooks without resolvable capability tags (need judgment or catalog
  coverage, not keyword guessing).
- Stub capabilities (`optisweep_service_restart`, `ignition_restart`,
  `rms_map_reposition`) still thin — no catalog card to enrich from.
- `wcs_sql_catalog.activities` labels are still not first-class Procedure
  titles unless a matching runbook already existed.
- Incident migration still not started — and, per the 2026-09-08 direction
  (§1), will not be a `migrate_incident_case.py`-shaped script when it
  happens; it's the ingestion agent's job. **Started 2026-09-08 — see §8.**
- Runtime agent tools still deferred (by product request).

---

## 8. Incident migration, agent-executed (all 4 cases, 2026-09-08)

Per §1's direction, this is not a deterministic parser. Every judgment
below — entity resolution, Claim predicate/polarity, Relationship choice,
what gets a new Entity vs. resolves to an existing one — was made by
directly reading `incidenceknowledgeingestion`'s Stage 4 canonical incident
record and timeline events for case_228086, the same reasoning a real
extraction+reconciliation agent call would do. A Python harness did only
mechanical work afterward: construct the pydantic objects from the values
already decided, resolve/create via the existing `EntityRegistry` (seeded
from the live 2,186-entity corpus so incident content resolves against
real operational entities, not a parallel set), run `validate_batch()`,
write. This section is the replicable record of that judgment — read this,
not a script, to do the next case.

### 8.1. The judgment framework applied

Case_228086's Stage 4 output is 50 timeline events, each with `event_type`,
`summary`, `details`, `systems`, `evidence_support_type`, `confidence`.
Every event, without exception, produces exactly one `EvidenceUnit`
(`evidence_kind=incident_timeline_event`, `source_type=support_case`,
`locator.timeline_event_order` set) — that part is not a judgment call,
it's Part 1 §1.2/§9's "preserve all source links" rule applied literally.
What varies per event is whether it ALSO produces a Claim, a Relationship,
or a new Entity, decided by reading the event's actual content against the
locked boundary (§2):

- **`system_event` (direct log/error excerpts)** → Claim, `polarity=affirmed`
  almost always (these are literal Event Viewer/system-log text, not
  interpretation) on the affected system/component entity.
- **`symptom_reported`/`status_update` stating a real operational fact**
  → Claim, polarity judged from the event's own `confidence` field and
  whether the wording itself hedges ("reported," "appears to," "thought
  there was") — not a blanket rule; e.g. event 33 ("Michell Flynn *thought*
  there was a removed AGV...") is explicitly speculative in its own source
  text and was marked `uncertain` for that reason, not because
  `diagnostic_note` events are uncertain by type.
- **`diagnostic_note`/`diagnostic_request`/`follow_up` that is pure
  investigative dialogue with no new system fact** (e.g. "asked whether
  someone knew how to verify an Ignition crash") → EvidenceUnit only, no
  Claim. The question itself isn't a fact about OptiSweep; the *answer*,
  when later events state it, is.
- **`action_taken` describing a real remediation action that matches an
  EXISTING Capability** (Ignition restart, RMS AGV resync, OptiSweep
  service reset) → a Claim describing what happened, PLUS a
  `Relationship(APPLIES_TO)` from the existing capability to the affected
  entity — this incident is real-world corroborating evidence for a
  capability the corpus already has, which is the Reinforce branch of the
  continual-learning model (§4.1), not a new-candidate.
- **`validation_check`/`validation_result` matching an existing Capability's
  own verification action** (GetAgvStatuses, Ignition status page, WCS
  service state) → `Relationship(APPLIES_TO)` from the capability to the
  entity it validated, same Reinforce logic. Concretely: 4 existing
  capabilities (`capability:ignition_restart`,
  `capability:confirm_wcs_api_responsiveness`,
  `capability:confirm_wcs_service_health`,
  `capability:confirm_ignition_gateway_health`) all got real incident-use
  evidence this way, entirely by resolving against capability ids already
  in the corpus — none were guessed or fuzzy-matched, each was confirmed by
  reading the capability's own name/id against what the event actually
  described doing.
- **`diagnostic_evidence_shared`** — judged individually per event: some are
  pure "a screenshot was shown" acts with no independent fact (evidence
  only), others carry a real, citable system observation (e.g. event 34's
  SQL query results naming 8 real AGV state values — `LeavingCharger`,
  `MovingToChargerExitQueue`, etc. — became a Claim specifically because
  that vocabulary is a concrete, reusable fact worth preserving, grounding
  future SQL/state work in an actually-observed query rather than an
  invented one).
- **`case_status_change` and pure Salesforce case-tracking content**
  (case creation, priority, status transitions) → EvidenceUnit only. This
  is incident-administrative metadata, not OptiSweep operational knowledge
  — it stays as provenance but doesn't become a Claim about the product.

**Corroborating duplicates are preserved, not collapsed.** Several real
facts (the OptiSweep service crash at 6:36 AM, the RMS-based AGV resync,
the Ignition status page check) were independently reported through two
different channels — a case-comment page AND a Teams chat message (events
37/38, 39/40), or two separate screenshot captures of the same screen
(events 23/24, 25/26/27). Each such pair still produces its OWN
`EvidenceUnit` (never collapsed — every event is its own bounded source
citation) while contributing to the SAME Claim via `merge_record()`
unioning `source_refs` — so the Claim ends up citing multiple independent
corroborating sources, which is a stronger evidentiary position than a
single citation, and exactly what "corroboration" should look like in this
schema.

**Every incident-derived record must carry `constraints.sites` — caught as
a real gap AFTER the first pass, fixed retroactively (2026-09-08).** The
first pass through case_228086 left `constraints` empty on all 35 Claims,
8 Relationships, and 50 EvidenceUnits, which per Part 1 §3.3 means "globally
applicable to all of OptiSweep" — wrong for incident content. An incident
observation ("the OptiSweep service crashed at 6:36 AM," "GetAgvStatuses
returned HTTP 200") is a fact about what happened at ONE site on ONE day,
not a universal fact about the product the way an operational-source
manual's description of how a screen works is. All 4 known incident cases
(case_218550, case_223554, case_228086, case_228723) are the same site —
UPS Fort Worth, TX (Haslet), internally coded TXRTH in the source data,
labeled slightly differently across the 4 cases' own extractions ("UPS
Haslet TX (TXRTH)," "UPS Fort Worth, TX (Haslet)"). Standardized on
`ups_haslet` as the `constraints.sites` slug — not invented, this is the
exact value the architecture lock doc's own §3.3 worked example already
uses (`brain/DESIGN_RATIONALE.md` line 186),
so it was picked to match established precedent rather than create a new
one. **Rule for every future incident from this site**: every Claim,
Relationship, and EvidenceUnit that record produces gets
`constraints.sites = ["ups_haslet"]`, added in the same pass that creates
the record, not retrofitted after — this was only caught here because it
was flagged directly, not because the harness checked for it.

**New Entities need the same judgment call, and it doesn't default to
"site-scoped" just because the source is an incident.** Checked each of
case_228086's 3 new entities individually: `entity:ui_screen:acb_system_1_rms_screen`
and `entity:component:small_sort_operation_site` are genuinely specific to
this site's own installation (the latter was even already named
`small_sort_operation_site` for exactly this reason, per §8.2 below) and
got `constraints.sites = ["ups_haslet"]`. `entity:system:service_control_manager`
is a generic Windows subsystem — every OptiSweep deployment runs on
Windows and has one — and correctly stayed globally applicable
(`constraints: {}`) even though it was first observed and created from
this site's incident data. The source an entity was FIRST extracted from
does not determine its scope; what the entity actually IS does.

### 8.2. Real resolution mistakes made and caught (worth reading before the next case)

Three entities were nearly created as duplicates of already-existing,
correctly-typed corpus entities — caught only by explicitly checking each
candidate against the live registry (name + alias + relationship search)
before accepting the harness's first-pass result, not by trusting the
`get_or_create` call blindly:

1. **"AGVs / robotic system" was about to become a new `component`**, when
   `entity:system:optisweep_agv_fleet` (a `system`, not `component`)
   already existed and was already connected via a real Relationship. The
   entity_type mismatch (`component` vs. `system`) meant the registry's
   alias index never found it on the first pass — same class of miss as
   the casing-collision duplicate mechanism from `BRAIN_BUILD_PROCESS.md`
   §6.12/§6.13, just triggered by a fresh extraction instead of a retype.
   Fixed by resolving to the existing entity explicitly.
2. **"auto bag out procedure" was about to become a new `component`**, when
   `entity:system:bag_out_operations` already existed describing the same
   real concept (bare/thin, but real and connected). Fixed by resolving to
   it and adding the incident's specific aliases ("auto bag out procedure,"
   "manual bag out") onto the existing entity instead.
3. **"ACB System 1" was initially typed `system`**, but reading the actual
   evidence text closely showed it is an RMS SCREEN TITLE ("ACB System 1 -
   RMS", subtitle "AMR ACB, TT Sorter"), not a second physical ACB system
   distinct from the corpus's existing `entity:system:acb_system`. Retyped
   to `ui_screen` and related to `acb_system` via `Relationship(DISPLAYS)`
   instead of left as a free-floating, wrongly-typed system-level entity.

**A fourth issue was found and deliberately NOT fixed mid-task**: the
existing `entity:system:event_viewer` already carries `"SCM"` as one of its
aliases, apparently conflating Service Control Manager with the Event
Viewer log interface from an earlier backfill pass. This incident's
evidence makes clear SCM is a genuinely distinct Windows subsystem (it logs
the service-termination event Event Viewer displays, but is not the same
thing as the viewer). A new `entity:system:service_control_manager` was
created rather than continuing to fold SCM into `event_viewer`, but the
pre-existing `"SCM"` alias on `event_viewer` was left as-is — fixing an
unrelated prior decision was out of scope for this task and would have
confused what changed for what reason. Flagged here as a known, small,
low-priority cleanup item for a future pass (same shape as the
deliberately-deferred duplicate pairs already tracked in
`entity_duplicate_merges.py`).

**The generalizable lesson**: an incident's vocabulary for a system it
references ("AGVs," "the robotic system," "auto bag out") is almost never
going to exactly match how that system was named when it was first
captured from operational/catalog material. Checking a candidate's name
AND its plausible synonyms AND its entity_type against the live registry —
not just calling `get_or_create` and trusting the result — is required
every time, and is itself a judgment call the agent has to make, not
something `EntityRegistry`'s alias-slug matching alone can guarantee gets
right.

**A fifth, more consequential gap: the first pass never produced a single
symptom-occurrence Claim, despite the corpus already having 39+ real
`symptom` entities this incident is a textbook occurrence of — caught only
because it was flagged directly (2026-09-08), fixed retroactively.** Every
Claim in the first pass was subject-scoped to a `system`/`component`
entity ("OptiSweep service crashed," "WCSWebApplication faulted"). That's
correct as far as it goes, but it stopped one step short: this corpus
already has `entity:symptom:service_crash_or_restart`,
`entity:symptom:site_stoppage`, `entity:symptom:sort_lifecycle_stuck`, and
`entity:symptom:web_app_fault` — each already wired into the ontology via
`symptom --may_indicate--> capability` and (mostly) `system --observes-->
symptom` relationships from the operational-source backfill — and this
incident is a real, dated, evidenced occurrence of four of them at once.
Not recording that connection means an agent later asking "when has
`service_crash_or_restart` actually happened, and what did it look like
in practice" would get nothing from this incident, despite this incident
being exactly that kind of grounding case.

**The fix, and the rule for every future incident**: after the per-event
pass (§8.1) is done, make a SECOND pass — read the corpus's existing
`symptom` entity list (not a keyword search against it; read the actual
names and their existing `may_indicate`/`observes` relationships) and ask,
for each one, "did this incident's events describe an occurrence of this
symptom?" For every real match:
1. Add a Claim with the symptom entity as `subject_entity_id`, predicate
   `occurred_at_site` (a new predicate, distinct from `has_detail` — the 7
   existing symptom-subject Claims in the corpus use `has_detail` to
   generically DESCRIBE what a symptom is, from reference/manual material;
   `occurred_at_site` specifically asserts THIS symptom HAPPENED, dated,
   at one site, evidenced by specific incident events — a materially
   different kind of assertion that deserves its own predicate rather than
   overloading `has_detail`), citing every relevant event's EvidenceUnit
   (all corroborating events at once, not just the first one found), and
   carrying the same `constraints.sites` tag as every other incident record
   (§8.1).
2. Check whether the directly-affected system already has an `OBSERVES`
   relationship to that symptom anywhere in the corpus; if not, add one
   (case_228086 was missing `optisweep_services --observes-->
   service_crash_or_restart` and `optisweep_services --observes-->
   unplanned_restart` entirely — `entity:system:optisweep_services` had
   ZERO outgoing relationships before this fix, a gap from the original
   operational-source backfill that this incident work happened to
   surface, not create).
3. Do NOT retype or re-subject the original system-level Claims from
   §8.1 — they stay as-is. The symptom-occurrence Claim is additive,
   connecting the same evidence to the corpus's existing symptom
   vocabulary, not a replacement for the concrete system-level fact.
4. It is a correct, complete outcome for some events to have no symptom
   match — not every incident event needs to map onto an existing symptom
   entity, and forcing a match where none genuinely fits would be the same
   mistake as the false-positive duplicate patterns already documented
   elsewhere in this corpus (`BRAIN_BUILD_PROCESS.md` §6.8). Of case_228086's
   50 events, roughly a dozen contributed to the 5 symptom Claims found;
   the rest (memory-trend detail, validation-check specifics, case-tracking
   metadata) genuinely don't describe a symptom occurrence and correctly
   don't get one.

Case_228086 result: 5 new symptom-occurrence Claims
(`service_crash_or_restart`, `unplanned_restart`, `site_stoppage`,
`sort_lifecycle_stuck`, `web_app_fault`) and 3 new `OBSERVES` relationships,
added retroactively. `validate_batch()` — still 0 errors after the fix;
`pytest brain/tests/` — 41 passed.

### 8.3. Results (case_228086, final — includes the §8.2 symptom-claim fix)

- 50/50 timeline events → 50 EvidenceUnits (100% preserved, none dropped or
  merged away)
- 40 Claims total: 35 system/component-level Claims from the per-event pass
  (§8.1) + 5 symptom-occurrence Claims added in the second pass (§8.2) —
  `service_crash_or_restart`, `unplanned_restart`, `site_stoppage`,
  `sort_lifecycle_stuck`, `web_app_fault`, each `predicate=occurred_at_site`,
  each citing every corroborating event's evidence at once
- 11 Relationships: 4 `APPLIES_TO` edges corroborating existing Capabilities
  with real incident-use evidence (Reinforce branch), 1 `CAUSES`
  (OptiSweep service crash → AGV desync, the incident's central causal
  finding), 1 `CONTROLS` (RMS → AGV fleet, the resolution action), 1
  `OBSERVES` (Service Control Manager → OptiSweep service), 1 `DISPLAYS`
  (ACB System 1 RMS screen → ACB System), plus 3 more `OBSERVES` edges from
  the §8.2 fix connecting the directly-affected systems to the symptoms
  they exhibited (including closing a real pre-existing gap:
  `entity:system:optisweep_services` had zero outgoing relationships in
  the whole corpus before this)
- 3 new Entities, all individually justified after ruling out 3 near-misses
  against the existing registry (§8.2): `entity:ui_screen:acb_system_1_rms_screen`,
  `entity:component:small_sort_operation_site` (deliberately NOT resolved
  to the existing `traditional_small_sort_*` entities — those describe the
  pre-OptiSweep legacy small-sort model, a different real referent despite
  the word overlap), `entity:system:service_control_manager`
- Written to `brain/data/local/incidents/case_228086/` (evidence_units.json,
  claims.json, relationships.json) — a new top-level directory alongside
  `ontology_catalogs/` and `operational_sources/`, since an incident is
  neither; the 3 new entities were merged directly into the shared
  `ontology_catalogs/entities.json` registry, same as every other source.
- Every Claim, Relationship, and EvidenceUnit this incident produced
  carries `constraints.sites = ["ups_haslet"]` (retrofitted after the fact
  once flagged — see the standing rule above); the 2 site-specific new
  entities carry it too, the 1 generic new entity (Service Control
  Manager) correctly does not.
- `validate_batch()` across the full corpus (entities, capabilities,
  claims, relationships, evidence, AND the 289 Procedures from §7 — a
  quick first validation pass that omitted Procedures wrongly reported 289
  pre-existing, unrelated errors having nothing to do with this incident
  work; re-running with Procedures included showed those were never real)
  — 0 errors. `pytest brain/tests/` — 41 passed.

### 8.4. Still open (after case_228086 alone — see §8.5 for the remaining 3 cases, now done)

- No incident-specific Playbook/Procedure was drafted from any case yet —
  §5's Procedure/Playbook generation (grounded in Capability fields per
  §5.1) is a separate, later step from getting each incident's raw
  Evidence/Claim/Relationship content into Brain in the first place.

### 8.5. The remaining 3 cases (case_218550, case_223554, case_228723 — completed 2026-09-08)

Same judgment framework as §8.1/§8.2 applied to each, from the start this
time (`constraints.sites = ["ups_haslet"]` on every record from the first
write, symptom-occurrence pass done as step 2 of each case rather than
retrofitted). Per-case harnesses were scratch/session material again, not
committed to `brain/migration/`, per §1's standing direction.

**case_218550** ("system stopped at bag-out after sorting"): 32/32 events
→ 32 EvidenceUnits, 29 Claims, 5 Relationships, 0 new entities (everything
resolved to the existing registry — `bag-out stage` → `bag_out_operations`,
`AGV/robots` → `optisweep_agv_fleet`, `HMI` → `hospital_hmi`, `Tipper 1`
→ the generic `tipper_hmi`, judged too thin/low-confidence a single mention
to justify a new site-specific numbered entity the way `ACB System 1` did
in case_228086). Symptom pass: 3 Claims — `bag_out_stuck` (bag-out
repeatedly entering a stuck 'request' state and never completing, tried
twice), `agv_tracking_or_path_lost` (AGV 202 repeatedly losing QR code;
a separate AGV not moving for 3 hours), `robot_task_or_command_stuck`
(an unresolved tote exchange; a stuck-task error visible only on the
hospital HMI).

**case_223554** ("ACB hospital station unable to induct totes"): 43/43
events → 43 EvidenceUnits, 33 Claims, 7 Relationships, 1 new entity
(`entity:component:agv_hospital_station_server` — judged distinct from
both `hospital_hmi`, the operator-facing UI/lane surface, and
`hospital_station_overview`, the physical-station concept, because the
incident consistently describes a SERVER backing the AGV-facing hospital
logic specifically, needing its own services reset, independent of the two
existing entities). This case had a genuine root-cause finding worth
recording precisely: removing an AGV without removing its associated tote
disabled the hospital station (`entity:system:optisweep_agv_fleet --causes-->
hospital_station_overview`) — stated directly by support with an admitted
responsible party, so judged `polarity=affirmed` rather than `uncertain`
even though most of this case's other diagnostic notes were hedged
speculation. Also captured a real, reusable operational guidance statement
distinct from the incident narrative itself: "operators at the tippers
should pause the station during recovery, or everything goes to hospital."
Symptom pass: 3 Claims — `hospital_diversion` (empty totes and
recovery-time traffic unexpectedly routing to hospital), `zone_agv_mismatch`
(two AGVs found under the same rack in the same zone), `site_stoppage`
(evening recurrence: could not start the sort / went down mid-sort). One
deliberate NON-match, worth reading as the counter-example to blind
pattern-matching: `service_crash_or_restart` was considered for the
OptiSweep-services reset in the closure notes but rejected — that reset
was a deliberate recovery ACTION support chose to take, with no
crash/unexpected-termination log evidence the way case_228086's Service
Control Manager Event 7031 occurrence had; forcing the match would have
been exactly the false-positive-by-surface-similarity mistake §3 already
documents as a lesson. The reset is still captured, just as a plain Claim
+ `CONTROLS` relationship, not a symptom occurrence.

**case_228723** ("ACB system down in zone 5... robot 158 removed"): 26/26
events → 26 EvidenceUnits, 15 Claims, 3 Relationships, 0 new entities.
Notable judgment calls: individual robot numbers (158, 153) were kept as
detail text inside Claims on `optisweep_agv_fleet` rather than given their
own entities — a specific AGV's transient state during one incident is not
a reusable ontology concept the way a named subsystem is. The incident's
own stated root cause (robot 158 "shown to not be mapped") was resolved
directly onto the corpus's EXISTING `entity:state:device_roster_mapping_and_fleet_membership_state`
and `entity:state:zone_pairing_health_state` — both created during the
capability state-vs-action fix (`BRAIN_BUILD_PROCESS.md` §6.10) specifically
to be the checkable-condition targets for `confirm_device_roster_state`/
`confirm_zone_pairing_state` — rather than inventing new entities, and a
`CAUSES` relationship was added directly between the two existing states
(`device_roster_mapping... --causes--> zone_pairing_health_state`) since
this incident is real, dated evidence for exactly that causal link. A
genuine source inconsistency (the case subject says "ACB System Down" but
one resolution-detail line says "the ECB system was reported functional
again") was preserved AS a naming inconsistency, not silently resolved to
one or the other — the canonical incident record itself flags this as an
open SME-review item, and this migration respected that rather than
guessing which name was "correct." Symptom pass: 4 Claims —
`pairing_failure` (zone 5 unable to pair, the incident's named core
symptom), `zone_agv_mismatch` (robot 158 unmapped), `hospital_diversion`
(every replacement AMR routing to hospital instead of pairing),
`agv_tracking_or_path_lost` (robot 153 losing QR code, hedged in the
source itself as only possibly stuck).

**Combined final result, all 4 incident cases**: 151/151 timeline events
preserved as EvidenceUnits (100%, zero dropped across all 4 cases), 121
Claims, 28 Relationships, 4 new Entities total (one per case except
case_218550 and case_228723, which resolved entirely against the existing
registry). Full-corpus `validate_batch()` — entities, capabilities, claims,
relationships, evidence, AND the 289 Procedures from §7, across all 5
operational sources and all 4 incident cases at once — 0 errors.
`pytest brain/tests/` — 41 passed.

**The pattern held up across all 4 cases without needing new judgment
categories** — every real content type this incidence data contains
(system-level facts, symptom occurrences, causal findings, operational
guidance, source-naming inconsistencies, deliberately-uncertain hedged
claims, robot-specific transient detail) was already covered by the
framework §8.1/§8.2 established on the first case. What varied case to
case was which existing entities/symptoms/states the content resolved
against, not the shape of the judgment being applied — a reasonable signal
that this framework, not a bigger rule set, is the right unit to hand to
the eventual runtime ingestion agent (§4.2's `classify_candidate`/
`reconcile_candidate` tools), rather than trying to enumerate every
possible incident-content pattern in advance.

Incident migration for all currently-available cases is complete. The next
new incident (whenever it arrives) is the first real test of whether this
framework, written down here, is sufficient on its own for someone/something
else to execute — or the ingestion agent itself, once built (§4/§11.1),
picking this up directly rather than a person reading this section first.

---

## 9. Capability metadata backfill, agent-executed (2026-09-08)

Directed by the user after noticing an empty `capability:*` record in
`brain/data/local/ontology_catalogs/capabilities.json` in the editor
(`description`, `when_to_use`, `not_for`, `target_entity_ids`,
`allowed_surface_entity_ids`, `required_role_ids`, `role_paths`,
`sql_field_notes`, `api_checks`, `observables` all empty on the 3 stub
capabilities) — asked for a full backfill across "all operational sources,"
with every rule/decision documented here, per the same standing instruction
as §6.10 of `BRAIN_BUILD_PROCESS.md` ("no hardcoding or regex but with your
brain. LLM changes, document all rules and decisions in the agent decision
notes"). This is a Capability-field enrichment pass in the shape §7 already
established as the precedent — not a new migration script (per §1, none
was written; the edits were made directly against
`brain/data/local/ontology_catalogs/capabilities.json` after reading real
evidence for each field, the same judgment §7.3/§8 already model) — scoped
specifically to gaps §7.4/§7.5 had already flagged as open but never closed.

### 9.1. Scope, established by reading the actual corpus first

Before touching anything, the full 31-capability corpus was audited
field-by-field (not assumed from the one record the user pointed at) to
find every real gap, distinguishing "empty because no evidence exists yet"
from "empty because an earlier pass never wrote it despite evidence already
being in the corpus":

- **3 capabilities fully empty** (`optisweep_service_restart`,
  `ignition_restart`, `rms_map_reposition`) — confirmed via §7.5/§6.6 as
  the "referenced only" stubs with no `capability_catalog.json` card of
  their own (they exist solely as bare ids inside other capabilities'
  `support_contract.forbidden_capability_ids`/`required_evidence_capability_ids`).
- **10 capabilities with empty `target_entity_ids`**, **11 with empty
  `sql_field_notes`**, **16 with empty `api_checks`** — a materially
  different kind of gap from the 3 stubs: these are otherwise fully-
  populated, real capabilities (description/when_to_use/not_for/role_paths/
  observables all present from §7's 2026-09-03 run) that simply never had
  these three specific fields filled, even where real evidence for them
  already existed elsewhere in the corpus or in
  `docs/ontology/catalogs/capability_catalog.json`'s own source cards.

This second class is the one worth naming as a lesson: §7.4 only reported
`role_paths`/`sql_field_notes.database_entity_id`/Procedure promotion
coverage, not `target_entity_ids`/`api_checks` coverage specifically, so
this gap was invisible in that pass's own results table even though the
underlying source catalog cards (read directly from
`docs/ontology/catalogs/capability_catalog.json` for this pass) already
had the answer sitting in their own `api_checks: [...]` arrays the whole
time (e.g. `zone_config_state`'s `["GetZoneConfig", "UpdateZoneConfig"]`,
`rms_soft_stop`'s `["PauseAGVs", "ResumeAGVs"]`) — an enrichment pass
reporting coverage only on the fields it explicitly targets does not prove
other, unreported fields aren't also thin; the fix here was re-reading
every field of every capability against its own source card, not trusting
an earlier pass's own summary of what it fixed.

### 9.2. Rule: `target_entity_ids` resolves to the capability's own existing VERIFIES/CONTROLS target, never a new lookup

For every non-stub capability with an empty `target_entity_ids`, the
correct value was not derived by guessing at a plausible entity — it was
found by reading the capability's OWN existing `Relationship` edges first:

```
python: relationships where from_id == this capability's id
```

Every one of the 7 capabilities fixed this way (`confirm_ignition_gateway_health`,
`confirm_wcs_service_health`, `confirm_wcs_api_responsiveness`,
`confirm_windows_service_and_event_log_evidence`,
`confirm_ups_chat_or_stunnel_health`, `recover_agv_physically`,
`pause_or_resume_agv_fleet`) already had a `VERIFIES` or `CONTROLS` edge to
a real, already-existing paired state/symptom entity from §6.10's
state-vs-action fix (e.g. `capability:confirm_ignition_gateway_health
--verifies--> entity:state:ignition_gateway_health_state`) — the
relationship existed, but the capability's own denormalized
`target_entity_ids` field, which is supposed to name the same thing for
fast lookup without a graph traversal, had simply never been back-filled
to match it. This is the same class of gap as §7's original finding
(`role_paths` restored from catalog text that already existed but was
dropped on migration) — the fact was already IN the Brain, just not
propagated to every field that should echo it.

**Rule for the future agent**: when `target_entity_ids` is empty on a
capability that has real content elsewhere (description, role_paths,
observables all populated), check its own outgoing `VERIFIES`/`CONTROLS`
relationships FIRST, before treating this as a research task requiring new
evidence. A capability's relationships are more authoritative than its own
possibly-stale denormalized id list, precisely because §6.10 already did
the hard judgment work of creating the correct pairing — reusing it here
is a Reinforce-shaped operation (§4.1), not a New-candidate one.

For `confirm_zone_configuration_state` and `pause_or_resume_agv_fleet`,
no such relationship existed yet (their state-vs-action pairing under
§6.10 didn't produce a dedicated state entity distinct from what
`allowed_surface_entity_ids` already implies), so the fallback rule
applied instead: search the entity registry directly for an existing,
already-real entity whose name matches what the capability's own
`description` says it checks/controls (`entity:ui_screen:zone_config` +
`entity:component:zone_config` + `entity:state:zone_configuration_staging_state`
for the former; `entity:state:agv_fleet_pause_soft_stop_state` — found by
name search, already existed with exactly the right semantics — for the
latter). Both were confirmed against real, already-populated entity
records, not created new.

### 9.3. Rule: `sql_field_notes`/`api_checks` come only from the source capability card's own fields, never invented from the capability's label

`docs/ontology/catalogs/capability_catalog.json` is the same hand-curated,
authoritative source §7.3 already reads from — every one of its 28 real
cards carries its own `api_checks: [...]` and `backend_mappings[].note`/
`sql_model_links` fields, populated by the people who wrote the catalog.
Where a Brain capability's `api_checks`/`sql_field_notes` was empty AND the
matching catalog card had real content in the equivalent field, that
content was copied over directly (`zone_config_state` → `GetZoneConfig`/
`UpdateZoneConfig`; `rms_soft_stop` → `PauseAGVs`/`ResumeAGVs`) — this is
pure data-propagation, not inference, and needed no new evidence beyond
what §7.3 already established as authoritative.

Where the catalog card's OWN equivalent field was also empty
(`gateway_health`, `wcs_service_health`, `wcs_api_responsiveness`'s
`sql_field_notes` equivalent, `windows_service_or_event_log`,
`agv_physical_recovery`'s `sql_field_notes`, `ups_chat_or_stunnel_health`),
the field was left empty rather than fabricated — confirmed by reading the
actual source JSON, not assumed. This matters because 3 of these
(`gateway_health`, `wcs_service_health`, `ups_chat_or_stunnel_health`) are
capabilities whose real diagnostic surface (Ignition gateway UI, Windows
Services MMC, Stunnel connection list) genuinely has no SQL model behind
it per the catalog author's own `sql_model_links: []` — writing a
plausible-sounding `SqlFieldNote` for these would misrepresent something
that is honestly UI/log-based, not database-backed, the same "don't invent
a query onto a Capability" rule already locked in `brain/README.md`'s core
rules and `capability.py`'s own module comment.

One case needed the caveat text itself preserved, not just the field
value: `confirm_zone_pairing_state`'s `sql_field_notes` were filled from
`zone_pairing_state`'s catalog card `backend_mappings[].note`, which
explicitly states *"Do not treat this as a source-confirmed
pairing-specific SQL model"* — the cross-linked RobotDatabaseModel/
RobotLocationDatabaseModel fields are the closest available backend
evidence for a pairing symptom, not a dedicated pairing model. That
caveat was copied verbatim into each `SqlFieldNote.purpose` string rather
than dropped, because writing the field/table reference alone without the
caveat would make a hedged, cross-linked inference read as confirmed fact
to whatever later agent (a Procedure/Playbook generator, per §5.1) reads
it next — the honesty of the source's own uncertainty is itself
information that must survive the copy, not an editorial nicety.

### 9.4. Rule: filling a stub capability with zero catalog card requires operational/incident evidence, not the fact that a card is missing

The 3 fully-empty stubs (`optisweep_service_restart`, `ignition_restart`,
`rms_map_reposition`) could not be filled from `capability_catalog.json`
at all — confirmed by grepping the catalog for all 28 real card ids and
finding none of these three among them, exactly as §6.6/§7.5 already
documented. `BRAIN_BUILD_PROCESS.md` §6.6 explicitly warned that writing
placeholder description text for these "would misrepresent how
well-understood they actually are" — that warning was about inventing
content with NO evidence, not a blanket ban on ever filling these records.
The actual rule applied here: search the full corpus (operational-source
evidence units, incident evidence/relationships) for real, concrete
mentions before deciding a stub stays a stub.

All three had real, previously-unconnected evidence sitting in the corpus:

- **`optisweep_service_restart`** and **`ignition_restart`**: found by
  reading `training_video_day2`'s transcript segments about tipper
  heartbeats going flat ("if you're not getting heartbeats, you have to
  restart Opti Sweep because OPC is stupid... ignition sometimes takes
  longer so it needs to be restarted") and, more concretely,
  case_228086's own incident evidence — a `gwcmd -r` command run from the
  Ignition install directory (events 018/022, confirming
  `ignition_restart` as a real, executed action against the Ignition
  gateway specifically) and an explicit two-step escalation documented in
  the incident's own procedure text ("verify OptiSweep service is still
  responding... if no response, restart OptiSweep," event 028 — confirming
  `optisweep_service_restart` as a DISTINCT, second-line action taken only
  after an Ignition restart doesn't clear the symptom, not a synonym for
  the same action). This distinction — two separate capabilities, ordered
  by which is tried first — was only visible by reading the incident's own
  procedural sequence, not from either transcript segment alone, which is
  why `ignition_restart.not_for` and `optisweep_service_restart.when_to_use`
  cross-reference each other's escalation order explicitly rather than
  describing each in isolation.
  There was already a real, existing `Relationship`
  (`capability:ignition_restart --applies_to--> entity:system:ignition_gateway`,
  citing `evidence:case_228086:event_018`) proving this capability's
  real-world use had already been recorded during §8's incident migration
  but never propagated back to fill the capability's OWN record — the same
  denormalization gap as §9.2, just discovered from the opposite direction
  (a relationship existed pointing from incident work back at a still-empty
  stub capability).
- **`rms_map_reposition`**: found by reading `aveva_hmi_catalog.json`'s own
  evidence array directly (not a keyword match against the id) —
  `evidence:training_video_day1:aveva_hmi_evidence_60` describes the "AGV
  Go-to function for manual repositioning": an operator selects a target
  by code or by clicking a map cell and confirms, for an AGV already in a
  green/ready state. This evidence unit was already cited by 25 other,
  unrelated entities sharing the same catalog evidence pool (the exact
  §6.8 finding that identical `source_refs` is a weak signal on this
  corpus) — reading the actual text, not just noting it existed, is what
  confirmed it was real, on-topic, groundable content for this specific
  capability and not a spurious pool-sharing coincidence.

Each of the 3 stubs' `description`/`when_to_use`/`not_for`/`role_paths`/
`observables`/`support_contract` was then written directly from this
evidence, following the same discipline as §8.1's per-event judgment: only
what the cited text actually supports, nothing extrapolated beyond it
(e.g. `rms_map_reposition.required_role_ids` was set to L2/L3 only,
matching the training video's own coaching framing of this as a support
action rather than a routine operator task — not asserted as certain, but
the most defensible reading of who is shown performing it in the source).
`sql_field_notes` was left empty on all 3 — none of the three evidence
sources describe a SQL model, and the "no invention" rule from §9.3
applies identically here.

### 9.5. Result

12 of 31 capabilities edited directly in
`brain/data/local/ontology_catalogs/capabilities.json` (no new script;
per §1, none should be added for this kind of fill): the 3 stubs
fully populated end-to-end, plus `target_entity_ids`/`sql_field_notes`/
`api_checks` gaps closed on `confirm_zone_pairing_state`,
`confirm_zone_configuration_state`, `pause_or_resume_agv_fleet`,
`confirm_ignition_gateway_health`, `confirm_wcs_service_health`,
`confirm_wcs_api_responsiveness`, `confirm_windows_service_and_event_log_evidence`,
`recover_agv_physically`, `confirm_ups_chat_or_stunnel_health` — each
edit traced to a specific, cited piece of already-ingested evidence
(catalog card field, operational-source transcript segment, or incident
event), never inferred from a capability's own label or id.
`sql_field_notes`/`api_checks` were deliberately left empty on capabilities
whose own catalog source card had nothing there either (§9.3) — a fully
audited "no known evidence exists yet" is a different, and equally valid,
end state from "populated," and this pass did not force placeholder
content into either just to reduce the empty-field count. Full-corpus
`validate_batch()` (2,189 entities, 31 capabilities, 1,917 claims, 11,570
relationships, 3,491 evidence units, 289 procedures) — 0 errors;
`pytest brain/tests/` — 41 passed.

### 9.6. Still open

- `role_paths`/`required_role_ids`/`observables`/`when_to_use`/`not_for`
  remain unpopulated on 3 capabilities only if a future pass discovers a
  capability §7.4 counted as "has role_paths" but whose content is
  actually thin — not re-checked field-by-field in this pass beyond the
  9 capabilities named in §9.1's scope; a full re-audit of the other 19
  fully-populated-looking capabilities' actual guidance QUALITY (not just
  non-emptiness) was out of scope here, same caveat §6.8/§6.12 already
  apply to "populated but not necessarily excellent" content elsewhere in
  the corpus.
- `sql_field_notes`/`api_checks` stay genuinely empty on `gateway_health`,
  `wcs_service_health`, `wcs_api_responsiveness` (SQL side only —
  `api_checks` there is populated), `windows_service_or_event_log`,
  `agv_physical_recovery` (SQL side only), `ups_chat_or_stunnel_health` —
  not a gap this pass could close without inventing content; would need
  new source-backed evidence (a future operational source, incident, or
  catalog update) before these can be filled, per §9.3's rule.
- The `ignition_restart`/`optisweep_service_restart` escalation-order
  finding (§9.4) came from reading ONE incident case's (case_228086's) own
  procedural text closely. All 4 incident cases are now migrated (§8) —
  worth a quick pass over case_218550/case_223554/case_228723's evidence
  for corroborating or contradicting restart sequencing before treating
  case_228086's ordering as universal; not done as part of this pass.

---

## 10. Drawing the agent's boundaries: Create / Audit-Merge / Migrate (2026-09-08)

Directed by the user: with §4/§4.1/§4.2 (the pipeline-stage tool design)
and §7/§8/§9 (three real, hand-executed precedent passes) both in place,
think concretely about what SKILLS and TOOLS the eventual ingestion agent
needs, and draw explicit boundaries between three activities named
directly: **creating** Brain records (across sources — operational,
incident, interaction/feedback), **auditing & merging** existing records,
and **migrating** records (bulk backlog work). This section is that
boundary design. It does not introduce new schemas or write code — per
§11.4 of the architecture lock, building the actual agent/tools remains
deferred; this is the contract those tools should follow once that
deferral lifts.

### 10.1. The axis that was already decided, and the axis that wasn't

Two tool lists already exist in this repo and agree with each other:

- **§4.2's four pipeline-stage tools** — `extract_evidence` →
  `classify_candidate` → `reconcile_candidate` →
  `validate_and_prepare_for_review` — a **stage** axis: what kind of
  transformation is happening to one piece of material right now.
- **`brain/DESIGN_RATIONALE.md`'s
  `brain_service/{extraction,classification,reconciliation,validation,
  persistence,review}.py`** plus its MCP tool list
  (`extract_evidence`/`classify_candidate`/`reconcile_candidate`/
  `persist_brain_records`/`approve_brain_diff`/`reject_brain_diff`) — the
  same four stages, named identically, plus the persistence/approval steps
  §4.2's fourth tool folds together. This is a network-callable wrapper
  around the same stage axis, not a competing design.
- **Architecture lock §11.3's 7 Foundry tools**
  (`get_ingestion_run`/`load_source_packet`/`get_brain_context`/
  `resolve_entities`/`validate_brain_records`/`persist_brain_records`/
  `record_reconciliation_result`) — lower-level primitives underneath the
  four stages (e.g. `classify_candidate` needs `get_brain_context` and
  `resolve_entities` internally; `validate_and_prepare_for_review` needs
  `validate_brain_records`). Still the same axis, one level down.

All three documents already agree on **what a stage does**. None of them
answer **who calls the stages, for what trigger, needing what different
retrieval shape** — that's the actual gap the user is pointing at by
naming three activities instead of one. Mapping the three named activities
onto the existing stage axis:

| Activity | Trigger | Which stages fire | New evidence involved? | What's actually missing |
|---|---|---|---|---|
| **Create** | New source material arrives (operational source, incident case, interaction/feedback event) | All four, in order, landing mostly on Reinforce/Patch/New-candidate | Yes — this is the defining feature | Nothing new. §7 (capability enrichment) and §8 (4 incident cases) are two full, successful executions of exactly this path already. |
| **Audit & merge** | A standing corpus-health question ("are there duplicates," "does everything still validate," "is this record's shape still correct"), not a source event | Only Reconcile-shaped logic (Patch/Conflict), but applied to **two-or-more EXISTING records against each other**, never new evidence against old | No — the entire input is already-ingested material | A tool contract does not exist. Named as a gap in §4.1 ("no callable implementation yet") and §6 item 3, but never designed. This is the actual boundary this section adds (§10.2). |
| **Migrate** | A human decides "there is a backlog of N sources/cases to run through Create" | Identical to Create, run N times | Yes, same as Create | Not a new decision-making tool — explicitly barred from being one by the 2026-09-08 rule (§1). Needs only a thin orchestration wrapper (§10.3). |

**The load-bearing distinction is Create vs. Audit-Merge, not Create vs.
Migrate.** Migrate is Create with a loop around it — §8's four incident
cases already proved this empirically: the *exact same* per-event judgment
framework (§8.1/§8.2), with no new categories, executed 4 times over a
real backlog with nothing but "which existing entities does THIS case's
content resolve against" varying case to case. Audit-Merge is genuinely
different in kind: it has no new evidence to extract, no source packet to
bound, and its "candidates" are pairs/sets of already-persisted records,
not raw text.

### 10.2. New tool: the Audit/Merge boundary

This is the one genuinely new contract this section adds, closing the gap
named in §4.1/§6. Two tools, deliberately narrow, mirroring why §4.2 split
Extraction from Classification from Reconciliation in the first place (one
bad judgment should not contaminate the next stage silently):

**Tool 5 — `find_audit_candidates`** (read-only corpus scan)

*Role*: Given a scope (a record type, an entity_type, "the whole
corpus," or a specific set of ids just touched by a Create run), return
groups of existing records that MIGHT be duplicates, mis-shaped
(entity-vs-claim boundary violations per §2), or carrying a dangling
reference — never decide anything, only surface candidates for the next
tool to judge. This tool is deliberately allowed to over-report; a
candidate that turns out fine on inspection is a correct, complete outcome
(§4.1's "flagged and left alone is a success of this check, not a failure
to resolve it" already established this for entity duplicates specifically
— generalized here to every audit-candidate kind).

*What it must check*, drawn directly from the four duplicate mechanisms
and two category-confusion patterns this corpus's own history already
found the hard way (`BRAIN_BUILD_PROCESS.md` §6.7, §6.8, §6.11, §6.12,
§6.13) — this list exists so the agent doesn't have to rediscover each
mechanism by accident the way a human review pass did the first time:

1. Near-identical or normalized-name-identical entities of the same
   `entity_type` (the casing/spacing-collision pattern, §6.12).
2. Same-name entities across DIFFERENT `entity_type`s that would collide
   if one side were ever retyped (the 4th mechanism, §6.13) — check this
   BEFORE any retype operation, not just periodically.
3. A `component`/`system` entity whose only relationship is a self-echoing
   `APPLIES_TO` back to the record it was extracted alongside (the
   bare-echo pattern, §6.11).
4. An entity whose own description reads as claim-shaped (verb-first,
   claim-verb constructions, 9+ word sentences — `is_claim_shaped()` from
   `entity_shape.py`) or, the harder case, reads as a claim despite having
   a short noun-phrase name (§6.12's `crash_example` finding — a type
   filter alone will miss this; sampling across ALL entity_types with no
   filter, per §6.12's explicit lesson, is required, not optional).
5. A `symptom`/`state` entity whose description is actually reference
   documentation, database-table-schema content, or a response/recovery
   description rather than the condition itself (§6.13's category-
   confusion patterns — the two sub-checks named there verbatim).
6. Any payload-embedded id-reference field (not just `Relationship`
   endpoints) pointing at an id absent from the current registry — this
   generalizes `validate_batch()`'s existing
   `validate_claim_references()`/`validate_capability_support_contract_references()`/
   `validate_procedure_playbook_references()` checks into an audit-trigger
   rather than only a write-time gate, so staleness introduced by a
   process outside this agent's own writes (a manual edit, a different
   session) is still caught.

*Output*: a list of `AuditCandidate` findings (see §10.2.1's schema), each
naming the record(s) involved, which check produced it, and — critically —
NOT a merge/fix decision. `find_audit_candidates` only finds; per §3's
already-confirmed lesson ("identical evidence" and "name/token overlap"
are candidate finders, never safe auto-merge signals"), nothing here is
allowed to auto-resolve.

**Tool 6 — `resolve_audit_candidate`** (judgment, one candidate at a time)

*Role*: Given one `AuditCandidate` plus the full content (evidence,
relationships, descriptions — not just the names that flagged it) of every
record it names, decide one of: **MERGE** (these are the same real thing;
specify winner, loser(s), and exactly which fields/relationships need
rewriting), **RETYPE** (a category-confusion fix — specify the corrected
`entity_type`/`capability_kind` and whether this creates a new same-name
collision per check #2 above, which must be re-run against the *proposed
new id* before finalizing), **RECLASSIFY** (an entity is actually
claim-shaped — specify the resolved subject entity the new Claim attaches
to, never fabricating a subject when nothing resolves), **NOT-A-DUPLICATE**
(a correct, complete, expected outcome — document why, so the same pair
doesn't get re-flagged and re-litigated every audit pass), or
**NEEDS-HUMAN** (genuinely ambiguous, e.g. the `tote_exchange_thresholds`
vs. `tote_exchange_threshold_categories` class from §3/§6.11 — two
independently-sourced, populated records describing the same real thing
from two different sources is NOT the same judgment as a bare echo, and
this tool must be able to say so rather than forcing every candidate into
MERGE or NOT-A-DUPLICATE).

*Prompting language*, following §4.2's existing tools' style exactly:

> You are resolving one audit candidate against the OptiSweep Brain. You
> have been given every record the candidate names, in full — not just the
> names/ids that caused them to be flagged, but their actual descriptions,
> relationships, and evidence. A name match or shared evidence pool is NOT
> sufficient grounds to merge on its own; you must find a structural or
> relationship-shape reason two records are the same real thing (what is
> each one actually connected to, independently of the other?).
>
> Decide exactly one of: MERGE, RETYPE, RECLASSIFY, NOT-A-DUPLICATE, or
> NEEDS-HUMAN. If MERGE, name the winner (prefer the more complete,
> non-garbled record — never the longer name alone) and specify every
> Relationship and payload-embedded id reference that must be rewritten so
> nothing dangles (checking Claims' `subject_entity_id`/`object.entity_id`
> and Capability's `support_contract` id lists, not just `Relationship`
> endpoints — this class of bug has recurred three times in this corpus's
> history; do not repeat it). If RETYPE, check whether the new id would
> collide with an already-existing record before finalizing — if it would,
> your answer is MERGE against that existing record, not a silent
> overwrite. It is a complete, correct answer to conclude NOT-A-DUPLICATE
> or NEEDS-HUMAN — do not force a merge or a fix to make the candidate
> queue shorter.
>
> Output: your decision, the specific records/fields affected, and your
> reasoning citing what each record is actually connected to.

**Why two tools, not one**: identical reasoning to §4.2's four-way split —
`find_audit_candidates` is a high-recall, low-precision scan (deliberately
over-reports); `resolve_audit_candidate` is the expensive, high-context
judgment call. Collapsing them means every scan result gets full judgment-
call treatment even when 90% of candidates are obviously unrelated
(§6.8's own finding: 41 groups shared identical source_refs, nearly all
false alarms) — wasteful, and it removes the seam where a bad scan
heuristic could otherwise be caught before consuming judgment-call budget
on garbage candidates.

### 10.2.1. The record this tool needs: `AuditCandidate` (new, minimal schema — not yet built)

Per the confirmed decision to persist findings durably rather than let
them live only in an in-memory return value or a one-off published report
(the exact failure mode §6.8/§6.11's early reports had — a real finding,
correctly identified, that required someone to remember it existed and
manually resolve it later): a small new record type is needed, in the same
`brain/schemas/` family as `EvidenceUnit`/`Entity`/etc.

```text
AuditCandidate
  id                    (type-prefixed, deterministic — hash of the
                         sorted record ids + check name, so re-running the
                         same scan doesn't create duplicate findings)
  check_name            (one of the 6 named in §10.2, or future additions)
  record_ids            (the 2+ existing Brain record ids this candidate
                         names)
  status                (open | resolved)
  resolution            (null until resolved; then one of MERGE/RETYPE/
                         RECLASSIFY/NOT-A-DUPLICATE/NEEDS-HUMAN, plus the
                         specific field-level changes if MERGE/RETYPE/
                         RECLASSIFY)
  resolved_by           (agent | human — distinguishes an LLM
                         resolve_audit_candidate judgment from a person
                         overriding it, same spirit as the deferred
                         validation_status field in §4)
  source_refs           (the evidence that grounded the resolution
                         decision itself, if any beyond the records' own
                         existing evidence)
```

This is deliberately the SAME shape as the deferred `validation_status`/
`review_status` field problem already named in §4 — both are "the Brain
needs to represent its own pending work, not just approved knowledge."
Building `AuditCandidate` without also resolving that broader field is
acceptable as a narrower first step (an audit finding is inherently
pending-review, so `status=open` already carries the semantics that field
would eventually generalize), but whoever designs `validation_status`
properly (§6's open question) should check whether `AuditCandidate` should
collapse into that more general mechanism rather than staying a parallel,
narrower one.

**Explicitly NOT decided here, left for whoever builds this**: whether
`resolve_audit_candidate`'s MERGE/RETYPE/RECLASSIFY decision executes
immediately (this tool both judges AND writes) or whether — matching
§4.2 Tool 4's pattern exactly — it only drafts the change for a fifth,
Curation-shaped step to approve before anything is written. Given that a
wrong MERGE has no clean undo (§6.8 already flagged this: "a wrong
cross-entity_type merge here has no clean undo the way
`consolidate_entities.py`'s narrow same-type rule does"), the strong
default should be the latter — `resolve_audit_candidate` proposes, a human
or the existing `validate_and_prepare_for_review` tool gates the actual
write — but this is flagged as a decision for build time, not locked here.

### 10.3. Migrate: no new tool, one thin orchestration wrapper

Confirmed: migration does not get its own judgment-bearing tool. Per §1's
standing rule (no new source-shape-specific script) and §8's empirical
proof (4 incident cases, 0 new judgment categories needed beyond §8.1/§8.2,
only which existing entities each case's content happened to resolve
against varied), the only thing migration legitimately needs beyond
Create's existing four tools is bookkeeping across a batch:

**Tool 7 — `run_migration_batch`** (pure orchestration, zero judgment)

*Role*: Given a list of source/case identifiers, call the Create path
(extract → classify → reconcile → validate) once per item, in order,
collecting a per-item outcome (`succeeded` / `needs_human_review` /
`failed`, with the specific validation errors or open questions for the
latter two) into one batch report. It contains no extraction, classification,
or reconciliation logic of its own — every judgment call still happens
inside the four existing tools, called once per batch item. This is
identical in spirit to `enrich_brain_knowledge.py`'s own per-source loop
(§7.3) and the incident harness's per-case loop (§8) — both already do
exactly this manually; `run_migration_batch` is naming that shape as a
reusable contract rather than a script.

*What it must NOT do*: retry a failed item with looser validation, skip an
item's `needs_human_review` outcome silently to keep the batch "clean," or
continue past an item whose failure suggests a systemic problem (e.g. the
same validation error on 3 consecutive items) without surfacing that
pattern — a batch tool that quietly downgrades its own failure signal to
keep moving is exactly the "silent overwrite" class of bug this corpus's
history (`BRAIN_BUILD_PROCESS.md` §6.13) already had to fix once in a
migration script; the orchestration wrapper inherits the same
responsibility not to paper over its own per-item failures.

*Relationship to Audit-Merge*: `run_migration_batch` may reasonably call
`find_audit_candidates` scoped to just the ids it created, once per item
or once at the end of the batch (mirroring §4.1's "duplicate-check is a
check every New-candidate passes through," now stated as literally the
same tool call) — but it does not implement duplicate-checking itself.
This is the concrete reason Audit-Merge had to be designed as its own
tool pair (§10.2) rather than folded into Reconciliation directly: both
Create (via `reconcile_candidate`'s per-candidate duplicate check, §4.1)
and Migrate (via this batch-scoped call) need to invoke it, and a
capability two different callers both need is a signal it belongs in its
own tool, not embedded inside just one of them.

### 10.4. The boundary, stated as one diagram

```text
                    ┌─────────────────────────────────────┐
                    │              CREATE                  │
                    │  trigger: new source material         │
                    │  (operational source, incident case,   │
                    │   interaction/feedback event)           │
                    │                                         │
                    │  extract_evidence → classify_candidate  │
                    │  → reconcile_candidate (calls           │
                    │  find_audit_candidates as its           │
                    │  duplicate-check step, §4.1)            │
                    │  → validate_and_prepare_for_review      │
                    └──────────────────┬──────────────────────┘
                                       │ called once per item by
                                       ▼
                    ┌─────────────────────────────────────┐
                    │             MIGRATE                  │
                    │  trigger: a human-identified backlog  │
                    │  run_migration_batch(items)           │
                    │  = loop over CREATE, zero new          │
                    │    judgment logic of its own            │
                    └───────────────────────────────────────┘

                    ┌─────────────────────────────────────┐
                    │           AUDIT & MERGE              │
                    │  trigger: standing corpus-health check │
                    │  (on-demand: human-invoked, or scoped  │
                    │   inline call from CREATE/MIGRATE —     │
                    │   no autonomous background sweep)       │
                    │                                         │
                    │  find_audit_candidates (read-only scan) │
                    │  → resolve_audit_candidate (judgment,   │
                    │    one candidate at a time)             │
                    │  → [proposes; does not itself write —   │
                    │     gated by validate_and_prepare_for_  │
                    │     review same as everything else]     │
                    │                                         │
                    │  persists findings as AuditCandidate    │
                    │  records (§10.2.1) so a finding survives│
                    │  across sessions instead of being lost  │
                    │  the way early one-off reports were     │
                    └───────────────────────────────────────┘
```

**The one-sentence version of the boundary**: Create and Migrate both
produce NEW records from NEW evidence and differ only in whether a human
runs the pipeline once or in a loop; Audit-Merge produces no new evidence
at all and instead asks whether EXISTING records are correct relative to
each other — that difference in what the input even is (new source text
vs. two-or-more already-persisted records) is why it needed its own tool
pair rather than being squeezed into Reconciliation's existing per-
candidate duplicate check, even though both ultimately call the same
underlying judgment ("are these the same real thing").

### 10.5. What this section deliberately leaves open

- The background-sweep mode for Audit-Merge (a scheduled, autonomous
  corpus scan rather than on-demand/inline-only) was explicitly considered
  and deferred, not designed — flagged here as a real future mode rather
  than silently dropped. It would need a findings queue and a scheduler
  that don't exist anywhere in this design yet, and per §10.2.1's
  discussion, probably wants the general `validation_status` mechanism
  (§6) settled first rather than building a second, parallel pending-work
  concept.
- Whether `resolve_audit_candidate` writes directly or only proposes
  (§10.2.1's last paragraph) is named as a real fork, not resolved — the
  strong recommendation is "proposes only," but this is a build-time
  decision, not locked here.
- `AuditCandidate`'s exact relationship to the still-undesigned
  `validation_status`/`review_status` field (§4, §6) is flagged, not
  resolved — they may end up the same mechanism.
- This section does not address the runtime/retrieval agent (`get_brain_context`
  as used by an answering assistant, per the plan doc's §9) at all — that
  is a fourth, separate concern (read-only consumption of Brain, not
  Create/Audit/Migrate) explicitly out of scope for this boundary pass.

---

## 11. Promoting the third shape: `EntityType.SYSTEM_ACTION` (2026-09-08)

Directed by the user directly: §2's third-shape note ("a system/API action
is something the system does when called, not a human action and not a
persistent state... worth flagging as a distinct sub-case if a dedicated
concept ever becomes useful") was accepted as now useful, and the schema
was changed rather than left as a documented deferral. This is a genuine
schema addition (`brain/schemas/entity.py`), not a data-only judgment call
like §9/§10 — recorded here for the same reason every other schema
decision in this document is: so a future agent knows WHY `system_action`
exists and what it is and isn't for, not just that it does.

### 11.1. Why `component` was never actually correct for this, just tolerable

`component` is Part 1's catch-all for "a named, look-up-able thing that
doesn't fit a more specific type" — correct in the weak sense that an API
endpoint IS a named, look-up-able thing, but this is exactly the same
weak-correctness problem `BRAIN_BUILD_PROCESS.md` §6.10 already found and
fixed for Capabilities named after the state they check instead of the
action they perform: a label can be technically valid under a loose type
while still obscuring a real, useful distinction. Concretely, folding
`GetAGVStatuses` (a read-only query, safe to call anytime) and
`UpdateZoneConfig` (a mutation the catalog's own notes flag as "rarely
customer-used" and high-risk) into the same undifferentiated `component`
bucket as "Tipper (a labeled diagram callout)" and "Zone Config (a UI
screen's associated component)" meant nothing in the schema itself could
answer "is this callable, and does calling it change system state" without
re-reading each entity's evidence by hand every time — exactly the kind of
question a Capability's `support_contract`/a Procedure's `exact_action`
needs answered when deciding whether an action is safe to suggest.

### 11.2. The new type: `EntityType.SYSTEM_ACTION`

Added to `brain/schemas/entity.py` alongside the other 10 MVP entity
types, with a real (not `EmptyPayload`) `SystemActionPayload`:

```text
SystemActionPayload
  invocation_kind: str = ""                        # free string, not an enum — see below
  access_surface_entity_ids: list[str] = []         # entity ids, validated well-formed
  mutates_state: bool | None = None                 # None = genuinely unknown, not "no"
```

**`invocation_kind` is a free string, not an enum, on purpose.** The
corpus's only real source for it (`wcs_api_catalog.json`'s
`objects[].group` — `"system"`/`"agvs"`/`"totes"`) is the catalog
author's own subject-matter grouping, not a stable technical taxonomy of
HOW an action is invoked (REST call vs. RMS UI button vs. SSMS stored
procedure, say). Forcing it into a small closed enum now would either
throw away real source vocabulary or invent categories the evidence
doesn't actually support — the same "don't invent structure the evidence
doesn't ground" rule applied throughout §9. A future source (a second API
surface, a CLI tool) can extend the vocabulary without a schema migration,
since it's just a string field.

**`mutates_state` is nullable, not defaulted to `False`.** A system action
whose mutation status genuinely isn't known from any evidence yet must be
distinguishable from one confirmed read-only — defaulting to `False` would
silently assert safety that hasn't actually been verified, which is
exactly the kind of unearned confidence §9.3's "don't invent a query onto
a Capability" rule already guards against for SQL notes. Every one of the
29 real entries migrated in §11.3 below has an explicit `True`/`False`
judgment, grounded either in the action's own name (`Get*` reads,
everything else mutates) or, for the one genuinely ambiguous case
(`ExecutedAgvCommand`), the catalog's own note text ("re-exec active
command if OptiSweep missed Geek callbacks" — confirmed as a real
mutation, not guessed from the name alone).

**`access_surface_entity_ids` reuses the exact validation pattern already
established on `Capability.support_contract`/`SqlFieldNote`** — a list of
entity ids, checked well-formed (`entity:` prefix) via the same
`is_well_formed_id` helper, not a bare string list. This is what lets a
future Procedure/Playbook agent (§5.1) answer "what surface do I call this
through" without re-deriving it from evidence text every time.

### 11.3. The migration: 29 `component` entities retyped

Scope was established by cross-referencing, not guessed: every capability
in `brain/data/local/ontology_catalogs/capabilities.json` with a
populated `api_checks` list names 28 distinct real API action strings;
`docs/ontology/catalogs/wcs_api_catalog.json`'s own `objects[]` array
(the WCS API's closed, hand-curated, authoritative endpoint list — the
same source §9.3 already established as authoritative for `api_checks`
content) independently confirmed 26 of those as its canonical entries,
with `group`/`access_surface` detail to ground the new payload from. Two
more real matches (`entity:component:initialize_tote`,
`entity:component:exchange_sorter_side_zone`) are the same real actions
under a second, differently-formatted name from a different source —
already-known, deliberately-not-merged near-duplicates of
`initializetote`/`exchangesortersidezone` per `BRAIN_BUILD_PROCESS.md`
§6.12's "genuinely independently-real-record" finding — retyped alongside
their canonical counterparts so both spellings land in the correct class;
whether the two spellings should ALSO be merged with each other stays the
separate, already-open near-duplicate question
`entity_duplicate_merges.py`'s docstring already tracks, not something
this correction resolves or should resolve. One `api_checks` name
(`GetChargersStatus`) had no matching entity at all — a gap, not a
miscategorization, left alone.

Applied as new entries in the existing `entity_type_corrections.py` /
`apply_entity_type_corrections.py` pair (pattern 4 in that module's
docstring) rather than a new script — this is the same hand-judged
`old_id -> new_type` correction mechanism §6.13 already built and
`BRAIN_BUILD_PROCESS.md` §9 already documents as a required, permanent
step of the rebuild order, extended with new entries the same way
`capability_state_pairings.py`/`entity_duplicate_merges.py` have already
grown by entries rather than by new files. `apply_entity_type_corrections.py`
gained one new branch (mirroring its existing `database_table` payload-
override branch) plus a `SYSTEM_ACTION_PAYLOAD_OVERRIDES` dict, hand-
populated from `wcs_api_catalog.json`'s own `group` field per entry and a
single shared `access_surface_entity_ids = [entity:system:wcs_api]` (the
catalog's own single top-level `access_surface` value).

**Collision check, per §6.13's already-learned lesson (a retype must
verify its new id against the existing registry before writing, not
assume uniqueness)**: run and confirmed clean before writing — all 29 new
`entity:system_action:*` ids were unoccupied, zero collisions, zero
merges. Every reference across the corpus was rewritten by the existing
script's Relationship/Claim rewrite logic (the same two reference kinds
§6.13 already generalized `apply_entity_type_corrections.py` to handle):
90 `Relationship` endpoints in `ontology_catalogs/relationships.json`, 29
more in `training_video_day2/relationships.json`, and 1 `Claim` reference
in `training_video_day2/claims.json` — the only 3 files (of the full
corpus, ontology + 5 operational sources + 4 incident cases) that actually
referenced any of the 29 old ids, confirmed by a corpus-wide search before
running the script, not assumed from the script's own source list.
`Capability.target_entity_ids`/`support_contract` payload fields were also
checked directly (per the same §6.10/§6.13 lesson about payload-embedded
id references) and confirmed to reference none of these 29 ids — the
capability side of this gap (missing `api_checks` strings, not missing
entity ids) was already the subject of §9's separate backfill.

**Result**: `entities.json` unchanged in total count net of the retype
(29 `component` → 29 `system_action`, 0 collisions so 0 entities lost to
merging); full-corpus `validate_batch()` (2,190 entities, 31 capabilities,
1,998 claims, 11,587 relationships, 3,592 evidence units, 289 procedures)
— 0 errors; `pytest brain/tests/` — 41 passed.

### 11.4. What this does and doesn't change elsewhere

- **Capability `api_checks` stays a free-text string list, not
  `system_action` entity ids.** Considered and deliberately NOT changed:
  `api_checks` is meant to be quickly scannable free text on the
  Capability record itself (matching how `sql_field_notes` keeps `field`
  as a string even though `database_entity_id`/`table_entity_id` are real
  ids) — converting it to a list of entity ids would be a separate,
  larger schema change affecting all 31 capabilities' existing data, out
  of scope for what the user asked for here. The new `system_action`
  entities are additive, richer context a future agent CAN cross-reference
  by name (`api_checks: ["GetAGVStatuses"]` on a Capability now has a real
  `entity:system_action:getagvstatuses` record to resolve against, with a
  known `mutates_state`), not a replacement for the existing field.
- **§10's Audit/Merge tool boundary directly benefits from this.**
  `find_audit_candidates`'s category-confusion check (§10.2, check #5) was
  written to catch `symptom`/`state` content that's actually something
  else; the same reasoning now applies to `component` — a future audit
  pass should check whether any REMAINING `component` entity is actually
  an uncaptured system/API action (e.g. a command surfaced by a future
  operational source that isn't in `wcs_api_catalog.json`'s closed list),
  using the same "put a person's name in front of it" style test used for
  Entity/Capability: does this look up as a name (component) or does it
  read as something invoked with a call signature and a return/side
  effect (system_action)?
- **Not migrated, and deliberately so**: no other `component` entity was
  retyped. The scope was bounded to entities matching a real, cited
  `api_checks` name or the closed `wcs_api_catalog.json` object list —
  not "every component that sounds action-like," which would have been
  exactly the untethered, evidence-free judgment §9.3/§9.4's "no
  invention" rule already forbids. Any future system_action candidate
  needs its own citable evidence the same way these 29 did.

---

## 12. Playbooks promoted for the first time (2026-09-08)

Directed by the user after noticing Brain had zero `Playbook` records
despite the schema being built (§5.3) months earlier. This section is the
replicable record of that promotion — the schema was never the gap; the
promotion pass simply had never been run, and running it surfaced two more
real, previously-invisible gaps along the way.

### 12.1. What was actually missing (established before writing anything)

Checked directly rather than assumed: `find brain/data/local -iname
playbooks.json` returned nothing, anywhere — 0 Playbook records across the
whole corpus, confirmed before any promotion work started. `Procedure`
records DID exist (289, from §7's 2026-09-03 enrichment run), but that run
only walks `brain/data/local/operational_sources/<source>/` — it never
scans `brain/data/local/incidents/<case>/`, so any incident-native runbook
was invisible to it by construction, not by a bug.

The real, promotable playbook material lives in
`shared_pipeline_stages/data/output/shared/stage_8_finalized_playbooks/` —
genuine branching graphs (nodes, typed outcomes, evidence-cited branches),
one directory per extraction experiment:

- `prompt_a_one_per_incident/`: exactly one playbook per incident case (4
  total).
- `prompt_b_multi_flow/`: allows more than one playbook per case when the
  incident's content is separable into distinct flows (5 total — case_223554
  splits into a `hospital_tote_induction` flow and a `site_sort_unavailable`
  flow).

`docs/design_decisions/stage_8_playbook_finalization.md` is explicit and
unambiguous that **neither variant is canonical**: "Treating Stage 8 output
as canonical would prematurely freeze extraction experiments (Prompt A vs
B) before SME review," and every finalized playbook there already carries
`validation_status: needs_sme_review` in its own source data — which maps
directly onto `Playbook.validation_status`'s existing schema default.
Per the user's explicit direction, this promotion brings in BOTH variants,
tagged by extraction source, rather than picking one — Brain becomes the
place the A/B comparison happens (an SME reviewing both), not something
that pre-decides it.

### 12.2. A second, distinct gap found while resolving playbook node references

17 distinct bare `procedure_id` strings are referenced across the 9
playbooks' `procedure_reference`-typed nodes (`resolved_runbook_ids`).
Checked against the 289 already-promoted Procedures by suffix match: only
12/17 resolved. The other 5 were not a matching-logic problem — they were
**genuinely un-promoted runbooks**, confirmed by finding their real source
files:

- 4 are incident-native finalized runbooks
  (`incidenceknowledgeingestion/data/output/incidents/<case>/stage_6_finalized_runbooks/finalized_runbooks/`)
  — real files, never touched by §7's enrichment run for the structural
  reason above (`case_218550`, `case_223554`, and 2 more under
  `case_228086`'s own Stage 6 output — one of the 4 was found only
  retroactively, see §12.2.1).
- 1 (`proc_recover_from_agv_fault_during_exchange_recovery_v1`) is an
  OPERATIONAL-source runbook (`manual_optisweep_om_v3`) with empty
  `capability_tags` and no `Relationship(USES)` fallback — exactly one of
  §7.4's originally-reported "11 runbooks skipped (`no_capability`)," which
  `enrich_brain_knowledge.py`'s own "never invent" rule correctly refused
  to guess a capability for at the time. Reading its own title/summary
  directly ("stopping RMS, removing the faulted AGV... introducing a new
  tote and placing an empty AGV") confirmed this is
  `capability:recover_agv_physically`'s exact scope ("On-site remove/add
  AGV, bump recovery, or isolation from active fleet") — a judgment call
  made here and documented, not invented from the runbook's id/title alone
  the way the "never invent" rule forbids. This is the correct way to close
  a `no_capability` skip: read the content and ground the answer in it,
  not guess from the runbook's slug.

Both classes were promoted via a disposable harness (not committed, per
§1) that reuses `enrich_brain_knowledge.py`'s existing, already-proven
`_promote_runbook_to_procedures` function directly rather than
re-implementing runbook-to-Procedure logic — the only new code was
building the `EvidenceUnit(sme_note)` wrapper per raw runbook file (same
shape as Pass 1's `migrate_operational_source.py` already uses for
operational-source finalized runbooks: `id: evidence:<source>:runbook_<procedure_id>`,
`text: summary or title`, `structured_payload: whole record`) and, for
incident-native runbooks, tagging `constraints.sites = ["ups_haslet"]` per
§8.1's standing rule for anything sourced from this site's incident data.
Multi-tagged runbooks correctly produced multiple Procedures (one per
resolvable capability, exactly §7.3's documented behavior) — 12 new
Procedures total from 4 real runbook files (289 → 301).

**12.2.1. A duplicate-write bug, found and fixed mid-pass, not shipped
silently.** The harness script initially had two bugs: (1) its `--write`
persistence step hardcoded a partial case list (`["case_223554",
"case_228086"]`) that excluded `case_218550` even after `case_218550`'s
runbook was added to the promotion scope, and (2) it appended to existing
`evidence_units.json`/`procedures.json`/`relationships.json` files without
deduplicating by id, so running `--write` more than once (which happened
here, once to catch bug #1) silently tripled some records. Caught by
directly counting records vs. unique ids in the written files immediately
after — not assumed clean because the dry-run counts looked right — the
same "verify the write, don't trust the dry-run" discipline
`BRAIN_BUILD_PROCESS.md` §6.13 already had to learn once for a migration
script's silent-overwrite bug. Fixed by (a) deriving the write loop's case
list from the same dict the promotion logic already iterates over instead
of a second hardcoded list, and (b) making every write merge-by-id
(`existing_by_id[r.id] = r` semantics) rather than blind list
concatenation, so a re-run is idempotent instead of accumulating
duplicates. The corpus was then deduplicated directly (kept first
occurrence per id, content was identical across the accidental repeats
since generation is deterministic) rather than needing a full rebuild —
confirmed via unique-id counts, not assumed.

### 12.3. Judgment calls made converting the raw playbook JSON into `Playbook` records

The raw Stage 8 output is NOT a clean drop-in for the schema — each node
in the raw data carries dozens of retrieval-debug fields (per-candidate
cosine/jaccard scores, a full `retrieval_eligibility_trace` listing every
runbook considered and rejected) that have no place in a governed Brain
record. Filtering this down to what the schema actually models required
real per-field judgment, not a structural transform:

1. **`source_refs` could not use the raw data's own citation shape.** Every
   node/branch in the raw JSON cites evidence as `{page_ref: "case_X:page_N",
   quote_or_summary, site_code, ...}` dicts — but incident timeline
   `EvidenceUnit`s in Brain use `locator.timeline_event_order`, never a page
   number (§8.1), so `page_ref` cannot resolve to any real Brain evidence
   id. `related_event_ids` (format `incident_<case>_event_<NNN>`) DOES
   resolve cleanly to `evidence:case_<case>:event_<NNN>` — checked and
   confirmed 100% resolution (153 total references, 0 misses) across all 9
   playbooks BEFORE committing to this as the citation strategy, not
   assumed. Every node's `source_refs` uses its own `related_event_ids`,
   converted; every branch reuses its parent node's same set (a branch
   condition is drawn from the same node's diagnostic content, not
   independently sourced in the raw data).
2. **`prompt_b` has a node_type (`branching_condition`) with no
   `PlaybookNodeType` equivalent.** Only 2 real instances exist corpus-wide.
   Read both directly rather than extending the enum for a 2-instance
   naming variant: both read as genuine diagnostic-decision content
   ("distinguish an AGV sequence... from a tote or task condition,"
   "choose whether... or whether the evidence does not support that
   path") — mapped to `DIAGNOSTIC_DECISION`, the same test §2's
   Entity/Capability boundary already uses (read what it actually asserts,
   don't trust the label).
3. **`ontology_capabilities[].id` is internally inconsistent within the
   same node** — the same node's list can contain BOTH a bare pre-rename
   catalog slug (`"fleet_system_status"`) and an already-prefixed id
   (`"capability:fleet_system_status"`) for the identical capability, with
   no consistent ordering. Taking the first list entry (the naive
   approach, tried first) crashed pydantic validation on the bare form.
   Fixed by resolving every candidate through
   `enrich_brain_knowledge._catalog_slug_to_capability_id` (the same
   PAIRINGS-aware resolver §7.3 already uses for `capability_tags`) after
   stripping any `capability:` prefix first, rather than trusting either
   form or the list's ordering.
4. **Multi-candidate `procedure_reference` nodes needed per-node
   disambiguation, not a first-match default.** A `resolved_runbook_ids`
   bare id can now resolve to MULTIPLE real Procedures (when the
   underlying runbook was multi-capability-tagged, per §7.3's "one
   Procedure per resolvable capability" rule) — `PlaybookNode.procedure_id`
   is a single field, so one had to be chosen. 5 such cases were found and
   judged individually by reading each node's own `title`/`intent` against
   each candidate Procedure's capability, never applying the same answer
   twice without re-checking:
   - `case_228086` node "Restore the affected OptiSweep or gateway
     service" → `confirm_ignition_gateway_health` (both prompt_a and
     prompt_b's equivalent node — same judgment, verified independently
     for each since they carry different node_ids).
   - `case_228086` node "Correct residual AGV synchronization state" using
     "the authorized RMS recovery procedure" → `recover_agv_physically`
     (a real floor-recovery action, over an SSMS-state-inspection
     alternative from the same multi-tagged runbook).
   - `case_223554`'s hospital-tote runbook is 3-way multi-tagged
     (`tote_lifecycle_state`/`agv_physical_recovery`/`fleet_system_status`)
     and is cited by 3 DIFFERENT nodes across the two extraction variants,
     each describing a genuinely different recovery scope — judged
     individually, not the same answer applied three times:
     `prompt_a`'s single generic node (which names all three concerns at
     once, a symptom of one-flow-per-incident forcing multiple concerns
     into one node) was resolved to `recover_agv_physically` as the most
     concrete, distinct RECOVERY action it names; `prompt_b`'s
     `hospital_tote_induction` flow's own node ("correct the affected AGV
     or tote state") resolved to `confirm_tote_lifecycle_state`; `prompt_b`'s
     `site_sort_unavailable` flow's own node ("service or Hospital Lane
     recovery path") resolved to `confirm_fleet_system_status`. This is a
     concrete illustration of why `prompt_b`'s multi-flow separation is
     substantively more precise than `prompt_a`'s single-flow-per-incident
     shape for at least this one case — exactly the kind of finding an SME
     comparing the two variants (§12.1) should see, not something this
     promotion pass should paper over by forcing one answer.
5. **`next_node_id: ""` (empty string, meaning terminal) converts to
   `None`** to match the schema's `Optional[str]` — the raw data has no
   `null`, only empty string, for a branch with no successor.

### 12.4. Result

9 `Playbook` records written to each referenced case's own
`brain/data/local/incidents/<case>/playbooks.json` (a new file per case,
alongside the existing `evidence_units.json`/`claims.json`/
`relationships.json`/`procedures.json`): 2 for `case_218550`, 3 for
`case_223554` (1 from prompt_a + 2 from prompt_b's split), 2 for
`case_228086`, 2 for `case_228723`. Each carries `id:
playbook:<extraction_tag>:<case>:<distinguishing_token>`,
`constraints.sites = ["ups_haslet"]`, and `validation_status:
needs_sme_review` (never silently upgraded to approved — matching every
other "nothing before Curation is production-eligible" rule in this
document). One new `EvidenceUnit(sme_note)` per raw playbook JSON file (9
total, `structured_payload` holding the whole raw record, same "stage
instead of modeling" pattern §3's mapping table already uses for Stage 5/6
runbook-candidate content) plus the 12 new Procedures from §12.2.

Full-corpus `validate_batch()` (2,190 entities, 31 capabilities, 2,008
claims, 11,599 relationships, 3,606 evidence units, 301 procedures, **9
playbooks** — including `validate_procedure_playbook_references()`
checking every node's `capability_id`/`procedure_id`/`symptom_entity_id`/
`allowed_role_entity_ids` against the full corpus's known ids) — 0 errors.
`pytest brain/tests/` — 41 passed.

### 12.5. Still open

- **Resolved 2026-09-08, see §12.6**: entry-symptom / node-symptom
  resolution against the real `entity:symptom:*`/`entity:state:*`
  registry. §12.6 documents both the one-time backfill (applied to all 9
  playbooks) and, per explicit user correction, the reusable method a
  future ingestion-pipeline classification step should call for any new
  incident — not a static lookup table.
- **Resolved 2026-09-08, see §12.7**: the `stage_8_comparison_report.json`
  A/B comparison and the cross-variant (`prompt_a` vs `prompt_b`) content
  comparison. §12.7 documents the reusable comparison method plus a
  case-by-case finding for the 4 cases at hand — deliberately NOT applied
  as a schema field or an automatic "always prefer X" rule; it is a
  Curation-shaped finding for SME review, matching §4/§10's "propose,
  never silently decide" pattern.
- **Cross-incident canonical-playbook deduplication itself remains
  undone**, and correctly so — the design doc's own stated NEXT step
  ("Canonical playbook... Future shared stage after SME review and
  cross-incident dedup") is explicitly out of scope for Stage 8, and by
  extension for this promotion too. All 9 playbooks still stand as
  independent, unreviewed records; §12.7's comparison finding is an input
  to that future step, not a substitute for it.
- **This promotion covered only the 4 incident cases already migrated
  (§8).** Any future incident case follows the same two-step shape
  established here: promote its Stage 6 finalized runbooks as Procedures
  FIRST (§12.2's pattern, checking capability_tags/USES-relationship
  resolution honestly rather than assuming success), then promote its
  Stage 8 finalized playbook(s) (§12.3's judgment framework) — not a new
  procedure, the same one, generalized.
- The disposable harness scripts used here (`promote_incident_procedures.py`,
  `promote_playbooks.py`, `apply_symptom_entity_mapping.py`) are
  scratch/session material, per §1's direction that no new
  source-shape-specific script should be added to `brain/migration/` — if
  a similar harness is useful for the next incident case's Playbook
  promotion, treat it as disposable execution plumbing again, not a
  reusable migration tool. **The hand-judged dicts these scripts apply
  (`symptom_entity_mapping.py`'s `PLAYBOOK_ENTRY_SYMPTOMS`/`NODE_SYMPTOMS`,
  `promote_playbooks.py`'s `PROCEDURE_ID_OVERRIDES`) are records of a
  one-time backfill decision, not a generalizable procedure — see §12.6
  for the actual reusable method a future ingestion-pipeline step should
  follow, since a static node_id-keyed lookup table has nothing to offer
  the NEXT incident's playbook.**

### 12.6. The reusable method (not just the answer key) — corrected 2026-09-08

**User correction, mid-session, worth recording verbatim in spirit**: after
resolving §12.5's symptom-entity gap for the 4 already-migrated cases via a
hand-judged, node-id-keyed dict (`symptom_entity_mapping.py`), the user
flagged that this must not be mistaken for the actual fix — "make sure
we're not hardcoding too much... this needs to happen in the ingestion
pipeline in the future." The dict is a correct, honest record of what WAS
decided for 4 specific, already-migrated incidents (same status as
`capability_state_pairings.py`/`entity_duplicate_merges.py`/
`entity_type_corrections.py` — permanent, hand-judged, re-appliable
records of a backfill decision, per `BRAIN_BUILD_PROCESS.md` §9's "these
are required, permanent fixtures, not one-time cleanup" pattern for that
exact class of file). But unlike those three, nothing about THIS
resolution step had yet been written down as a repeatable METHOD — only as
a lookup table whose keys are literal `node_id` strings from 4 specific
playbooks. A 5th incident's playbook has no `node_id` in this dict at all;
without a documented method, whoever handles it would have no choice but
to re-derive the whole matching approach from scratch, reading this
section's prose as inspiration at best.

**The actual reusable procedure, stated once so it generalizes**, following
the exact style of §4.2's tool prompts (concrete enough to hand to a real
tool call, not abstract "use judgment" prose):

> Given one Playbook (or its raw pre-Brain candidate, before promotion) and
> its `observed_entry_symptoms` (playbook-level) or one node's own
> `title`/`intent`/`unhealthy_indicators` (node-level), resolve it against
> Brain's existing `entity:symptom:*`/`entity:state:*` registry:
>
> 1. Retrieve candidate entities by querying the registry for `symptom`/
>    `state` entities whose `name`/`aliases` share vocabulary with the free
>    text — this is the SAME retrieval `get_brain_context` (§11.3,
>    undesigned but named) would need to supply to any classification tool,
>    not a bespoke lookup for this task. Do not limit retrieval to an exact
>    substring match — `entity:symptom:bag_out_stuck` must be findable from
>    "Automated bag-out stops after sorting," which shares no exact
>    substring beyond "bag-out."
> 2. For each candidate, check whether the free text is actually describing
>    THAT specific condition, not a merely-related one — the same
>    discipline §2's Entity/Capability boundary test and §10.2's audit
>    checks already require (read what it actually asserts, don't pattern
>    match on shared words alone). Confirmed failure mode from this exact
>    pass: `entity:symptom:hospital_diversion` shares the word "hospital"
>    with a bag-out playbook's "hospital-area HMI shows a fault," but names
>    a completely different condition (AMRs incorrectly routing TO the
>    hospital lane) — word overlap without meaning match is not a real
>    resolution, matching the exact same lesson §3/§10.2 already
>    established for entity-duplicate detection ("identical evidence" and
>    "name/token overlap" are candidate finders, never resolution signals
>    on their own).
> 3. Prefer a real relationship-shape check when one exists: does a
>    candidate symptom/state entity already have a `may_indicate` edge to a
>    capability this playbook's own nodes also reference? A confirmed
>    structural link (like the `capability_id` resolution in §12.3 already
>    draws from `ontology_capabilities[].id`) is stronger evidence than a
>    name match alone, the same "structural or relationship-shape
>    confirmation" §3/§10.2 already require before trusting a candidate.
> 4. If nothing in the retrieved candidates genuinely matches, resolve to
>    NOTHING — leave `symptom_entity_id`/`entry_symptom_entity_ids` for
>    that item unset. Per the user's explicit direction this session and
>    the confirmed "flagged and left alone is a success of this check, not
>    a failure to resolve it" lesson (§4.1, §10.2): a correct empty
>    resolution is a complete, valid outcome, never a gap that should be
>    papered over with an inexact forced match. This is why the actual
>    2026-09-08 backfill left 1 of `bagout_agv_sequence`'s 5 entry symptoms
>    and 1 of its 3 diagnostic nodes unresolved (§12.5's now-corrected
>    account) rather than forcing all of them to resolve to something.
> 5. Node scope: only nodes whose OWN diagnostic content checks a distinct
>    condition get a `symptom_entity_id` — a `procedure_reference`/
>    `validation_gate`/`escalation_gate` node acts on or validates the
>    outcome of the diagnostic node(s) before it; it does not itself check
>    a new condition and should not be given one just to fill the field.
>
> This is not a new tool — it is the SAME shape as §4.2's `classify_candidate`
> (free text + retrieved context → a resolved reference, or an honest "no
> match," never invented) applied to Playbook/node content instead of a raw
> extraction candidate. A future ingestion-pipeline step that promotes a
> new incident's playbook should call this same classification logic
> per-symptom-string, not re-derive the approach, and DEFINITELY not
> maintain a hand-typed dict of every incident that has ever existed —
> that shape only ever worked for the 2026-09-08 backfill because the
> universe of already-migrated incidents was small and fixed (4 cases, 9
> playbooks) at the moment this pass ran.

**What this corrects about §12.5's original framing**: the original
"still open" bullet (now folded into this section) undersold the gap by
treating "run the resolution once" as the goal. The actual gap this
correction closes is documenting that resolution as a *repeatable
classification step*, callable by the eventual ingestion agent (§4/§10),
not a backfill deliverable whose value expires once these 4 cases are
covered.

### 12.7. Comparing `prompt_a` vs `prompt_b`: the reusable method, then one application

Same discipline as §12.6, applied to the second and third §12.5 items
together (they turned out to be one task: reading `stage_8_comparison_report.json`
IS the input to doing the actual comparison, not a separate step). Written
as a documented method first, then applied once to the 4 cases at hand —
explicitly labeled as a backfill instance, not the permanent mechanism,
per the same correction as §12.6.

**Why this can't just be "attach the report's fields to the Playbook
record"**: `stage_8_comparison_report.json` is itself a one-off artifact
of comparing exactly two NAMED prompt variants from one specific pipeline
experiment. A future incident's playbook generation may produce one
candidate, three, or a completely different pair of extraction strategies
with a differently-shaped comparison report — there is no guarantee a
"prompt_a_vs_prompt_b" report ever exists again in this shape. Baking
`branch_graph_completeness: 0.9434` onto a Playbook record as a schema
field would hardcode a fact with no path to ever being refreshed, exactly
the failure mode the user's correction (§12.6) already named. `Playbook.confidence`
already exists as the generic per-candidate quality signal (populated from
each raw playbook's own self-reported `confidence` during promotion,
§12.4) — that is the right field for a SINGLE candidate's self-assessed
quality. Comparing MULTIPLE candidates against each other for the same
incident is a different kind of judgment (relative, not absolute) and
belongs in a Curation-shaped finding, not a record field.

**The reusable method**, generalized from what this pass actually did:

> When more than one Playbook candidate exists for the same incident
> (regardless of why — different extraction prompts, different pipeline
> runs, different agent attempts), a Curation-shaped comparison step should:
>
> 1. Read whatever structured quality signal the generating process
>    actually produced for each candidate (link-confidence rates,
>    branch-graph completeness, `needs_graph_repair` flags, or their
>    future equivalents — never assume a specific report shape exists;
>    read what's there and treat its absence as "no aggregate signal
>    available," not an error).
> 2. Read the actual node-level content of both candidates for the SAME
>    real-world case side by side — the aggregate numbers tell you WHERE to
>    look closer, they do not replace reading the content. Concretely in
>    this pass: the numbers alone (prompt_b's higher branch-graph-completeness,
>    0.9434 vs 0.881) said prompt_b's graphs were structurally more complete,
>    but only reading the actual `procedure_reference` node text for
>    case_223554 (§12.3 item 4) revealed WHY — prompt_a's single generic
>    node forces three distinct recovery concerns (tote-state correction,
>    physical AGV handling, service/lane recovery) into one node with no
>    way to distinguish which applies, while prompt_b's two-flow split gives
>    each concern its own node with unambiguous capability resolution. The
>    number flagged that something was different; reading the content is
>    what explained what and why.
> 3. State the finding as a comparison, not a verdict that silently
>    replaces one candidate with another — matching §4's Reconciliation
>    model (`CONFLICT` is additive, both stand until a human decides) and
>    §10.2's `resolve_audit_candidate` design (propose, never silently
>    overwrite). Neither `prompt_a` nor `prompt_b`'s records should be
>    deleted or marked inferior in the schema; the comparison is itself the
>    deliverable, handed to whoever does SME review.
> 4. Where the case-by-case content reveals one variant is more useful for
>    a SPECIFIC case, say so specifically — a global "prompt_b is better"
>    conclusion would be exactly the kind of over-generalization §3
>    already warns against (a keyword rule standing in for reading the
>    actual record). This pass found prompt_b's split was concretely more
>    useful for `case_223554` specifically; it did not conclude prompt_b
>    is unconditionally better for the other 3 cases, where each case
>    produced only one flow either way and the comparison has less to show.

**Applying it once, to the 4 cases at hand (2026-09-08 backfill instance)**:

Read `stage_8_comparison_report.json`'s aggregate numbers alongside each
case's actual node content (already read in full during §12.3's promotion
work, re-consulted here for this comparison specifically):

- **Aggregate signal**: `prompt_b` has substantially lower
  high-confidence-link-rate (0.024 vs `prompt_a`'s 0.111 — worse) but
  higher branch-graph-completeness (0.9434 vs 0.881 — better) and fewer
  duplicate-runbook references (7 vs 9). `prompt_a` flags 1 playbook
  needing graph repair (`hospital_induct_flow`); `prompt_b` flags 2
  (`site_sort_unavailable`, `sitewide_robotic_stoppage`) — worse on this
  axis, though "needs_graph_repair" is a boolean the promoted records
  didn't reject on (§12.4's `validate_batch()` passed for both regardless,
  since graph-repair is the SOURCE pipeline's own QA concept, not a Brain
  schema requirement).
- **Content-level finding, case_223554 specifically (§12.3 item 4,
  restated as the comparison conclusion it actually is)**: `prompt_b`'s
  two-flow split (`hospital_tote_induction` / `site_sort_unavailable`) is
  concretely more useful than `prompt_a`'s single `hospital_induct_flow`
  playbook for this case — the split gives each of the case's two
  genuinely distinct real-world concerns (hospital tote induction failure
  vs. broader site-sort unavailability) its own unambiguous diagnostic
  path and procedure-reference resolution, where `prompt_a`'s single node
  named all three underlying recovery concerns at once with no way to
  distinguish them.
- **Content-level finding, the other 3 cases**: `prompt_a` and `prompt_b`
  produced structurally near-identical single-flow graphs for `case_218550`
  and `case_228723` (same node count, same overall shape, `prompt_b` adding
  1 extra diagnostic step in each — a finer-grained but not more USEFUL
  distinction on inspection). `case_228086`'s `prompt_b` version adds one
  genuinely useful extra diagnostic node (a dedicated Ignition-gateway-health
  check, node_3, separating "is the gateway itself unhealthy" from "should
  I restart the OptiSweep/gateway service" — `prompt_a`'s equivalent flow
  folds this distinction into its single recovery node) — a real,
  citable improvement, smaller than case_223554's but genuine.
- **Overall recommendation for SME review, not a resolved decision**: no
  single variant should be treated as the winner across all 4 cases.
  `prompt_b`'s per-case splitting/extra-node behavior is more useful
  specifically where a case genuinely contains separable concerns
  (`case_223554` clearly, `case_228086` to a lesser degree); for
  `case_218550`/`case_228723`, where the underlying incident is
  genuinely one flow, `prompt_a`'s simpler graph with no loss of real
  content is no worse and has better link-confidence. This is exactly
  the kind of case-by-case, non-uniform finding a human reviewer needs to
  actually decide the eventual canonical playbook per case — which is why
  it is written here as a finding for review, not applied as an automatic
  "always prefer prompt_b" rule anywhere in the corpus.

**Not done, deliberately**: no Playbook record was deleted, marked
inferior, or given a new field encoding this comparison — per the method's
point 3, this finding is additive documentation for the still-pending
cross-incident canonical-playbook step the design doc already names as
out of scope for Stage 8 (§12.1), not something this pass should have
silently pre-decided by picking a winner in the data itself.

---

## 13. Full design-doc re-read and three findings (2026-09-08)

Directed by the user: re-read `brain/DESIGN_RATIONALE.md` and `docs/design_decisions/`
in full and evaluate where Brain actually stands relative to the locked
design, not just relative to this session's own prior work. Three findings
came out of that re-read; all three were then investigated (not assumed)
before deciding what, if anything, to fix.

### 13.1. Finding 1 (real, fixed): role entities carried zero identity-level facts

`docs/ontology/support_roles_components_and_adjacency.md` and
`docs/design_decisions/handoff_support_roles_access_matrix.md` lock a
specific org model: `operator` is customer/client site personnel, never
FORTNA; L1/L2/L3/L4 are all FORTNA support and all remote; RMS soft stop
(pause) is an L2/L3-only software action, never a physical E-stop
substitute; AVEVA HMI is site/operator-only, no direct FORTNA login.

Checked directly before concluding this was missing: `entity:role:operator`/
`l1_support`/`l2_support`/`l3_support` already carry 101 `role_path_guidance`
Claims total (from §7's 2026-09-03 enrichment run) — deep, per-capability
"how this role acts for capability X" text. That is real and rich. But
**zero identity-level Claims existed on any of the 4 role entities**, and
all 4 entities' own `description`/`aliases` fields were empty — the locked
org facts were reconstructable only by reading all 28 capabilities'
`role_paths` text and noticing the pattern, never asserted once as a
standalone fact. A related gap found in the same check: `entity:role:l4_support`
did not exist at all, despite "L4" being a real, referenced escalation
target in at least 6 capabilities' own free-text `escalate` observables
(`optisweep_service_restart`, `ignition_restart`,
`confirm_agv_active_error_state`, `confirm_zone_pairing_state`,
`confirm_zone_configuration_state`, `confirm_ignition_gateway_health`) —
those references had nothing to resolve to.

**Fixed**: created 8 new `EvidenceUnit(sme_note)` records citing
`support_roles_components_and_adjacency.md` (matching the existing
`evidence:support_roles_components_and_adjacency_md:*` citation convention
already used for 32 capability↔failure-pattern edges from the same
source) — one per distinct locked fact (operator-is-customer, FORTNA-tiers-
are-remote, on-site-work-is-operator, L1/L2-L3/L4 operational posture,
soft-stop-vs-E-stop, AVEVA-site-only). Filled `description`/`aliases` on
all 4 existing role entities (grow-richer-never-regress: only set
`description` since it was empty, unioned `aliases`). Created
`entity:role:l4_support` as a new `Entity(role)`. Added 15 new identity-
level Claims (`has_architecture_note`/`not_applicable_to`, reusing the
exact predicates Pass 0 already established rather than inventing new
ones) asserting the org-model facts directly on the role entities they're
about, each citing the specific evidence unit that grounds it. Corpus:
2,190 → 2,191 entities, 181 → 196 claims, 992 → 1,000 evidence units (ontology
catalogs file). Full-corpus `validate_batch()` — 0 errors; `pytest` — 41 passed.

### 13.2. Finding 2 (real, NOT a Brain gap — a pipeline-level discrepancy): `expects_capability`/`expects_surface` claimed done, actually empty everywhere

`docs/design_decisions/stage_5_8_c2_b2_b1_changelog.md` claims a "C-regen"
backfill made `expects_capability`/`expects_surface`/`preferred_audience`
fields complete on playbook nodes ("46/46 expects nodes complete," dated
2026-08-03, citing `scripts/backfill_playbook_expects.py`). Investigated
via a research pass rather than trusting either the doc or a quick
spot-check: **every single occurrence of `expects_capability` across every
playbook-candidate file, both extraction variants, all 4 cases, and every
downstream stage (Stage 5 candidates through Stage 11 publish bundles) is
an empty list — 0/108 populated, corpus-wide.**

Root cause, confirmed: `scripts/backfill_playbook_expects.py` is real
(161 lines, a working standalone CLI that would populate these fields via
`_infer_capabilities`/`_infer_surfaces`/`_infer_audience`), but **neither
the script nor the changelog documenting it were ever committed to git**
(`git log --all` returns nothing for either path), and no log file
anywhere on disk contains the script's own characteristic
`touched=`/`nodes_changed=` output — the one log the changelog's C-regen
entry could plausibly reference (`data/output/regen_stage8_b5.log`) is a
Stage 8 finalize log, unrelated to this script's stdout. The script, the
changelog, and their two related test files all share an identical mtime
(2026-08-31 13:41:45 — a bulk-copy/checkout timestamp, not an execution
one), while the actual `playbook_candidates.json` data files have
distinct, earlier mtimes (Aug 5–8), i.e. untouched since before the script
existed. The one existing test for this script
(`test_backfill_playbook_expects_audience.py`) only unit-tests its inner
`_infer_audience()`/`backfill_node()` helpers against synthetic in-memory
dicts — it never calls `process_playbook_file()` or `main()`, so it proves
nothing about whether the script was ever run against real files.

**Assessment: documented-but-never-executed, not a completed regen I
simply looked in the wrong place for.** The changelog's "Done"/"46/46"
status is either aspirational (written before running) or describes a run
whose output was never persisted — either way, it does not describe the
current state of the repo's data.

**Why this is flagged here but NOT fixed as a Brain-data change**: this is
a **source-pipeline** gap (`incidenceknowledgeingestion`'s own Stage 5
output), not a Brain promotion gap. §12's Playbook promotion did not lose
or fail to propagate this data — it was never there to propagate; the
promotion correctly used `ontology_capabilities[]` (which WAS populated)
as its `capability_id` resolution source instead (§12.3), and every
Playbook/PlaybookNode this session wrote validates and resolves correctly
without `expects_*`. Running `backfill_playbook_expects.py` now, then
re-deriving `capability_id`/`allowed_role_entity_ids` from its output
instead of `ontology_capabilities[]`, is a legitimate future improvement
to Playbook node quality — but it is source-pipeline work (running/fixing
a script outside `brain/`, then re-running the §12 promotion), explicitly
out of scope for a Brain-data-only fix, and not undertaken here without
the user separately deciding to run/validate that script first.

### 13.3. Finding 3 (investigated, turned out already correct): the AVEVA-is-site-only rule

Originally flagged as "implicit, not asserted" based on reading only
`Capability.role_paths` text (`zone_configuration_state`'s guidance steers
L1/L2 away from direct AVEVA access without stating the rule outright).
Checking `Claim`s on `entity:system:aveva_hmi` directly (not just
Capability role_paths) before treating this as a gap showed **the rule was
already correctly and explicitly asserted**: `not_applicable_to` Claims
already state "FORTNA direct Aveva login (No access)" and
`has_architecture_note` already states "Operator-only access per role
matrix," both already citing real evidence. This was a mistaken finding
from the original design-doc re-read — corrected here rather than
"fixed" a second time, since there was nothing to fix; §13.1's new
`not_applicable_to` Claims on the role entities themselves (§13.1) are
additive, giving the SAME fact a second, role-side assertion (system
"aveva_hmi has no FORTNA access" AND role "l1/l2/l3_support has no AVEVA
access" both now exist, which is more complete, not a duplicate of a
wrongly-flagged gap) — not a correction of something that was actually
broken.

**Lesson for future gap-finding passes**: checking only one record type's
one field (`Capability.role_paths`) for a fact's presence is not
sufficient to conclude the fact is missing from Brain — the same fact can
already be asserted as a `Claim` on a different entity entirely (the
system/surface side, not the role side, in this case). The §13.1
methodology (check Claims on the actual subject entity before concluding
absence) is the correct pattern; the original design-doc-re-read
assessment that flagged this as gap #3 skipped that check.

---

## 14. Closing three §14-deferred items: status lifecycle, Cosmos containers, ContextPacket (2026-09-08)

Directed by the user after the §13 re-read surfaced that the original
design doc's Phase 0 ("architecture freeze") was never actually completed
for the Brain specifically — `brain/DESIGN_RATIONALE.md`
§14 explicitly named "single status versus expanded governance model,"
"Cosmos container/partition-key implementation details," and "retrieval
chunks, embeddings, ranking, and ContextPacket schema" as deferred, not
undecided-forever. This section closes all three as one coherent package,
schema/documentation only — no Cosmos, retrieval, or runtime agent code,
per the same §14 and per architecture lock §11.4's "do not create the
agent... or a Foundry dependency now."

### 14.1. `ValidationStatus`: one field on `BrainRecord`, not a side table

Resolved the fork explicitly left open at §6: does `validation_status`
live on `BrainRecord` directly, or in a separate `reviews` container
referencing what it reviews? **Answer: both, for different halves of the
same problem.** `ValidationStatus` (a new enum, `brain/schemas/common.py`)
lives on every record's shared envelope, because the design doc's
five-way Reconciliation model (reinforce/patch/conflict/gap/new-candidate)
and `BRAIN_BUILD_PROCESS.md` §2.1's catalog-vs-operational authority
asymmetry both apply to every record type — Entity/Claim/Relationship/
Capability, not just Procedure/Playbook (which already had their own
bespoke, unvalidated `validation_status: str` field, now removed in favor
of the shared one — one mechanism, not two). The separate `reviews`
container (§14.2) holds the WORK ITEM of getting a record from one status
to another — the field says where a record currently stands; the review
record says what's being proposed to change that.

```python
class ValidationStatus(str, Enum):
    CATALOG_AUTHORITATIVE = "catalog_authoritative"
    OPERATIONAL_UNREVIEWED = "operational_unreviewed"
    NEEDS_SME_REVIEW = "needs_sme_review"
    SME_APPROVED = "sme_approved"
    CONFLICTING = "conflicting"
    DEPRECATED = "deprecated"
```

Six values, not two, because a single boolean (reviewed/unreviewed) loses
the real distinction `BRAIN_BUILD_PROCESS.md` §2.1 already found matters:
hand-curated catalog content and unreviewed LLM extraction are BOTH
"not SME-approved" in a binary model, but treating them identically would
erase exactly the asymmetry §2.1 flagged as real ("nothing distinguishes
'this is governed policy' from 'this is one source's observation'").
`CATALOG_AUTHORITATIVE` and `OPERATIONAL_UNREVIEWED` describe how a record
ENTERED the corpus (assigned once, at backfill/ingest time);
`NEEDS_SME_REVIEW`/`SME_APPROVED`/`CONFLICTING`/`DEPRECATED` describe where
a record sits in the review lifecycle (assigned/transitioned by
Reconciliation/Curation as the design doc's §12 learning loop runs). A
record moves from an entry status toward a lifecycle status as review
happens — the two families are sequential stages of one field, not an
accidentally-flat enum.

Default: `OPERATIONAL_UNREVIEWED` — the honest default for a newly-created
record with no other information, not an optimistic one.

**Backfilled across the entire existing corpus** (a disposable scratch
harness per §1, not a new committed script), using the exact split
`BRAIN_BUILD_PROCESS.md` §2.1 already established as real: all 31
`Capability` records → `CATALOG_AUTHORITATIVE` unconditionally (every
capability is hand-curated regardless of which sources later added
evidence to it — added evidence doesn't change who curated the record's
own fields, matching §2.1's "a later source strengthening an earlier one
is the normal case"); `Entity` records whose `source_refs` are entirely
catalog-sourced (evidence id prefixes `catalog_capabilities`/
`catalog_wcs_sql`/`support_roles_components_and_adjacency_md`) or have no
`source_refs` at all (a bare Pass-0 stub) → `CATALOG_AUTHORITATIVE` (17
entities — close to §2.1's historical count of 13, the difference being
corpus growth since that count was taken, including this session's own
`entity:role:l4_support`); every other `Entity`, plus every `Claim`/
`Relationship`/`EvidenceUnit` in the corpus → `OPERATIONAL_UNREVIEWED`
(2,174 entities, 196 claims, 545 relationships, 1,000 evidence units in
`ontology_catalogs/` alone — an honest default, not a promotion, since
none of this has actually been SME-reviewed); existing `Procedure`/
`Playbook` records' old bespoke `validation_status="needs_sme_review"`
value mapped straight across to `NEEDS_SME_REVIEW` (301 procedures, 9
playbooks) rather than the generic default, preserving the one real,
meaningful status distinction those two record types already had.
Confirmed idempotent (re-running the backfill twice produces identical
values, no duplicates or drift). Full-corpus `validate_batch()` — 0
errors; `pytest brain/tests/` — 58 passed (41 existing + 17 new, §14.2/§14.4).

### 14.2. `BrainReview`: `AuditCandidate` (§10.2.1) generalized and superseded before being built

`brain/schemas/review.py` — new record type, `RecordType.REVIEW`. Directly
answers §6's "or a separate `reviews` container" half of the fork, matching
the original design doc's §7 Cosmos table exactly (`reviews` container,
partition key `/status`, "SME review queues, diffs, decisions, and
rationale"). Generalizes §10.2.1's narrower `AuditCandidate` sketch (never
implemented — no migration cost to retiring it) to cover ALL FIVE of the
design doc §12 learning-loop branches, not just audit findings:

```python
class ReviewKind(str, Enum):
    REINFORCE = "reinforce"
    PATCH = "patch"
    CONFLICT = "conflict"
    GAP = "gap"
    NEW_CANDIDATE = "new_candidate"
    AUDIT_FINDING = "audit_finding"   # subsumes AuditCandidate's one use case

class ReviewResolution(str, Enum):
    MERGE = "merge"
    RETYPE = "retype"
    RECLASSIFY = "reclassify"
    NOT_A_DUPLICATE = "not_a_duplicate"
    NEEDS_HUMAN = "needs_human"
    APPROVED = "approved"
    REJECTED = "rejected"

class BrainReview(BrainRecord):
    kind: ReviewKind
    affected_record_ids: list[str]   # 1+ existing Brain record ids, any type
    check_name: str | None = None     # only meaningful when kind=AUDIT_FINDING
    proposed_change: str = ""
    status: Literal["open", "resolved"] = "open"
    resolution: ReviewResolution | None = None
    resolved_by: Literal["agent", "human"] | None = None
```

Field-level validators enforce the shape rules that make this record
honest rather than just typed: `affected_record_ids` must be non-empty and
every id well-formed (checked generically, no `expected_prefix`, since a
review can name any record type — an Entity, a Claim, a Capability, even
another Review); `resolution` and `status="resolved"` are required
together (a resolution with no resolved status, or a resolved status with
no stated resolution, are both meaningless half-states); `check_name` is
rejected unless `kind=AUDIT_FINDING` (prevents a stray field implying an
audit check ran when the review is actually a Reconciliation branch).

`brain/validators.py` gained `validate_review_references()` — checks
`affected_record_ids` resolves against the batch's known ids, wired into
`validate_batch()` alongside every other payload-embedded-id-reference
check (the same class of check that recurred as a missed gap three times
before becoming standing practice, per §4's lesson — added here from the
start rather than discovered later).

**Left genuinely open, not resolved here** (same discipline as
`AuditCandidate`'s own "explicitly NOT decided here" list): whether
`resolve_audit_candidate`/a Reconciliation tool call writes the eventual
approved change directly, or only ever proposes it for a human/Curation
step to apply — `BrainReview.resolution` records WHAT was decided, not
WHO is allowed to execute it against the corpus. That remains a build-time
decision for whoever implements the actual Reconciliation/Curation agent.

### 14.3. Cosmos containers: three new rows on the existing Part 1 §10.2 table, not a new table

Extended, not rewritten — `OPTISWEEP_BRAIN_PART1_ARCHITECTURE_LOCK.md`
§10.2's original 7-container table (from before `Procedure`/`Playbook`
existed) keeps every existing row unchanged. New rows:

| Container | Partition key | Records | Why |
|---|---|---|---|
| `brain_procedures` | `/capability_id` | `Procedure` records | Matches the existing table's own pattern (`brain_claims` by `/subject_entity_id`, `brain_relationships` by `/from_id`) — partition by the field a Procedure is always looked up through: "what are the approved steps for capability X." |
| `brain_playbooks` | `/entry_symptom_entity_ids[0]` | `Playbook` records | Playbooks are symptom-driven routing targets, not capability-driven ones (`docs/design_decisions/stage_5_6_playbook_extraction_modes.md`'s own runtime flow: "symptom input → routing/classification → selected playbook") — the actual hot-path lookup a runtime agent makes is by observed symptom, not by capability or case id. |
| `brain_reviews` | `/status` | `BrainReview` records | Matches the original design doc §7's `reviews` container exactly — the dominant access pattern for a review queue is "give me everything still open," not a lookup by any single record it references. |

The current `OPTISWEEP_STORAGE_BACKEND=local|azure` split and "local mode
writes the same validated records to local JSON bundles" rule apply to
these three new containers identically — no new storage mechanism, same
contract.

### 14.4. `ContextPacket`: schema only, per §14's explicit deferral of the retrieval engine itself

`brain/schemas/context_packet.py` — a bare pydantic model (not a
`BrainRecord` — it is assembled per-call, never persisted as corpus
knowledge itself), following the original design doc §8's packet-section
table directly:

```python
class ContextPacket(BaseModel):
    task: dict[str, Any]
    current_state: dict[str, Any] = {}
    entities: list[str] = []
    approved_knowledge: list[str] = []
    evidence_excerpts: list[str] = []
    relevant_incidents: list[str] = []
    policies: list[str] = []
    conflicts: list[str] = []
    required_output_schema: dict[str, Any] | None = None
```

Every list field holds Brain record IDs, never inlined record content —
the packet is a bounded, cited pointer set a consuming service resolves
immediately before the LLM call, matching the design doc §8's own "packet
sizes should be budgeted" principle and Part 1's "IDs are stable and
typed, never titles" rule applied to the retrieval layer too.

**The concrete mechanism that finally closes the governed-vs-raw gap**:
`APPROVED_KNOWLEDGE_STATUSES = frozenset({CATALOG_AUTHORITATIVE,
SME_APPROVED})`, a module-level constant stated as a rule, not just
documented in prose — `approved_knowledge` must only ever be populated
from records whose `validation_status` is in this set.
`OPERATIONAL_UNREVIEWED`/`NEEDS_SME_REVIEW`/`CONFLICTING`/`DEPRECATED`
records are Reconciliation/Curation working material; a context packet
handed to an LLM call must never cite them as approved guidance. This is
the actual, checkable form of the gap named repeatedly across §4/§6/§13
("nothing distinguishes governed knowledge from raw extraction") — now
that `ValidationStatus` (§14.1) exists, this filter is a one-line rule
instead of an unenforceable aspiration.

Retrieval traversal is documented (design doc §9's table, restated with
real Brain type names) but explicitly NOT implemented — no embeddings, no
ranking, no Cosmos query code, per §14's own deferral and architecture
lock §11.4:

| Need | Retrieval target | Traversal (real `RelationshipType`s, `brain/schemas/relationship.py`) |
|---|---|---|
| Procedure selection | `brain_procedures`, filtered to `approved_knowledge`-eligible status | `Entity(symptom)` —`MAY_INDICATE`→ `Capability` —`USES`← `Procedure` |
| Playbook routing | `brain_playbooks`, keyed by `entry_symptom_entity_ids` | Direct partition-key lookup by observed symptom entity id |
| Product explanation | `brain_claims`, `brain_entities` | `Entity` —(any `Claim.subject_entity_id`)→ `Claim` |
| Similar cases | `brain_playbooks`/incident-sourced `Claim`s | `Entity(symptom)` ←`observes`— `Entity(system)`, cross-referenced against incident `constraints.sites` |
| Evidence citation | `brain_evidence` | Direct `source_refs` id lookup — no traversal, exact citation |
| Conflict resolution | `brain_reviews`, `kind=CONFLICT`, `status=open` | Direct partition-key (`/status`) scan |

### 14.5. What remains deferred, restated precisely

- Cosmos itself — provisioning, physical containers, actual queries. Only
  the local-JSON-mirrored schema/contract exists.
- Retrieval implementation — embeddings, hybrid search, ranking, packet
  budgeting logic. `ContextPacket` is the target shape a future
  context-builder service must produce; nothing produces it yet.
- The Reconciliation/Curation agent itself, and therefore who is actually
  authorized to write a `BrainReview.resolution` and act on it (§14.2's
  open item) — still explicitly deferred per architecture lock §11.4.
- `merge_record()` still has no real conflict detection (§4's
  still-standing gap) — `ValidationStatus.CONFLICTING` gives conflicts a
  place to live once detected, but detecting them is unchanged from
  before this section.

## 15. Closing two more §14 deferrals: real Cosmos storage, real retrieval (2026-09-08)

Directed by the user after the provider/tool-set build (see
`AGENT_AZURE_HANDOFF.md and brain/DESIGN_RATIONALE.md`'s milestone log for the full
provider/tool history): of the gaps named at the end of that build,
prioritize Azure Cosmos storage and real (embeddings-based) retrieval now;
leave audit-merge auto-execution, an SME review UI, LLM-judgment
validation against real model output, `merge_record()` conflict
detection, and everything `appcode`-side for later — those remain
documented gaps, not silently dropped.

### 15.1. `AzureStorageProvider`: Brain's own Cosmos containers, live-tested

`providers/azure_storage.py` implements `StorageProvider` against Brain's
own container set (`providers/azure_cosmos_config.py`), completely
separate from `shared_pipeline_stages/stage_11/cosmos_publisher.py`'s
pre-Brain publish containers (`runbooks`, `playbooks_prompt_a`, etc.) —
same Cosmos account (`optisweepsupportdev` /
`optisweep_knowledge_phase0`), different container set, never conflated.

**Real containers were provisioned on the live account**, not just
designed: `providers/scripts/provision_brain_cosmos_containers.py`
created all 9 (`brain_evidence`, `brain_entities`, `brain_claims`,
`brain_relationships`, `brain_capabilities`, `brain_procedures`,
`brain_playbooks`, `brain_reviews`, `brain_ingestion_runs`), confirmed via
a real container-listing call before and after (10 pre-existing
containers → 19), with no throughput header (this account is
serverless/shared-throughput, confirmed empirically: creating a probe
container with no `x-ms-offer-throughput` succeeded, matching every
existing container's own creation — none of which were created by any
script in this repo either, since no Cosmos container-creation code
existed anywhere before this session).

**One real design correction made while building this**: Part 1 §10.2's
container plan states `brain_playbooks`' partition key as
`entry_symptom_entity_ids[0]` — but Cosmos partition keys must be a real
top-level scalar JSON property, and that field is a list. Rather than
special-case one container's declared partition key path, EVERY Brain
container (including `brain_playbooks`) now declares
`COSMOS_PARTITION_KEY_PATH = "/_partition_key"`, a synthetic field
`AzureStorageProvider` computes and writes at save time via
`partition_key_value()` — one partition key SHAPE for every container,
still partitioning by the semantically-meaningful field
`PARTITION_KEY_FIELD_BY_RECORD_TYPE` names. `partition_key_value()` also
had to explicitly unwrap str-Enum fields via `.value` (`Entity.entity_type`,
`Capability.capability_kind`, `BrainReview.status`) — `str(some_enum)`
returns `"EntityType.SYSTEM"`, not `"system"`, which would have silently
partitioned every entity into one wrong bucket per type if shipped
unchecked; caught by testing `partition_key_value()` against all 19,768
real corpus records before writing anything to Cosmos, not just a
handful of synthetic fixtures.

**Live-verified, not just unit-tested with mocks**: a real
`Entity`/`EvidenceUnit` pair was written via `AzureStorageProvider.
save_brain_records()`, read back via `load_brain_context()`, confirmed
byte-identical on the fields that matter, and cleaned up; the same for
`save_ingestion_run()`/`load_ingestion_run()`. Every document read back
from Cosmos needed its system fields (`_rid`/`_self`/`_etag`/`_ts`) and
this repo's own synthetic `_partition_key` field stripped before pydantic
validation — every `BrainRecord` uses `ConfigDict(extra="forbid")`, so an
unstripped read fails validation on every single row; `_strip_cosmos_fields()`
closes this, found by the first live round-trip attempt failing exactly
this way.

`azure_storage.py` remains untested against real credentials in CI (no
CI exists yet for this repo) — the live verification above was a manual,
one-time confirmation pass in this session, cleaned up immediately after.
Ongoing correctness rests on `providers/tests/test_azure_storage.py`'s
mocked-HTTP unit tests (7 tests) plus `test_azure_cosmos_config.py`'s
partition-key tests (8 tests, one per record type against real schema
constructors).

### 15.2. Real semantic retrieval: embeddings backfilled, `get_brain_context` gained a `query_text` path

**The gap this closes**: `get_brain_context` (§14.4) could only ever
answer "what's connected to this entity I already know the id of" — it
had no path from a free-text question to a starting entity id at all.
That's the literal retrieval-engine gap §14.4 named as deferred
("embeddings, ranking... explicitly NOT implemented").

**`brain_service/embedding_text.py`**: one function, `embedding_text_for()`,
choosing which fields represent each of the 7 embeddable record types for
search purposes (Entity: name+aliases+description; Claim:
subject+predicate+object+note; EvidenceUnit: raw content.text; Capability:
name+description; Procedure: title+summary+when_to_use; Playbook:
title+goal; Relationship: from+type+to+note) — deliberately NOT a blind
`model_dump()` dump, so the embedded text matches how a person would
actually describe searching for that record. `BrainReview` is excluded
from the backfill (§4's approved-knowledge distinction: reviews are
pending working material, not corpus content a "what does Brain know"
search should surface).

**`brain_service/retrieval.py::find_similar_records()`**: embeds the query
once, brute-force cosine-ranks every stored vector (optionally filtered
to one record type), returns the top-k above a minimum score. Brute force
is a deliberate, stated choice, not an oversight — correct and fast
enough at the current ~20K-record scale (confirmed, not assumed: real
queries against the real, backfilled corpus return in well under a
second); an ANN index is explicitly future work for whenever corpus scale
actually makes brute force the bottleneck, not before.

**The corpus was actually backfilled**, not left for later:
`brain_service/scripts/backfill_embeddings.py` ran against the real local
corpus (19,768 embeddable records: 3,614 evidence units, 2,191 entities,
2,023 claims, 11,599 relationships, 31 capabilities, 301 procedures, 9
playbooks — matching §14.1's counts exactly), storing vectors via the new
`StorageProvider.save_embeddings()`/`load_all_embeddings()` methods (added
to the interface and implemented in both `LocalStorageProvider` —
one JSON file per record type under a new `embeddings/` directory,
excluded from `load_brain_context()`'s scope-scanning the same way
`ingestion_runs/` already was — and `AzureStorageProvider`, a new shared
`brain_embeddings` Cosmos container partitioned by record_type). Real
semantic search was confirmed working against the real backfilled data
mid-build: querying "AGV heartbeat error causing sync issues" against the
real entity embeddings correctly surfaced `agv_errors` (0.677),
`agv_troubleshooting` (0.643), `agv_error_status` (0.638) as the top three
matches, in sensible descending-score order — not a synthetic fixture
result.

**`get_brain_context` gained `query_text`/`embeddings`/`semantic_top_k`/
`semantic_min_score` parameters**, composable with the original
`entity_ids` path (both can be passed together — explicit ids and
semantic matches merge into one traversal frontier). A semantic Entity
match feeds the existing relationship-hop traversal exactly like an
explicit `entity_ids` seed would; a semantic Claim/EvidenceUnit match is
cited directly into the packet without needing graph traversal, since a
matched claim or evidence excerpt already IS the relevant thing, not
something reached via a relationship. Wired through
`mcp_server/tools.py::tool_get_brain_context` and the `get_brain_context`
MCP tool itself, both gaining the same `query_text` parameter — the
embedding provider is only constructed when `query_text` is actually
given, confirmed by a test that fails loudly if
`get_embedding_provider()` is called when it shouldn't be.

### 15.3. Two real corpus id collisions, found by the embedding backfill itself, fixed

The embedding backfill (§15.2) is an id-keyed upsert
(`StorageProvider.save_embeddings()` dedupes by `record_id`) run against
the WHOLE corpus at once for the first time — no prior pass ever loaded
every claim and every relationship across every scope simultaneously and
checked for id collisions the way this one incidentally did. It found two,
both real and both pre-existing (neither caused by anything in this
session's own code):

**Finding 1 — claim-id collision, a genuine naming bug.**
`claim_id(subject_token, predicate_token)` (`brain/id_generation.py`) has
no source-disambiguating component. `training_video_day1` and
`training_video_day2` each independently produced an `operational_context`
record sharing the identical `context_id` for a topic both days'
training covers (AGV status fields, system state reference, zone
configuration) — `migrate_operational_source.py`'s
`claim_id(rec["context_id"], "details")` then faithfully derived the
identical claim id for two genuinely different claims: different
`subject_entity_id` (`entity:metric:agv_status_popup_information_fields`
vs. `entity:metric:agv_status_fields_and_vitals`), different asserted
content, different evidence. Confirmed via `grep` that neither id was
referenced anywhere else in the corpus before touching anything. Fixed by
`brain/migration/fix_training_video_claim_id_collisions.py` (the
established one-off-correction-script pattern, per §1 — this is 3 known
records, not a source-shape-specific parser): day2's copy of each of the
3 colliding ids was renamed with a `_day2_` disambiguator
(`claim:ctx_training_video_day2_agv_status_fields_v1:details`, etc.); day1
keeps its original, unqualified id. Confirmed fixed two ways: (a)
`Counter` over every claim id in the corpus now shows zero duplicates
(previously 3, silently shadowing day2's claims in any id-keyed load);
(b) a semantic search for "AGV status popup fields and vitals" now
returns BOTH the day1 and day2 claims as two independent top results,
where before the fix only one could ever be visible at a time depending
on load order. `claim_id()` itself was NOT changed — the structural gap
(no source component) still exists for any future collision of this
exact shape; this fix closes the 3 known instances, not the root cause,
consistent with how every other id-shape defect in this corpus's history
(§3, §6 of `BRAIN_BUILD_PROCESS.md`) was closed: hand-judge the known
instances, apply mechanically, leave the generator function as a
documented open risk rather than redesigning it speculatively.

**Finding 2 — relationship-id "collision," actually a missing merge
step, not a naming bug.** Two pairs of incidents
(`case_218550`/`case_228723`, and `case_223554`/`case_228723`) each
correctly produced the SAME relationship id for what is genuinely the
same real-world edge (e.g. `entity:system:rms_ui` —OBSERVES→
`entity:system:optisweep_agv_fleet`) — `relationship_id(from_token,
relationship_type, to_token)` has no source component either, but here
that's the CORRECT behavior per Part 1 §9 ("resolve referenced names to
existing entities/relationships where possible"): two incidents observing
the same structural fact should collapse onto one record, each
contributing its own evidence, exactly like the design doc's Reinforce
branch (§4.1) describes. The bug was that no merge step had ever actually
run across incident scopes — each incident's own `relationships.json` was
written independently and never reconciled against the others. Fixed by
`brain/migration/merge_cross_incident_relationship_duplicates.py` using
`merge_record()` for `source_refs` (safe: list-union is exactly what
`merge_scalar_field`/`merge_list_field` already does) — but NOT for
`note`, which needed a deliberate deviation: `merge_record()`'s scalar-fill
semantics only fill an EMPTY field from incoming, so a bare
`merge_record()` call would have silently dropped one incident's note
whenever the other incident's note was already non-empty (both were
real, independently meaningful text, not one-empty-one-populated — the
case `merge_scalar_field` is designed for). Caught by reading the dry-run
output before writing anything, not by any test: fixed by concatenating
both notes with `" | "` when they differ, rather than trusting
`merge_record()`'s default scalar behavior for this one field. The
earlier-created record in each pair was kept as the canonical id; the
later, now-redundant on-disk copy was removed from its own incident's
`relationships.json`. This is confirmed a narrow, 2-pair fix, NOT a
corpus-wide audit — no systematic scan for this same pattern (same edge,
independently asserted by two-or-more incidents, never merged) has been
run beyond the 2 pairs the embedding backfill happened to surface; a real
`find_audit_candidates`-style check for this specific pattern (group
relationships by id across ALL scopes, not just entities by name — see
§10.2's 6 existing checks, none of which currently do this) remains a
documented gap, not fixed here.

Both fixes are covered by `brain/tests/test_corpus_id_collision_fixes.py`
— asserting against the REAL on-disk local corpus (not synthetic
fixtures), confirming zero duplicate claim/relationship ids remain and
that both merged relationships retain both incidents' `source_refs`.
Full-corpus `validate_batch()` re-run after both fixes: 0 errors. The
embedding backfill was re-run (targeted, 3 records) to embed day2's newly
renamed claims — final embedding count: 19,766 (2,023 claims + 11,597
relationships + 3,614 evidence units + 2,191 entities + 31 capabilities +
301 procedures + 9 playbooks — every embeddable record in the corpus
exactly once, no collisions).

### 15.4. What remains deferred, restated precisely (updates §14.5)

- Cosmos containers now provisioned and live-tested for Brain records AND
  embeddings; still no CI coverage against real credentials, and no
  automated re-provisioning path beyond the idempotent provisioning
  script itself.
- Retrieval is now real (embeddings + brute-force cosine ranking) for the
  local backend; the same `find_similar_records()` call works against
  `AzureStorageProvider` unchanged (same `StorageProvider` interface), but
  the Cosmos-backed corpus has not itself been backfilled with embeddings
  in this session — only the local corpus was.
- No packet-budgeting/ranking-within-the-packet logic — `get_brain_context`
  still returns every match above `semantic_min_score` up to
  `semantic_top_k`, with no further truncation by total packet size.
- Everything named in §14.5 and the handoff doc's "Known gaps" list
  beyond items 1–2 remains exactly as deferred: audit-merge
  auto-execution, an SME review UI, LLM-judgment tools validated against
  real model output (not just scripted fakes), `merge_record()` conflict
  detection, and all `appcode`-side work.

## 16. Closing the biggest remaining gap: reconciliation now actually writes (2026-09-09)

Directed by the user ahead of ingesting real new incidents: every prior
milestone (§9–§15) built the full extract→classify→reconcile→validate
chain, but `validate_and_prepare_for_review` (§4.2 Tool 4) only ever
DRAFTED a `BrainReview` describing a proposed change — grep confirmed
`merge_record()`/`save_brain_records()` were never actually called
anywhere in the live ingestion path. `ingest_incident_pdf` would run a
real incident through the full LLM judgment chain and produce a stack of
review descriptions, with the corpus itself completely unchanged. This
section closes that gap.

### 16.1. The write model, decided explicitly (not the design doc's original framing)

The original design doc's framing ("nothing before Curation should be
treated as production-eligible knowledge," architecture lock and §4)
implied every outcome should stay proposal-only until a human approves
it. Directed otherwise here: **write everything, always — let
`validation_status` be the safety signal, not "written vs. not
written."** Concretely, for every `ReconciliationOutcome` except GAP (no
record exists yet to write for a Gap — it names a hole, not a candidate):

- **REINFORCE** / **PATCH** → `merge_record()` onto the existing target
  record, `validation_status` untouched (merging never regresses an
  already-approved status backward).
- **NEW_CANDIDATE** → a new Entity/Claim/Relationship/Capability is
  constructed and written with `validation_status=OPERATIONAL_UNREVIEWED`
  — visible, findable via `get_brain_context`, but excluded from
  `ContextPacket.approved_knowledge` until an SME flips it to
  `SME_APPROVED` (§14.4's `APPROVED_KNOWLEDGE_STATUSES` filter already
  enforces this; no new filtering logic was needed).
- **CONFLICT** → a NEW Claim is created with
  `validation_status=CONFLICTING`, citing which existing claim it
  disagrees with in its `note`. The original claim is never touched —
  design doc §12's "both stand, flagged as contested" holds exactly as
  specified; only the ALWAYS-WRITE default changed, not the
  never-silently-overwrite rule.
- **GAP** → only the `BrainReview` is saved. Nothing else exists to write.

A `BrainReview` is still saved for every outcome including the four that
now also write a record — it is the audit trail of what changed and why,
not a substitute approval gate.

### 16.2. New module: `brain_service/persistence.py`

`apply_reconciliation(storage, reconciled, *, scope)` is the one new
entry point: runs `validate_and_prepare_for_review` first (unconditionally
— the mechanical checks never get skipped), then performs the write for
every non-GAP, non-validation-failure case. Returns an `ApplyResult`
(`review`, `written_record | None`, `skipped_reason | None`) so a caller
can tell "wrote a record," "GAP, nothing to write," or "write attempted
and failed" apart cleanly.

Four private builders (`_build_entity`/`_build_claim`/
`_build_relationship`/`_build_capability`) construct a real typed record
from `ClassifiedCandidate.proposed_fields` — a genuinely new piece of
logic this codebase didn't have before, since every prior tool treated
`proposed_fields` as an opaque dict to pass along, never something to
actually validate into a schema instance. `Entity` construction uses the
existing `PAYLOAD_MODEL_BY_ENTITY_TYPE` lookup (brain/schemas/entity.py)
to pick the right payload shape per `entity_type` rather than guessing.

**`run_create_chain` (brain_service/create_chain.py) was updated to call
`apply_reconciliation` instead of the bare `validate_and_prepare_for_review`
call it used before** — this is the one-line change that makes
`ingest_incident_pdf`, `run_migration_batch`, and every pipeline stage
hook (`ingest_stage_output`) all get real writes automatically, since all
three already route through this shared chain function. `scope` had to
be threaded through as a new required parameter on `run_create_chain` and
both its callers (`pipeline_hook.py` already had `scope` available from
`ingest_stage_output`'s own signature but never passed it down --
confirmed by grep that this was a real, live gap, not
theoretical; `migration.py` gained an optional `scope_for_item` callable,
mirroring the existing `load_source_packet` caller-supplied-seam pattern,
defaulting to using the batch item id itself as the scope).

### 16.3. A real bug found on the FIRST live test, and what it revealed about the actual gap named in §6/§14.5

Before trusting this against a real incident, one live call was run
against a real, empty test corpus using `AzureOpenAILLMProvider` (not a
scripted fake) — chosen deliberately as the harshest case, since an empty
corpus forces every candidate down the NEW_CANDIDATE path with nothing to
compare against. The real response:

```json
{
  "subject_entity_id": null,
  "subject_entity_name": "OptiSweep service",
  "predicate": "restart status and preceding condition",
  "object": "was restarted after it stopped responding to heartbeat checks",
  "polarity": "AFFIRMED"
}
```

Three real problems, all traced to the same root cause: `classify_candidate`'s
prompt (and `proposed_fields`' intentionally loose typing, per
`brain_service/types.py`'s own docstring) never told the model what to do
when a Claim's subject has no existing Entity, or enforced exact enum
casing:

1. `subject_entity_id: null` with a separate `subject_entity_name` — the
   model correctly recognized it had no id to point to, but nothing told
   it (or the code reading its output) what to do about that. The naive
   fix would be to reject this as malformed; the actual fix is to
   recognize it as a REAL, EXPECTED outcome and say so: a new
   `UnresolvedClaimSubjectError`, caught specifically in
   `apply_reconciliation` and surfaced as `"NEEDS ENTITY FIRST: ..."` —
   naming the proposed entity name, not a generic write failure. This
   does NOT yet automatically create the missing Entity first and retry
   the Claim (that would be a genuinely new orchestration step —
   two-candidates-from-one — deliberately not built here; flagged as a
   real next-step gap in §16.4).
2. `polarity: "AFFIRMED"` (uppercase) vs. the schema's lowercase
   `"affirmed"` — `_normalize_enum()` (a new, small, reusable helper)
   case-insensitively resolves any string against an Enum's values before
   falling back to a caller-supplied default, applied to every enum-typed
   field across all four builders (`EntityType`, `Polarity`,
   `RelationshipType`, `CapabilityKind`). This is a schema-enforcement gap
   named generically in AGENT_DESIGN_NOTES.md's earlier sections (the LLM
   "reliably gets the CONCEPT right... but not always the exact casing");
   now closed at the one place it was actually load-bearing (record
   construction), not attempted at the prompt level, which would need to
   be perfectly followed every single call to be reliable.
3. `object: "was restarted after it stopped responding..."` (a bare
   string) instead of the documented `{"kind": "literal", "value": "..."}`
   shape — `_normalize_claim_object()` accepts both, since
   `proposed_fields` was already deliberately designed as loosely-typed
   (types.py's docstring: "does not have to emit the final validated
   record").

A second live call, against the REAL, populated local corpus (not an
empty test one) with a sentence about a tote stuck at bag-out, correctly
wrote a genuinely new `entity:state:tote_stuck_at_bag_out_station` — the
model correctly judged it distinct from the existing, similarly-named
`entity:symptom:bag_out_stuck` rather than treating a shared topic as a
false match. This is a positive, useful confirmation the duplicate-check
discipline (§4.1/§10.3) holds under real model output too, not just
scripted test fakes. (This scratch write was deleted immediately after
confirming it — not part of the corpus going forward.)

This is the first entry in this document confirming the four LLM
judgment tools' behavior against REAL model output rather than
`ScriptedLLM` fakes (the gap named as open in §6 and the handoff doc's
"Known gaps" item 5) — narrowly, for two hand-picked sentences, not the
systematic replay-known-judgments eval §6 originally proposed, which
remains undone.

### 16.4. What this still doesn't do (real, stated gaps — not silently dropped)

- **No automatic "create the missing Entity, then retry the Claim"
  orchestration.** `UnresolvedClaimSubjectError` surfaces cleanly as a
  review a human can act on, but nothing automatically spawns a second
  NEW_CANDIDATE Entity classification pass and re-attempts the Claim
  against it. On a corpus this thin, this will likely be the single most
  common "needs_human_review" reason for a while — worth watching once
  real incidents run through this.
- **`resolve_audit_candidate` still proposes without executing** (§10.2's
  original, still-standing deferral) — this section only wired up writes
  for the Create-path chain (extract→classify→reconcile→validate), not
  the Audit-Merge path's MERGE/RETYPE/RECLASSIFY resolutions.
- **No systematic eval against the known-correct backfill judgments** —
  §16.3's two live calls are real signal, not a substitute for the
  replay-28-capability-pairings/37-reclassified-entities/12-duplicate-merges
  eval named in §6, which remains undone.
- **The `_apply_merge` "does not resolve to an existing record" branch is
  provably unreachable in the current call path** (validation already
  catches a dangling `affected_record_id` first) — kept as deliberate
  defense-in-depth, documented as such in its own comment, not deleted as
  dead code.

## 17. Tool 8 — `draft_procedure`: Procedures drafted FROM Brain, not the static ontology catalog

**Why this exists.** The pre-Brain Stage 5/6 pipeline
(`incidenceknowledgeingestion/.../stage5_runbook_candidates.py`,
`stage6_runbook_finalization.py`) drafts runbook candidates by calling
`shared_pipeline_stages/ontology_rag.py::ontology_snippets_for_stage5/6()`
— a keyword/regex lookup against the static `docs/ontology/catalogs/*.json`
files, with no LLM judgment and no connection to Brain at all (confirmed
by reading both modules directly: Brain is never imported). That path
still runs and still produces the `Procedure` records currently in the
corpus (via `brain_service/adapters/finalized_runbooks.py` feeding the
existing Create-path chain). `draft_procedure` is a second, independent
path: given a Capability id already in Brain, it drafts a new Procedure
grounded in that Capability's own populated fields
(`observables`/`sql_field_notes`/`support_contract`/`when_to_use`/
`not_for`/`role_paths`/`api_checks`) plus `get_brain_context`-retrieved
Entities/Claims/evidence — closing the gap named in §5.2 and confirmed by
code-reading rather than assumption.

**Follows the existing seven-tool pattern exactly**, per explicit user
instruction ("we want to make sure this follows the existing agents"):
- `brain_service/prompts/draft_procedure.md` — a standalone prompt file,
  not inlined in Python, mirroring `classify_candidate.md`'s judgment-
  boundary style (never invent a SQL field/command/threshold not present
  in the evidence; record what's missing in `gaps` instead of guessing).
- `brain_service/types.py::DraftedProcedure`/`DraftedProcedureStep`/
  `DraftedProcedureAction` — new intermediate types, NOT a reuse of
  `ClassifiedCandidate`'s loose `proposed_fields` dict. Unlike a raw
  candidate being classified into an ambiguous target shape, a Procedure's
  target shape is already fully known (drafted FROM one specific
  Capability) — so the intermediate type is field-for-field typed, making
  a bad LLM response fail as a clear schema error on the drafted shape
  itself, not one layer removed inside Procedure construction.
- `brain_service/procedure_drafting.py::draft_procedure()` — same call
  shape as `classify_candidate`/`reconcile_candidate`: load context via
  `get_brain_context` (seeded from the Capability's own
  `target_entity_ids`/`allowed_surface_entity_ids`/`required_role_ids`),
  then one `llm.generate_json(...)` call against the prompt + schema.
- `build_procedure_record()` — mirrors `persistence.py`'s
  construct-then-check-references-then-return pattern exactly, including
  a new `DanglingProcedureReferenceError` (same shape as
  `persistence.DanglingReferenceError`) that fires when a drafted
  Procedure references a role entity id that is well-formed but does not
  actually exist in the corpus — checked BEFORE construction, live-tested
  and confirmed firing correctly against an invented role id.
- `write_drafted_procedure()` — writes the Procedure plus an auditable
  `BrainReview(kind=NEW_CANDIDATE)` in one `save_brain_records` call,
  matching `apply_reconciliation`'s write-everything-as-
  `OPERATIONAL_UNREVIEWED` model (2026-09-09) — a drafted Procedure is new
  content generation, not a Reconciliation decision on an existing delta,
  so writing is a separate, explicit, caller-invoked step
  (`write=True` at the MCP boundary) rather than automatic, giving the
  caller a chance to inspect `gaps` first.
- Exposed via MCP as `draft_procedure` (`mcp_server/tools.py`/`server.py`),
  the 8th tool, following the existing thin-wrapper pattern exactly (no
  business logic in the MCP layer itself).

**Live-tested against the real corpus and real Azure OpenAI**
(2026-09-09), not just `ScriptedLLM` fakes — against
`capability:confirm_device_roster_state` (chosen for its rich existing
grounding: 15+ source_refs, 4 required roles, populated observables,
already used earlier in this session to verify the scope-mismatch bug
fix). Result: a genuinely well-grounded 7-step Procedure, every step
citing real evidence ids (training-video transcripts, runbook prose,
support-role adjacency notes), correctly respecting the Capability's own
`not_for` boundary (declined to fold in active-error-code triage), and
constructing into a schema-valid `Procedure` record confirmed via a full
pydantic round-trip. Critically, where the retrieved evidence didn't
specify an exact WCS SQL join, the exact GetAGVStatuses API parameters, or
an escalation destination, the model reported these as `gaps` rather than
inventing plausible-sounding specifics — the judgment boundary the prompt
asks for held under a real call, not just in the prompt's own wording.
This scratch draft was never written to the real corpus (`write_drafted_procedure`
was never called against real storage in this test) — a pure dry-run of
`draft_procedure` + `build_procedure_record`.

**What this does NOT yet do:**
- **No Playbook agent yet.** Per explicit build-order decision, `draft_procedure`
  was built and live-tested first since a Playbook's
  `PROCEDURE_REFERENCE` nodes need real Procedure ids to reference — a
  `draft_playbook` tool (drafting symptom-driven branching from incident
  Claims + already-approved Procedures, per §5.2's "runbooks are not
  incident-only" correction) is the direct next step, following this same
  pattern.
- **No automatic reconciliation against an EXISTING Procedure for the same
  Capability.** `draft_procedure` always drafts fresh; it does not check
  whether a Procedure already exists for this `capability_id` and offer
  to merge/patch it the way `reconcile_candidate` does for Entities/
  Claims/Relationships/Capabilities. Per the schema's own docstring,
  multiple Procedures per Capability are expected (different sources/
  incidents) — but nothing yet decides when a new draft should instead be
  a PATCH to an existing one. Left as an open question, matching §6's
  still-open reconciliation-of-multiple-runbooks item.
- **Not yet wired into any pipeline stage hook.** `ingest_stage_output`
  (§9) still only runs the four Create-path tools; nothing calls
  `draft_procedure` automatically from Stage 5/6. Whether/how to connect
  the two (replace the static-catalog call, or run both and compare) is
  intentionally left for after the user's new incident ingestion produces
  real cases to test against — not decided speculatively here.
- **The old Stage 5/6 static-catalog path is untouched** — this is an
  additive second path, not a replacement, per this section's opening
  paragraph.

## 18. Tool 9 — `draft_playbook`: symptom-driven branching FROM Brain's own graph

**Why this exists, and why it comes after `draft_procedure`.** A Playbook
never embeds a Procedure's steps (schema docstring) — its
`procedure_reference` nodes cite `procedure_id` only. That makes it
structurally dependent on real Procedures already existing, so
`draft_playbook` was built second, per the explicit build-order decision
made before starting this work. It replaces the same static-catalog
dependency `draft_procedure` replaced, but for Stage 8's playbook
finalization (`shared_pipeline_stages/stage_8/`) instead of Stage 5/6 —
and closes §5.2's "runbooks are not incident-only" correction directly:
the tool's own retrieval draws on the Capability/Procedure graph
corpus-wide, not one incident's own candidates.

**A retrieval gap found and solved the same way `draft_procedure` solved
it.** `get_brain_context`'s traversal reaches connected Entities via
Relationships, and `ContextPacket` only ever carries entity/evidence ids
(its own docstring: "never inlined record content") — it has no
Capability- or Procedure-shaped field at all. So `draft_playbook` does
what `draft_procedure` already established as the pattern: call
`get_brain_context` for the traversal (seeded on the entry symptom id(s),
`hops=2`, filtered to `MAY_INDICATE`/`VERIFIES`/`CAUSES`/`CONTRIBUTES_TO`
— the four relationship types that connect a symptom to a diagnostic
path, matching §14.4's 2-hop worked example), then separately load the
full Capability records the traversal's relationship endpoints point at,
and the existing Procedures already drafted for each of those
Capabilities (id/title/summary only, never their steps — a Playbook must
never see enough of a Procedure to be tempted to restate its content).

**Same two-phase shape as `draft_procedure`:**
- `brain_service/types.py::DraftedPlaybook`/`DraftedPlaybookNode`/
  `DraftedPlaybookBranch` — field-for-field typed, same rationale as
  `DraftedProcedure` (a Playbook's target shape is already fully known
  once you have the symptom graph; a bad LLM response should fail as a
  drafted-shape schema error, not one layer removed).
- `brain_service/prompts/draft_playbook.md` — same judgment-boundary
  style: never invent a branching rule, error code, or routing decision
  not present in the retrieved evidence; report an unresolved branch
  point in `gaps` instead of guessing a plausible split. Explicitly
  instructs never citing a `procedure_id` not shown in the retrieved
  existing-procedures list.
- `brain_service/playbook_drafting.py::build_playbook_record()` — mirrors
  `build_procedure_record()`'s construct-then-check-references pattern,
  with a new `DanglingPlaybookReferenceError` covering THREE reference
  kinds a Playbook can dangle on (`capability_id`, `procedure_id`,
  `symptom_entity_id`), where `procedure_id` is the highest-value check:
  the entire purpose of a Playbook is routing to a REAL, already-vetted
  Procedure, so an invented `procedure_id` slipping through would be the
  worst-case failure for this tool specifically. `Playbook`'s own
  validators (`brain/schemas/playbook.py`) already catch malformed id
  SHAPE and branch targets that don't resolve WITHIN the playbook; this
  adds the existence-IN-CORPUS check those validators cannot perform
  themselves (they have no storage access).
- `write_drafted_playbook()` — same explicit-opt-in write model as
  `write_drafted_procedure`, writing the Playbook plus an auditable
  `BrainReview(kind=NEW_CANDIDATE)`.
- Exposed via MCP as the 9th tool (`mcp_server/tools.py`/`server.py`),
  same thin-wrapper pattern, `write=False` by default.

**Live-tested against the real corpus and real Azure OpenAI** (2026-09-09)
using `entity:symptom:system_fault` — chosen because it has two real
`MAY_INDICATE` edges (to `capability:confirm_agv_active_error_state` and
`capability:confirm_wcs_system_faults`), and both target capabilities
already have multiple real Procedures, making it the first real case
where a drafted Playbook could genuinely branch between two independently
-verified diagnostic paths rather than trivially chaining one symptom to
one procedure. Result: a real 6-node decision graph — a
`diagnostic_decision` entry node branching healthy/unhealthy/inconclusive/
escalate into either a second `diagnostic_decision` node (for the
WCS-fault path) or directly to a `procedure_reference` node, two
`procedure_reference` nodes each citing a REAL, pre-existing
`procedure_id` (not invented), and two `escalation_gate` nodes for
conflicting/inconclusive evidence. Every node's `source_refs` cited real
ids. `gaps` correctly named exactly what the retrieved evidence didn't
support: no procedure existed yet for confirmed WCS-fault remediation
itself, no cross-check priority rule between the AGV-first and
WCS-first paths, and no validation-gate procedure was retrievable — the
model reported these rather than inventing a plausible-sounding
resolution. The record constructed cleanly and passed a full pydantic
round-trip. The dangling-reference guard was separately confirmed firing
on a deliberately invented `procedure_id`. This was a pure dry-run
(`write_drafted_playbook` never called against real storage) — the real
corpus is unmodified.

**What this still doesn't do:**
- **No automatic reconciliation against an existing Playbook covering the
  same entry symptom(s).** Same open question as `draft_procedure`'s
  equivalent gap — nothing checks whether a Playbook already exists for
  this symptom cluster before drafting a new one.
- **Not yet wired into any pipeline stage hook** (Stage 8's playbook
  finalization is untouched) — same deliberate deferral as
  `draft_procedure`, pending real incident cases to test the wiring
  decision against.
- **No check that a `procedure_reference` node's cited Procedure is
  actually approved/trustworthy** — `build_playbook_record` only checks
  the `procedure_id` EXISTS in the corpus, not its `validation_status`. A
  Playbook can currently route to an `operational_unreviewed` Procedure
  just as readily as an `sme_approved` one. Worth revisiting once real
  Playbooks are actually reviewed and approved, so a routing decision
  doesn't quietly depend on unreviewed content.

## 19. Brain ingestion defaults ON; pipeline audit; Stage 7/8 bridge/adapter modules (2026-09-09)

### 19.1. `BRAIN_INGESTION_ENABLED` now defaults ON

User-directed reversal: "brain ingestion should always be enabled."
`brain_service/pipeline_hook.py::brain_enabled()` now returns `True` when
the env var is unset, and `False`/opt-out only on an explicit `0`/`false`/
`no`. All 9 affected test files (the module's own `test_pipeline_hook.py`
plus each pipeline's 4 `test_stageN_brain_hook.py` files) were updated:
each "gate is off" test now explicitly sets `BRAIN_INGESTION_ENABLED=0`
rather than relying on `delenv` (which now means ON), and a new
`test_hook_calls_ingest_stage_output_by_default` test was added per file
confirming the unset-env-var path actually fires. `.env.example`'s
comment updated to match. All 45 gate-related tests plus the full
249→266-test Brain suite (see §19.3) pass.

**A stash-recovery incident during verification, corrected before
proceeding**: while confirming these test changes didn't regress
pre-existing (unrelated) test failures, a `git stash`/`git stash pop`
used to compare against a clean tree hit a Windows file-unlink error
partway through the pop, silently leaving one of the user's own
already-uncommitted files
(`operationalknowledgeingestion/src/optisweep_ingestion/stage1_training_video_builder.py`)
reverted to its last-committed version instead of the pop's intended
content. Caught by diffing the working tree against the stash object
before dropping it (`git diff --stat stash@{0}`), not by assuming the pop
succeeded — restored the one affected file via
`git checkout stash@{0} -- <path>`, confirmed a zero-line diff against
the stash, then dropped it. No data was lost, but this is a concrete
example of why "the command exited/appeared to finish" is not the same
as "the operation fully completed" for anything touching the working
tree — always diff-verify after a stash operation that errors, before
trusting it and moving on.

### 19.2. Ingestion pipeline audit: are Stage 7/8 over-built?

Before any Stage 7/8 integration work, the user asked whether shared
Stage 7 (cross-source runbook merge) and shared Stage 8 (playbook-to-
runbook linking) are actually necessary, given their size. A full-pipeline
research pass found:

- **Stage 7 rarely merges anything.** A real run
  (`shared_pipeline_stages/data/output/shared/stage_7_merged_runbooks/runbook_merge_report.json`,
  2026-08-09): 270 input runbooks, 262 (97%) passed through Stage 6.5
  untouched, only 8 (3%) reached the Stage 7 LLM across 3 clusters, and
  all 3 came back `"split"` — zero merges in that run
  (`llm_merge_count: 0`). An earlier tuning run did show 2 real merges. So
  Stage 7's demonstrated value skews toward "correctly documents why
  similar-looking runbooks stay separate," not "catches duplicates,"
  though it does occasionally do the latter.
- **Stage 8's own pilot-scope gate has an unresolved discrepancy.** Its
  design doc (`docs/design_decisions/stage_8_playbook_finalization.md`)
  still says "pilot scope: 2 incidents only... do not expand until pilot
  review passes," with no pilot-review-outcome artifact found anywhere in
  the repo. `docs/development_status.md` shows Stage 8 already running
  across 4 cases, and `sme_review_runbooks/README.md` says the SME review
  packs were "cleared" (reset), not "approved." Not resolved in this
  session — flagged to the user as a discrepancy, not silently ignored.
- **Nothing outside the ingestion pipeline consumes Stage 8's output live
  today** — Stage 9 (validator) and Stage 11 (Cosmos publish) are its
  real in-repo consumers; the actual app repo reads published Cosmos
  containers, not these JSON files directly.
- **`draft_procedure`/`draft_playbook`'s own docstrings already state**
  they're meant to eventually replace this machinery, but as built today
  they lack Stage 8's compatibility-type filtering, confidence tiers,
  backend-vs-UI evidence pairing, and Stage 7's cross-source merge/dedup
  judgment entirely — Brain's tools draft fresh from the graph; they
  don't yet do any of Stage 7/8's adjudication work.

**User's decision, given this**: keep Stage 7/8 exactly as they are (no
retirement, no simplification pass) and build the Brain integration
alongside them as originally planned — this section's §19.3/§19.4 modules
are the result. The pilot-status discrepancy and the "is 10,584 lines of
Stage 8 logic worth it long-term" question were both explicitly left
open, not resolved, pending separate follow-up.

### 19.3. `shared_pipeline_stages/brain_ontology_bridge.py` — Brain-backed drop-in replacements for two `ontology_rag.py` call sites

`shared_pipeline_stages/stage_8/playbook_builder.py` currently calls
exactly two `ontology_rag.py` functions (confirmed by repo-wide grep — no
other call sites exist): `ontology_contracts_for_capabilities()` (line
422) and `ontology_snippets_for_stage5_playbook()` (line 457), both
reading from the static `docs/ontology/catalogs/*.json` files.
`playbook_builder.py` itself is currently uncommitted/actively edited on
this branch (`normalize.py` alone carries a +3400 line uncommitted diff),
so per user direction this bridge module was built standalone, NOT wired
into `playbook_builder.py` yet — swapping the two imports is a two-line
change deferred until the in-flight Stage 8 work lands.

- `brain_contracts_for_capabilities(capability_ids, *, storage)` — exact
  signature/return-shape match for `ontology_contracts_for_capabilities`.
  Reads Brain's real `Capability.support_contract` field directly (no
  reshaping needed, it already matches); `backend_mappings` is derived
  from `Capability.sql_field_notes`, grouped by table, mirroring the
  shape the original function synthesizes from `primary_models`/
  `field_highlights` for the same downstream consumer.
- `brain_snippets_for_stage5_playbook(text, *, embeddings, storage,
  artifacts=None)` — exact signature/return-shape match for
  `ontology_snippets_for_stage5_playbook`. Uses real semantic search
  (`brain_service/retrieval.py::find_similar_records`) instead of the
  original's kind-then-score ranking (Brain has no equivalent snippet-kind
  taxonomy); return shape confirmed against the ACTUAL consumer
  (`shared_pipeline_stages/stage_8/action_synthesis.py::_selected_ontology_entities`,
  which only reads `id`/`title`/`score`/`source_refs`/`text` keys — read
  directly, not assumed) rather than the shape `ontology_rag.py` happens
  to produce.
- 8 tests, `brain_service`-style (`LocalStorageProvider` + a fake
  `EmbeddingProvider`), all passing.

### 19.4. `shared_pipeline_stages/brain_output_adapter.py` — canonical_runbooks.json/canonical_playbooks.json → real Brain Procedure/Playbook records

Additive alongside Stage 7/8's existing JSON output, not a replacement —
Stage 7/8's own compatibility/scoring/confidence logic
(`link_scoring.py`/`normalize.py`/`capability_derivation.py`) is
untouched; this module runs strictly AFTER that logic has already
produced its finalized dict.

**Follows `brain/migration/enrich_brain_knowledge.py`'s established
precedent exactly** for the hardest problem here: `canonical_runbooks.json`/
`canonical_playbooks.json` cite their own provenance as free-form objects
(`source_document_id`/`page`/`quote_or_summary`), not Brain evidence ids —
there is nothing for an individual step/branch to cite directly. Rather
than inventing one synthetic evidence id per citation object (manufacturing
false precision this data doesn't have), the whole runbook/playbook dict
is wrapped as ONE `EvidenceUnit` (`content.structured_payload` holds it
verbatim, matching the existing migration script's exact pattern), and
every derived Procedure/Playbook field cites that single evidence id.

- `canonical_runbook_to_procedure(runbook, *, index, source_id)` — builds
  a `Procedure` only if at least one `capability_tags[]` entry resolves to
  an EXISTING Brain `Capability` (never invented); reuses
  `brain/migration/capability_state_pairings.py::PAIRINGS` and the exact
  three-step resolution (direct id → PAIRINGS rename → fuzzy suffix match)
  `enrich_brain_knowledge.py::_catalog_slug_to_capability_id` already
  validated for this identical slug-mismatch problem — confirmed
  necessary by testing against real data: capability_tags[] uses
  PRE-RENAME slugs (`"device_roster_state"`), Brain's real ids use the
  renamed convention (`"capability:confirm_device_roster_state"`); a
  naive direct-slug guess resolved ZERO of the first 60 real runbooks
  before this fix.
- `canonical_playbook_to_playbook(playbook, *, index, source_id)` —
  resolves each node's `resolved_runbook_ids`/`linked_primary_procedure`
  (Stage 7's own `"proc_*_v1"` ids) against whatever real Brain
  `procedure:*` id was assigned when that SAME runbook was promoted via
  `canonical_runbook_to_procedure` in the same corpus (matched via the
  wrapping EvidenceUnit's `structured_payload.procedure_id` — Brain's own
  `procedure_id()` naming has no fixed relationship to Stage 7's ids). A
  node whose linked runbook hasn't been promoted yet is downgraded from
  `procedure_reference` to `diagnostic_decision` rather than emitting a
  `procedure_reference` node with a fabricated `procedure_id` — the gap is
  named in the result, never silently dropped. Dangling branch targets
  (pointing at a node id not in this same playbook) are cleared with a
  named gap rather than letting `Playbook`'s own validator hard-fail the
  whole record over source data this adapter doesn't control.
- Both role resolution (`_resolve_role`) and capability resolution
  (`_resolve_capability_id`) only ever return an id that ALREADY EXISTS in
  the corpus — mirrors `persistence.py`'s/`procedure_drafting.py`'s
  `DanglingReferenceError` discipline exactly, extended to a third input
  source (pre-Brain pipeline output, not just an LLM's own proposal).
- **A real performance bug found and fixed during live-data testing**: the
  first version called `storage.load_brain_context()` (a full corpus
  scan) once per role/capability/procedure-id lookup, per runbook — for
  268 real runbooks against the ~20K-record local corpus, this was still
  running after 4.5 minutes. Fixed by introducing `BrainCorpusIndex`
  (a frozen dataclass) and `build_corpus_index(storage)`, called ONCE per
  batch and passed into both adapter functions instead of a bare
  `storage` — reduced to 0.72s to build the index plus 0.07s to adapt all
  268 runbooks. This is the same class of lesson as this session's
  earlier stash-recovery incident (§19.1): a slow-but-eventually-correct
  first pass is not the same as a validated one — the 4.5-minute run
  (confirmed still completing with identical 257-built/11-gap numbers)
  is what caught this, not code review alone.
- **Live-tested against the real corpus, not just hand-crafted
  fixtures**: all 268 real runbooks from
  `shared_pipeline_stages/data/output/shared/stage_7_merged_runbooks/canonical_runbooks.json`
  — 257 built into schema-valid Procedures (zero round-trip validation
  errors), 11 skipped for having no `capability_tags` at all (a genuine
  data-completeness gap, not a resolution bug — confirmed by checking:
  zero tags were unresolvable, the 11 gaps were all empty-tag-list cases).
  All 4 real playbooks from
  `stage_8_finalized_playbooks/prompt_a_one_per_incident/canonical_playbooks.json`
  built cleanly with zero gaps once their referenced runbooks were
  promoted first in the same test run. The dangling-reference downgrade
  was separately confirmed via unit test. A scratch corpus scope
  (`_live_test_scratch`) written during this live test was deleted
  immediately after — not part of the corpus going forward.
- 9 tests (`test_brain_output_adapter.py`), all passing; combined with
  §19.3's 8, brings the total `brain`/`providers`/`brain_service`/
  `mcp_server`/new-bridge-modules suite to **266 passing tests**.

**Deliberately not done in this pass** (superseded — see §20.2:
`brain_ontology_bridge.py` was wired into `playbook_builder.py` once the
Stage 7/8 branch was committed): at the time of writing, neither module
is wired into `playbook_builder.py` yet (that file is still uncommitted/
in-flux); no decision made yet on WHEN a caller should invoke
`canonical_runbook_to_procedure`/`canonical_playbook_to_playbook` in a
real pipeline run (once per Stage 7/8 run? on demand? gated by
`BRAIN_INGESTION_ENABLED` like the other hooks?) — left open pending the
Stage 7/8 work landing and the user's new incident ingestion providing a
real case to decide against.

## 20. Stage 7/8 committed and reviewed; ontology bridge wired in; full corpus pushed to live Cosmos (2026-09-09)

### 20.1. Stage 7/8 diff reviewed before commit — three real bugs found and fixed

Once the Stage 7/8 branch's large uncommitted diff (§19's stated blocker)
was ready to commit, a genuine code-review pass (not a rubber stamp)
found and fixed three real bugs before committing:

- **`playbook_builder.py`'s pool-only runbook pass-through never
  hydrated `source_id`/`source_type`/`source_path`/`validation_status`**,
  unlike the sibling branch for runbooks already in
  `canonical_runbooks.json` — confirmed causing a live `KeyError` against
  8 of 270 real pool runbooks, and a currently-failing test. Fixed by
  extracting the shared hydration logic into a new
  `_hydrate_runbook_from_pool()` helper both branches now call.
- **`link_scoring.py::node_expects_capabilities()` used `or` instead of a
  set union** between `required_evidence_concepts` and
  `expects_capability` — silently dropping one field's contents whenever
  the other was populated, feeding 13 call sites of core scoring logic.
- **`normalize.py::_infer_unhealthy_destination()` bypassed its own
  recovery-prerequisite safety gate** (`_transition_allowed`) via a
  keyword-regex fallback, specifically on the unhealthy/inconclusive
  branch — exactly the branch most likely to describe a fault in matching
  language (residual/abnormal/fault/recover/...) before recovery had
  actually happened. Removed the bypass; the function now falls through
  to the existing sequential-diagnostic fallback instead, same as when no
  branch hint matches at all.

All three fixed and verified against the real 121-test Stage 7/8 suite
before committing (separate commit from the Brain subsystem's own
commit, keeping the two concerns distinguishable in history). A stray,
previously-untracked 764-line/32-test file
(`test_stage_8_retrieval_eligibility.py`) was caught by the review and
included in the commit — it would otherwise have silently stayed
decoupled from the logic it tests.

### 20.2. `brain_ontology_bridge.py` wired into `playbook_builder.py` — full replacement, no static-catalog fallback

Per explicit user direction ("always use Brain now, remove the static
catalog path entirely"), the two `ontology_rag.py` calls in
`_finalize_playbook_candidate` were replaced outright with
`brain_ontology_bridge.py`'s Brain-backed equivalents — not gated behind
a config flag the way `Stage8BuildConfig.allow_lexical_fallback`/
`use_mock_embedder` gate other optional behaviors in this same file.
`build_stage8_finalized_playbooks` gained `brain_storage`/
`brain_embeddings` parameters, defaulting to real providers via
`mcp_server.providers_config`'s existing factory functions (the same
provider-selection pattern the MCP server itself uses) when not supplied.

**Immediately surfaced a real, concrete consequence of the "no fallback"
decision**: the one existing test that calls `build_stage8_finalized_playbooks`
directly (`test_stage8_pilot_build_without_llm`) had no mock Brain
providers of its own — it only mocked Stage 6.5's own embedder
(`use_mock_embedder=True`) — so it silently fell through to constructing
a real `AzureOpenAIEmbeddingProvider` and a real `LocalStorageProvider`
against the actual local corpus. Observed taking 168 seconds (the real
Azure calls actually succeeded, just slowly) before being fixed with an
isolated `LocalStorageProvider(root=tmp_path / "_brain_storage")` and a
zero-network fake embedder — 36 seconds after. This is the same class of
lesson as §19.1's stash-recovery incident and §19.4's output-adapter
performance bug: a slow-but-eventually-passing test run is a signal to
investigate the cause, not a result to accept and move past.

### 20.3. Full local corpus pushed to live Cosmos

A new `providers/scripts/sync_local_brain_to_cosmos.py` — idempotent
(upserts by each record's own content-derived id via
`AzureStorageProvider.save_brain_records`, safe to re-run after a partial
failure), push-only (never deletes from Cosmos), and ordered by
dependency (Entities/EvidenceUnits first, since nearly every other record
type cites one of these; Reviews last) — was built to push the entire
local corpus to the already-provisioned 10 Brain Cosmos containers.

**Staged deliberately, per user agreement, rather than pushing ~20K
records blind**: a 31-record Capabilities-only push ran first and was
verified with a real read-back (`AzureStorageProvider.load_brain_context(record_type=CAPABILITY)`
returned all 31, correctly reconstructed as typed `Capability` objects,
e.g. `capability:optisweep_service_restart`) before committing to the
full run.

**The full sync completed successfully: 19,766/19,766 records pushed,
zero failures, in 2,792 seconds (~46.5 minutes)** — 2,191 entities, 3,614
evidence units, 2,023 claims, 11,597 relationships, 31 capabilities, 301
procedures, 9 playbooks, 0 reviews. Verified independently after
completion rather than trusting the script's own exit code alone: a
fresh `load_brain_context(record_type=...)` call for every one of the 7
present record types returned a count matching the local corpus exactly
(0 discrepancies across all 7 types). Content integrity spot-checked too
— pulled a real `Playbook` (`playbook:one_per_incident:218550:bagout_agv_sequence`,
6 nodes) and a real `Procedure`
(`procedure:confirm_hospital_diversion_path:case_218550_proc_hospital_hmi_lane_ui_fault_acknowledge_retry_check_v1`,
3 steps) back from Cosmos, confirming both reconstruct with full nested
content intact, not just a matching top-level count. The Brain corpus now
genuinely lives in Cosmos in full, not only the local dev store.

## 21. Brain HTTP API built for appcode (OPTISWEEP_APP_BRAIN_HTTP_BOUNDARY.md, 2026-09-09)

### 21.1. The contract, and what it changed

appcode (the separate runtime/app repo) proposed a real architectural
split, confirmed back after checking it against what actually exists in
this repo (their contract doc itself is not readable from here — no
local copy, no reachable appcode checkout — so every confirmation below
is grounded in this repo's own code, not assumed from their prose):

- The app talks to Brain over **HTTP**, not MCP — MCP stays for Codex/
  internal agents only. Nothing HTTP-shaped existed anywhere in this repo
  before this section (confirmed by grep for fastapi/flask/uvicorn
  imports — zero hits) — this is new server infrastructure, not newly
  exposing something already built.
- Brain hosts the HTTP API and owns all `brain_*` container mutation.
  Appcode is a client only — no Brain write credentials on their side.
- Four routes: `POST /context/retrieve`, `POST /context/troubleshoot`,
  `POST /feedback`, `GET`+`POST /reviews/{id}/resolve`.
- **Critical response rule, independently verified as a real, current
  gap before agreeing to it**: `ContextPacket` (`brain/schemas/context_packet.py`)
  is genuinely ID-only today — every field is `list[str]`, by explicit
  original design ("never inlined record content"). If an HTTP endpoint
  had shipped returning a raw `ContextPacket`, appcode would have gotten
  exactly the bare-id shape their rule warns against. This was the
  concrete reason `brain_service/hydration.py` (§21.2) exists.
- **Feedback write policy: confirmed as sync-write**, matching the exact
  model already shipped for pipeline ingestion (§persistence.py's
  2026-09-09 write model) — not a new, app-specific policy. `/feedback`
  routes straight through the existing `run_create_chain` (Create-path
  chain), no new write logic needed.
- **`/reviews/{id}/resolve` "Brain applies corpus changes" surfaced a
  real, pre-existing gap** that had to be closed, not just documented:
  `resolve_audit_candidate` (Tool 6) explicitly never executes its own
  proposed resolution against the corpus — a long-standing, deliberately
  deferred item (§10.2.1 in the original design). appcode's contract
  requires it to actually apply. Locked scope after discussion: **MERGE
  executes for real now** (the common, well-understood case); **RETYPE**
  and **RECLASSIFY are accepted but not applied** — both would rewrite a
  record's own id (ids embed `entity_type`, e.g. `entity:symptom:x`),
  cascading into every `Relationship`/`Claim` referencing the old id
  across an 11,597-relationship graph, and nothing in this codebase
  (`AuditResolutionResponse.fields_to_rewrite`/`winner_record_id`) was
  ever wired into a real execution path before this. Explicit design
  stance: a caller must never be told a corpus id changed when it didn't
  — an unsupported resolution comes back `applied=False` with a plain-
  language `detail`, never a silent no-op and never an attempted
  best-effort rewrite.
- Hydration limits proposed and confirmed: **10–15 excerpts, ~1,500–2,000
  chars each** (anchored on `get_brain_context`'s own existing
  `semantic_top_k=10` default — NOT `embedding_text_for`'s ~500-char
  search-indexing convention, which appcode correctly flagged as too
  short for something a person/LLM needs to actually read downstream).

### 21.2. `brain_service/hydration.py` — the critical-response-rule implementation

`hydrate_context_packet(packet, storage=...)` resolves every id across a
`ContextPacket`'s `entities`/`approved_knowledge`/`evidence_excerpts`/
`conflicts` fields into real content, deduplicated (an id can legitimately
appear in more than one field), ordered so `approved_knowledge` ids are
hydrated FIRST — a truncated response must lose working/conflict material
before ever losing approved material, never the reverse. Each excerpt is
labeled `approved` (status in `APPROVED_KNOWLEDGE_STATUSES` — reusing that
existing filter, not re-deriving it), `conflict` (status is
`CONFLICTING`), or `working` (everything else, including a `BrainReview`
itself, which has no approval concept of its own). Text comes from the
existing `embedding_text_for()` (one function, two now-different
consumers: search indexing at ~500 chars there, human/LLM-facing
hydration at up to 2000 chars here), truncated and flagged `truncated=True`
rather than silently cut with no signal. 9 tests, including one asserting
the exact "approved survives truncation, working/conflict gets dropped
first" ordering behavior.

### 21.3. `brain_service/audit_execution.py` — MERGE actually applied

`apply_audit_resolution(storage, review, winner_record_id=...)` — new
module closing the §21.1 gap for MERGE specifically. Reuses `merge_record`
(the exact same "grow richer, never regress" mechanic REINFORCE/PATCH
already use in `persistence.py`) to fold every non-winner
`affected_record_ids` entry's fields into the winner, writes the merged
winner back to ITS OWN real scope via `find_scope_for_record` (the same
scope-mismatch lesson from the 2026-09-09 persistence work — never the
caller's scope), and marks every losing record `ValidationStatus.DEPRECATED`
rather than deleting it (`StorageProvider` has no delete method at all,
confirmed by reading its full interface — deprecation is the only
existing, already-modeled "this is no longer current" lifecycle state,
consistent with this whole system's "never destroy, always flag"
philosophy already established for CONFLICT). RETYPE/RECLASSIFY/
NOT_A_DUPLICATE/NEEDS_HUMAN all return `applied=False` with a plain
explanation, never raising and never silently doing nothing without
saying so. Idempotent — merging into an already-deprecated loser a second
time correctly reports it as NOT re-mutated. 10 tests.

### 21.4. `http_server/` — the actual FastAPI app

New top-level package, sibling to `mcp_server/`, both calling into the
same `brain_service/` functions underneath (no logic forked between
transports) and sharing `mcp_server/providers_config.py`'s existing
provider-selection factories directly (renamed its docstring to reflect
it's no longer MCP-only, not duplicated into a second copy).

- `http_server/models.py` — request/response pydantic models for all four
  routes. `TroubleshootRequest` is genuinely distinct from
  `ContextRetrieveRequest`: session/node/signal-aware
  (`session_id`/`playbook_id`/`current_node_id`/`observed_signals`),
  folding session signals into the semantic query text rather than
  treating "signal" as a structured Brain concept it doesn't have.
- `http_server/routes.py` — the actual handler logic, zero FastAPI import
  (mirrors `mcp_server/tools.py`'s separation from `mcp_server/server.py`'s
  transport wiring), so every handler is directly unit-testable with fake
  providers. `handle_resolve_review` lets an SME's explicit `resolution`
  override whatever `resolve_audit_candidate` itself proposed (a human's
  direct judgment call outranks an agent's proposal), defaulting to
  running Tool 6 first when the SME doesn't specify one.
- `http_server/app.py` — the FastAPI wiring itself: 5 endpoints (4 routes,
  one of which is GET+POST), each a thin pass-through to `routes.py`,
  with `ReviewNotFoundError`→404 and validation/merge errors→400 mapped
  at this layer only (business logic never raises HTTP-flavored
  exceptions itself).
- 13 tests: 7 direct handler tests (`test_routes.py`, real business-logic
  assertions — e.g. confirming the critical response rule holds, confirming
  `open_count` reflects the TOTAL open count independent of a status
  filter) + 6 through a real `TestClient` (`test_app.py`, confirming
  actual routing/status-code/validation behavior, not just handler logic
  in isolation).

### 21.5. A real, live-tested bug found and fixed: Cosmos had zero embeddings

Live-tested `/context/retrieve` against real Azure providers immediately
after building it — first against local storage (worked correctly,
`excerpt_count: 15`, `truncated_excerpt_count: 172`, real hydrated text
with correct status labels) — then, per this session's own standing
practice of testing against the real target backend before calling
anything done, against `OPTISWEEP_STORAGE_BACKEND=azure` directly.

Two real, distinct bugs surfaced from that one live test, neither
hypothetical:

1. **`get_storage_provider()` still rejected `"azure"` outright** — its
   own error message said "azure storage is deferred," which had been
   true when originally written but was stale: `AzureStorageProvider` has
   been real, live-tested, and holding the full 19,766-record corpus
   since earlier in this same session. Fixed by wiring the `"azure"`
   branch in (3 new tests, `mcp_server/tests/test_providers_config.py`).
2. **Real Cosmos returned `200 OK` with `excerpt_count: 0`** even after
   fix #1 — traced to `sync_local_brain_to_cosmos.py` (§20.3) having only
   ever pushed the 7 `BrainRecord` containers, never the SEPARATE
   embeddings corpus (`save_embeddings`/`load_all_embeddings`) that
   `get_brain_context`'s semantic search actually reads from for any
   `query_text`-based call. Confirmed directly:
   `AzureStorageProvider().load_all_embeddings()` returned 0 while the
   local corpus held all 19,766. This would have silently broken BOTH
   `/context/retrieve` and `/context/troubleshoot` in production against
   the real backend appcode is meant to use — a 200-with-empty-results
   response, not an error, meaning it could easily have gone unnoticed
   without this specific live-against-Cosmos test. Fixed by extending
   `sync_local_brain_to_cosmos.py` with an embeddings-sync step (runs
   automatically after the 7-container sync, or standalone via
   `--embeddings-only`), then running it for real against live Cosmos.

**A third bug, found by that same real run, not by review**: the first
real embeddings-sync attempt crashed outright after 2,000/19,766 pushed
with `socket.gaierror: [Errno 11001] getaddrinfo failed` — a transient
DNS failure, the exact same class of failure the embedding backfill
script (§16.3-era work) already had to handle and does handle (its own
docstring: "hit one transient DNS failure partway through and resumed
correctly... with zero duplicate work"). `_sync_embeddings`'s batch loop
had no try/except at all, unlike the sibling 7-container sync loop just
above it in the same file, which already catches-and-continues per batch
— an inconsistency introduced when the embeddings step was added, not
present in the original record-sync code. Fixed with a one-retry-then-
record-and-continue policy matching the existing record-sync loop's own
discipline. Confirmed the crash caused no data loss (`AzureStorageProvider`'s
upsert is idempotent by record id) by checking Cosmos directly before
re-running: 3,559 embeddings had actually landed (more than the last
printed 2,000-checkpoint, since the crash hit mid-batch after that
print) — the re-run picked up cleanly from there with no duplication.

**The re-run itself then hit a second, longer real outage** — not a
one-off blip this time: the run's own progress log shows a ~41,000-second
stall between the 6,000 and 8,000 checkpoints (2,111s → 12,258s elapsed)
and another one between 12,000 and 14,000 (13,131s → 55,015s), both
consistent with an extended real network interruption, not a bug. The
1-retry policy from the first fix is correctly designed for a brief blip,
not an outage lasting that long — it retried once, waited 2 seconds,
failed again, and correctly recorded the failure and moved on rather than
crashing the whole run a second time (the fix held). End result: 19,641
of 19,766 pushed, 125 failed after retry, all the same
`getaddrinfo failed` DNS error. **This is the correct, intended behavior
for a bounded retry policy — a policy that retries forever risks a stuck
process instead, so the real fix for "the outage outlasted 1 retry" is a
separate, explicit follow-up pass, not a longer wait baked into the main
sync.** That follow-up is `--missing-embeddings` (new): diffs local vs.
remote by id (confirmed 108 actually missing — slightly fewer than the
125 the main run's own count showed for a reason not fully
pinned down, most likely a handful landing on a save_embeddings batch's
partial success before the final failure was raised, but not chased
further since verifying by direct id-diff against real Cosmos state, not
count arithmetic, is the correct source of truth here) and retries each
individually up to 5 times with exponential backoff (up to 30s) — for
closing a gap left by a real extended outage, not the main sync's
1-retry blip tolerance.

**`--missing-embeddings` closed the gap completely on its first run**:
all 108 previously-missing embeddings pushed successfully in 22 seconds
with zero further failures (the earlier outage had genuinely cleared).
Confirmed independently, not trusted from the script's own exit code:
a fresh direct `AzureStorageProvider().load_all_embeddings()` call
returned **exactly 19,766 / 19,766** — the complete local embeddings
corpus, fully present in Cosmos with no gap remaining.

**Then the real end-to-end test that actually matters**: called
`POST /brain/v1/context/retrieve` through the real FastAPI app against
`OPTISWEEP_STORAGE_BACKEND=azure` (not local storage, not a mock) with
query text `"AGV active error confirm state"`. Result:
`status=200`, `excerpt_count=15`, `truncated_excerpt_count=172` —
identical numbers to the earlier local-storage test of the same query,
with real semantically-relevant hydrated excerpts
(`entity:system:agv_error_monitoring`, `entity:system:agv_status_popup`,
`entity:system:agv_active_error_database_model`, ...) correctly labeled
and status-tagged. Semantic search against the real production Cosmos
backend is confirmed fully working, not just "the vectors exist" —
closing out §21's embeddings gap for real.

(Note on query latency at this corpus size: a full cross-partition
`load_all_embeddings()` scan over ~19,766 documents took 210-235 seconds
in direct testing during this verification — worth knowing before reading
a query that takes several minutes as a hang. This is a real
characteristic of the current brute-force approach at this scale, not a
new regression; `brain_service/retrieval.py`'s own docstring already
flags brute-force cosine search as "revisit... once the corpus is large
enough that this becomes the actual bottleneck" — this measurement is
concrete evidence that point may be closer than previously assumed for
the Cosmos backend specifically, though local storage's own in-process
cache keeps its own repeat-query cost far lower. Not addressed in this
pass; noted for whoever next looks at retrieval performance.)

This is the same category of lesson as §19.1's stash-recovery incident,
§19.4's 168s-vs-36s test timing, and §20's output-adapter performance
bug: **the specific value of testing against the real target, not just a
local/mocked stand-in, is that it catches exactly the class of gap a
passing local test cannot see.** A `200 OK` with an empty body is the
quietest possible failure mode — no exception, no stack trace, nothing
that would fail a shallow smoke test — and would not have been caught
without deliberately testing the real Cosmos path before telling appcode
this was ready.

## 22. Brain HTTP API deployed to Azure Container Apps (2026-09-10)

Full detail in `AGENT_AZURE_HANDOFF.md and brain/DESIGN_RATIONALE.md`'s 2026-09-10
milestone entry (the appcode-facing record); brief pointer here for the
internal log. Deployed as its own Container App (`optisweep-brain-http`)
in `optisweepai`/`managedEnvironment-optisweepai-a18c`, alongside the
live `optisweepai-troubleshooting-app`, following that app's exact
pattern (system-assigned identity, ACR pull via that identity, secrets
from the shared `optisweep-ai-keyvault`).

Two real, non-obvious problems hit during deployment, both resolved by
verifying against the real system rather than assuming a tool's own
success/failure report:
1. `az acr build`'s local source-packaging step choked on a Windows
   path-length limit inside `operationalknowledgeingestion/data/output/`
   before `.dockerignore` filtering even applied — resolved by building
   from a clean, minimal robocopy'd temp directory (1.81MB) instead of
   fighting the full ~4.6GB repo tree.
2. `az role assignment create`/`list` failed with a persistent
   `MissingSubscription` error for this CLI session specifically (a
   Graph/AAD permission gap, not a transient failure — tested multiple
   invocation forms). Could not grant `Key Vault Secrets User` to the new
   container's managed identity via CLI; the user granted it directly in
   the Portal. Verified indirectly but conclusively: `az containerapp
   secret set`'s own Key Vault-reference validation would have failed
   immediately if the identity lacked the role, and it did not.

Live-verified against the real deployed URL (not local storage, not
`TestClient`): `POST /brain/v1/context/retrieve` returned `200` with 15
real hydrated excerpts, byte-for-byte matching every prior local test of
the same query. `/docs`, `/openapi.json`, and `GET /brain/v1/reviews`
(correctly empty) all confirmed live.

## 23. Real latency root cause found and fixed — 210-235s cold to ~1.5-2s warm (2026-09-10)

appcode asked for an ANN index to fix cold-retrieve latency
(~210-235s, measured against the deployed API). **The actual root cause
was not vector-search speed** — found by reading the real call chain
before reaching for a vector library, not by assuming the framing in the
request was correct:

1. **`get_storage_provider()`/`get_embedding_provider()`/`get_llm_provider()`
   were called fresh on every single route handler invocation.**
   `AzureStorageProvider` already had a working embeddings cache (built in
   §16-era work) that could never actually warm up in production, since a
   brand-new instance was constructed per request — every call, not just
   the first, paid a full network round-trip. Fixed with process-lifetime
   singletons in `http_server/app.py` (`_get_storage()`/`_get_embeddings()`/
   `_get_llm()`, lazily constructed once, guarded by a lock since FastAPI
   runs sync route handlers in a thread pool — two concurrent cold
   requests must not each construct and discard their own instance). 4
   new tests, including one that actually races 5 threads against the
   lock and confirms the factory ran exactly once.
2. **`get_brain_context()` called `find_similar_records()` 3 times per
   request (entities/claims/evidence), each re-embedding the identical
   `query_text` from scratch** — a real Azure OpenAI/Foundry network call,
   3x redundant. Fixed: `find_similar_records()` now accepts a
   pre-computed `query_vector` (still accepts bare `query_text` for the
   one other real call site, `brain_ontology_bridge.py`, which has no
   reason to precompute); `get_brain_context()` embeds once and reuses
   the vector for all three searches.
3. **The real dominant cost**: `AzureStorageProvider.load_brain_context()`
   (and `load_brain_records()`) had ZERO caching at all, unlike
   `load_all_embeddings()` — every call re-fetched the ENTIRE container
   from Cosmos via a fresh cross-partition scan (11,597 relationships,
   2,191 entities, 2,023 claims), and a single `/context/retrieve` call
   triggers 3-4 of these (initial entity lookup + one relationship scan
   per hop + a claim scan). Fixed with the identical per-record-type
   caching pattern already proven for embeddings
   (`_records_cache: dict[RecordType, list[BrainRecordUnion]]`, populated
   in `_query_container`, invalidated precisely — only the written record
   type's cache entry is cleared on `save_brain_records`, not the whole
   cache, so writing a Capability doesn't force Relationship/Claim/Entity
   readers to pay a fresh scan on their next call). 3 new tests
   (cache-hit-after-first-call, invalidates-the-written-type,
   does-NOT-invalidate-other-types).

**Real measurements against the actual deployed Container App** (not
local, not estimated): cold call after a fresh revision deploy = 49.3s
(expected — first call still pays the full uncached scans once); warm
call, same query = **1.99s**; warm call, different query = 1.56s; warm
`/context/troubleshoot` call = 1.64s. All three confirmed returning
identical content/excerpt counts to every prior test (`excerpt_count: 15`,
`truncated_excerpt_count: 172` for the AGV query) — the fix changed
speed, not correctness.

**No ANN index was built, and none was needed for this problem.** An ANN
index would have sped up the brute-force cosine comparison step
specifically — a step that was never actually the bottleneck (confirmed:
the comparison itself runs in milliseconds over 20K vectors in pure
Python; the 210-235s was 100% uncached network I/O). Building one anyway
would have added real complexity (a new dependency, an index-rebuild
story for corpus growth, a new failure mode) to fix a problem that
didn't exist, while leaving the actual bottleneck (3x redundant
embedding calls, zero-cache full-container scans) completely untouched.
This is the same "verify before building" discipline as every other
milestone in this log — the framing of a request ("build an ANN index")
is not the same as its root cause, and the two turned out to be
different problems here.

## 24. RETYPE now actually applies on SME approve; RECLASSIFY stays deliberately unapplied (2026-09-10)

appcode's other ask alongside ANN: `resolve_review` always returned
`applied: false` for every resolution except MERGE, including RETYPE —
an SME could approve a RETYPE and nothing would happen to the corpus.
appcode's stated acceptance: success → `applied: true` +
`mutated_record_ids`; failure → `applied: false` + a clear `detail`
(never silent success); an idempotent/dry-run story.

**Scope decision (confirmed with user, not inferred)**: implement RETYPE
for real; leave RECLASSIFY explicitly unapplied with its own distinct
reason, rather than lumping both under one generic "not applied yet"
message the way the code did before this change. The two resolutions
are not the same shape of problem — RETYPE is a mechanical id/type
correction (`entity_type` is wrong on an otherwise-correct `Entity`
record); RECLASSIFY means the record is the wrong *kind* entirely (a
`Claim` that should have been an `Entity`, or similar) and converting
that shape by machine would mean fabricating fields a human never
supplied. RECLASSIFY's `detail` now says exactly that ("no mechanical
procedure... requires human judgment about what survives the
conversion") instead of sharing RETYPE's old message.

**What `_apply_retype()` (`brain_service/audit_execution.py`) actually
does**, in order, refusing (raising `RetypeTargetError`, never silently
no-oping) at the first failed check:

1. Requires exactly one `affected_record_id` on the review (a RETYPE is
   a single-record operation by definition) and a `new_entity_type`
   string (the one piece of information the LLM resolver step could not
   infer on its own — `resolve_audit_candidate.md`'s prompt was updated
   to require `fields_to_rewrite = {"entity_type": "<value>"}` whenever
   its decision is RETYPE, and `BrainReview` gained a matching
   `fields_to_rewrite: dict[str, Any]` field, defaulted empty for
   backward compatibility with every review already persisted in
   Cosmos before this field existed).
2. Resolves `new_entity_type` against the real `EntityType` enum —
   refuses an unrecognized value rather than writing a record with a
   type nothing else in the system understands.
3. Confirms the target record is actually an `Entity` (RETYPE only ever
   applies to Entities, per the prompt's own locked boundary) — refuses
   for any other record kind, pointing the caller at RECLASSIFY instead.
4. **Payload-compatibility check**: compares
   `PAYLOAD_MODEL_BY_ENTITY_TYPE[old_type]` against
   `[new_type]` — refuses the retype outright if they differ AND the
   existing payload actually holds real data (an empty/default payload
   is always safe to retype past). This is the concrete answer to "what
   happens to payload data on a type change" — refuse rather than
   silently drop fields a human would need to notice went missing.
5. Builds the new id via `entity_id(new_type.value, name)` (the same
   id-generation function used everywhere else, not a bespoke string
   format) and checks it doesn't already collide with an existing
   record — if it would, that's a MERGE against the existing record,
   not a retype, and the prompt already tells the LLM resolver to catch
   this itself; the execution step re-checks it independently rather
   than trusting the LLM's own answer blindly.
6. **The cascade**: walks every other record in the full corpus via a
   generic recursive dict/list/str walker (`_substitute_id_in_value`) —
   not a per-schema enumeration of "which fields hold entity ids" (that
   list has been wrong before, three times, per
   `resolve_audit_candidate.md`'s own note about
   `Claim.subject_entity_id`/`Capability.support_contract` being missed
   historically) — and rewrites every exact string match of the old id
   to the new one, wherever it appears in any record of any type.
7. Marks the old id `DEPRECATED` rather than deleting it (`StorageProvider`
   has no delete capability anywhere in this system; "flag, never
   destroy" is the same pattern MERGE already uses for a losing record).
8. Runs `validate_batch()` against the full post-cascade corpus state
   *before writing anything* — if the cascade would leave any record
   invalid or any reference dangling, nothing is written and
   `RetypeTargetError` is raised with the validator's own detail.
9. Writes every mutated record in one batch and returns
   `AuditExecutionResult(applied=True, mutated_record_ids=[...])`.

**Known, explicitly documented limitation**: `Relationship.id` and
`Claim.id` are themselves derived from the ids of the records they
reference at creation time. This function rewrites the *reference
fields* inside those records (e.g. `Relationship.from_id`) but does
**not** regenerate the relationship/claim's own id to match — doing
that would itself cascade further (anything referencing the
relationship/claim by its old id would need rewriting too), which is a
second, harder problem RETYPE's own acceptance criteria didn't ask for.
This is tracked in the result's `detail` whenever it actually occurs,
never silently.

**Live-tested against the full local corpus, not just unit fixtures**
(the fixture-only tests already passing — 8 new tests in
`brain_service/tests/test_audit_execution.py` covering the renamed-and-
cascaded happy path plus every refusal branch above — confirm the logic
in isolation, but corpus-scale behavior needed its own check): copied
the real local corpus (`brain/data/local`, 632.80 MB) to a scratch
directory, never touching the real data, and ran a real RETYPE against
`entity:state:communication_loss_to_xle` → `symptom`. Result: `applied:
true`, 2.02s, 6 `mutated_record_ids` — the new
`entity:symptom:communication_loss_to_xle`, the now-`DEPRECATED` old id,
and **4 `BrainReview` records** whose own `affected_record_ids` lists
held the old id. Confirmed by direct inspection after the write: the
old entity's `validation_status` is `DEPRECATED`; the new entity has
`entity_type == EntityType.SYMPTOM` with the name preserved; each of the
4 review records had the old id replaced with the new one inside
`affected_record_ids` while every *other* id already in those same
lists (`entity:system:rms_ui`, `entity:role:l2_support`, etc.) was left
untouched. This is the generic dict-walker doing exactly what it's
supposed to at real scale — it reached inside review payloads, not just
the entity/relationship records the hand-written fixture tests
exercised — without a bespoke "does BrainReview hold entity ids"
special case anywhere in the code.

**Idempotency / dry-run story** (per appcode's ask): RETYPE is not
naturally idempotent as a bare re-run — a second call against the same
`affected_record_id` will fail at step 3 (the old id's record is now
`DEPRECATED` but still an `Entity`, so it would actually attempt a
second retype of an already-deprecated record) or step 5 (the new id
now already exists, so it refuses with the collision check). Either way
the second call fails loudly with a clear `RetypeTargetError` detail
rather than silently double-applying or silently no-oping — which
satisfies "never silent success" even without a dedicated dry-run mode.
No separate dry-run flag was built: `validate_batch()` already runs
before any write happens, so a caller who wants a preview can construct
the same review and inspect a `RetypeTargetError` (or its absence) as
the dry-run signal, without a second code path to keep in sync with the
real one.

**Wired end-to-end**: `http_server/routes.py`'s `handle_resolve_review`
now extracts `new_entity_type` from either the request body directly
(human-supplied via the SME UI) or from `fields_to_rewrite.entity_type`
on the LLM-produced review (agent-supplied), and passes it through to
`apply_audit_resolution`. `RetypeTargetError` is added to
`http_server/app.py`'s exception-to-HTTP-400 mapping alongside the
existing `NoWinnerRecordError`/`UnresolvableRecordError`, so a refused
RETYPE reaches appcode as a 400 with the real reason in `detail`, not a
500.

**Deployed as `optisweep-brain-http:v4`** (ACR build `ca4`, 33s;
`az containerapp update` to revision `optisweep-brain-http--0000006`,
100% traffic). Re-ran the §23 regression check against the live v4
revision post-deploy to confirm the latency fixes and the new RETYPE
code coexist without interference: cold `/context/retrieve` (AGV query)
= 39.6s, `excerpt_count: 15` (matches the known-good baseline exactly);
warm same-query = 1.82s; warm different-query = 1.73s,
`excerpt_count: 0` (a well-formed empty result — "conveyor jam sensor
fault detection" genuinely isn't represented in this AGV/tote-sortation
corpus, confirmed by inspecting the response shape, not an error).
Confirmed the resolve route's error handling is live and correctly
wired (a resolve against a nonexistent review id returns a real 404 via
`ReviewNotFoundError`, not a 500 — proves the `RetypeTargetError` import
didn't break the existing exception chain). Did **not** exercise the
RETYPE happy path against real production data: `GET /brain/v1/reviews?
status=open` returned zero open reviews at deploy time, so there is no
real SME-pending case to safely apply one against, and manufacturing a
synthetic review just to test would mean writing fake data into
production for no real gain — the corpus-scale test above already
validated the identical code path against a full real-data copy. The
next real RETYPE this system executes will be the first genuine one,
against a real open review.
