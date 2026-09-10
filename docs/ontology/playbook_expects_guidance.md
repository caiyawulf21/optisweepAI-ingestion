# Playbook capability metadata guidance

Guidance for Stage 8 capability metadata and backward-compatible Stage 5
`expects_*` fields. Constrained IDs still come from
[`taxonomy/runbook_capability_taxonomy.json`](taxonomy/runbook_capability_taxonomy.json).
Rich job/surface/SQL detail lives in [`catalogs/capability_catalog.json`](catalogs/capability_catalog.json)
and [`catalogs/wcs_sql_catalog.json`](catalogs/wcs_sql_catalog.json).

Stage 5 incident playbook discovery is source-grounded. It must not use this
ontology guidance to add a surface, choose a diagnostic tool, or author an
indicator or branch. Stage 5 emits `required_evidence_concepts` from incident
evidence; Stage 8 may use ontology and catalog detail to select the current
support surface.

**Consumers:** Stage 8 linking LLM, humans/SME, and legacy Stage 5 metadata normalization.  
**Downstream:** Shared Stage 8 links using `expects_*` ∩ runbook tags.

## Stage 8 ontology RAG → detailed nodes

Stage 8 packets carry richer `ontology_snippets` (DB models, capability cards,
surfaces). Use them to author **detailed** diagnostic/branching/validation
nodes:

1. Ground `expected_or_observed_result` healthy / unhealthy / inconclusive signals in named tools/views from the cards (RMS pages **and/or** SSMS models).
2. Emit `expects_*` only when the node job and ontology cards support them — **do not invent** tags to force Stage 8 multi-link.
3. Prefer model cards for exact state/error rows (`SystemDatabaseModel`, `SystemStateModel`, `SystemActiveErrorModel`, `AgvActiveErrorDatabaseModel`, …).
4. Incident evidence still wins on conflicts. Do not paste snippet prose into placeholders.

## No post-process field filling

Normalize/backfill must **not** auto-fill or rewrite `expects_capability` / `expects_surface` / `preferred_audience` beyond taxonomy ID filtering and surface alias canonicalization (`ssms` → `wcs_sql`). Hardcoded shortlists and “always add rms_ui+wcs_sql” fills cause irrelevant runbook attachment.

## Surfaces — RMS is not preferred over SSMS

SSMS holds **system state** (`SystemDatabaseModel` / `SystemStateModel`) as well as **active errors**. For remotely attainable jobs:

- Treat `rms_ui` and `wcs_sql` as **equal-weight** corroboration paths when the capability card lists both.
- Do **not** treat RMS as the primary and SSMS as optional.
- SSMS is especially valuable when the branch needs exact status enums, error codes, or active-error rows.
- Emit surfaces the node actually needs; do not auto-insert missing ones in code.
- Canonical SSMS id is `wcs_sql`. SQL text stays in runbooks.

## Capability disambiguation (advisory only)

| Capability | Job | SSMS anchors (examples) |
| --- | --- | --- |
| `agv_active_errors` | Active AGV/system error rows | `AgvActiveErrorDatabaseModel`, `SystemActiveErrorModel`, `AgvErrorModel` |
| `fleet_system_status` | Overall system / fleet up vs down | `SystemDatabaseModel`, `SystemStateModel` (+ RMS Overall System) |
| `device_roster_state` | Roster / mapping / location | Robot location / robot models |
| `hospital_diversion` | Hospital lane / induct / diversion | Hospital models + `hospital_hmi` |
| `zone_pairing_state` | Zone unable to obtain a pair | Pairing-related views + RMS |

Use any taxonomy capability the ontology cards support — do not collapse every node into this table.

### AGV fault checks corroborate with active-error SQL

Any diagnostic/branching/validation node whose job is to confirm an AGV fault,
error, or abnormal-error condition (regardless of which surface is primary —
RMS fleet/AGV-status view, HMI, or SSMS) should also emit `agv_active_errors`
as a capability, so the active-error SQL model (`SystemActiveErrorModel` /
`AgvActiveErrorDatabaseModel`) is retrievable as corroborating evidence
alongside the primary check. This is corroboration, not a replacement — do
not drop the node's primary capability (e.g. `device_roster_state`,
`fleet_system_status`) in favor of `agv_active_errors` alone. Apply this
whenever the node's evidence concerns AGV/system error or fault state, not
only when the incident source explicitly names the SQL model.

### HMIs, RMS, and other components share the same backend state

RMS and the various operator/site HMIs (Hospital HMI, Tipper HMI, AVEVA,
etc.) are different front-end views over the same underlying WCS/Helix
backend state — they are not independent systems. When a node's evidence
comes from one of these UI surfaces, the corresponding SSMS model(s) behind
that surface remain valid corroborating evidence per the "RMS is not
preferred over SSMS" rule above, even when the node's primary surface is an
HMI rather than RMS. Do not treat HMI-sourced evidence as SQL-incompatible.

## Audience

- `rms_ui` → primarily `operator` (+ optional `L1_support`).
- `wcs_sql` → `L2_support` / `L3_support`. Dual-surface nodes may list both, e.g. `["operator", "L2_support"]`.
- Follow the Role / Component Access Matrix.

## Heuristic backfill

`scripts/backfill_playbook_expects.py` is best-effort only. Prefer LLM Stage 5 with ontology RAG. Do not use backfill to force surfaces/capabilities onto every node.

## Change control

Keep capability `sql_model_links` in sync with `wcs_sql_catalog.json`. Taxonomy ID adds require SME approval in the taxonomy JSON.
