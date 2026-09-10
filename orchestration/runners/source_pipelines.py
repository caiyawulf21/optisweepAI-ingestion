from __future__ import annotations

from pathlib import Path

from orchestration.paths import (
    DEFAULT_INCIDENT_STAGES,
    DEFAULT_OPERATIONAL_STAGES,
    INCIDENT_SCRIPT,
    OPERATIONAL_ROOT,
    OPERATIONAL_SCRIPT,
    TRAINING_STAGE1_SCRIPT,
    TRAINING_STAGE2_SCRIPT,
    default_incident_output_dir,
    default_operational_output_dir,
)
from orchestration.runners import run_python_script

OP_SCRIPTS = OPERATIONAL_ROOT / "scripts"


def run_incident_pipeline(
    *,
    source_pdf: Path,
    case_id: str,
    output_dir: Path | None = None,
    stages: str = DEFAULT_INCIDENT_STAGES,
    use_llm: bool = True,
    max_workers: int = 4,
    ocr_backend: str = "azure_cv",
    stage2_artifact_gate: str = "none",
    source_title: str | None = None,
) -> tuple[Path, str]:
    out = output_dir or default_incident_output_dir(case_id)
    out.mkdir(parents=True, exist_ok=True)
    args = [
        "--source-pdf",
        str(source_pdf),
        "--case-id",
        case_id,
        "--output-dir",
        str(out),
        "--stages",
        stages,
        "--ocr-backend",
        ocr_backend,
        "--stage2-artifact-gate",
        stage2_artifact_gate,
        "--max-workers",
        str(max_workers),
        "--copy-source",
    ]
    if source_title:
        args.extend(["--source-title", source_title])
    if use_llm:
        args.append("--llm")
    output = run_python_script(INCIDENT_SCRIPT, args)
    return out, output


def run_manual_pipeline(
    *,
    source_pdf: Path,
    output_dir: Path | None = None,
    stages: str = DEFAULT_OPERATIONAL_STAGES,
    use_llm: bool = True,
    max_workers: int = 4,
    source_id: str | None = None,
    source_title: str | None = None,
    ocr_backend: str = "azure_cv",
) -> tuple[Path, str]:
    stem = source_id or source_pdf.stem
    out = output_dir or default_operational_output_dir(stem)
    out.mkdir(parents=True, exist_ok=True)
    args = [
        "--source-pdf",
        str(source_pdf),
        "--output-dir",
        str(out),
        "--stages",
        stages,
        "--source-type",
        "manual",
        "--max-workers",
        str(max_workers),
        "--ocr-backend",
        ocr_backend,
    ]
    if source_id:
        args.extend(["--source-id", source_id])
    if source_title:
        args.extend(["--source-title", source_title])
    if use_llm:
        args.append("--llm")
    output = run_python_script(OPERATIONAL_SCRIPT, args)
    return out, output


def run_training_video_pipeline(
    *,
    source_video: Path,
    transcript_vtt: Path,
    output_dir: Path | None = None,
    stages: str = DEFAULT_OPERATIONAL_STAGES,
    use_llm: bool = True,
    max_workers: int = 4,
    source_id: str | None = None,
    source_title: str | None = None,
    ocr_backend: str = "azure_cv",
) -> tuple[Path, str]:
    stem = source_id or source_video.stem
    out = output_dir or default_operational_output_dir(stem)
    out.mkdir(parents=True, exist_ok=True)
    selected = {s.strip() for s in stages.split(",") if s.strip()}
    messages: list[str] = []

    stage1_dir = out / "stage_1_source_bundle"
    stage2_dir = out / "stage_2_source_artifacts"
    stage4_dir = out / "stage_4_operational_context"
    stage5_dir = out / "stage_5_runbook_candidates"
    stage6_dir = out / "stage_6_finalized_runbooks"

    if "1" in selected:
        stage1_args = [
            "--source-video",
            str(source_video),
            "--transcript-vtt",
            str(transcript_vtt),
            "--output-dir",
            str(out),
            "--ocr-backend",
            ocr_backend,
        ]
        if source_id:
            stage1_args.extend(["--source-id", source_id])
        if source_title:
            stage1_args.extend(["--source-title", source_title])
        messages.append(run_python_script(TRAINING_STAGE1_SCRIPT, stage1_args))

    if "2" in selected:
        segments = stage1_dir / "training_video_slide_segments.json"
        artifacts = stage1_dir / "source_artifacts.json"
        if not segments.exists() or not artifacts.exists():
            raise FileNotFoundError(
                "Training video Stage 2 requires Stage 1 outputs "
                f"({segments.name}, {artifacts.name})."
            )
        messages.append(
            run_python_script(
                TRAINING_STAGE2_SCRIPT,
                [
                    "--training-segments",
                    str(segments),
                    "--source-artifacts",
                    str(artifacts),
                    "--output-dir",
                    str(out),
                ],
            )
        )

    source_bundle = stage2_dir / "source_bundle.json"
    enriched_artifacts = stage2_dir / "source_artifacts_enriched.json"

    if "4" in selected:
        if not use_llm:
            raise ValueError("Training video Stage 4 requires use_llm=True.")
        messages.append(
            run_python_script(
                OP_SCRIPTS / "stage4_extract_operational_context.py",
                [
                    "--source-bundle",
                    str(source_bundle),
                    "--source-artifacts",
                    str(enriched_artifacts),
                    "--output-dir",
                    str(out),
                    "--llm",
                ],
            )
        )

    if "5" in selected:
        if not use_llm:
            raise ValueError("Training video Stage 5 requires use_llm=True.")
        messages.append(
            run_python_script(
                OP_SCRIPTS / "stage5_extract_runbook_candidates.py",
                [
                    "--source-bundle",
                    str(source_bundle),
                    "--source-artifacts",
                    str(enriched_artifacts),
                    "--operational-context",
                    str(stage4_dir / "operational_context.json"),
                    "--output-dir",
                    str(out),
                    "--llm",
                    "--max-workers",
                    str(max_workers),
                ],
            )
        )

    if "6" in selected:
        messages.append(
            run_python_script(
                OP_SCRIPTS / "stage6_finalize_runbooks.py",
                [
                    "--runbook-candidates",
                    str(stage5_dir / "runbook_candidates.json"),
                    "--source-artifacts",
                    str(enriched_artifacts),
                    "--operational-context",
                    str(stage4_dir / "operational_context.json"),
                    "--source-bundle",
                    str(source_bundle),
                    "--output-dir",
                    str(out),
                    "--max-workers",
                    str(max_workers),
                ],
            )
        )

    if "8" in selected:
        messages.append(
            run_python_script(
                OP_SCRIPTS / "stage8_link_relationships.py",
                [
                    "--output-dir",
                    str(out),
                    "--source-artifacts",
                    str(enriched_artifacts),
                    "--operational-context",
                    str(stage4_dir / "operational_context.json"),
                    "--finalized-runbooks-dir",
                    str(stage6_dir / "finalized_runbooks"),
                    "--runbook-candidates",
                    str(stage5_dir / "runbook_candidates.json"),
                ],
            )
        )

    return out, "\n".join(m for m in messages if m)
