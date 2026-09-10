# Components — Who has access? (SME check)

**Site / operator** = customer/client (not FORTNA)  
**L1 / L2/L3** = FORTNA remote (**on Zscaler**) — **Access** means they can **interact** with the system, not view-only

| Component | Site / operator | L1 | L2/L3 |
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
| Building / ACB overview HMI | Access | Access? | Access? |
| AVEVA HMI | Access | No access | No access |

**Notes for reviewers**

- L1 / L2/L3 access assumes **on Zscaler**. Off Zscaler = no access.
- **Access** = can interact (not view-only).
- **RMS soft stop** = pause-style stop in RMS; **L2/L3 only**. Not a physical E-stop.
- **E-stop** = physical only; **site / operator only**. FORTNA never performs E-stop.
- **AVEVA HMI** = floor / site only.
- Building / ACB overview = **Access?** — confirm.

Please correct any cell and reply.
