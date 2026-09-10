"""Refresh shared catalog after a source Stage 6 regen.

Shared Stage 6.5 rebuilds the pool from all discoverable Stage 6 roots.
Shared Stage 7 merges into the canonical catalog. Shared Stage 8 re-links
incident playbooks against that catalog.

Call this at the end of per-source regen scripts so Day1/Day2 (and similar)
OpenAI-only paths do not leave Stage 8 on a stale pool.
"""

from __future__ import annotations

import os

from orchestration.runners.shared_publish import run_shared_publish_pipeline


def shared_refresh_enabled() -> bool:
    raw = os.getenv("REGEN_REFRESH_SHARED", "1").strip().lower()
    return raw not in {"0", "false", "no", "off"}


def shared_refresh_stages() -> str:
    return os.getenv("REGEN_SHARED_STAGES", "6.5,7,8").strip() or "6.5,7,8"


def refresh_shared_after_source_regen(*, label: str = "source") -> None:
    if not shared_refresh_enabled():
        print(
            f"=== Shared refresh skipped after {label} "
            f"(REGEN_REFRESH_SHARED=0) ===",
            flush=True,
        )
        return

    stages = shared_refresh_stages()
    print(
        f"=== Shared refresh after {label} Stage 6 "
        f"(stages={stages}; pool rebuilt from all Stage 6 roots) ===",
        flush=True,
    )
    run_shared_publish_pipeline(stages=stages, use_llm=True)
    print(f"=== Shared refresh after {label} complete ===", flush=True)
