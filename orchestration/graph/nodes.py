from __future__ import annotations

from pathlib import Path

from orchestration.paths import (
    DEFAULT_INCIDENT_STAGES,
    DEFAULT_OPERATIONAL_STAGES,
    DEFAULT_SHARED_STAGES,
    OUTPUT_COSMOS_PUBLISH,
    OUTPUT_ROOT,
    OUTPUT_SME_REVIEW,
    default_incident_output_dir,
    default_operational_output_dir,
    discover_source_roots,
)
from orchestration.routing import classify_upload
from orchestration.runners.assemble_delivery import (
    assemble_delivery_output,
    publish_cosmos_from_output,
)
from orchestration.runners.shared_publish import run_shared_publish_pipeline
from orchestration.runners.source_pipelines import (
    run_incident_pipeline,
    run_manual_pipeline,
    run_training_video_pipeline,
)
from orchestration.state import IngestionState


def _append_message(state: IngestionState, message: str) -> list[str]:
    return [*(state.get("messages") or []), message]


def _append_error(state: IngestionState, message: str) -> list[str]:
    return [*(state.get("errors") or []), message]


def classify_source(state: IngestionState) -> IngestionState:
    source_path = Path(state["source_path"])
    companions = [Path(p) for p in state.get("companion_paths") or []]
    routed = classify_upload(source_path, companions)

    output_dir = state.get("output_dir")
    if not output_dir:
        if routed.source_type == "incident" and routed.case_id:
            output_dir = str(default_incident_output_dir(routed.case_id))
        elif routed.source_id:
            output_dir = str(default_operational_output_dir(routed.source_id))
        else:
            output_dir = str(default_operational_output_dir(source_path.stem))

    source_stages = state.get("source_stages")
    if not source_stages:
        source_stages = (
            DEFAULT_INCIDENT_STAGES
            if routed.source_type == "incident"
            else DEFAULT_OPERATIONAL_STAGES
        )

    return {
        **state,
        "source_type": routed.source_type,
        "case_id": routed.case_id,
        "source_id": state.get("source_id") or routed.source_id,
        "source_title": state.get("source_title") or routed.source_title,
        "companion_paths": [str(p) for p in routed.companion_paths],
        "output_dir": output_dir,
        "source_stages": source_stages,
        "shared_stages": state.get("shared_stages") or DEFAULT_SHARED_STAGES,
        "use_llm": state.get("use_llm", True),
        "run_shared_publish": state.get("run_shared_publish", False),
        "publish_to_cosmos": state.get("publish_to_cosmos", False),
        "publish_scope": state.get("publish_scope") or "all",
        "shared_publish_scope": state.get("shared_publish_scope") or "case",
        "ocr_backend": state.get("ocr_backend") or "azure_cv",
        "max_workers": state.get("max_workers") or 4,
        "status": "running",
        "current_node": "classify_source",
        "messages": _append_message(
            state,
            f"Classified {source_path.name} as {routed.source_type}"
            + (f" (case {routed.case_id})" if routed.case_id else ""),
        ),
        "errors": state.get("errors") or [],
    }


def route_after_classify(state: IngestionState) -> str:
    source_type = state.get("source_type") or "unknown"
    if source_type == "incident":
        return "run_incident"
    if source_type == "manual":
        return "run_manual"
    if source_type == "training_video":
        return "run_training_video"
    return "fail_unknown"


def run_incident(state: IngestionState) -> IngestionState:
    case_id = state.get("case_id")
    if not case_id:
        return {
            **state,
            "status": "failed",
            "current_node": "run_incident",
            "errors": _append_error(
                state,
                "Incident uploads require a case id in the filename (e.g. Case 228086 Data.pdf).",
            ),
        }
    try:
        out, log = run_incident_pipeline(
            source_pdf=Path(state["source_path"]),
            case_id=case_id,
            output_dir=Path(state["output_dir"]),
            stages=state.get("source_stages") or DEFAULT_INCIDENT_STAGES,
            use_llm=bool(state.get("use_llm", True)),
            max_workers=int(state.get("max_workers") or 4),
            ocr_backend=state.get("ocr_backend") or "tesseract",
            source_title=state.get("source_title"),
        )
        return {
            **state,
            "output_dir": str(out),
            "current_node": "run_incident",
            "messages": _append_message(state, log or f"Incident pipeline complete: {out}"),
        }
    except Exception as exc:
        return {
            **state,
            "status": "failed",
            "current_node": "run_incident",
            "errors": _append_error(state, str(exc)),
        }


