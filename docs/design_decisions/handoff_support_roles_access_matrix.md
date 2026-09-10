# Handoff — Support roles & component access matrix

Short status for the next agent. Full design: [`docs/ontology/support_roles_components_and_adjacency.md`](../ontology/support_roles_components_and_adjacency.md). Linking/Day 2 plan: [`stage_8_capability_tags_and_linking_plan.md`](stage_8_capability_tags_and_linking_plan.md).

## Goal (done for role assignment)

Define who can access/interact with OptiSweep software by role, then bake that into runbook/playbook prompts that emit roles.

## Org / role model (locked)

- `operator` = customer/client site staff — **not** FORTNA
- L1 / L2/L3 / L4 = FORTNA; **all remote**
- On Zscaler, L1 and L2/L3 can **interact** (not view-only) with allowed remotes
- E-stop (physical) = site/operator only
- RMS soft stop = pause in RMS, **L2/L3 only** — not E-stop
- AVEVA HMI = floor/site only (no FORTNA access)

## Access matrix (current)

| Component | Site/operator | L1 | L2/L3 |
| --- | --- | --- | --- |
| RMS | Access | Access | Access |
| RMS soft stop (pause) | — | No access | Access |
| E-stop (physical) | Access | No access | No access |
| WCS API | No access | Access | Access |
| WCS/Helix DB (SSMS) | No access | Access | Access |
| Event Viewer / Services | No access | Access | Access |
| Ignition gateway | No access | Access | Access |
| WebVisu / tipper HMI | Access | Access | Access |
| Hospital HMI | Access | Access | Access |
| Building/ACB HMI | Access | Access? (SME TBD) | Access? |
| AVEVA HMI | Access | No access | No access |

## Docs

| Doc | Notes |
| --- | --- |
| `docs/ontology/support_roles_components_and_adjacency.md` | Fuller roles/adjacency/branching (L1 vs L2/L3 = tool depth, not remote vs on-site) |
| `docs/design_decisions/sme_component_access_matrix.md` | Short Teams/screenshot SME sheet |
| `docs/ontology/sme_component_access_matrix.md` | Mirror of locked matrix (was stale — synced) |
| `stage_prompts/shared/role_component_access_matrix.md` | **Canonical** prompt snippet |

## Prompt integration (done)

- Stage 6/7: appended at runtime via `shared_pipeline_stages/stage_prompts.py` (`compose_stage6_*` / `compose_stage7_*`)
- Incident Stage 5: runbook + playbook (base, A, B) — **inline** matrix
- Operational Stage 5: discovery + backfill (role guidance updated) — **inline**
- Operational Stage 7 drafting: inline
- **Not Stage 8** (`compose_stage8_system_prompt` does not append; no role output fields)
- Tests: `shared_pipeline_stages/tests/test_stage_prompts.py`

## Related (same thread family)

Prefer capability + surface + role tags over hardcoded adjacency / Stage 8 adjacency agent — see `stage_8_capability_tags_and_linking_plan.md` (Track A/B/C). Role matrix answers **who may execute**; tags + Stage 5 C1/C2 still needed so Day 2 SSMS runbooks attach.

## Open for SME

- Building/ACB overview: Access for L1/L2/L3 or site-only like AVEVA?
- Confirm Zscaler gate and soft-stop wording with CSE

## Do not

- Treat `operator` as FORTNA
- Call RMS soft stop an E-stop
- Give FORTNA AVEVA or physical E-stop
- Revert ontology SME sheet to “FORTNA has no RMS”
