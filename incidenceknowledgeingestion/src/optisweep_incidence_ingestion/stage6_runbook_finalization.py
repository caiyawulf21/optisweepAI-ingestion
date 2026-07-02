"""Stage 6 - Incident source runbook finalization from Stage 5 candidates."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

from dotenv import load_dotenv

from optisweep_incidence_ingestion.utils.json_utils import read_json, write_json

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from shared.stage_prompts import (
    compose_stage6_system_prompt,
    load_prompt_file,
    resolve_stage6_incident_prompt_path,
    resolve_stage6_structure_reference_path,
)
from optisweep_ingestion.stage6_runbook_finalization import (
    normalize_runbook,
    parse_llm_response,
    validate_runbook,
    write_runbook_review_html,
    write_runbook_review_markdown,
)

FOUNDRY_API_VERSION = "2025-04-01-preview"
CLASSIC_AZURE_OPENAI_API_VERSION = "2024-10-21"

MAX_CHARS = 900
MAX_PAGE_CHUNK_TEXT_CHARS = 5000


class Stage6RunbookFinalizationClient(Protocol):
    def finalize(self, packet: dict[str, Any]) -> dict[str, Any]:
        ...


class AzureOpenAIStage6RunbookFinalizationClient:
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
        default_prompt = resolve_stage6_incident_prompt_path()
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
                with _urlopen_no_proxy(request, timeout=240) as response:
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


def create_stage6_incident_runbooks(
    *,
    runbook_candidates_path: str | Path,
    source_artifacts_enriched_path: str | Path,
    canonical_incident_record_path: str | Path,
    timeline_events_path: str | Path,
    stage4_evidence_chunks_path: str | Path,
    source_package_path: str | Path,
    output_dir: str | Path,
    llm_client: Stage6RunbookFinalizationClient,
    max_workers: int = 4,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    candidates = read_json(runbook_candidates_path)
    artifacts = read_json(source_artifacts_enriched_path)
    canonical_record = read_json(canonical_incident_record_path)
    timeline = read_json(timeline_events_path)
    evidence_handoff = read_json(stage4_evidence_chunks_path)
    package = read_json(source_package_path)
    if not isinstance(candidates, list):
        raise ValueError("runbook_candidates.json must contain a list.")
    if not isinstance(artifacts, list):
        raise ValueError("source_artifacts_enriched.json must contain a list.")

    artifact_index = {str(item.get("artifact_id")): item for item in artifacts if item.get("artifact_id")}
    event_index = {str(item.get("event_id")): item for item in (timeline.get("events") or []) if item.get("event_id")}
    source_package = _compact_source_package(package, canonical_record)

    output_path = Path(output_dir)
    finalized_dir = output_path / "finalized_runbooks"
    review_dir = output_path / "review_markdown" / "runbooks"
    finalized_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)

    if not candidates:
        report = _build_report(
            source_id=source_package.get("source_id"),
            source_case_id=source_package.get("source_case_id"),
            candidate_count=0,
            finalized_count=0,
            failed=[],
            warnings=["No Stage 5 runbook candidates to finalize."],
        )
        write_json(output_path / "runbook_finalization_report.json", report)
        write_json(output_path / "incident_source_package.json", _package_with_stage6_refs(package, output_path, report))
        return [], report

    finalized: list[dict[str, Any]] = []
    failed: list[dict[str, Any]] = []
    warnings: list[str] = []
    packets = [
        build_incident_finalization_packet(
            candidate=candidate,
            artifacts=artifact_index,
            events=event_index,
            canonical_record=canonical_record,
            evidence_handoff=evidence_handoff,
            source_package=source_package,
        )
        for candidate in candidates
        if isinstance(candidate, dict)
    ]

    workers = max(1, max_workers)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(_finalize_one, packet, llm_client, artifact_index): packet
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
            review_path = output_path / f"{candidate_id}_review.md"
            review_path.write_text(
                write_runbook_review_markdown(
                    runbook,
                    artifact_index=artifact_index,
                    review_markdown_path=review_path,
                ),
                encoding="utf-8",
            )
            html_path = output_path / f"{candidate_id}_review.html"
            html_path.write_text(
                write_runbook_review_html(
                    runbook,
                    artifact_index=artifact_index,
                    review_html_path=html_path,
                ),
                encoding="utf-8",
            )
            legacy_review_path = review_dir / f"{candidate_id}.md"
            legacy_review_path.write_text(
                write_runbook_review_markdown(
                    runbook,
                    artifact_index=artifact_index,
                    review_markdown_path=legacy_review_path,
                ),
                encoding="utf-8",
            )
            legacy_html_path = review_dir / f"{candidate_id}.html"
            legacy_html_path.write_text(
                write_runbook_review_html(
                    runbook,
                    artifact_index=artifact_index,
                    review_html_path=legacy_html_path,
                ),
                encoding="utf-8",
            )
            finalized.append(runbook)

    report = _build_report(
        source_id=source_package.get("source_id"),
        source_case_id=source_package.get("source_case_id"),
        candidate_count=len(candidates),
        finalized_count=len(finalized),
        failed=failed,
        warnings=warnings,
    )
    write_json(output_path / "runbook_finalization_report.json", report)
    write_json(output_path / "incident_source_package.json", _package_with_stage6_refs(package, output_path, report))
    return finalized, report


def build_incident_finalization_packet(
    *,
    candidate: dict[str, Any],
    artifacts: dict[str, dict[str, Any]],
    events: dict[str, dict[str, Any]],
    canonical_record: dict[str, Any],
    evidence_handoff: dict[str, Any],
    source_package: dict[str, Any],
) -> dict[str, Any]:
    related_artifact_ids = _string_list(candidate.get("related_artifact_ids"))
    related_event_ids = _string_list(candidate.get("related_event_ids"))
    chunk_ids = _chunk_ids_from_refs(candidate.get("source_refs") or [])
    return {
        "packet_type": "stage_6_incident_runbook_finalization_packet",
        "schema_version": "0.1",
        "runbook_candidate": candidate,
        "related_artifacts": [_compact_artifact(artifacts[artifact_id]) for artifact_id in related_artifact_ids if artifact_id in artifacts],
        "timeline_events": [_compact_event(events[event_id]) for event_id in related_event_ids if event_id in events],
        "canonical_incident_record": _compact_canonical_record(canonical_record),
        "evidence_chunks": {
            "page_text_chunks": [
                _compact_page_text_chunk(chunk)
                for chunk in evidence_handoff.get("page_text_chunks") or []
                if isinstance(chunk, dict) and str(chunk.get("chunk_id") or "") in chunk_ids
            ],
            "artifact_evidence_chunks": [
                chunk
                for chunk in evidence_handoff.get("artifact_evidence_chunks") or []
                if isinstance(chunk, dict) and str(chunk.get("chunk_id") or "") in chunk_ids
            ],
        },
        "source_package": source_package,
        "instructions": [
            "Finalize exactly one incident-derived source-specific runbook from the supplied candidate.",
            "Use only incident evidence from this packet.",
            "Do not merge with other candidates or sources.",
        ],
    }


def _finalize_one(
    packet: dict[str, Any],
    llm_client: Stage6RunbookFinalizationClient,
    artifact_index: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], list[str]]:
    candidate = packet.get("runbook_candidate") or {}
    source_package = packet.get("source_package") or {}
    lineage = _LineageAdapter(source_package, candidate)
    response = llm_client.finalize(packet)
    runbook = normalize_runbook(response, candidate, lineage)
    if not runbook.get("related_event_ids"):
        runbook["related_event_ids"] = _string_list(candidate.get("related_event_ids"))
    metadata = runbook.get("metadata") if isinstance(runbook.get("metadata"), dict) else {}
    metadata["created_by"] = "stage_6_incident_runbook_finalization"
    metadata["source_quality"] = "incident_case"
    metadata["incident_context"] = candidate.get("metadata", {}).get("incident_context") or {
        "case_id": source_package.get("source_case_id") or "",
    }
    runbook["metadata"] = metadata
    errors = validate_runbook(runbook, set(artifact_index), set())
    return runbook, errors


class _LineageAdapter:
    def __init__(self, source_package: dict[str, Any], candidate: dict[str, Any]) -> None:
        self.source_id = str(source_package.get("source_id") or candidate.get("source_id") or "")
        self.source_type = "incident_case"
        self.source_title = str(source_package.get("source_title") or candidate.get("source_title") or "")
        self.source_version = str(candidate.get("source_version") or "")
        self.ingestion_batch_id = str(source_package.get("ingestion_batch_id") or candidate.get("ingestion_batch_id") or "")


def _build_report(
    *,
    source_id: str | None,
    source_case_id: str | None,
    candidate_count: int,
    finalized_count: int,
    failed: list[dict[str, Any]],
    warnings: list[str],
) -> dict[str, Any]:
    return {
        "stage": "stage_6_incident_runbook_finalization",
        "llm_used": True,
        "prompt": "stage_prompts/stage_6/stage6_incident_runbook_finalization_prompt.md",
        "structure_reference": "stage_prompts/stage_6/stage6_runbook_finalization_structure_reference.md",
        "source_id": source_id,
        "source_case_id": source_case_id,
        "candidate_count": candidate_count,
        "finalized_runbook_count": finalized_count,
        "failed_candidate_count": len(failed),
        "failed_candidates": failed,
        "warnings": warnings,
        "notes": [
            "Stage 6 finalizes incident-derived source-specific runbooks from Stage 5 runbook candidates only.",
            "Playbook Prompt A/B outputs are not finalized in Stage 6.",
            "Cross-source merging happens at Shared Stage 6.5/7.",
        ],
        "built_at": datetime.now(timezone.utc).isoformat(),
    }


def _package_with_stage6_refs(
    package: dict[str, Any],
    output_path: Path,
    report: dict[str, Any],
) -> dict[str, Any]:
    enriched_package = dict(package)
    source_bundle = dict(enriched_package.get("source_bundle") or {})
    stage_status = dict(source_bundle.get("stage_status") or {})
    stage_status.update(
        {
            "stage_6": "complete",
            "ready_for_shared_runbook_pool": report.get("failed_candidate_count", 0) == 0,
        }
    )
    file_refs = dict(source_bundle.get("file_refs") or {})
    file_refs.update(
        {
            "runbook_finalization_report": str(output_path / "runbook_finalization_report.json"),
            "finalized_runbooks_dir": str(output_path / "finalized_runbooks"),
            "finalized_runbooks_review_dir": str(output_path / "review_markdown" / "runbooks"),
        }
    )
    source_bundle["stage_status"] = stage_status
    source_bundle["file_refs"] = file_refs
    enriched_package["source_bundle"] = source_bundle
    enriched_package["stage6_output_refs"] = file_refs
    return enriched_package


def _compact_source_package(package: dict[str, Any], canonical_record: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_package_id": package.get("source_package_id"),
        "source_id": package.get("source_id"),
        "source_case_id": package.get("source_case_id") or canonical_record.get("source_case_id"),
        "source_title": package.get("source_title"),
        "source_type": package.get("source_type") or "incident_case",
        "ingestion_batch_id": package.get("ingestion_batch_id"),
    }


def _compact_canonical_record(record: dict[str, Any]) -> dict[str, Any]:
    site = record.get("site") if isinstance(record.get("site"), dict) else {}
    return {
        "incident_id": record.get("incident_id"),
        "source_case_id": record.get("source_case_id"),
        "title": record.get("title"),
        "status": record.get("status"),
        "site_label": site.get("primary_label") or site.get("observed_location_text") or "",
        "what_resolved_it": _truncate(record.get("what_resolved_it"), MAX_CHARS),
        "symptoms": record.get("symptoms") or [],
        "systems_involved": record.get("systems_involved") or [],
    }


def _compact_event(event: dict[str, Any]) -> dict[str, Any]:
    return {
        "event_id": event.get("event_id"),
        "event_order": event.get("event_order"),
        "timestamp": event.get("timestamp"),
        "event_type": event.get("event_type"),
        "actor_role": event.get("actor_role"),
        "summary": _truncate(event.get("summary"), MAX_CHARS),
        "details": _truncate(event.get("details"), MAX_CHARS),
        "systems": event.get("systems") or [],
        "source_refs": event.get("source_refs") or [],
        "artifact_refs": event.get("artifact_refs") or [],
    }


def _compact_page_text_chunk(chunk: dict[str, Any]) -> dict[str, Any]:
    return {
        "chunk_id": chunk.get("chunk_id"),
        "page_refs": chunk.get("page_refs") or [],
        "text": _truncate(chunk.get("text") or chunk.get("combined_text") or "", MAX_PAGE_CHUNK_TEXT_CHARS),
    }


def _compact_artifact(artifact: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_id": artifact.get("artifact_id"),
        "page_number": artifact.get("page_number"),
        "image_type": artifact.get("image_type"),
        "evidence_role": artifact.get("evidence_role"),
        "short_description": _truncate(artifact.get("short_description"), MAX_CHARS),
        "retrieval_text": _truncate(artifact.get("retrieval_text"), MAX_CHARS),
        "source_refs": artifact.get("source_refs") or [],
    }


def _chunk_ids_from_refs(refs: list[Any]) -> set[str]:
    chunk_ids: set[str] = set()
    for ref in refs:
        if isinstance(ref, dict) and ref.get("chunk_id"):
            chunk_ids.add(str(ref["chunk_id"]))
    return chunk_ids


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _truncate(value: Any, max_chars: int) -> str:
    text = " ".join(str(value or "").split())
    if len(text) <= max_chars:
        return text
    return text[: max(0, max_chars - 3)].rstrip() + "..."


def _clean_env_value(value: str | None) -> str:
    cleaned = (value or "").strip().strip('"').strip("'")
    if cleaned in {"", "your-api-version", "your_api_version", "<api-version>"}:
        return ""
    return cleaned


def _urlopen_no_proxy(request: urllib.request.Request, timeout: int) -> Any:
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    return opener.open(request, timeout=timeout)