def run_manual(state: IngestionState) -> IngestionState:
    try:
        out, log = run_manual_pipeline(
            source_pdf=Path(state["source_path"]),
            output_dir=Path(state["output_dir"]),
            stages=state.get("source_stages") or DEFAULT_OPERATIONAL_STAGES,
            use_llm=bool(state.get("use_llm", True)),
            max_workers=int(state.get("max_workers") or 4),
            source_id=state.get("source_id"),
            source_title=state.get("source_title"),
            ocr_backend=state.get("ocr_backend") or "azure_cv",
        )
        return {
            **state,
            "output_dir": str(out),
            "current_node": "run_manual",
            "messages": _append_message(state, log or f"Manual pipeline complete: {out}"),
        }
    except Exception as exc:
        return {
            **state,
            "status": "failed",
            "current_node": "run_manual",
            "errors": _append_error(state, str(exc)),
        }


def run_training_video(state: IngestionState) -> IngestionState:
    companions = [Path(p) for p in state.get("companion_paths") or []]
    transcript = next((p for p in companions if p.suffix.lower() in {".vtt", ".srt"}), None)
    if transcript is None:
        return {
            **state,
            "status": "failed",
            "current_node": "run_training_video",
            "errors": _append_error(
                state,
                "Training video uploads require a companion .vtt/.srt transcript in the same folder.",
            ),
        }
    try:
        out, log = run_training_video_pipeline(
            source_video=Path(state["source_path"]),
            transcript_vtt=transcript,
            output_dir=Path(state["output_dir"]),
            stages=state.get("source_stages") or DEFAULT_OPERATIONAL_STAGES,
            use_llm=bool(state.get("use_llm", True)),
            max_workers=int(state.get("max_workers") or 4),
            source_id=state.get("source_id"),
            source_title=state.get("source_title"),
            ocr_backend=state.get("ocr_backend") or "tesseract",
        )
        return {
            **state,
            "output_dir": str(out),
            "current_node": "run_training_video",
            "messages": _append_message(state, log or f"Training video pipeline complete: {out}"),
        }
    except Exception as exc:
        return {
            **state,
            "status": "failed",
            "current_node": "run_training_video",
            "errors": _append_error(state, str(exc)),
        }


def fail_unknown(state: IngestionState) -> IngestionState:
    return {
        **state,
        "status": "failed",
        "current_node": "fail_unknown",
        "errors": _append_error(
            state,
            "Could not classify upload. Drop PDFs into data/inbox/incidents or data/inbox/manuals, "
            "or videos (+ .vtt) into data/inbox/videos.",
        ),
    }


def route_after_source(state: IngestionState) -> str:
    if state.get("status") == "failed":
        return "finalize"
    if state.get("run_shared_publish"):
        return "run_shared_publish"
    return "assemble_delivery"


def run_shared_publish(state: IngestionState) -> IngestionState:
    try:
        configured = [Path(p) for p in state.get("source_roots") or []]
        # Stage 6.5 has no merge-with-existing-pool capability of its own (see
        # shared_pipeline_stages/stage_6_5/pool_builder.py's build_runbook_pool):
        # runbook_pool.json / canonical_runbooks.json are a pure function of
        # whatever source_roots are passed in, with no accretive step. Scoping
        # these roots to only the newly ingested case would silently shrink
        # Stage 8's entire runbook catalog to that one case, breaking linking
        # for every other case/manual/training source. Roots must therefore
        # stay full-corpus regardless of shared_publish_scope; only Stage 8's
        # case_ids (which candidates get finalized, not what catalog they can
        # link against) are safe to scope by default.
        roots = configured or discover_source_roots()
        if state.get("output_dir"):
            out = Path(state["output_dir"])
            if out.exists() and out not in roots:
                roots = [*roots, out]
        full_regen = (state.get("shared_publish_scope") or "case").strip().lower() == "all"
        log = run_shared_publish_pipeline(
            source_roots=roots,
            stages=state.get("shared_stages") or DEFAULT_SHARED_STAGES,
            use_llm=bool(state.get("use_llm", True)),
            publish_to_cosmos=bool(state.get("publish_to_cosmos", False)),
            case_ids=_case_ids_for_shared(state, all_case_ids=full_regen),
        )
        return {
            **state,
            "source_roots": [str(p) for p in roots],
            "current_node": "run_shared_publish",
            "messages": _append_message(state, log or "Shared publish pipeline complete."),
        }
    except Exception as exc:
        return {
            **state,
            "status": "failed",
            "current_node": "run_shared_publish",
            "errors": _append_error(state, str(exc)),
        }


def route_after_shared(state: IngestionState) -> str:
    if state.get("status") == "failed":
        return "finalize"
    return "assemble_delivery"


