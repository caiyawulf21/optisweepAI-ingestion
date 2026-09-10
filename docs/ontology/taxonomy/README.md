# Runbook / playbook capability taxonomy

Frozen pilot vocabulary for tagging runbooks and (later) playbook nodes.

**File:** [`runbook_capability_taxonomy.json`](runbook_capability_taxonomy.json) (`schema_version` **0.4**)

| Dimension | Purpose |
| --- | --- |
| `capabilities` | Same diagnostic/recovery **job** across tools (thin IDs here; **rich cards** in [`../catalogs/capability_catalog.json`](../catalogs/capability_catalog.json)) |
| `access_surfaces` | How the job is done (`rms_ui`, `wcs_sql` / SSMS, HMIs, `stunnel`, `apidog`, …) |
| `audience_roles` | Who may execute (`operator` = customer/client; L1–L4 = FORTNA remote) |
| `failure_patterns` | When the job is relevant |
| `procedure_intents` | observe / diagnose / recover / validate |
| `capability_failure_edges` | Capability ↔ failure_pattern links (Stage 6/8) |
| `surface_activities` | Surface ↔ activity ↔ observables ↔ capability hints |
| `catalog_refs` | Pointers to deep reference catalogs under [`../catalogs/`](../catalogs/) |

Deep **WCS SQL / API / other surface** field semantics live in `docs/ontology/catalogs/` (reference only — not `expects_*` IDs). Inline `wcs_sql_catalog` / `wcs_api_catalog` on this file are thin indexes (`relocated_to`) for older consumers.

## Rules

- Treat capability / surface / role / failure / intent IDs as the constrained vocab for LLM tagging (Stage 6) and `expects_*` (Stage 5, Track C2).
- `wcs_sql` is the canonical surface id; `ssms`, `helix_db`, `wcs_db` are aliases.
- Same capability + different surface ⇒ valid Stage 8 multi-link — not a hardcoded peer list.
- Put table/column/API names in **runbook** steps when source-backed; playbook nodes name the job + surface class only.
- Do not expand constrained IDs casually; SME-approved additions only. Catalog rows may grow when they map to an existing job.
- Field meanings require OCR/transcript/SQL-guide evidence (`evidence` / `needs_sme`); do not invent.

## Stage 5 / Stage 6 mini-RAG

Constrained IDs still append via `taxonomy_prompt_appendix()`. Packet-wired snippets: Stage 5 ≤2 surface/capability; Stage 6 ≤3 model/capability/activity — `shared_pipeline_stages/ontology_rag.py`. Design: [`../../design_decisions/ontology_surface_catalogs_and_stage6_rag.md`](../../design_decisions/ontology_surface_catalogs_and_stage6_rag.md).

## A0 completeness sources

1. Day 2 training VTT + Stage 1/2 OCR (`training_video_day2`)
2. Active AGV error SQL guide (`Helix2x_1Prod_Robotics` / `SystemActiveErrorModel`)
3. **OptiSweep Training Slides [INTERNAL ONLY].pdf** — authoritative PascalCase models, SorterSweeper models, APIs, Ignition/Stunnel/OptiSweep host trio
4. Day 1 RMS/AVEVA frames (thinner surface seeds); OM manual reserved under `docs/ontology/sources/om_manual/`

### 0.4 changes

- Externalized deep catalogs to `docs/ontology/catalogs/`
- Field-level WCS SQL meanings from Day2 transcript/OCR where evidenced
- Added capability↔failure and surface activity cross-links
- Reserved `docs/ontology/sources/` for Day1 + OM packs in the same store

## Related

- [Ontology index](../README.md)
- [Support roles & adjacency](../support_roles_components_and_adjacency.md)
- [Stage 8 capability tags plan](../../design_decisions/stage_8_capability_tags_and_linking_plan.md)
- [Role / component access matrix (prompt)](../../../stage_prompts/shared/role_component_access_matrix.md)
