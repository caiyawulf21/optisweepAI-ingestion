# How the OptiSweep Brain is built

This documents the actual process used to migrate existing ingestion output into
`brain/` records, the decisions made along the way (including bugs found and
fixed against real data), and what remains deliberately deferred. It exists so
a future agent or tool — the Foundry-backed ingestion agent described in
`brain/DESIGN_RATIONALE.md` §11 — can be built
from this process instead of rediscovering it.

Everything below reflects `brain/migration/` as it stands after the corrected
run. Numbers are from the real, current corpus, not estimates.

---

## 1. Why a migration exists at all

The Brain (`brain/schemas/`: `EvidenceUnit`, `Entity`, `Claim`, `Relationship`,
`Capability`) is new. The existing pipelines
(`operationalknowledgeingestion/`, `incidenceknowledgeingestion/`) have been
producing knowledge for months in their own stage-specific JSON shapes. The
migration's job is to read every one of those existing outputs and produce
Brain records that are:

- **Lossless** — every field in the source output lands somewhere in the
  Brain, either as structured knowledge (Entity/Claim/Relationship/
  Capability) or as verbatim `EvidenceUnit.content.structured_payload` when
  Part 1's schemas don't yet model that structure (see §5).
- **Convergent** — the same real-world thing (a screen, a database table, a
  capability) resolves to the *same* Brain entity regardless of which source
  mentioned it, per Part 1 §9.
- **Standardized** — every source, operational or incident, produces the same
  five record types through the same promotion logic. No source gets a
  thinner or ad hoc treatment.

## 2. Pass order and why it matters

```
Pass 0: docs/ontology/catalogs/  →  brain/migration/migrate_ontology_catalogs.py
Pass 1: operationalknowledgeingestion/data/output/<source>/  →  brain/migration/migrate_operational_source.py
Pass 2: incidenceknowledgeingestion/data/output/incidents/<case>/  →  the Brain ingestion agent (2026-09-08 direction: NOT a migrate_incident_case.py script — see AGENT_DESIGN_NOTES.md §1)
```

**Pass 0 runs first and is authoritative.** `docs/ontology/catalogs/` (14
surface catalogs + a 26-entry capability catalog + a WCS SQL catalog) is
hand-curated and already ontology-shaped — it defines canonical entities
(`entity:system:wcs`, `entity:database_table:robotlocationdatabasemodel`, …)
and capabilities before any noisier per-source extraction runs. Every later
pass resolves against this registry first, so "WCS" mentioned in a training
video and "WCS" mentioned in the manual converge onto the one entity Pass 0
already created, instead of each source inventing its own.

**Passes 1 and 2 share one running `EntityRegistry` and one capability
dict**, threaded through `--registry-in/--registry-out` and
`--capabilities-in/--capabilities-out` CLI flags on each script. Each source
is migrated as a separate CLI invocation (not one big all-sources script) so
a single source's output can be inspected and re-run independently — this
mattered in practice (see §6).

### 2.1. How the two lanes actually differ, today and going forward

The user asked directly for this distinction after seeing Pass 0 and Pass 1
merge into one undifferentiated pool of entities. What's true today, and
what isn't yet:

**What's true today: one shared graph, no marked lane.** Once migration
finishes, a Brain record carries no field saying "I came from a hand-curated
catalog" vs. "I came from a training video." `source_refs` still trace back
to the originating `EvidenceUnit` (and from there to `source_type` —
`"ontology_catalog"` vs. `"manual"`/`"training_video"` — so the distinction
*is* reconstructable), but nothing in `Entity`/`Claim`/`Capability`
prioritizes or filters on it. Concretely, of 2,178 entities: 13 exist
*only* because of the catalogs, 2,072 exist *only* because of the 5
operational sources, and 93 are touched by both — a catalog-seeded entity
(e.g. `entity:system:wcs_sql`) that an operational source later added
evidence to, exactly per Part 1 §9's design ("a later source strengthening
an earlier one is the normal case").

**What actually differs in practice, even without a marked field:**

