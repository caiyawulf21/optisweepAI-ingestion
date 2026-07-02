"""Stage 6 LLM helpers for source-specific runbook finalization."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol
import hashlib
import html
import json
import os
import re
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from shared.stage_prompts import (
    compose_stage6_system_prompt,
    load_prompt_file,
    resolve_stage6_operational_prompt_path,
    resolve_stage6_structure_reference_path,
)

from operationalknowledgeingestion.src.optisweep_ingestion.schemas.runbook_candidate import (
    ALLOWED_PROCEDURE_TYPES,
    ALLOWED_ROLES,
    FORBIDDEN_FIELDS,
)
from operationalknowledgeingestion.src.optisweep_ingestion.tools.artifact_linker import collect_candidate_artifact_ids
from operationalknowledgeingestion.src.optisweep_ingestion.tools.context_id_resolver import resolve_context_ids
from operationalknowledgeingestion.src.optisweep_ingestion.services.id_generator import slugify
from operationalknowledgeingestion.src.optisweep_ingestion.services.source_ref_service import lineage_from_bundle
from operationalknowledgeingestion.src.optisweep_ingestion.utils.json_utils import read_json, write_json

FOUNDRY_API_VERSION = "2025-04-01-preview"
CLASSIC_AZURE_OPENAI_API_VERSION = "2024-10-21"

MAX_SECTION_TEXT_CHARS = 6000
MAX_ARTIFACT_TEXT_CHARS = 1200
MAX_CONTEXT_TEXT_CHARS = 1200


class RunbookFinalizationClient(Protocol):
    def finalize(self, packet: dict[str, Any]) -> dict[str, Any]:
        ...


class AzureOpenAIRunbookFinalizationClient:
    def __init__(
        self,
        endpoint: str | None = None,
        api_key: str | None = None,
        deployment: str | None = None,
        api_version: str | None = None,
        prompt_path: str | Path | None = None,
        structure_reference_path: str | Path | None = None,
    ) -> None:
        load_dotenv()
        self.endpoint = _clean_env_value(endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")).rstrip("/")
        self.api_key = _clean_env_value(api_key or os.getenv("AZURE_OPENAI_API_KEY"))
        self.deployment = _clean_env_value(deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT"))
        env_api_version = _clean_env_value(os.getenv("AZURE_OPENAI_API_VERSION"))
        self.api_version = _clean_env_value(api_version) or self._default_api_version(env_api_version)
        default_prompt = resolve_stage6_operational_prompt_path()
        task_prompt = load_prompt_file(prompt_path or default_prompt)
        self.prompt = compose_stage6_system_prompt(
            task_prompt,
            structure_reference_path=structure_reference_path or resolve_stage6_structure_reference_path(),
        )
        missing = [
            name
            for name, value in [
                ("AZURE_OPENAI_ENDPOINT", self.endpoint),
                ("AZURE_OPENAI_API_KEY", self.api_key),
                ("AZURE_OPENAI_DEPLOYMENT", self.deployment),
                ("AZURE_OPENAI_API_VERSION", self.api_version),
            ]
            if not value
        ]
        if missing:
            raise RuntimeError("Azure OpenAI is not configured. Set these environment variables: " + ", ".join(missing))

    def finalize(self, packet: dict[str, Any]) -> dict[str, Any]:
        body = {
            "messages": [
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": json.dumps(packet, ensure_ascii=False)},
            ],
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
        }
        errors: list[str] = []
        for url, headers, include_model in self._candidate_requests(self.api_version):
            request_body = body | ({"model": self.deployment} if include_model else {})
            request = urllib.request.Request(
                url,
                data=json.dumps(request_body).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            try:
                with urllib.request.urlopen(request, timeout=240) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                return parse_llm_response(payload["choices"][0]["message"]["content"])
            except urllib.error.HTTPError as exc:
                details = exc.read().decode("utf-8", errors="replace")
                errors.append(f"HTTP {exc.code}: {details}")
                if exc.code not in {400, 404}:
                    raise RuntimeError(f"Azure OpenAI request failed with HTTP {exc.code}: {details}") from exc
            except urllib.error.URLError as exc:
                raise RuntimeError(f"Azure OpenAI request failed: {exc.reason}") from exc
        raise RuntimeError("Azure OpenAI request failed for endpoint patterns tried: " + " | ".join(errors))

    def _candidate_requests(self, api_version: str) -> list[tuple[str, dict[str, str], bool]]:
        encoded_deployment = urllib.parse.quote(self.deployment, safe="")
        query = urllib.parse.urlencode({"api-version": api_version})
        headers = {"Content-Type": "application/json", "api-key": self.api_key}
        parsed = urllib.parse.urlparse(self.endpoint)
        if self._is_foundry_project_endpoint():
            foundry_base = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, "", "", "", "")).rstrip("/")
            return [(f"{foundry_base}/models/chat/completions?{query}", headers, True)]
        return [(f"{self.endpoint}/openai/deployments/{encoded_deployment}/chat/completions?{query}", headers, False)]

    def _is_foundry_project_endpoint(self) -> bool:
        parsed = urllib.parse.urlparse(self.endpoint)
        return parsed.netloc.endswith(".services.ai.azure.com") and "/api/projects/" in parsed.path

    def _default_api_version(self, env_api_version: str = "") -> str:
        parsed = urllib.parse.urlparse(self.endpoint)
        if parsed.netloc.endswith(".services.ai.azure.com") and "/api/projects/" in parsed.path:
            return FOUNDRY_API_VERSION
        return env_api_version or CLASSIC_AZURE_OPENAI_API_VERSION


def finalize_operational_runbooks(
    *,
    runbook_candidates_path: str | Path,
    source_artifacts_path: str | Path,
    operational_context_path: str | Path,
    source_bundle_path: str | Path,
    output_dir: str | Path,
    llm_client: RunbookFinalizationClient,
    llm_used: bool = True,
    max_workers: int = 4,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    candidates = read_json(runbook_candidates_path)
    artifacts = read_json(source_artifacts_path)
    contexts = read_json(operational_context_path)
    bundle = read_json(source_bundle_path)
    if not isinstance(candidates, list):
        raise ValueError("runbook_candidates.json must contain a list.")
    if not isinstance(artifacts, list):
        raise ValueError("source_artifacts_enriched.json must contain a list.")
    if not isinstance(contexts, list):
        raise ValueError("operational_context.json must contain a list.")

    lineage = lineage_from_bundle(bundle)
    artifact_index = {str(item.get("artifact_id")): item for item in artifacts if item.get("artifact_id")}
    context_index = {str(item.get("context_id")): item for item in contexts if item.get("context_id")}
    section_index = {str(item.get("section_id")): item for item in (bundle.get("sections") or []) if item.get("section_id")}

    output_path = Path(output_dir)
    finalized_dir = output_path / "finalized_runbooks"
    review_dir = output_path / "review_markdown" / "runbooks"
    finalized_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)

    if not candidates:
        report = _build_report(
            source_id=lineage.source_id,
            source_type=lineage.source_type,
            candidate_count=0,
            finalized_count=0,
            failed=[],
            warnings=["No Stage 5 runbook candidates to finalize."],
            llm_used=llm_used,
        )
        write_json(output_path / "runbook_finalization_report.json", report)
        return [], report

    if not llm_used:
        raise ValueError("Stage 6 requires --llm. Fake runbook finalization is not supported.")

    finalized: list[dict[str, Any]] = []
    failed: list[dict[str, Any]] = []
    warnings: list[str] = []

    packets = [
        build_operational_finalization_packet(
            candidate=candidate,
            artifacts=artifact_index,
            contexts=context_index,
            sections=section_index,
            lineage=lineage,
            all_artifacts=artifacts,
        )
        for candidate in candidates
        if isinstance(candidate, dict)
    ]

    workers = max(1, max_workers)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(_finalize_one, packet, llm_client, artifact_index, context_index): packet
            for packet in packets
        }
        for future in as_completed(futures):
            packet = futures[future]
            candidate_id = str((packet.get("runbook_candidate") or {}).get("candidate_id") or "unknown")
            try:
                runbook, errors = future.result()
            except Exception as exc:
                failed.append({"candidate_id": candidate_id, "error": str(exc)})
                continue
            if errors:
                failed.append({"candidate_id": candidate_id, "error": "; ".join(errors)})
                warnings.append(f"Validation failed for {candidate_id}: {'; '.join(errors)}")
                continue
            write_json(finalized_dir / f"{candidate_id}.json", runbook)
            review_path = review_dir / f"{candidate_id}.md"
            review_path.write_text(
                write_runbook_review_markdown(
                    runbook,
                    artifact_index=artifact_index,
                    review_markdown_path=review_path,
                ),
                encoding="utf-8",
            )
            html_path = review_dir / f"{candidate_id}.html"
            html_path.write_text(
                write_runbook_review_html(
                    runbook,
                    artifact_index=artifact_index,
                    review_html_path=html_path,
                ),
                encoding="utf-8",
            )
            finalized.append(runbook)

    report = _build_report(
        source_id=lineage.source_id,
        source_type=lineage.source_type,
        candidate_count=len(candidates),
        finalized_count=len(finalized),
        failed=failed,
        warnings=warnings,
        llm_used=llm_used,
    )
    write_json(output_path / "runbook_finalization_report.json", report)
    return finalized, report


def build_operational_finalization_packet(
    *,
    candidate: dict[str, Any],
    artifacts: dict[str, dict[str, Any]],
    contexts: dict[str, dict[str, Any]],
    sections: dict[str, dict[str, Any]],
    lineage: Any,
    all_artifacts: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    artifact_list = all_artifacts or list(artifacts.values())
    related_artifact_ids = collect_candidate_artifact_ids(
        candidate,
        artifact_list,
        contexts,
        max_results=10,
    )
    related_context_ids = _string_list(candidate.get("related_context_ids"))
    section_ids = _section_ids_from_refs(candidate.get("source_refs") or [])
    return {
        "packet_type": "stage_6_operational_runbook_finalization_packet",
        "schema_version": "0.1",
        "runbook_candidate": candidate,
        "related_artifacts": [_compact_artifact(artifacts[artifact_id]) for artifact_id in related_artifact_ids if artifact_id in artifacts],
        "related_context_records": [_compact_context(contexts[context_id]) for context_id in related_context_ids if context_id in contexts],
        "source_sections": [_compact_section(sections[section_id]) for section_id in section_ids if section_id in sections],
        "source_lineage": {
            "source_id": lineage.source_id,
            "source_type": lineage.source_type,
            "source_title": lineage.source_title,
            "source_version": lineage.source_version,
            "ingestion_batch_id": lineage.ingestion_batch_id,
        },
        "instructions": [
            "Finalize exactly one source-specific runbook from the supplied candidate.",
            "Use only evidence from this packet.",
            "Do not merge with other candidates or sources.",
        ],
    }


def normalize_runbook(
    response: dict[str, Any],
    candidate: dict[str, Any],
    lineage: Any,
    context_index: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    runbook = response.get("runbook") if isinstance(response.get("runbook"), dict) else dict(response)
    candidate_id = str(candidate.get("candidate_id") or runbook.get("candidate_id") or "").strip()
    title = str(runbook.get("title") or candidate.get("title") or "").strip()
    procedure_id = str(runbook.get("procedure_id") or _procedure_id_from_candidate(candidate_id, title)).strip()
    runbook["procedure_id"] = procedure_id
    runbook["candidate_id"] = candidate_id
    runbook["title"] = title
    runbook["procedure_type"] = _allowed(
        runbook.get("procedure_type") or candidate.get("likely_procedure_type"),
        ALLOWED_PROCEDURE_TYPES,
        "operation",
    )
    runbook["role_required"] = _allowed(
        runbook.get("role_required") or candidate.get("likely_role_required"),
        ALLOWED_ROLES,
        "operator",
    )
    runbook["responsible_role"] = _allowed(runbook.get("responsible_role") or runbook["role_required"], ALLOWED_ROLES, runbook["role_required"])
    runbook["supporting_roles"] = [
        role for role in _string_list(runbook.get("supporting_roles")) if role in ALLOWED_ROLES
    ]
    if candidate.get("support_safe") is not None and runbook.get("support_safe") is None:
        runbook["support_safe"] = candidate.get("support_safe")
    runbook["summary"] = str(runbook.get("summary") or candidate.get("summary") or "").strip()
    runbook["when_to_use"] = str(runbook.get("when_to_use") or candidate.get("candidate_goal") or "").strip()
    runbook["not_for"] = _string_list(runbook.get("not_for"))
    runbook["safety_notes"] = _string_list(runbook.get("safety_notes"))
    runbook["access_or_tools_needed"] = _string_list(runbook.get("access_or_tools_needed")) or _string_list(
        candidate.get("access_or_tools_needed")
    )
    raw_context_ids = _string_list(runbook.get("related_context_ids")) or _string_list(
        candidate.get("related_context_ids")
    )
    if context_index:
        resolved_context_ids, _ = resolve_context_ids(raw_context_ids, context_index)
        runbook["related_context_ids"] = resolved_context_ids
    else:
        runbook["related_context_ids"] = raw_context_ids
    runbook["steps"] = _normalize_steps(runbook.get("steps") or [], candidate.get("rough_steps") or [])
    runbook["success_criteria"] = _string_list(runbook.get("success_criteria"))
    runbook["healthy_conditions"] = _string_list(runbook.get("healthy_conditions"))
    runbook["failure_conditions"] = _string_list(runbook.get("failure_conditions")) or _string_list(
        candidate.get("failure_or_escalation_notes")
    )
    runbook["escalation_guidance"] = _string_list(runbook.get("escalation_guidance"))
    runbook["commands"] = _dict_list(runbook.get("commands"))
    runbook["screens_or_images"] = _dict_list(runbook.get("screens_or_images"))
    runbook["visual_references"] = _dict_list(runbook.get("visual_references"))
    runbook["source_refs"] = _dict_list(runbook.get("source_refs")) or _dict_list(candidate.get("source_refs"))
    runbook["image_refs"] = _dict_list(runbook.get("image_refs"))
    runbook["source_candidate_ids"] = _string_list(runbook.get("source_candidate_ids")) or ([candidate_id] if candidate_id else [])
    runbook["source_lineage"] = _dict_list(runbook.get("source_lineage"))
    runbook["missing_details"] = _string_list(runbook.get("missing_details"))
    runbook["validation_status"] = str(runbook.get("validation_status") or "needs_sme_review")
    metadata = runbook.get("metadata") if isinstance(runbook.get("metadata"), dict) else {}
    metadata.update(
        {
            "product": metadata.get("product") or "OptiSweep",
            "version": metadata.get("version") or 1,
            "merge_status": "source_finalized",
            "created_by": "stage_6_runbook_finalization",
            "source_id": metadata.get("source_id") or lineage.source_id,
            "source_type": metadata.get("source_type") or lineage.source_type,
            "source_title": metadata.get("source_title") or lineage.source_title,
            "source_version": metadata.get("source_version") or lineage.source_version,
            "ingestion_batch_id": metadata.get("ingestion_batch_id") or lineage.ingestion_batch_id,
            "source_quality": metadata.get("source_quality") or candidate.get("metadata", {}).get("source_quality") or lineage.source_type,
        }
    )
    runbook["metadata"] = metadata
    return runbook


def validate_runbook(
    runbook: dict[str, Any],
    known_artifact_ids: set[str],
    known_context_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    for field in ["procedure_id", "candidate_id", "title", "summary"]:
        if not str(runbook.get(field) or "").strip():
            errors.append(f"missing {field}")
    if runbook.get("procedure_type") not in ALLOWED_PROCEDURE_TYPES:
        errors.append("invalid procedure_type")
    if runbook.get("role_required") not in ALLOWED_ROLES:
        errors.append("invalid role_required")
    steps = runbook.get("steps") or []
    if not steps:
        errors.append("missing steps")
    for field in FORBIDDEN_FIELDS:
        if field in runbook:
            errors.append(f"forbidden field present: {field}")
    for artifact_id in _artifact_ids_in_runbook(runbook):
        if artifact_id not in known_artifact_ids:
            errors.append(f"unknown artifact_id: {artifact_id}")
    for context_id in runbook.get("related_context_ids") or []:
        if context_id not in known_context_ids:
            errors.append(f"unknown related_context_id: {context_id}")
    if str(runbook.get("metadata", {}).get("merge_status") or "") != "source_finalized":
        errors.append("metadata.merge_status must be source_finalized")
    return errors


def write_runbook_review_markdown(
    runbook: dict[str, Any],
    *,
    artifact_index: dict[str, dict[str, Any]] | None = None,
    review_markdown_path: str | Path | None = None,
    repo_root: Path | None = None,
) -> str:
    lines: list[str] = []
    metadata = runbook.get("metadata") if isinstance(runbook.get("metadata"), dict) else {}
    review_path = Path(review_markdown_path).resolve() if review_markdown_path else None
    root = repo_root or REPO_ROOT
    asset_link_cache: dict[str, str] = {}
    lines.extend(
        [
            f"# {runbook.get('title') or 'Runbook'}",
            "",
            "## Runbook Header",
            "",
            "| Field | Value |",
            "| --- | --- |",
            f"| Procedure ID | `{runbook.get('procedure_id')}` |",
            f"| Title | {runbook.get('title')} |",
            f"| Procedure Type | `{runbook.get('procedure_type')}` |",
            f"| Primary Role | `{runbook.get('role_required')}` |",
            f"| Supporting Roles | {', '.join(f'`{role}`' for role in runbook.get('supporting_roles') or []) or 'None'} |",
            f"| Support Safe | {'Yes' if runbook.get('support_safe') else 'No'} |",
            f"| Validation Status | `{runbook.get('validation_status')}` |",
            f"| Merge Status | `{metadata.get('merge_status')}` |",
            "",
            "## Summary",
            "",
            str(runbook.get("summary") or ""),
            "",
            "## When To Use",
            "",
            str(runbook.get("when_to_use") or ""),
            "",
        ]
    )
    if runbook.get("not_for"):
        lines.extend(["## Do Not Use For", "", *_bullet_lines(runbook.get("not_for") or []), ""])
    if runbook.get("safety_notes"):
        lines.extend(["## Safety And Operational Notes", "", *_bullet_lines(runbook.get("safety_notes") or []), ""])
    if runbook.get("access_or_tools_needed"):
        lines.extend(["## Access Or Tools Needed", "", *_bullet_lines(runbook.get("access_or_tools_needed") or []), ""])
    if runbook.get("related_context_ids"):
        lines.extend(["## Related Operational Context", "", *_bullet_lines(runbook.get("related_context_ids") or []), ""])
    lines.extend(["## Procedure Steps", ""])
    for step in runbook.get("steps") or []:
        if not isinstance(step, dict):
            continue
        step_number = step.get("step_number") or "?"
        lines.extend(
            [
                f"### Step {step_number} — {step.get('title') or 'Untitled Step'}",
                "",
                f"**Responsible role:** {step.get('responsible_role') or runbook.get('role_required')}",
                "",
                "**Instruction:**",
                str(step.get("instruction") or ""),
                "",
                "**Expected result:**",
                str(step.get("expected_result") or ""),
                "",
            ]
        )
        step_image_lines = _render_screen_or_image_markdown(
            step.get("screens_or_images") or [],
            artifact_index=artifact_index,
            review_markdown_path=review_path,
            repo_root=root,
            asset_link_cache=asset_link_cache,
        )
        if step_image_lines:
            lines.extend(["**Screens / Images:**", "", *step_image_lines, ""])
        if step.get("stop_or_escalate_if"):
            lines.extend(["**Stop or Escalate If:**", "", *_bullet_lines(step.get("stop_or_escalate_if") or []), ""])
        lines.append("---")
        lines.append("")
    if runbook.get("success_criteria"):
        lines.extend(["## Success Criteria", "", *_bullet_lines(runbook.get("success_criteria") or []), ""])
    if runbook.get("failure_conditions"):
        lines.extend(["## Failure Conditions", "", *_bullet_lines(runbook.get("failure_conditions") or []), ""])
    if runbook.get("escalation_guidance"):
        lines.extend(["## Escalation Guidance", "", *_bullet_lines(runbook.get("escalation_guidance") or []), ""])
    if runbook.get("missing_details"):
        lines.extend(["## Missing Details / Known Gaps", "", *_bullet_lines(runbook.get("missing_details") or []), ""])
    lines.extend(
        [
            "## Source Lineage",
            "",
            f"- Candidate IDs: {', '.join(runbook.get('source_candidate_ids') or [])}",
            f"- Source ID: `{metadata.get('source_id')}`",
            f"- Source Type: `{metadata.get('source_type')}`",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_runbook_review_html(
    runbook: dict[str, Any],
    *,
    artifact_index: dict[str, dict[str, Any]] | None = None,
    review_html_path: str | Path | None = None,
    repo_root: Path | None = None,
) -> str:
    review_path = Path(review_html_path).resolve() if review_html_path else None
    root = repo_root or REPO_ROOT
    asset_link_cache: dict[str, str] = {}
    metadata = runbook.get("metadata") if isinstance(runbook.get("metadata"), dict) else {}
    title = html.escape(str(runbook.get("title") or "Runbook"))
    parts = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        f"<title>{title}</title>",
        "<style>",
        "body { font-family: Segoe UI, Arial, sans-serif; max-width: 960px; margin: 2rem auto; line-height: 1.5; }",
        "table { border-collapse: collapse; width: 100%; margin: 1rem 0; }",
        "th, td { border: 1px solid #ccc; padding: 0.5rem; text-align: left; vertical-align: top; }",
        "figure { margin: 1rem 0; }",
        "img { max-width: 100%; height: auto; border: 1px solid #ddd; }",
        "figcaption { font-style: italic; color: #555; margin-top: 0.5rem; }",
        "hr { margin: 2rem 0; }",
        "</style>",
        "</head>",
        "<body>",
        f"<h1>{title}</h1>",
        "<h2>Runbook Header</h2>",
        "<table>",
        f"<tr><th>Procedure ID</th><td>{html.escape(str(runbook.get('procedure_id') or ''))}</td></tr>",
        f"<tr><th>Title</th><td>{title}</td></tr>",
        f"<tr><th>Procedure Type</th><td>{html.escape(str(runbook.get('procedure_type') or ''))}</td></tr>",
        f"<tr><th>Primary Role</th><td>{html.escape(str(runbook.get('role_required') or ''))}</td></tr>",
        f"<tr><th>Support Safe</th><td>{'Yes' if runbook.get('support_safe') else 'No'}</td></tr>",
        f"<tr><th>Validation Status</th><td>{html.escape(str(runbook.get('validation_status') or ''))}</td></tr>",
        f"<tr><th>Merge Status</th><td>{html.escape(str(metadata.get('merge_status') or ''))}</td></tr>",
        "</table>",
        "<h2>Summary</h2>",
        f"<p>{html.escape(str(runbook.get('summary') or ''))}</p>",
        "<h2>When To Use</h2>",
        f"<p>{html.escape(str(runbook.get('when_to_use') or ''))}</p>",
    ]
    parts.append("<h2>Procedure Steps</h2>")
    for step in runbook.get("steps") or []:
        if not isinstance(step, dict):
            continue
        step_number = step.get("step_number") or "?"
        step_title = html.escape(str(step.get("title") or "Untitled Step"))
        parts.extend(
            [
                f"<h3>Step {html.escape(str(step_number))} — {step_title}</h3>",
                f"<p><strong>Responsible role:</strong> {html.escape(str(step.get('responsible_role') or runbook.get('role_required') or ''))}</p>",
                "<p><strong>Instruction:</strong></p>",
                f"<p>{html.escape(str(step.get('instruction') or ''))}</p>",
                "<p><strong>Expected result:</strong></p>",
                f"<p>{html.escape(str(step.get('expected_result') or ''))}</p>",
            ]
        )
        step_blocks = _render_screen_or_image_html(
            step.get("screens_or_images") or [],
            artifact_index=artifact_index,
            review_markdown_path=review_path,
            repo_root=root,
            asset_link_cache=asset_link_cache,
        )
        if step_blocks:
            parts.extend(["<p><strong>Screens / Images:</strong></p>", *step_blocks])
        if step.get("stop_or_escalate_if"):
            parts.append("<p><strong>Stop or Escalate If:</strong></p><ul>")
            for item in step.get("stop_or_escalate_if") or []:
                parts.append(f"<li>{html.escape(str(item))}</li>")
            parts.append("</ul>")
        parts.append("<hr>")
    parts.extend(["</body>", "</html>"])
    return "\n".join(parts)


def parse_llm_response(content: str | dict[str, Any]) -> dict[str, Any]:
    if isinstance(content, dict):
        return content
    text = content.strip()
    fence = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if fence:
        text = fence.group(1).strip()
    return json.loads(text)


def _finalize_one(
    packet: dict[str, Any],
    llm_client: RunbookFinalizationClient,
    artifact_index: dict[str, dict[str, Any]],
    context_index: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], list[str]]:
    candidate = packet.get("runbook_candidate") or {}
    lineage = packet.get("source_lineage") or {}
    response = llm_client.finalize(packet)
    runbook = normalize_runbook(response, candidate, _LineageAdapter(lineage), context_index)
    errors = validate_runbook(
        runbook,
        set(artifact_index),
        set(context_index),
    )
    return runbook, errors


class _LineageAdapter:
    def __init__(self, data: dict[str, Any]) -> None:
        self.source_id = str(data.get("source_id") or "")
        self.source_type = str(data.get("source_type") or "")
        self.source_title = str(data.get("source_title") or "")
        self.source_version = str(data.get("source_version") or "")
        self.ingestion_batch_id = str(data.get("ingestion_batch_id") or "")


def _build_report(
    *,
    source_id: str,
    source_type: str,
    candidate_count: int,
    finalized_count: int,
    failed: list[dict[str, Any]],
    warnings: list[str],
    llm_used: bool,
) -> dict[str, Any]:
    return {
        "stage": "stage_6_operational_runbook_finalization",
        "llm_used": llm_used,
        "prompt": "stage_prompts/stage_6/stage6_operational_runbook_finalization_prompt.md",
        "structure_reference": "stage_prompts/stage_6/stage6_runbook_finalization_structure_reference.md",
        "source_id": source_id,
        "source_type": source_type,
        "candidate_count": candidate_count,
        "finalized_runbook_count": finalized_count,
        "failed_candidate_count": len(failed),
        "failed_candidates": failed,
        "warnings": warnings,
        "notes": [
            "Stage 6 finalizes source-specific runbooks from Stage 5 candidates.",
            "Cross-source merging happens at Shared Stage 6.5/7.",
        ],
        "built_at": datetime.now(UTC).isoformat(),
    }


def _procedure_id_from_candidate(candidate_id: str, title: str) -> str:
    base = candidate_id.removeprefix("candidate_") if candidate_id else slugify(title)
    slug = slugify(base) or slugify(title) or "procedure"
    return f"proc_{slug}_v1"


def _normalize_steps(raw_steps: list[Any], rough_steps: list[str]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for index, step in enumerate(raw_steps, start=1):
        if not isinstance(step, dict):
            continue
        record = dict(step)
        record["step_number"] = int(record.get("step_number") or index)
        record["title"] = str(record.get("title") or f"Step {index}").strip()
        record["instruction"] = str(record.get("instruction") or "").strip()
        record["expected_result"] = str(record.get("expected_result") or "").strip()
        record["actions"] = _dict_list(record.get("actions"))
        record["commands"] = _dict_list(record.get("commands"))
        record["screens_or_images"] = _dict_list(record.get("screens_or_images"))
        record["stop_or_escalate_if"] = _string_list(record.get("stop_or_escalate_if"))
        record["source_evidence"] = _dict_list(record.get("source_evidence"))
        normalized.append(record)
    if normalized:
        return normalized
    return [
        {
            "step_number": index,
            "title": f"Step {index}",
            "instruction": step,
            "expected_result": "",
            "actions": [],
            "commands": [],
            "screens_or_images": [],
            "stop_or_escalate_if": [],
            "source_evidence": [],
        }
        for index, step in enumerate(rough_steps, start=1)
        if str(step).strip()
    ]


def _artifact_ids_in_runbook(runbook: dict[str, Any]) -> set[str]:
    artifact_ids: set[str] = set()
    for ref in runbook.get("visual_references") or []:
        if isinstance(ref, dict) and ref.get("artifact_id"):
            artifact_ids.add(str(ref["artifact_id"]))
    for ref in runbook.get("screens_or_images") or []:
        if isinstance(ref, dict) and ref.get("artifact_id"):
            artifact_ids.add(str(ref["artifact_id"]))
    for step in runbook.get("steps") or []:
        if not isinstance(step, dict):
            continue
        for ref in step.get("screens_or_images") or []:
            if isinstance(ref, dict) and ref.get("artifact_id"):
                artifact_ids.add(str(ref["artifact_id"]))
    return artifact_ids


def _section_ids_from_refs(refs: list[Any]) -> list[str]:
    section_ids: list[str] = []
    seen: set[str] = set()
    for ref in refs:
        if not isinstance(ref, dict):
            continue
        section_id = str(ref.get("section_id") or "").strip()
        if section_id and section_id not in seen:
            seen.add(section_id)
            section_ids.append(section_id)
    return section_ids


def _compact_artifact(artifact: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_id": artifact.get("artifact_id"),
        "page_number": artifact.get("page_number"),
        "image_type": artifact.get("image_type"),
        "short_description": _truncate(artifact.get("short_description") or artifact.get("summary"), MAX_ARTIFACT_TEXT_CHARS),
        "retrieval_text": _truncate(artifact.get("retrieval_text"), MAX_ARTIFACT_TEXT_CHARS),
        "source_refs": artifact.get("source_refs") or [],
        "image_ref": artifact.get("image_ref"),
    }


def _compact_context(context: dict[str, Any]) -> dict[str, Any]:
    return {
        "context_id": context.get("context_id"),
        "context_type": context.get("context_type"),
        "title": context.get("title"),
        "summary": _truncate(context.get("summary"), MAX_CONTEXT_TEXT_CHARS),
        "retrieval_text": _truncate(context.get("retrieval_text"), MAX_CONTEXT_TEXT_CHARS),
        "source_refs": context.get("source_refs") or [],
        "image_refs": context.get("image_refs") or [],
    }


def _compact_section(section: dict[str, Any]) -> dict[str, Any]:
    return {
        "section_id": section.get("section_id"),
        "heading": section.get("heading"),
        "page_start": section.get("page_start"),
        "page_end": section.get("page_end"),
        "text": _truncate(section.get("text"), MAX_SECTION_TEXT_CHARS),
    }


def _allowed(value: Any, allowed: set[str], default: str) -> str:
    text = str(value or "").strip()
    return text if text in allowed else default


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _dict_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _truncate(value: Any, max_chars: int) -> str:
    text = " ".join(str(value or "").split())
    if len(text) <= max_chars:
        return text
    return text[: max(0, max_chars - 3)].rstrip() + "..."


def _resolve_artifact_image_path(raw_path: str, repo_root: Path = REPO_ROOT) -> Path | None:
    cleaned = str(raw_path or "").strip()
    if not cleaned:
        return None
    normalized = Path(cleaned.replace("\\", "/"))
    candidates = [
        normalized,
        repo_root / normalized,
        repo_root / "operationalknowledgeingestion" / normalized,
        repo_root / "incidenceknowledgeingestion" / normalized,
        Path.cwd() / normalized,
    ]
    seen: set[Path] = set()
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        if resolved in seen:
            continue
        seen.add(resolved)
        if resolved.is_file():
            return resolved
    return None


def _review_assets_dir(review_markdown_path: Path) -> Path:
    return review_markdown_path.resolve().parent / "assets"


def _asset_copy_name(artifact_id: str, suffix: str) -> str:
    digest = hashlib.sha1(artifact_id.encode("utf-8")).hexdigest()[:16]
    return f"{digest}{suffix.lower()}"


def _copy_review_asset(source: Path, review_markdown_path: Path, artifact_id: str) -> str:
    assets_dir = _review_assets_dir(review_markdown_path)
    assets_dir.mkdir(parents=True, exist_ok=True)
    dest = assets_dir / _asset_copy_name(artifact_id, source.suffix)
    if not dest.exists() or dest.stat().st_size != source.stat().st_size:
        shutil.copy2(source, dest)
    return f"assets/{dest.name}".replace("\\", "/")


def _review_asset_link(
    artifact_id: str,
    image_path: Path,
    review_markdown_path: Path,
    asset_link_cache: dict[str, str],
) -> str:
    cached = asset_link_cache.get(artifact_id)
    if cached:
        return cached
    link = _copy_review_asset(image_path, review_markdown_path, artifact_id)
    asset_link_cache[artifact_id] = link
    return link


def _markdown_image_link(image_path: Path, markdown_dir: Path) -> str:
    relative = os.path.relpath(image_path, markdown_dir.resolve())
    return relative.replace("\\", "/").replace(" ", "%20")


def _screen_or_image_caption(ref: dict[str, Any]) -> str:
    return str(
        ref.get("what_to_look_at")
        or ref.get("description")
        or ref.get("caption")
        or ""
    ).strip()


def _render_screen_or_image_markdown(
    refs: list[Any],
    *,
    artifact_index: dict[str, dict[str, Any]] | None,
    review_markdown_path: Path | None,
    repo_root: Path,
    asset_link_cache: dict[str, str] | None = None,
) -> list[str]:
    lines: list[str] = []
    seen_artifact_ids: set[str] = set()
    cache = asset_link_cache if asset_link_cache is not None else {}
    for ref in refs:
        if not isinstance(ref, dict):
            continue
        artifact_id = str(ref.get("artifact_id") or "").strip()
        if not artifact_id or artifact_id in seen_artifact_ids:
            continue
        seen_artifact_ids.add(artifact_id)
        caption = _screen_or_image_caption(ref)
        artifact = (artifact_index or {}).get(artifact_id)
        image_path = None
        if artifact:
            image_path = _resolve_artifact_image_path(
                str(artifact.get("storage_path") or artifact.get("image_ref") or ""),
                repo_root=repo_root,
            )
        if image_path and review_markdown_path:
            link = _review_asset_link(artifact_id, image_path, review_markdown_path, cache)
            lines.extend(
                [
                    f"![{artifact_id}]({link})",
                    "",
                ]
            )
            if caption:
                lines.extend([f"*{caption}*", ""])
            continue
        if caption:
            lines.append(f"- `{artifact_id}`: {caption}")
        else:
            lines.append(f"- `{artifact_id}`")
    return lines


def _render_screen_or_image_html(
    refs: list[Any],
    *,
    artifact_index: dict[str, dict[str, Any]] | None,
    review_markdown_path: Path | None,
    repo_root: Path,
    asset_link_cache: dict[str, str] | None = None,
) -> list[str]:
    blocks: list[str] = []
    seen_artifact_ids: set[str] = set()
    cache = asset_link_cache if asset_link_cache is not None else {}
    for ref in refs:
        if not isinstance(ref, dict):
            continue
        artifact_id = str(ref.get("artifact_id") or "").strip()
        if not artifact_id or artifact_id in seen_artifact_ids:
            continue
        seen_artifact_ids.add(artifact_id)
        caption = _screen_or_image_caption(ref)
        artifact = (artifact_index or {}).get(artifact_id)
        image_path = None
        if artifact:
            image_path = _resolve_artifact_image_path(
                str(artifact.get("storage_path") or artifact.get("image_ref") or ""),
                repo_root=repo_root,
            )
        if image_path and review_markdown_path:
            link = _review_asset_link(artifact_id, image_path, review_markdown_path, cache)
            safe_caption = html.escape(caption or artifact_id)
            blocks.append(
                "<figure>"
                f'<img src="{html.escape(link, quote=True)}" alt="{html.escape(artifact_id, quote=True)}" />'
                f"<figcaption>{safe_caption}</figcaption>"
                "</figure>"
            )
            continue
        if caption:
            blocks.append(f"<p><code>{html.escape(artifact_id)}</code>: {html.escape(caption)}</p>")
        else:
            blocks.append(f"<p><code>{html.escape(artifact_id)}</code></p>")
    return blocks


def _markdown_image_alt(text: str) -> str:
    cleaned = (
        str(text or "")
        .replace("`", "")
        .replace("[", "")
        .replace("]", "")
        .replace("\\", "/")
        .replace("\n", " ")
        .strip()
    )
    return cleaned or "screenshot"


def _bullet_lines(items: list[str]) -> list[str]:
    return [f"* {item}" for item in items if str(item).strip()]


def _clean_env_value(value: str | None) -> str:
    cleaned = (value or "").strip().strip('"').strip("'")
    if cleaned in {"", "your-api-version", "your_api_version", "<api-version>"}:
        return ""
    return cleaned