def assemble_delivery(state: IngestionState) -> IngestionState:
    try:
        configured = [Path(p) for p in state.get("source_roots") or []]
        roots = configured or discover_source_roots()
        if state.get("output_dir"):
            out = Path(state["output_dir"])
            if out.exists() and out not in roots:
                roots = [*roots, out]
        summary = assemble_delivery_output(source_roots=roots)
        return {
            **state,
            "source_roots": [str(p) for p in roots],
            "current_node": "assemble_delivery",
            "messages": _append_message(
                state,
                f"Assembled delivery under {OUTPUT_ROOT} "
                f"(sme_review={OUTPUT_SME_REVIEW.name}, cosmos_publish={OUTPUT_COSMOS_PUBLISH.name}); "
                f"summary={summary}",
            ),
        }
    except Exception as exc:
        return {
            **state,
            "status": "failed",
            "current_node": "assemble_delivery",
            "errors": _append_error(state, str(exc)),
        }


def route_after_assemble(state: IngestionState) -> str:
    if state.get("status") == "failed":
        return "finalize"
    if state.get("publish_to_cosmos"):
        return "publish_cosmos"
    return "finalize"


def publish_cosmos(state: IngestionState) -> IngestionState:
    try:
        # Cumulative publishes must upload the full corpus. Scoped uploads create thin
        # newest partitions that break AUTO_PUBLISH_VERSION apps.
        requested = _resolve_publish_scope(state)
        scope = "all"
        if requested != "all":
            # Keep the requested scope only when explicitly allowing partial publish.
            allow_partial = bool(state.get("allow_partial_publish", False))
            if allow_partial:
                scope = requested
            else:
                scope = "all"
        uploaded, version_id, warnings, counts = publish_cosmos_from_output(
            OUTPUT_COSMOS_PUBLISH,
            publish_scope=scope,
            default_case_id=state.get("case_id"),
        )
        message = (
            f"Cosmos upload from {OUTPUT_COSMOS_PUBLISH}: uploaded={uploaded}, "
            f"scope={scope}, requested_scope={requested}, version={version_id or 'n/a'}, counts={counts}"
        )
        if warnings:
            message = f"{message}; warnings={warnings}"
        next_state: IngestionState = {
            **state,
            "publish_scope": scope,
            "current_node": "publish_cosmos",
            "messages": _append_message(state, message),
        }
        if not uploaded:
            next_state["status"] = "failed"
            next_state["errors"] = _append_error(
                state,
                "Cosmos upload did not complete. Check COSMOS_* env vars, publish scope, and "
                f"{OUTPUT_COSMOS_PUBLISH / 'cosmos_upload_report.json'}.",
            )
        return next_state
    except Exception as exc:
        return {
            **state,
            "status": "failed",
            "current_node": "publish_cosmos",
            "errors": _append_error(state, str(exc)),
        }


def finalize(state: IngestionState) -> IngestionState:
    status = state.get("status")
    if status != "failed":
        status = "succeeded"
    return {
        **state,
        "status": status,
        "current_node": "finalize",
        "messages": _append_message(state, f"Ingestion finished with status={status}"),
    }


def _case_ids_for_shared(state: IngestionState, *, all_case_ids: bool = True) -> list[str] | None:
    """Case ids for Stage 8 finalization.

    Stage 8's writer now merges case-scoped output rather than overwriting
    it (see playbook_builder.py's _merge_case_scoped), so scoping to just the
    case(s) that changed no longer destroys other cases' finalized playbooks
    -- Stage 11's id-keyed cumulative merge was already safe either way. When
    all_case_ids is False (the default for a routine single-case ingestion),
    scope to the case/source just ingested; pass shared_publish_scope="all"
    (all_case_ids=True) to force full-corpus regeneration.
    """
    scope = (state.get("publish_scope") or "all").strip().lower()
    if scope.startswith("case:") and scope not in {"case:auto", "case:uploaded"}:
        return [scope.split(":", 1)[1].removeprefix("case_")]
    if not all_case_ids:
        if state.get("case_id"):
            return [str(state["case_id"])]
        roots = [Path(p) for p in state.get("source_roots") or []]
        case_ids = [root.name.removeprefix("case_") for root in roots if root.name.startswith("case_")]
        return case_ids or None
    roots = [Path(p) for p in state.get("source_roots") or []] or discover_source_roots()
    case_ids = []
    for root in roots:
        name = root.name
        if name.startswith("case_"):
            case_ids.append(name.removeprefix("case_"))
    if state.get("case_id") and str(state["case_id"]) not in case_ids:
        case_ids.append(str(state["case_id"]))
    return case_ids or None


def _resolve_publish_scope(state: IngestionState) -> str:
    scope = (state.get("publish_scope") or "all").strip()
    lowered = scope.lower()
    if lowered in {"case", "case:auto", "case:uploaded"}:
        if state.get("case_id"):
            return f"case:{state['case_id']}"
        if state.get("source_id"):
            return f"source:{state['source_id']}"
        return "all"
    if lowered in {"source", "source:auto"}:
        if state.get("source_id"):
            return f"source:{state['source_id']}"
        return "all"
    return scope