- **Authority of origin, not enforced but implicit in the numbers.** The 13
  catalog-only entities and all 31 capabilities are hand-curated —
  `docs/ontology/catalogs/*.json` was written and reviewed by people who
  know the product, with `when_to_use`/`not_for`/`support_contract` fields
  that encode real operational judgment (§6.5). The 2,072 operational-only
  entities are LLM extraction output from Stage 4 context records, unreviewed.
  Right now the Brain treats a `Capability`'s `support_contract.forbidden_capabilities`
  (hand-authored policy) and an operational-lane `Claim`'s `has_related_fact`
  (LLM-extracted, unreviewed) with equal weight — nothing distinguishes
  "this is governed policy" from "this is one source's observation." That
  asymmetry is real and, per the original OptiSweep Brain design doc's §12
  ("assistant responses, raw chat speculation, and a one-off incident must
  never become production guidance by themselves — they are learning
  evidence until corroborated and approved"), is exactly the gap the
  eventual review/promotion workflow is meant to close. Nothing in Part 1
  closes it yet — there is no `validation_status`/`authority` field on any
  record (deliberately deferred, §8/§14).
- **Density and structure.** Catalog capabilities carry `sql_field_notes`,
  `observables`, `support_contract` — structured, governance-grade detail.
  Operational-lane content is almost entirely `EvidenceUnit`/`Claim` free
  text (`has_detail`, `has_related_fact`, `observed_in_artifact`) — real,
  source-backed, but unstructured. This is why §6.6's catalog backfill wrote
  operational discoveries into catalog `evidence[]` arrays rather than
  trying to force them into `when_to_use`/`support_contract` shape: the
  operational lane's raw material isn't there yet, and manufacturing that
  structure from free text would be fabrication, not extraction.
- **What each lane is capable of contributing.** The catalogs define the
  vocabulary (what a "capability" is, what surfaces exist, what a symptom
  means) — they set the ontology's *shape*. Operational sources populate and
  extend that shape with volume and specific, situated facts (the design
  doc's §5: "operational sources contribute 'what should happen'; incidents
  and training material add 'what actually happened'"). A capability like
  `robot_location_state` was only writable at all (§6.6) because an
  operational source's `applies_to` scope tags supplied the missing SQL
  model/field detail a catalog author hadn't documented yet — the lanes are
  complementary, not redundant, even though they're unmarked in the data.

**What would need to change to make this a real mechanism, not just an
observation** (not built — this is the "decide together" half of the
question): a `source_authority` or `validation_status` enum on `BrainRecord`
(catalog-derived / SME-reviewed / operational-lane-unreviewed), precedence
rules for when an operational-lane `Claim` conflicts with a catalog
`Capability`'s stated policy, and a retrieval-time filter that can prefer
governed knowledge over raw extraction when both exist. All three are
explicitly named as deferred in §8/§14 — anchored to a review/promotion
workflow that isn't part of Part 1's scope, and building it ahead of that
workflow risks encoding governance rules with no governance process behind
them yet.

## 3. The record-type mapping (operational lane)

| Existing stage output | Brain record | Notes |
|---|---|---|
| Stage 1 `pages[]`/`sections[]` (manual) | `EvidenceUnit(document_section)`, `is_verbatim: true` | Empty-text pages/sections are skipped, not stubbed. |
| Stage 1 `training_video_slide_segments.json` (training video) | `EvidenceUnit(training_video_segment)`, `is_verbatim: true` | **Not** the synthesized `stage_2_source_artifacts/source_bundle.json` — that file re-strings the same 80 segments into a pages/sections shape purely for Stage 4/5 tooling compatibility; migrating both would duplicate every piece of evidence. `video_start_seconds`/`video_end_seconds` map to the real `EvidenceLocator` fields. |
| Stage 2/3 artifact `caption_text` + `nearby_text` | `EvidenceUnit(image_or_ocr_region)`, `is_verbatim: true` | The un-enriched, literal surrounding text. |
| Stage 3 artifact enrichment (`detailed_description`, `short_description`, `tags`, `what_to_look_at`, `enrichment_notes`) | `EvidenceUnit(image_or_ocr_region)`, `is_verbatim: false`, **plus** promoted `Entity`/`Claim` (see §4) | This is Azure Computer Vision + Azure OpenAI vision-model output — see §4 for why it must not stay evidence-only. |
| Stage 4 `operational_context[]` (12 `context_type` values) | `Entity` (type chosen by `CONTEXT_TYPE_TO_ENTITY_TYPE`) + `Claim(has_detail)` for the record's `details` text | `title` is the entity name (specific, per-record). `applies_to` becomes `Relationship(applies_to)` to a broader system entity — **never** the entity's own name (see §6, bug #1). |
| Stage 5 `runbook_candidates.json` | `EvidenceUnit(sme_note)`, whole record in `structured_payload` | No Procedure schema exists yet (Part 1 §14 defers it); the full candidate is preserved so Part 2 has a lossless input. |
| Stage 6 `finalized_runbooks/*.json` | `EvidenceUnit(sme_note)`, whole record in `structured_payload`, plus `Relationship(uses)` to each `capability_tags` entry | Same reasoning — steps/prerequisites/etc. stay in `structured_payload` until a Procedure schema exists. |
| Stage 8 `relationship_links.json` | `Relationship` | `link_type` → `RelationshipType` via `LINK_TYPE_TO_RELATIONSHIP_TYPE`. Only links whose both endpoints resolve to an already-migrated record become live relationships (see §6, bug #2 — stale link files are regenerated, not silently dropped). |

## 4. Promoting vision/OCR content into the graph (not just evidence)

Azure Computer Vision + Azure OpenAI vision enrichment (Stage 3) produces
real content about *what an image shows*, not just where it sits in a
document. The first version of this migration captured that content as
`EvidenceUnit` only — inert, cited by nothing. That is a real gap: a photo's
`what_to_look_at: ["Tipper (Item 1)", "Chute (Item 2)", ...]` is describing
actual OptiSweep components, and leaving it as unlinked evidence means it
never contributes to entity/relationship reasoning the way text-derived
context does.

The fix, in `migrate_artifacts()`:

- **Numbered diagram callouts** (`"Tipper (Item 1)"`, matched by
  `_split_item_label()`'s `"(Item N)"` suffix pattern) are treated as an
  unambiguous named component. They become `Entity(component)` +
  `Relationship(displays)` from the artifact's evidence unit to that entity.
- **Unlabeled observations** (`"Foot brake position (engaged/disengaged)"`,
  `"Stacklight color state (Solid Red, Solid Green, ...)"`) are **not**
  promoted to entities — an observation is not a new named thing. They become
  `Claim(observed_in_artifact)` instead, with the artifact's subject entity
  as the claim subject.
- **`detailed_description`** becomes `Claim(has_visual_description)`.
- **`tags`** deliberately do **not** auto-generate `Capability` relationships.
  A first attempt matched tag words against capability-slug words (e.g. tag
  `"tipper"` → `capability:tipper_station_fault` because both contain
  "tipper"). This is keyword overlap, not semantic understanding — a generic
  photo of tipper hardware is not evidence that photo supports a
  *fault-diagnosis* capability specifically. That logic was removed. `tags`
  remain available verbatim in `EvidenceUnit.content.structured_payload` for
  a real semantic-matching step later (§8).

This same distinction (numbered-label → entity, free-text observation →
claim, no keyword-based capability inference) should be the template for any
future source with vision-derived content, including incident screenshots
(Pass 2 — agent-executed per AGENT_DESIGN_NOTES.md §1, not a script; this
remains the right judgment principle regardless of who/what applies it).

## 5. What gets staged instead of modeled

Part 1's five schemas are deliberately narrow (architecture lock §1.7, §14).
Content that doesn't fit is never dropped — it is preserved whole inside
`EvidenceUnit.content.structured_payload`, so it survives losslessly and
Part 2 (once a Procedure/Playbook schema is designed) has a real input to
build from instead of needing to re-derive it from the original pipeline
output a second time. This currently covers:

- Stage 5/6 runbook candidate and finalized-runbook records (steps,
  prerequisites, `roles_and_responsibilities`, `visual_references`, etc.)
- (Planned, Pass 2) incident playbook candidates: `nodes[]`, `branch_hints[]`,
  `escalation_gates[]`, `validation_gates[]` — full graph structure
- (Planned, Pass 2) incident KPI/timing fields: `kpi_tracking`,
  `resolution_time`, `downtime_minutes`

## 6. Bugs found by running against real data (and their fixes)

This migration was **not** designed correctly on the first pass for every
case — real data surfaced real defects, each fixed before scaling out. This
list matters for a future agent: these are the failure modes to specifically
test for, not hypothetical concerns.

1. **Entity-name collapse (the significant one).** The original entity-naming
   logic used `applies_to[0] or title` as the entity name. `applies_to` is a
   broad scope tag (e.g. `"OptiSweep system"`) shared by dozens of unrelated
   context records — 30 completely different manual sections ("Document
   Structure", "Warranty Service Requirements", "Abbreviations and Acronyms",
   …) all collapsed onto **one** `entity:system:optisweep_system` node.
   Fixed by using `title` (the specific, per-record name) as the entity name,
   and converting `applies_to` into `Relationship(applies_to)` edges to the
   broader system entity instead. This alone changed operational-lane totals
   from 694→2,537 entities and 784→1,660 claims — the earlier numbers were
   wrong, not just conservative.
2. **Stale `stage_8` relationship links.** Two of five operational sources
   (`manual_optisweep_om_v3`, `training_video_day1`) had `relationship_links.json`
   generated against an *older* version of Stage 4/5/6 output — Stage 6 had
   been re-run/pruned afterward without re-running Stage 8, so ~98% of links
   referenced IDs that no longer existed. Root-caused via each source's
   `relationship_linking_report.json` (`record_counts` at generation time vs.
   current on-disk counts) rather than assumed. Fixed by re-running the
   existing deterministic `operationalknowledgeingestion/scripts/stage8_link_relationships.py`
   for the two stale sources — not by loosening the migration's resolution
   logic to tolerate dangling references.
3. **UTF-8 BOM.** Several stage output files are BOM-prefixed; a plain
   `utf-8` read raised `JSONDecodeError`. Fixed by reading with
   `utf-8-sig` everywhere in `brain/migration/common.py`.
4. **Windows `MAX_PATH`.** One finalized-runbook filename (276 chars)
   exceeded Windows' 260-char path limit and raised `OSError` on open.
   Fixed with a `\\?\` extended-length-path fallback in `load_json_dir()`
   rather than silently skipping the file.
5. **Missing capability registry threading.** `Capability` records referenced
   by `Relationship(uses)` (from `capability_tags`) were never actually
   passed into `validate_batch()`'s known-ID set, and a `capability_tags`
   value not already in Pass 0's 27 capabilities had no creation path at
   all — it just produced a relationship to a nonexistent ID. Fixed by
   threading a shared `capabilities: dict[str, Capability]` through the
   source migration (mirroring the existing `EntityRegistry` pattern) with a
   real `_get_or_create_capability()`.
6. **Tag→capability keyword matching (see §4).** Built, inspected, found to
   over-claim semantic relevance, and removed rather than shipped as a
   false-precision heuristic.
7. **Entity naming collapsed distinct records onto one node.** `applies_to`
   (a broad scope tag shared by dozens of records) was used as the entity
   name instead of the record's own `title` — 30 unrelated manual sections
   all collapsed onto one `entity:system:optisweep_system`. Fixed by using
   `title` as the name and modeling `applies_to` as an `APPLIES_TO`
   relationship instead (see §6.5 for the fuller writeup — this was found
   and fixed in the same session as the capability-detail and entity-merge
   work below, prompted directly by the user noticing per-source entity
   counts looked too low).
8. **`Capability` only captured 8 of the ~23 fields on a real source card**
   (`when_to_use`, `not_for`, field-level SQL purpose, `observables`, the
   full `support_contract` ground-truth data were all silently dropped).
   Unlike Stage 5/6 runbooks, this content was never staged as a fallback
   either — a real gap in applying the "nothing is dropped" rule
   consistently. See §6.5.
9. **Entity/capability re-encounters only ever merged `source_refs`.** A
   second source describing an already-known entity never enriched its
   description, aliases, or payload — the entity accumulated citations but
   never got more complete. See §6.5.

## 6.5. Capability schema extension, generic merge, and entity consolidation

This was a second corrective pass, prompted directly by the user asking two
questions after reviewing the corpus: "how does the ontology connect to the
operational sources?" and "the ontology doesn't have enough capability
detail — are we overgeneralizing and losing information?" Both were
confirmed as real defects, not just areas for future polish, by inspecting
actual output rather than re-explaining the design.

**Capability schema extension** (`brain/schemas/capability.py`): added
`when_to_use`, `not_for` (list[str]), `sql_field_notes` (list[SqlFieldNote]:
table entity id + field + purpose — the field-level "why" that bare
`target_entity_ids` names lose), `api_checks` (list[str]), `observables`
(healthy/degraded/escalate signal lists), and `support_contract`
(`SupportContract`: diagnostic vs. control surface entity ids, required-
evidence and forbidden capability ids, preferred surface — this is the exact
SQL/WCS "ground truth" governance data the original OptiSweep Brain design
doc's diagnosis said was missing from the pipeline). All fields are
additive with defaults; existing fixtures/tests needed no changes.

Two of `SupportContract`'s referenced capability slugs
(`optisweep_service_restart`, `ignition_restart` — named as *forbidden*
capabilities by other cards but never given their own card) had no
`Capability` record to point at. Fixed by creating minimal stub records for
any capability slug referenced-but-undefined in the source catalog, so a
`SupportContract` reference always resolves to a real record.

**Generic "grow richer, never regress" merge** (`brain/migration/merge.py`,
new module): `merge_record(existing, incoming_fields)` unions list fields,
recurses one level into nested pydantic sub-models (so `Observables`,
`SupportContract` etc. merge field-by-field rather than being replaced
wholesale), and fills an empty/None scalar field from an incoming value
without ever overwriting a populated one. Both `EntityRegistry.get_or_create`
and `CatalogMigration._get_or_create_capability` were rewritten to use it
instead of only merging `source_refs`. One correctness detail worth keeping
in mind if this is extended later: `model_copy(update=...)` does not
re-validate, so a raw dict merged into a list of typed sub-models (e.g.
`Capability.sql_field_notes`, `Entity.payload.key_fields`) would silently
stay an unvalidated dict inside an otherwise-typed list — `merge_record`
works around this by re-running the *whole* merged state through
`model_validate` rather than `model_copy`, at both the top level and inside
the nested-submodel branch. `Entity.payload`'s field annotation also needed
`pydantic.SerializeAsAny[EntityPayload]` — without it, `model_dump_json()`
emitted spurious `PydanticSerializationUnexpectedValue` warnings because the
serializer tried each `EntityPayload` Union member against the runtime
object in declaration order before reaching the correct one; the dumped data
was actually fine, but the warning was real noise worth eliminating.

**Entity consolidation** (`brain/migration/consolidate_entities.py`, new
script, run after a full Pass 1): merges near-duplicate `system`/`component`
entities created when different sources name the same real thing slightly
differently (`"OptiSweep WCS"` / `"Fortna WCS"` / `"WCS"`). Deliberately a
separate, inspectable post-hoc pass rather than built into
`EntityRegistry.resolve()` — a wrong merge made silently mid-migration has
no review step and permanently loses a distinction; a dry-run report you can
read before trusting it does not.

The matching rule is narrow on purpose: two entities of the *same*
`entity_type` merge only when their names produce an *exactly equal* token
set after stripping the two known brand words (`optisweep`, `fortna`) — not
substring overlap, not a similarity score. Two guards were added after the
first version produced wrong merges against the real corpus:

- Any name containing a digit is excluded from matching entirely. Token-SET
  equality is blind to order, so `"page_2_image_1"` and `"page_1_image_2"`
  would otherwise collide onto the identical token multiset despite being
  different artifacts — a real false-positive merge found in the first
  dry-run.
- A token set reduced to a single *generic* word (`system`, `module`,
  `subsystem`, `service`, `software`, `robot`) is excluded — these are the
  entire remaining name for many genuinely different things once brand words
  are stripped (`"OptiSweep system"` the whole platform is not safely the
  same as every other bare `"system"` mention). A single *specific*
  acronym-shaped word (`"wcs"`) is not excluded — that asymmetry is exactly
  what makes `"OptiSweep WCS"`/`"Fortna WCS"` mergeable while a bare
  `"system"` is not.

Canonical-survivor selection prefers the longest name, but a second guard
(`_looks_garbled`) rejects a name whose words substantially repeat
themselves (a duplicated-extraction artifact, e.g. `"...control system bag
out"` appended after `"...system bag out control"`) so a garbled long name
never wins over a clean shorter one just for being longer.

Result on the current corpus: 10 merges (`Fortna WCS`→`OptiSweep WCS`, both
tipper-side variants, `Tipper Subsystem`, `tipper/operator stations`,
`Zone configuration`, `Tote management`, one garbled bag-out-control
duplicate). **Running this after Pass 1 leaves the just-consolidated
`entities.json` referenced by stale `Relationship`/`Claim`/`Capability`
files from the pre-consolidation Pass 1 run** — the fix is re-running every
Pass 1 source migration one more time (cheap; each is idempotent and
re-derives its records fresh from the current registry), not hand-patching
IDs in place. `consolidate_entities.py` writes an
`entity_consolidation_remap.json` alongside its output specifically so this
dependency isn't missed.

## 6.6. Writing operational-lane discoveries back into docs/ontology/catalogs/

Sections 1–6.5 only describe information flowing INTO the Brain from the
catalogs (Pass 0 seeds the registry; Pass 1 resolves against it). The user
asked directly whether operational-lane discoveries flow back OUT into the
hand-curated catalog source files themselves — they didn't, by design, since
the catalogs are read live by `shared_pipeline_stages/ontology_rag.py` for
Stage 5/6 mini-RAG and a wrong write there has a different blast radius than
a wrong write into `brain/data/local/`.

**Process**: given the scale (2,423 of 2,529 entities had zero catalog
provenance), a review report was generated FIRST (published as an artifact,
not written to disk) rather than writing anything blind. The report covered:
one real data-quality bug (`site_stoppage`, a failure pattern, was listed as
a `capability_hint` in `building_acb_hmi_catalog.json`'s `acb_area_status`
activity — inconsistent with its correct usage as `related_failure_patterns`
in 7 other catalog files; this had caused Pass 0 to create a spurious
`capability:site_stoppage` stub duplicating the correctly-modeled
`entity:symptom:site_stoppage`); 6 capability slugs referenced only via
other cards' `support_contract.required_evidence`/`forbidden_capabilities`
but never given their own card; and operational-lane claims matched against
each catalog's own aliases/objects/screens_or_views.

**After user approval to act on all of it:**

1. Fixed the `site_stoppage` bug directly in `building_acb_hmi_catalog.json`
   (removed from `capability_hints`, added to `related_failure_patterns`
   alongside the file's existing `hospital_diversion` entry, which uses the
   same capability/symptom name-overload pattern legitimately and consistently
   elsewhere — that one was left alone).
2. Wrote two new capability cards into `capability_catalog.json` —
   `robot_location_state` and `tote_association_state` — using real detail
   already present in *other* cards' `support_contract.backend_mappings`
   (`device_roster_state` and `tote_lifecycle_state` respectively already had
   fully fleshed-out SQL model/field mappings for these concepts; they were
   lifted into their own first-class cards rather than invented). The
   remaining 3 of the 6 referenced-but-undefined slugs
   (`optisweep_service_restart`, `ignition_restart`, `rms_map_reposition`)
   were left as pure references — there is no real evidence anywhere to write
   a card from, only their names as forbidden/required-evidence gates on
   other capabilities, and writing placeholder description text for them
   would misrepresent how well-understood they actually are.
3. Backfilled `evidence[]` arrays (additive only — never touched
   `screens_or_views`/`objects`/capability lists, so no existing schema
   contract Stage 5/6 mini-RAG depends on changed shape) across all 12
   surface catalogs plus `wcs_sql_catalog.json`, in two passes run as
   one-off scripts (not checked into the repo — they were a manually
   reviewed, run-once backfill against this specific corpus snapshot, not a
   repeatable tool; the logic is documented here so it can be rebuilt
   properly, as real tooling, if this needs to run again): (a) automatic
   alias-matching against each catalog's existing
   `aliases`/`objects`/`screens_or_views`, with a cross-surface name-hint
   exclusion list added after the first dry run showed
   `tipper_hmi_catalog.json`'s broad aliases (operator station, HMI, AGV)
   catching content plainly named after a different surface (`"Hospital HMI
   2.1 Manual Control Screen"`, `"ACB System Overview Screen Legend"`); and
   (b) a hand-curated name→catalog mapping for the ~375 candidates the
   automatic matcher missed entirely, built by reading the full name list
   rather than adding more keyword heuristics — deliberately left ~120 of
   those unmapped (pure narrative/meta content, or too vague to place
   confidently) rather than force a placement.
4. Re-ran the full rebuild order from §9 (Pass 0 → all 5 sources → consolidate
   → all 5 sources again) so the Brain's local records reflect the enriched
   catalogs. Corpus-wide `validate_batch` still zero errors afterward.

**Net effect**: catalog `evidence[]` entries grew from 195 to 710 across the
17 files under `docs/ontology/catalogs/`; `capability_catalog.json` grew from
26 to 28 real cards (plus 3 remaining pure stub references, down from 6 after
the `site_stoppage` fix removed one spurious stub entirely).

**What this means for a future extraction agent**: the matching logic used
here (alias overlap + a curated exception/exclusion list) is exactly a
placeholder for real semantic matching. It works at this corpus's scale
because a human read every unmatched name before mapping it — that does not
scale to a live ingestion pipeline processing new sources continuously. This
is the concrete shape of the "semantic tag/description → Capability
matching" gap already named in §8 below, now with a worked example of what
doing it by hand looked like and why it doesn't generalize.

## 6.7. Entity-vs-claim audit and the two-pass shape check

Prompted by the user spotting one real example directly
(`entity:component:go_to_function_recovery...`, name reading as a full
scenario sentence, description opening "The training slide presents the
Go-to function as..."). Two separate defects were in that one entity, and
both turned out to be systemic rather than one-off:

1. **Category error**: some Stage 4 context records describe a *process* or
   *behavior* ("the WCS communicates with the sorter PLC to control
   diversion") rather than naming a real thing. Modeling that as its own
   `Entity` produces an orphaned node nothing else references — the fact is
   stranded instead of being attached to the real entity (WCS) it's actually
   about.
2. **Evidence-reference leak**: `description` fields were copied verbatim
   from Stage 3/4 LLM output, which sometimes frames itself as reporting
   what a source said ("The training slide presents...") instead of stating
   the fact directly.

**The audit.** The original hypothesis was that defect #1 was concentrated
in two context types (`operation_reference`, `troubleshooting_reference`).
An audit of all 2,529 entities against the test *"is this a name someone
would look up, independent of any specific claim about it?"* proved that
wrong: tracing the confirmed mis-modeled entities back to their source
records showed those two types accounted for only 25% of the problem — the
rest was spread across nearly every context type, plus entities created
outside Stage 4 context records entirely (the vision-promotion path). **The
boundary cannot be drawn at the context_type level — it has to be a
per-record content check.** The audit sorted every entity into four tiers:
119 CLEAR_CLAIM (unambiguous), 47 AMBIGUOUS (heuristic couldn't call it — the
user reviewed these directly and confirmed all 47 are claims too), 96
description-only cleanup, 2,267 correctly modeled.

**The fix, `brain/migration/entity_shape.py`** (new module,
`is_claim_shaped()` + `strip_source_reference_leak()`): a per-record
heuristic — claim-verb constructions ("is used to", "depends on", "applies
to"), verb-first/imperative names ("Confirm...", "Add..."), and
sentence-length names (≥9 words) mark a claim; short noun-phrase names don't.
Wired into `migrate_operational_source.py`'s `migrate_operational_context()`
as a genuine two-pass split: named (entity-shaped) records are migrated
first so their entities exist in the registry, then claim-shaped records are
migrated in a second pass, resolving their `applies_to` values against that
now-populated registry and attaching their content as a `Claim` on whatever
real entity resolves — never fabricating a subject. When nothing resolves,
the record's content stays fully preserved as `EvidenceUnit`; it just isn't
promoted to a structured `Claim`.

Fixing this in the general migration logic (not just relabeling existing
data) dropped CLEAR_CLAIM-shaped entity creation from 119 to 0 on a full
rebuild — the class of defect no longer recurs on future runs, which matters
more than fixing the existing 119 by hand would have.

**Bugs found while wiring this in**, each real and each fixed:

- `_migrate_claim_shaped_context_record` didn't set `raw_id_to_brain_id` for
  a context record when its `applies_to` resolved to nothing, so a Stage 8
  `relationship_links.json` entry referencing that `context_id` would
  silently fail to resolve — a real regression (stage_8 unresolved-link rate
  on `training_video_day1` jumped from ~0% to 8.5%) caught by re-checking
  that specific number after the first version of the fix, not assumed
  fixed. Corrected by mapping the context_id to the record's primary
  `EvidenceUnit` id in that case instead of leaving the mapping unset.
- The `applies_to` → `APPLIES_TO` relationship path (a different code path
  from record-title entity creation) had no `is_claim_shaped()` check at
  all, so a claim-shaped `applies_to` value ("Add Robot function") still
  became its own low-quality entity even after the main fix. Fixed with the
  same check on that path.
- The vision-promotion path's `_artifact_subject_entity()` used a training-
  video artifact's raw `title` field unconditionally, which is sometimes
  garbled OCR'd slide-footer text ("Overview What is Optisweep? 3 FORTNA ALL
  RIGHTS RESERVED. CONFIDENTIAL FO RTNA") rather than a real name. Fixed to
  fall back to the artifact_id (uninformative but honest) when the title is
  claim-shaped.
- A record whose `applies_to` list included an *alias* of its own entity
  (not just an exact title match — the existing self-skip check only caught
  exact-string title matches) produced a meaningless self-referential
  `APPLIES_TO` relationship (`entity X applies_to entity X`). Found via one
  of the 47 AMBIGUOUS entities resolving "to itself" during reclassification
  — 18 such edges existed across the corpus. Fixed by comparing resolved
  entity ids, not raw strings, before creating the relationship.

**Reclassifying the 119 + 47 = 166 already-created entities**
(`brain/migration/reclassify_ambiguous_entities.py`, new, one-time script,
not part of the regular rebuild): for each, find its own existing
`APPLIES_TO` target (created by the normal migration path before the entity
was flagged) and use that as the new `Claim`'s subject; remove the entity;
drop any `Relationship` that referenced it (repointing to an arbitrary
replacement isn't correct for every relationship type, so those edges are
simply dropped — the content survives as the new Claim, not as a dangling
relationship). All 166 resolved to a real, distinct subject entity.

**Rewriting the 96 leaked descriptions**: `strip_source_reference_leak()`
only safely handles "The X states/notes/confirms that Y" → "Y" (dropping the
frame leaves a complete sentence). It deliberately does not attempt "The X
describes Y as Z" → "Y is Z", since that needs restructuring around Y and Z
that a regex cannot do without risking a grammatically broken result — and
in practice this pattern dominated the real corpus (0 of the last 82 were
safely auto-rewritable). Per explicit instruction, those 82 were rewritten
by hand — read each description, restate the fact directly, preserve every
piece of real content, verified none dropped information. No script exists
for this step; it was direct editing, documented here as the record of what
was done and why a mechanical version wasn't used.

**Net effect of §6.7 on the full rebuild**: entities 2,529 → 2,219 (from the
two-pass shape-check fix alone, before any reclassification) → 2,184 (after
reclassifying the 35 that survived the automatic check — 12 of the original
47 AMBIGUOUS resolved automatically once the root-cause fixes landed and
consolidation ran again); CLEAR_CLAIM and AMBIGUOUS tiers both at 0 on
re-audit; DESC_NEEDS_CLEANUP 96 → 6 (the remaining 6 are `LEAK_RE` false
positives — legitimate sentences that happen to contain the word "manual" or
"segment" as real content, e.g. "on page 209 of the manual" — verified by
hand, not further rewritten).

## 6.8. Duplicate and thin-entity audit

Prompted by the user asking to check for duplicates across the whole
registry and flag entities with little source_refs/description/payload.

**Duplicates.** The obvious signal — two entities sharing an identical
`source_refs` set — turned out to be a weak one on this corpus: Pass 0
attaches the same small `evidence[]` pool from a catalog file to every
record derived from that file, so 41 groups of entities shared identical
ref sets while being genuinely unrelated (27 distinct WCS API endpoints all
cite the same 38 catalog evidence snippets; `role:operator`/`role:l1_support`/
`role:l2_support` share a snippet that names all three). Name-overlap alone
was equally unreliable in the other direction — `"AGVs with totes"` and
`"AGVs without totes"` share every word but one and cite the same evidence
while being opposite states, not duplicates.

**One real, confirmed, fixed duplicate class**: `tipper_hmi_catalog.json`
lists each VISU_* screen in both `screens_or_views[]` and `objects[]` under
the same catalog-internal `id` (the `objects[]` entry even carries `"kind":
"visu_screen"`, marking it as a cross-reference rather than a distinct
object). The migration built one entity from each array, producing an
`entity:ui_screen` and an `entity:component` with the same name and
identical 159-item source_refs — 6 pairs (VISU_MCP_DUAL, VISU_DATA,
VISU_MANCONTROL, VISU_MDS, VISU_IO_DIAG, VISU_ALARM). Fixed in
`migrate_surface_catalog()`: `screens_or_views[]` is processed first,
building a catalog-id → entity map; when an `objects[]` entry's id is
already in that map, the existing `ui_screen` entity is reused instead of
creating a second `component` entity for the same real screen.

**7 genuine near-duplicate candidates, not auto-merged**: pairs sharing an
identical (small, 2–3 item) source_refs set AND clearly overlapping names —
e.g. `component:"Get Zone Configuration function"` and
`system:"Get Zone Configuration"`, both built from the exact same two
context records, most likely the same real capability named once from a
record's own title and once from a different record's `applies_to` scope
tag. Reported (see the published Duplicate & Thin Entity Report artifact)
rather than merged automatically — a wrong cross-`entity_type` merge here
has no clean undo the way `consolidate_entities.py`'s narrow same-type,
exact-token-match rule does, and 7 pairs is small enough for a direct
decision rather than a heuristic.

**Thin entities**: 1,138 of 2,178 (52%) have exactly 1 source_ref, an empty
description, and an empty payload — almost entirely `system` (883) and
`component` (255). Traced to two intentionally-minimal creation paths, not a
defect: numbered diagram callouts (`"Tipper (Item 1)"` → a bare `component`
named "Tipper", by design — a labeled part in a diagram has nothing more to
say than its name and the artifact it appears in) and `applies_to` scope
tags (a system referenced once, in passing, by another record). Most carry
at least one `DISPLAYS`/`APPLIES_TO` relationship, so they are connected into
the graph, just minimal. Whether any of the 1,138 are themselves unrecognized
duplicates of a richer entity is a real open question the identical-
source_refs signal can't answer reliably at n=1 ref — flagged, not resolved.

## 6.9. Pass 0 never produced a Claim; the state-vs-action boundary

Two more findings from the user reviewing the corpus directly.

**Pass 0 emitted zero Claims, ever.** `migrate_surface_catalog()` read
`purpose` into `Entity.description` but never read `architecture_notes[]` or
`gaps[]` at all — not even flattened into text, silently dropped. Both are
real, citable assertions: `architecture_notes` ("OPC path also connects
hospital tags via Ignition") is exactly Claim material, and `gaps` (the
catalog authors' own flagged incompleteness — "hospital HMI screen
dictionary thinner than tipper, needs expansion") maps directly onto
`Claim(polarity=uncertain)`. `not_for[]` had the same problem but only for
surface catalogs — it was already read for `capability_catalog.json`.
Fixed: `architecture_notes` → `Claim(has_architecture_note, affirmed)`,
`gaps` → `Claim(has_known_gap, uncertain)`, `not_for` → `Claim
(not_applicable_to, negated)`, all on the surface's own `system` entity.
Result: Pass 0 now emits 80 Claims where it emitted 0 before.

**Every capability is named after the state it checks, not the action of
checking it.** Raised directly: is `agv_active_errors` an entity (the AGV's
error state) or a capability (an action)? Checking the actual data: the
record's `job` field ("Confirm whether AGVs/robots currently have active
error or fault state") and `role_paths` (operator/L1/L2/L3) are already
correctly human-action-shaped — only the record's *identity*
(`id`/`label`: "AGV active errors") is state-shaped, and no paired entity
for the state itself (`entity:symptom:agv_active_error`) exists anywhere in
the Brain. Auditing all 28 top-level capabilities found this is completely
systemic — **28/28, zero exceptions** — while some of the 14 surface
catalogs' own `activities[]` entries already get this right ("Check
building/ACB area status", "Confirm tipper WebVisu/OPC heartbeats"),
proving the correct shape already exists elsewhere in the same ontology and
was just never applied to the top-level capability catalog. Locked the
actual boundary: an Entity is a thing OR a state of a thing that exists
independent of anyone checking it; a Capability is something a human
(operator/L1/L2/L3) does to diagnose/verify/act on that state, connected to
it by `Relationship(VERIFIES)` — never a replacement for the state entity.
Reported (not fixed) — see the published State vs. Action Boundary Audit
artifact. The fix needs three things per capability: create the missing
state/symptom entity, re-identify the capability around its verb, and link
them with `VERIFIES`. Explicitly deferred to LLM-assisted judgment rather
than another regex heuristic — the audit's own PascalCase/verb-prefix
classifier already misfired on `"Apidog — X"` labels from an em-dash
alone, which is exactly the kind of brittleness a bigger rule set doesn't
fix.

**Direction going forward, stated explicitly by the user**: further
investment in migration-script precision (deterministic stage-output
parsing) is de-prioritized. Production Brain records will most likely come
from LLM output, which does not need to trace back to a specific stage-4/5/6
JSON shape the way the current migration scripts assume. Schema and
architecture decisions from here should be designed around "what would an
LLM extraction call produce" rather than "what does this specific upstream
JSON field look like" — see §10 (production runtime picture, added below)
for how this reframes the Pass 0/1 migration scripts' role once this
system is live.

## 6.10. Fixing the state-vs-action problem: judged pairings, not a bigger rule set

Completes the fix reported (not applied) at the end of §6.9, per the user's
explicit instruction: *"do a full audit and change as needed, no hardcoding
or regex but with your brain. LLM changes, document all rules and decisions
in the agent decision notes."*

**Process.** All 27 capabilities that needed fixing (of the 28 total — see
below) were read individually, in full: `id`, `label`, `job`, `description`,
`when_to_use`. Each was judged against the Entity/Capability boundary locked
in §6.9 and `brain/AGENT_DESIGN_NOTES.md` §2. This produced
`brain/migration/capability_state_pairings.py`'s `PAIRINGS` dict — 28
hand-authored entries (one per real capability), each recording:
`state_entity_type` (state vs. symptom — judged per capability, not derived
from a keyword), `state_entity_name`, the capability's corrected verb-first
`new_capability_id_suffix`/`new_capability_label`, its corrected
`capability_kind`, and whether the capability-to-state relationship is
`verifies` or `controls`. The module docstring documents this is not a
mechanical transform.

**Finding: 25 of 27 are pure verification capabilities** ("confirm whether X
is true"). **2 are different in kind, not just naming**:
- `rms_soft_stop` ("Pause/resume AGVs via RMS soft stop") *controls* a state
  (whether the fleet is paused) rather than checking it.
- `agv_physical_recovery` ("Coordinate on-site AGV add/remove/bump
  recovery") is a recovery action that resolves a symptom, not a check of
  one.

**A second hardcoded-heuristic bug found while reading the data, not by
auditing for it.** `CAPABILITY_KIND_BY_PREFIX` in
`migrate_ontology_catalogs.py` assigns `capability_kind` by testing whether
a capability's *slug* contains one of a fixed set of substrings
("verify"/"check"/"query"/"restart"/"recover"/"clear"), defaulting silently
to `diagnostic` otherwise. `rms_soft_stop` and `agv_physical_recovery`
matched none of them and were both silently misclassified as `diagnostic`,
despite their own `job` fields already describing a control/recovery
action in plain language. Same class of bug as the identity mismatch
itself — a keyword rule standing in for reading the record. Fixed by
judgment in `PAIRINGS` (`capability_kind: "operation"`/`"recovery"`,
`relationship_type: "controls"` for these two; `"verification"`/`"verifies"`
for the other 25). `CAPABILITY_KIND_BY_PREFIX` itself was left in place in
`migrate_ontology_catalogs.py` (Pass 0 still runs it on a fresh rebuild) —
it is overridden post-hoc by `apply_capability_state_pairings.py`, which is
why that script is now a required, permanent step of the rebuild order
(§9), not optional cleanup.

**Application** — `brain/migration/apply_capability_state_pairings.py`,
`--write` to apply (dry-run by default): for each of the 28 pairings,
creates the paired state/symptom Entity if it doesn't already exist, adds a
`VERIFIES`/`CONTROLS` Relationship from the capability's *new* id to that
entity, re-identifies the capability (new id/label/kind; old id retired),
and rewrites every reference to the old capability id elsewhere in the
corpus so nothing dangles.

**Two rounds were needed to actually get to zero dangling references** —
the first pass under-scoped "elsewhere in the corpus":
1. First run only rewrote `from_id`/`to_id` in the 5 operational sources'
   own `relationships.json` files. It missed `docs/ontology/catalogs`-derived
   relationships that point *at* a capability from the other direction —
   Pass 0's own `may_indicate` (symptom → capability) and `supports`
   (database_table → capability) relationships, which live in
   `ontology_catalogs/relationships.json` itself, not in any operational
   source. `validate_batch()` caught this immediately: 253 relationships
   with a `to_id` referencing a retired capability id.
2. Fixing that surfaced a second gap: `Capability.support_contract`'s own
   `required_evidence_capability_ids`/`forbidden_capability_ids` fields are
   capability-to-capability references that `validate_batch()` does **not**
   check (it validates Relationship endpoints, not arbitrary id-list fields
   inside a record's payload) — so these 27 stale references would have
   silently shipped without complaint. Found by explicitly grepping
   `support_contract` for old capability ids after the relationship fix,
   not by validator output.

Both gaps are now closed in `apply_capability_state_pairings.py` itself
(it remaps `ontology_catalogs/relationships.json` in place before
combining it with the newly-created relationships, and separately remaps
every capability's `support_contract` id lists), and the script was made
correctly idempotent for this purpose: even when a capability was already
re-identified on a prior run (and so is skipped for record-level changes),
its old→new id mapping is still registered so a second run still finds and
fixes any references that an earlier, narrower version of the script left
dangling. Final state: `validate_batch()` — 0 errors across the full
corpus (2,206 entities, 31 capabilities, 1,697 claims, 11,287
relationships, 3,441 evidence units); `python -m pytest brain/tests/ -q` —
23 passed; 0 stale `support_contract` references remaining.

**Lesson for the future ingestion/reconciliation agent** (also recorded in
`brain/AGENT_DESIGN_NOTES.md`): an id-rename/re-identification operation on
any record type must be treated as a corpus-wide operation, not a
local edit — it has to search every *kind* of place another record could
reference that id, including id-list fields inside a payload/sub-model,
not just `Relationship.from_id`/`to_id`. `validate_batch()` checking
Relationship endpoints only, and not payload-embedded id references, is
itself a gap worth closing before this pattern recurs at agent-authored
scale.

## 6.11. Resolving the 7 reported near-duplicate pairs

Completes item #2 of the user-confirmed audit scope, using the 7 pairs
reported (not resolved) in the published Duplicate & Thin Entity Report
(§6.8). Per the same standing instruction as §6.10 ("no hardcoding or
regex but with your brain"), each pair's actual cited evidence text and
relationships were read directly rather than trusting the report's
identical-source_refs-plus-name-overlap signal as sufficient on its own —
consistent with §6.8's own finding that the signal is weak on this corpus
(41 groups shared identical source_refs; most were false alarms).

**Root cause, confirmed identical across all 7 pairs**: a `component`
entity built from a context record's own subject, plus a bare,
empty-description `system` entity built from that SAME context record's
`applies_to` self-reference back to its own subject. Reading each loser's
relationships confirmed it carried no independent fact — only the same
`applies_to` link and duplicate evidence `supports` edges back to the very
component it was extracted alongside. This is a real duplicate (one fact
named twice), not a case needing the "different states/different things"
caution from §6.8's false-positive examples.

One pair (`Barcode Interface Application`) turned out to be a 3-way
instance of the same pattern once traced: one rich component plus two bare
system echoes from two different context records that both happened to
reference it (`entity:system:barcode_interface_application` from one
context, `entity:system:barcode_interface_exe` from another).

**One pair deliberately NOT merged**: `entity:component:tote_exchange_thresholds`
(from the manual) and `entity:component:tote_exchange_threshold_categories`
(from training video day1) both describe the same real tote-exchange-
threshold screen, but neither is a bare echo of the other — both are
independently-sourced, populated component records from two different
sources. This is a genuine but different kind of judgment call (cross-source
component merge, not the bare-echo pattern) and was left open rather than
folded into this pass without its own dedicated review.

**Applied via** `brain/migration/entity_duplicate_merges.py` (the
hand-judged `MERGES` dict, 7 winners → 8 losers) and
`apply_entity_duplicate_merges.py` (`--write` to apply): merges each loser
into its winner via `merge_record()`, drops the loser, and rewrites every
Relationship reference to the loser id across `ontology_catalogs/relationships.json`
and all 5 operational sources' `relationships.json` — applying the §6.10
lesson directly (checked whether any Claim/Capability record referenced a
loser id outside of `Relationship` before running; none did, unlike the
`support_contract` case). A relationship that would become a self-reference
after remapping (the `applies_to` link that created the loser in the first
place — winner → winner) is dropped rather than kept, since "X applies_to
X" is not a meaningful fact.

Result: 2,206 → 2,198 entities (8 fewer), 11,287 → 11,280 relationships (7
remapped-and-kept + 7 self-references dropped, net -7, across the 3 sources
that actually referenced a loser). `validate_batch()` — 0 errors.
`pytest brain/tests/` — 23 passed. Spot-checked the 3-way Barcode Interface
merge directly: description/aliases/source_refs all correctly accumulated
onto the winner, and all 3 real (non-self-reference) relationships that
pointed at a loser now correctly point at the winner.

## 6.12. Re-judging the 35+82 fixed records, plus a sample-based full-corpus read

Completes items #3 and #4 of the user-confirmed audit scope: a slower,
more deliberate second pass over the entities already reclassified/rewritten
this session, plus a representative sample across every entity_type and all
31 capabilities to surface any NEW category of problem not yet found. Done
as one continuous pass since re-reading the 35+82 naturally led into
reading their neighbors.

**Re-judging the 35 reclassified entities**: read all 35 resulting Claims
directly (subject, predicate, object text). All still read as genuinely
claim-shaped on a second pass — no reversals. One pattern worth recording:
5 of the 35 resolved to the same subject, `entity:system:optisweep_system_overview`
— checked whether this was a sign of a too-generic catch-all subject; it
isn't. That entity is a real, richly-populated, top-level "OptiSweep as a
whole system" record (69 source_refs, a full description, 14 aliases) and
is the genuinely correct subject for broad claims that don't yet have a
more specific subsystem entity to attach to — multiple claims sharing one
broad, real subject is fine and expected; it would only be a defect if the
subject itself were thin or fabricated.

**Re-judging the 82 rewritten descriptions**: read the file directly.
Quality holds up — descriptions are consistently well-formed, source-frame
correctly stripped, no content lost. One apparent defect (`FORTNA�s` in
one description) turned out to be a false alarm: the character is a
correct UTF-8-encoded curly apostrophe (U+2019); the `�` is an artifact of
this session's own terminal/console encoding, not a data problem — checked
the raw code points directly before concluding anything was wrong.

**2 more claim-shaped entities found and reclassified**, not caught by the
original review because both are typed `symptom` (outside the name-pattern
scope of the original AMBIGUOUS list): `entity:symptom:crash_example`
("An example of a crash is presented" — describes a moment in a training
video, not a checkable system state; the underlying transcript genuinely
has no further content about what the crash actually was, so there's
nothing richer to recover) and `entity:symptom:repeat_incident_avoidance_as_a_training_concept`
("recurrence avoidance is an operational concern" — a training/pedagogy
theme, not a system state). Both had the same applies_to-target shape as
the original 35. Added to `reclassify_ambiguous_entities.py`'s permanent
list (now 37 entries) rather than handled as a one-off.

**Sample-based full-corpus read**: 125 entities sampled across all 10
entity_types (oversampling the smaller symptom/state/alarm/database/role
buckets) plus all 31 capabilities read directly. Two new findings:

1. **A second, distinct duplicate mechanism**: casing/spacing collisions.
   `entity_id()` slugifies `name` without normalizing case or word-boundary
   style, so the same real thing referenced once as "GeekAgv" (PascalCase)
   and once as "geek_agv" (lowercase-with-underscore) produces two
   different ids. Found by grouping all entities of the same `entity_type`
   by a fully-normalized name (lowercase, non-alphanumeric stripped) —
   7 pairs corpus-wide. Unlike the §6.11 bare-echo pattern, there is no
   reliable "richer side always wins" rule here — which side accumulated
   real relationships depends on which spelling happened to dominate the
   source material, not on data quality, so each pair was judged
   individually by reading its actual relationships (not just the name
   match). 4 confirmed as true duplicates and merged (`geek_agv`/`geekagv`,
   `opc_comms`/`opccomms`, `sorter_sweeper`/`sortersweeper`,
   `location_dwell_activity`/`locationdwellactivity` — the last confirmed
   by reading both sides' evidence text and finding genuinely
   complementary content, not assumed from the name collision alone). 3
   deliberately NOT merged after reading their relationships — see
   `entity_duplicate_merges.py`'s docstring for the full reasoning on each:
   `exchangesortersidezone`/`exchange_sorter_side_zone` and
   `initializetote`/`initialize_tote` are both cases where the
   "loser"-looking side is actually a second, independently-cited real
   record (not a bare echo — one has 20+ of its own `supports`
   relationships), and `close_out`/`closeout` turned out on inspection to
   describe genuinely different things (an action/concept vs. a tracked
   state field) that happen to share a name — a naming collision sitting on
   an unresolved type-boundary question, not a same-thing duplicate.
   Applied via the same `entity_duplicate_merges.py`/
   `apply_entity_duplicate_merges.py` pair as §6.11 (that script already
   generalized correctly — no code changes needed, only new entries in the
   judged mapping).
2. **The `CAPABILITY_KIND_BY_PREFIX` bug (§6.10) recurred a third time**,
   in a case §6.10 didn't cover: 3 capability slugs
   (`optisweep_service_restart`, `ignition_restart`, `rms_map_reposition`)
   are never independently defined in `capability_catalog.json` — they
   exist only as bare id-strings inside other capabilities'
   `forbidden_capability_ids`, so Pass 0 auto-creates a minimal "referenced
   only" stub for each with zero real content, going through the same
   keyword-substring `_capability_kind_for()` as every other capability.
   `rms_map_reposition` matched no keyword and silently defaulted to
   `DIAGNOSTIC` — wrong; repositioning something on a map is a control
   action. (The other two coincidentally matched "restart" → `RECOVERY`,
   which is correct, so left alone.) Since these stubs have no
   description/job content to pair a state entity against (unlike the 27
   in §6.10), this needed a smaller, separate fix rather than forcing them
   into the `PAIRINGS` shape: added `STUB_CAPABILITY_KIND_FIXES` alongside
   `PAIRINGS` in `capability_state_pairings.py`, applied by the same
   `apply_capability_state_pairings.py` (extended with one new step, still
   idempotent).

**Result**: 2,196 → 2,191 entities (2 more reclassified to Claims, 4 more
merged as casing-collision duplicates, 1 stub capability_kind corrected).
`validate_batch()` — 0 errors. `pytest brain/tests/` — 23 passed.

**Lesson for the future agent**: this pass found real defects in data that
had already been through two prior review passes (§6.7's original audit,
§6.8's duplicate report) — not because those passes were careless, but
because each used a narrower lens (name-pattern matching for claim-shape,
identical-source_refs for duplicates) that structurally couldn't see a
defect outside that lens (a `symptom`-typed entity, a casing-collision
duplicate with no shared source_refs). A full-corpus sample read with no
specific pattern in mind is a different, complementary check, not a
redundant one — worth keeping as a recurring practice, not a one-time
audit step.

## 6.13. Second operational-source audit: a new category-confusion class, and a bug that recurred three times

Requested directly: "audit the brain ontology one more time for the
operational data." Two background research-agent runs both crashed mid-task
(a server error, then a stalled stream) — each still surfaced one real,
independently-confirmed finding before dying (a `symptom` mistyping and a
`state` mistyping), which is why this pass leaned on direct manual
inspection rather than a third agent attempt.

**A new category-confusion pattern, distinct from §6.7's claim-shape and
§6.10's state-vs-action fixes**: `symptom` and `state` were both being used
as a catch-all for anything vaguely diagnostic-flavored, not just true
anomaly/checkable-condition content. Found by reading the FULL `symptom`
(52) and `state` (72) buckets directly, not a sample. Two sub-patterns:

- **Reference/data-description content mistyped as `symptom`** — 6 entities
  describe a documentation pointer, a database model's stored contents, or
  normal (non-anomalous) system behavior, not something wrong. E.g.
  `entity:symptom:api_request_and_response_behavior`: "OptiSweep API
  interactions are described primarily as data-fetching requests... without
  module-to-module request-flow tracing" — a neutral description of how the
  API behaves, not an anomaly.
- **Recovery-procedure descriptions mistyped as `symptom`** — 7 more
  entities describe the RESPONSE to a problem ("the procedure involves...",
  "the corrective action involves...") rather than the problem itself. One
  of these, `entity:symptom:agv_fault_during_exchange_recovery_concept`,
  turned out to have the IDENTICAL name as an already-existing, already
  correctly-typed `entity:component:agv_fault_during_exchange_recovery_concept`
  from §6.7's hand-rewrite list — a fourth duplicate-creation mechanism
  (same name, different `entity_type`, only possible to collide once one
  side is retyped, since `entity_id()` is type-prefixed) distinct from the
  three already documented in `entity_duplicate_merges.py`'s docstring.
- **Database table content mistyped as `state`** — 7 entities describe a
  database model's schema/field content (`SystemActiveErrorModel`,
  `SystemDatabaseModel`, lane activity records), the same confusion as
  above landing on `state` instead. Two of these
  (`entity:state:system_active_error_model`, `..._error_activity_model`)
  turned out to be the SAME fourth-mechanism collision — already-existing,
  richer `database_table` siblings existed under their real PascalCase
  names (`entity:database_table:systemactiveerrormodel`).

Applied via a new script pair, following the established pattern:
`brain/migration/entity_type_corrections.py` (a permanent hand-judged
`CORRECTIONS` dict, old_entity_id → new_entity_type, 20 entries) and
`apply_entity_type_corrections.py` (`--write` to apply): changes
`entity_type` (and therefore `id`, since `entity_id()` is type-prefixed),
gives `database_table` corrections a real, evidence-grounded
`database_name` (not fabricated — matched against the correctly-typed
sibling's own `database_name`), and rewrites every Relationship/Claim
reference to the old id across the corpus. 4 of the 20 corrections'
resulting new ids collided with an already-existing record and were
resolved via `entity_duplicate_merges.py`'s `MERGES` dict (2 for the
fourth-mechanism collisions above, 2 more for an ordinary same-content-
twice pattern found in the same sweep — a terse and a full extraction of
the identical manual troubleshooting section, e.g.
`obstruction_parcel_on_floor_troubleshooting` vs.
`obstruction_or_parcel_on_floor_troubleshooting`).

**A real bug, found and fixed mid-pass, not a one-off**: the first version
of `apply_entity_type_corrections.py` silently OVERWROTE an already-existing
record on collision (`entities_by_id[new_id] = entity`, unconditional) —
this destroyed the already-correct, already-hand-rewritten
`entity:component:agv_fault_during_exchange_recovery_concept` the first
time the script ran with `--write`. Caught by re-reading the written
output immediately after (not by any test — none existed for this path),
not assumed correct because the dry-run had looked fine. Fixed to route a
collision through `merge_record()` instead, and the **entire corpus was
rebuilt from Pass 0 forward** rather than hand-patching the one clobbered
record, since a silent-overwrite bug meant other silent damage couldn't be
ruled out without starting clean. This is the same "when you find a
migration bug, rebuild rather than patch around it" discipline used
throughout this project's history (e.g. the Stage 8 relationship_linking
staleness fix, an earlier session).

**Second, separate bug, found by explicitly checking for it rather than by
`validate_batch()`**: neither `apply_entity_duplicate_merges.py` (in use
since §6.11, an EARLIER session) nor the first version of
`apply_entity_type_corrections.py` (written THIS session) rewrote
`Claim.subject_entity_id`/`Claim.object.entity_id` references to a
merged-away or retyped id — only `Relationship` references. This is the
exact `support_contract`-dangling-reference class of bug from §6.10,
recurring a third time, in a third script, discovered only because it was
explicitly checked for (`grep`-equivalent over all Claims' subject ids
against the entity registry) rather than trusted to `validate_batch()`,
which had never checked this either. Found 5 real dangling claim
references already sitting in the corpus from PRIOR runs of
`apply_entity_duplicate_merges.py` — including one from the
`database_walkthrough_training_slide` merge in §6.12, an earlier session —
not just from this session's new corrections. Both scripts fixed to also
rewrite Claim references; **`brain/validators.py` extended** with
`validate_claim_references()` (checks `subject_entity_id`/
`object.entity_id` against known ids) and
`validate_capability_support_contract_references()` (finally closes the
§6.10 gap generically, rather than leaving it as a documented-but-open
item) so `validate_batch()` itself now catches this whole class of bug
going forward, instead of relying on someone remembering to grep for it
every time.

**Result**: full rebuild from Pass 0 (`migrate_ontology_catalogs.py` →
Pass 1 ×2 → `consolidate_entities.py` → `reclassify_ambiguous_entities.py`
→ `cleanup_entity_descriptions.py` → `apply_capability_state_pairings.py`
→ `apply_entity_type_corrections.py` → `apply_entity_duplicate_merges.py`)
— 2,186 entities, 31 capabilities, 1,697 claims, 11,270 relationships,
3,441 evidence units. `validate_batch()` — 0 errors, including under the
3 newly-added checks. `pytest brain/tests/` — 40 passed.

**Also checked, confirmed NOT a defect (real findings that turned out
fine)**: `entity:symptom:ai1_data_availability_and_default_dimensions`
(borderline phrasing but does describe a genuine anomaly chain — AI1 not
sending data → totes overflowing); `entity:symptom:operator_station_chute_debris`
and `entity:symptom:unplanned_restart_and_job_cleanup_issue` (both
genuinely anomaly-shaped); an apparent mojibake artifact in a claim's
object text (`FORTNA's`) that turned out to be a correctly-encoded curly
apostrophe (U+2019) misrendered only by this session's own terminal, not a
data defect — checked the raw code points before concluding anything was
wrong, consistent with not trusting a rendering artifact as ground truth.

**Also found, reported but NOT fixed this pass (deliberately deferred,
broader than a one-off entity fix)**: a systemic, corpus-wide
over-attachment pattern on `supports` relationships — entities (correctly-
typed ones included, e.g. `entity:symptom:operator_station_chute_debris`)
`supports` a broad, loosely-related sprawl of `runbook_proc` evidence
stubs from the same source document, not just evidence specifically about
that entity. This is a Pass 1 migration-time pattern (evidence attachment
appears to be scoped per-document-section rather than per-fact), not a
type-miscategorization, and fixing it is a different, larger scope than
this pass — noted for a future dedicated review.

## 7. Current corpus totals (fully consolidated, operational lane complete, catalogs backfilled, entity/claim audit resolved, VISU-screen duplicates fixed, Pass 0 Claim gap fixed, capability state-vs-action fixed, 7 near-duplicate pairs resolved, re-judge pass complete, second operational-source audit complete)

```
Pass 0 (ontology catalogs, post-backfill,
duplicate fix + Claim gap fix applied):    182 entities, 31 capabilities, 992 evidence units, 80 claims, 517 relationships
Pass 1 (5 operational sources), after
entity consolidation, the entity-vs-claim
reclassification (§6.7), the
duplicate-screen fix (§6.8), the
Pass 0 Claim gap fix (§6.9), the
capability state-vs-action fix (§6.10),
the 7-pair near-duplicate resolution
(§6.11), the re-judge pass (§6.12), and
the second operational-source audit
(§6.13):                                    2,186 entities (registry total; includes Pass 0 plus
                                             28 new state/symptom entities, minus 37 reclassified
                                             to Claims, minus 17 merged-away near-duplicates,
                                             plus 20 entity_type corrections applied — 4 of which
                                             collapsed into an existing record via merge rather
                                             than adding a new id),
                                             31 capabilities (2 stub capability_kind corrections
                                             total),
                                             3,441 evidence units,
                                             1,697 claims,
                                             11,270 relationships
```

Every record cross-validated with zero errors via
`brain.validators.validate_batch` across the full corpus (all entities,
capabilities, evidence, claims, and relationships from every source
together, not just per-source).

`video_training_inspection` produced zero records — it is genuinely
pre-Stage-1 scratch material (JPEG frames only, no JSON output yet), not a
migration gap.

Separately, `docs/ontology/catalogs/*.json` itself grew from 195 to 710
`evidence[]` entries and from 26 to 28 capability cards — see §6.6.

## 8. Explicitly deferred (do not build ahead of these)

Matches architecture lock §14 plus what this migration specifically
surfaced as needing real judgment rather than a mechanical rule:

- **Semantic tag/description → Capability matching.** Requires actually
  understanding what an artifact depicts or what a claim asserts, relative to
  a capability's real diagnostic scope — not keyword overlap. This is
  exactly the kind of bounded, typed extraction call the future ingestion
  agent's tools (architecture lock §11.3: `get_brain_context`,
  `resolve_entities`, `validate_brain_records`) are meant to perform, with a
  real LLM call reasoning over the artifact's `detailed_description` and the
  candidate capability's `description`/`when_to_use`/`not_for` fields.
- **Free-text `Claim` sentence → structured subject/predicate/object.**
  Incident `stage4_evidence_chunks.json`'s `source_supported_claims[].claim`
  values are plain sentences ("The case status shown is New"), not triples.
  Turning these into well-formed `Claim` records with a resolved
  `subject_entity_id` needs entity resolution against free text, which is a
  genuine LLM extraction task — Pass 2, not yet started, and per the
  2026-09-08 direction will be agent-executed rather than a deterministic
  script when it happens (AGENT_DESIGN_NOTES.md §1).
- **Procedure/Playbook schema design** (steps, branch logic, escalation
  gates) — **schema built** (`brain/schemas/procedure.py`,
  `brain/schemas/playbook.py`); Procedures are now populated from
  operational runbook evidence by
  `brain/migration/enrich_brain_knowledge.py` (see
  `AGENT_DESIGN_NOTES.md` §7). Playbook *instances* from the shared
  Stage 8 pipeline are still not promoted.
- **Any Foundry/agent runtime code.** Architecture lock §11.4 is explicit:
  "do not create the agent, agent tools, production credentials, or a
  Foundry dependency now." Offline enrichment (§7 of AGENT_DESIGN_NOTES)
  is the interim substitute for the Procedure/Capability field-filling
  agent.

## 9. Source files

```
brain/migration/
  common.py                       # load_json (BOM-safe), load_json_dir (long-path-safe), dump_records
  entity_registry.py               # EntityRegistry: resolve-by-(entity_type, slugified alias)-or-create
  entity_shape.py                  # is_claim_shaped(), strip_source_reference_leak() — the entity-vs-claim test (§6.7)
  merge.py                        # merge_record/merge_list_field/merge_scalar_field: grow-richer-never-regress merge
  migrate_ontology_catalogs.py    # Pass 0
  migrate_operational_source.py   # Pass 1, run once per source directory
  consolidate_entities.py         # post-hoc near-duplicate entity merge, run after a full Pass 1
  reclassify_ambiguous_entities.py # converts a fixed, reviewed list of pre-fix entities into Claims — 37 entries: original 35 (§6.7) + 2 more found in the §6.12 re-judge pass
  cleanup_entity_descriptions.py   # applies entity_description_rewrites.REWRITES + mechanical fallback (§6.7); re-run --write after every fresh rebuild
  entity_description_rewrites.py   # PERMANENT hand-written entity_id -> description dict, 82 entries (§6.7)
  capability_state_pairings.py     # PERMANENT hand-judged capability -> state/symptom entity pairings, 28 entries (§6.10), plus STUB_CAPABILITY_KIND_FIXES, 2 entries (§6.12, §6.13)
  apply_capability_state_pairings.py # applies capability_state_pairings.PAIRINGS + STUB_CAPABILITY_KIND_FIXES (§6.10, §6.12); re-run --write after every fresh rebuild
  entity_type_corrections.py       # PERMANENT hand-judged entity_type corrections, 20 entries (§6.13)
  apply_entity_type_corrections.py # applies entity_type_corrections.CORRECTIONS (§6.13); re-run --write after every fresh rebuild; MUST run before apply_entity_duplicate_merges.py
  entity_duplicate_merges.py       # PERMANENT hand-judged near-duplicate entity merge pairs — 13 winners/17 losers: original 7/8 (§6.11) + 4 casing-collision pairs (§6.12) + 4 more found in §6.13 (2 post-retype collisions, 2 same-content-twice)
  apply_entity_duplicate_merges.py # applies entity_duplicate_merges.MERGES (§6.11, §6.12, §6.13); re-run --write after every fresh rebuild
  enrich_brain_knowledge.py       # offline enrichment agent: role_paths, sql db ids, Procedure promotion, query claims (AGENT_DESIGN_NOTES §7)
  BRAIN_BUILD_PROCESS.md          # this file
```

**No `migrate_incident_case.py`, deliberately.** Per the 2026-09-08 direction
(AGENT_DESIGN_NOTES.md §1), incident case migration will not be a
hand-written, source-shape-specific script the way Pass 0/1 are — it is the
ingestion agent's job, following the §7 enrichment pass as precedent for
what "agent does the migration, not a script" looks like before real
runtime tools exist. Do not add a `migrate_incident_case.py` file to this
directory going forward.

Every script is a plain CLI (`python -m brain.migration.<name> --source <id>`),
local-first (writes to `brain/data/local/`, no Azure dependency), and
re-runnable — running a source migration twice with the same registry input
overwrites that source's own output deterministically rather than
accumulating duplicates, because entity/claim/relationship IDs are
content-derived (`brain/id_generation.py`), not random. The two exceptions
are `reclassify_ambiguous_entities.py` and the hand-rewrite step in §6.7:
both operate on a fixed, named, one-time list of pre-fix records — re-running
the standard Pass 0 → Pass 1 → consolidate → Pass 1 rebuild does NOT recreate
the 166 reclassified entities or re-leak the 82 rewritten descriptions,
because the root-cause fixes in `entity_shape.py` and
`migrate_operational_source.py` prevent them from being produced again.

**Rebuild-from-scratch order** (needed any time schemas or merge logic
change, not just the first time): `migrate_ontology_catalogs.py` →
`migrate_operational_source.py --source <each of the 5, in any order>` →
`consolidate_entities.py` → `migrate_operational_source.py --source <each of
the 5 again>` (re-resolves every Relationship/Claim against the
consolidated entity ids; skip this second full pass only if
`consolidate_entities.py`'s merge plan was empty) → **`reclassify_ambiguous_entities.py
--write` → `cleanup_entity_descriptions.py --write` →
`apply_capability_state_pairings.py --write` →
`apply_entity_type_corrections.py --write` →
`apply_entity_duplicate_merges.py --write`.**

**The last three scripts must run in exactly this order, last**, after the
entity/description fixes — like the other two, they are required permanent
fixtures, not one-time cleanup:
- `apply_capability_state_pairings.py`: `migrate_ontology_catalogs.py`'s
  `CAPABILITY_KIND_BY_PREFIX` (§6.10) still produces state-shaped capability
  ids/labels/kinds on every fresh Pass 0 run; nothing was changed at the
  Pass 0 root-cause level for this one.
- `apply_entity_type_corrections.py` (§6.13): the `symptom`/`state`
  category-confusion pattern isn't fixed at the migration root either — a
  fresh rebuild reproduces the exact same 20 mistyped entities every time.
  Must run AFTER capability pairings (so it doesn't need to reason about
  capability-created entities) and BEFORE entity-duplicate-merges, since
  several of its retypes produce a same-name collision that the next
  script resolves as an ordinary merge.
- `apply_entity_duplicate_merges.py`: the `applies_to` self-reference
  pattern that produces the bare-echo `system` entities (§6.11) is a
  structural byproduct of how context records are migrated, not fixed at
  the root either — a fresh rebuild reproduces the exact same loser
  entities every time (deterministic ids), so this script must run again to
  restore the clean state. It must run LAST because its `MERGES` dict
  includes entries that only exist as valid ids after
  `apply_entity_type_corrections.py` has already retyped them (e.g.
  `entity:database_table:system_active_error_model`, which does not exist
  under that id until the type-correction script creates it).

All three scripts are idempotent and safe to run even when nothing changed
(they still check for and repair any dangling references left by a partial
prior application — see §6.10's two-round fix, and §6.13's Claim-reference
fix, for why this matters). **If a script in this chain is ever modified
to fix a bug in how it rewrites references** (as happened in §6.13, twice,
in the same session), rebuild the ENTIRE corpus from `migrate_ontology_catalogs.py`
forward rather than re-running only the fixed script against
already-written output — a bug in a rewrite script may have already
corrupted data the fix can't retroactively detect (§6.13's silent-overwrite
bug is the concrete example: only a full rebuild guaranteed the clobbered
record's original content was actually restored, not just no-longer-being-
clobbered going forward).

**Correction, found by actually re-running a fresh rebuild rather than
assuming**: an earlier version of this note claimed the last two steps were
never needed again because entity ids are deterministic and the CLEAR_CLAIM/
root-cause fix holds. That is only half true. `CLEAR_CLAIM` genuinely does
stay at 0 on a fresh rebuild — the root-cause fix in `entity_shape.py`/
`migrate_operational_source.py` really does prevent that class from being
produced again. But the **35 AMBIGUOUS entities and the 82 leaked
descriptions are NOT prevented by any root-cause fix** — nothing in the
migration logic was changed to stop producing them (the AMBIGUOUS pattern
was deliberately left unfixed at the heuristic level, since tightening
`is_claim_shaped()` to also catch it produced 80 false positives against
real entity names — see §6.7). Because entity ids are deterministic, a fresh
rebuild reproduces the *exact same* 35 and 82 records every time, and
`reclassify_ambiguous_entities.py`/`cleanup_entity_descriptions.py --write`
must be re-run after every fresh rebuild to restore the clean state — they
are permanent fixtures (keyed by entity id in
`entity_description_rewrites.py`), not one-time patches.
