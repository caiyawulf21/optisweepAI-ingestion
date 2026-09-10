from __future__ import annotations

from pathlib import Path

from orchestration.paths import (
    DEFAULT_SHARED_STAGES,
    SHARED_OUTPUT,
    SHARED_SCRIPTS,
    discover_source_roots,
)
from orchestration.runners import run_python_script


def run_shared_publish_pipeline(
    *,
    source_roots: list[Path] | None = None,
    shared_output: Path | None = None,
    stages: str = DEFAULT_SHARED_STAGES,
    use_llm: bool = True,
    publish_to_cosmos: bool = False,
    case_ids: list[str] | None = None,
) -> str:
    # Stage 11 is not part of the ingest path. Build/upload happens only when
    # publish_to_cosmos is requested (or stages explicitly include "11").
    roots = source_roots or discover_source_roots()
    if not roots:
        raise FileNotFoundError("No source roots with Stage 6 outputs found for shared publish.")

    out = shared_output or SHARED_OUTPUT
    out.mkdir(parents=True, exist_ok=True)
    selected = {s.strip() for s in stages.split(",") if s.strip()}
    if publish_to_cosmos:
        selected.add("11")
    # Merge/link must never run against a stale pool after source Stage 6 regen.
    if selected & {"7", "8", "8.5", "9", "10", "11"}:
        selected.add("6.5")
    logs: list[str] = []

    pool_dir = out / "stage_6_5_runbook_pool"
    stage7_dir = out / "stage_7_merged_runbooks"
    stage8_dir = out / "stage_8_finalized_playbooks"
    stage85_dir = out / "stage_8_5_relationship_linking"
    stage9_dir = out / "stage_9_validation"
    stage10_dir = out / "stage_10_embeddings"

    if "6.5" in selected:
        args = ["--output-dir", str(out)]
        for root in roots:
            args.extend(["--source-root", str(root)])
        logs.append(run_python_script(SHARED_SCRIPTS / "stage6_5_build_runbook_pool.py", args))

    if "7" in selected:
        args = [
            "--pool-dir",
            str(pool_dir),
            "--output-dir",
            str(out),
        ]
        if use_llm:
            args.append("--llm")
        logs.append(run_python_script(SHARED_SCRIPTS / "stage7_merge_runbooks.py", args))

    if "8" in selected:
        if not use_llm:
            raise ValueError("Shared Stage 8 requires use_llm=True. Deterministic playbook finalization is not supported.")
        args = [
            "--pool-dir",
            str(pool_dir),
            "--stage7-dir",
            str(stage7_dir),
            "--output-dir",
            str(out),
            "--llm",
        ]
        for case_id in case_ids or _infer_case_ids(roots):
            args.extend(["--case-id", case_id])
        logs.append(run_python_script(SHARED_SCRIPTS / "stage8_finalize_playbooks.py", args))

    if "8.5" in selected:
        args = ["--output-dir", str(out), "--stage7-dir", str(stage7_dir), "--stage8-dir", str(stage8_dir)]
        for root in roots:
            args.extend(["--source-root", str(root)])
        logs.append(run_python_script(SHARED_SCRIPTS / "stage8_5_link_relationships.py", args))

    if "9" in selected:
        args = [
            "--stage7-dir",
            str(stage7_dir),
            "--stage8-dir",
            str(stage8_dir),
            "--stage85-dir",
            str(stage85_dir),
            "--output-dir",
            str(out),
        ]
        for root in roots:
            args.extend(["--source-root", str(root)])
        logs.append(run_python_script(SHARED_SCRIPTS / "stage9_validate_corpus.py", args))

    if "10" in selected:
        args = [
            "--stage7-dir",
            str(stage7_dir),
            "--stage8-dir",
            str(stage8_dir),
            "--output-dir",
            str(out),
        ]
        for root in roots:
            args.extend(["--source-root", str(root)])
        logs.append(run_python_script(SHARED_SCRIPTS / "stage10_generate_embeddings.py", args))

    if "11" in selected:
        args = [
            "--stage7-dir",
            str(stage7_dir),
            "--stage8-dir",
            str(stage8_dir),
            "--stage10-dir",
            str(stage10_dir),
            "--stage85-dir",
            str(stage85_dir),
            "--stage9-dir",
            str(stage9_dir),
            "--output-dir",
            str(out),
        ]
        for root in roots:
            args.extend(["--source-root", str(root)])
        # Candidate local bundle first.
        logs.append(run_python_script(SHARED_SCRIPTS / "stage11_publish_cosmos.py", args))
        # Then cumulative merge + operator-language enrichment + gate + smoke into delivery.
        from shared_pipeline_stages.stage_11.cumulative_publish import run_cumulative_stage11

        cumulative = run_cumulative_stage11(
            output_dir=out,
            source_roots=roots,
            skip_assemble=True,
            publish=False,
            copy_to_delivery=True,
            run_smoke=True,
        )
        logs.append(
            "Stage 11 cumulative publish complete: "
            f"version={cumulative.publish_version_id} cases={cumulative.case_ids} "
            f"playbooks={len(cumulative.playbook_ids)} smoke={cumulative.smoke_passed}"
        )

    return "\n".join(log for log in logs if log)


def _infer_case_ids(roots: list[Path]) -> list[str]:
    case_ids: list[str] = []
    for root in roots:
        name = root.name
        if name.startswith("case_"):
            case_ids.append(name.removeprefix("case_"))
    return case_ids or ["228086", "228723"]
