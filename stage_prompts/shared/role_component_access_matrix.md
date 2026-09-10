# Role / Component Access Matrix

Use this matrix when assigning `operator`, `L1_support`, `L2_support`, or `L3_support`.

**Role meanings**

| Role value | Who |
| --- | --- |
| `operator` | Site / customer/client staff — **not** FORTNA |
| `L1_support` | FORTNA L1 Technical Support (remote, on Zscaler) |
| `L2_support` / `L3_support` | FORTNA L2/L3 Escalation Support (remote, on Zscaler) |

**Access** = may interact with that software/service (not view-only).  
**No access** = do not assign this role as the executor for a procedure that requires that component.

L1 / L2 / L3 access assumes **on Zscaler**. Off Zscaler they have no remote access.

| Component | `operator` (site) | `L1_support` | `L2_support` / `L3_support` |
| --- | --- | --- | --- |
| RMS (fleet / AGV status web) | Access | Access | Access |
| RMS soft stop (pause — **not** E-stop) | — | No access | Access |
| E-stop (physical) | Access | No access | No access |
| OptiSweep / WCS API | No access | Access | Access |
| WCS / Helix DB (SSMS) | No access | Access | Access |
| Event Viewer / Windows Services | No access | Access | Access |
| Ignition gateway | No access | Access | Access |
| Tipper HMI / WebVisu / VISU | Access | Access | Access |
| Hospital HMI / lane UI | Access | Access | Access |
| Building / ACB overview HMI | Access | Access | Access |
| AVEVA HMI | Access | No access | No access |

**Hard rules**

1. Only `operator` may perform physical **E-stop**. Never assign E-stop to L1/L2/L3.
2. **RMS soft stop** (pause) is L2/L3 only — not E-stop; not L1.
3. **AVEVA HMI** is floor / site only (`operator`). FORTNA has no access.
4. Do not assign a role that has **No access** to a component the procedure/node requires.
5. Prefer the lowest safe role that has Access for every component the procedure needs.
