"""Stage 5 LLM discovery helpers for source-derived runbook candidates."""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Protocol

from dotenv import load_dotenv

from optisweep_ingestion.schemas.runbook_candidate import (
    ALLOWED_CONFIDENCE,
    ALLOWED_PROCEDURE_TYPES,
    ALLOWED_ROLES,
    FORBIDDEN_FIELDS,
)
from optisweep_ingestion.services.id_generator import make_candidate_id
from optisweep_ingestion.services.source_ref_service import apply_lineage, build_source_ref, lineage_from_bundle
from optisweep_ingestion.tools.report_writer import write_source_extraction_report
from optisweep_ingestion.utils.json_utils import read_json, write_json

FOUNDRY_API_VERSION = "2025-04-01-preview"
CLASSIC_AZURE_OPENAI_API_VERSION = "2024-10-21"

MAX_SECTION_TEXT_CHARS = 4500
MAX_CONTEXTS_PER_PACKET = 8
MAX_ARTIFACTS_PER_PACKET = 8
MAX_CANDIDATES = 200

PROCEDURAL_SECTION_KEYWORDS = [
    "starting",
    "stopping",
    "start",
    "stop",
    "startup",
    "shutdown",
    "operation",
    "operating",
    "add",
    "remove",
    "removal",
    "reset",
    "recover",
    "recovery",
    "fault",
    "initialize",
    "reference",
    "referencing",
    "jog",
    "home",
    "loto",
    "lockout",
    "tagout",
    "replacement",
    "installation",
    "inspect",
    "inspection",
    "maintenance",
    "scanner",
    "commissioning",
    "checklist",
    "download",
    "firmware",
    "after",
]

REQUIRED_PRIORITY_CANDIDATES = {
    "Start OptiSweep System": ["start", "system"],
    "Stop OptiSweep System": ["stop", "system"],
    "Start Operator Station": ["start", "operator station"],
    "Stop Operator Station": ["stop", "operator station"],
    "Check Tipper Heartbeat Stats": ["heartbeat"],
    "Check Operator Station Alarms": ["operator station", "alarm"],
    "Review VISU_IO_DIAG Screen": ["visu_io_diag"],
    "Use Hospital Add Tote Screen": ["add tote"],
    "Use Hospital Remove Tote Screen": ["remove tote"],
    "Recover AGV Bump Fault": ["agv", "bump"],
    "Recover Faulted AGV With Tote": ["faulted agv", "tote"],
    "Initialize Tote With Sorter Scanner": ["sorter", "scanner", "tote"],
}

IMPORTANT_SECTION_KEYWORDS = [
    "safety",
    "loto",
    "lockout",
    "overview",
    "hmi",
    "screen",
    "alarm",
    "fault",
    "operation",
    "operating",
    "startup",
    "starting",
    "stopping",
    "shutdown",
    "agv",
    "hospital",
    "operator station",
    "tipper",
    "sorter",
    "scanner",
    "troubleshoot",
    "maintenance",
    "replacement",
    "removal",
    "installation",
    "referencing",
    "commissioning",
    "checklist",
    "firmware",
    "after a power",
]


class CandidateLLMClient(Protocol):
    def discover(self, packet: dict[str, Any]) -> list[dict[str, Any]]:
        ...


class AzureOpenAIRunbookCandidateClient:
    def __init__(
        self,
        endpoint: str | None = None,
        api_key: str | None = None,
        deployment: str | None = None,
        api_version: str | None = None,
        prompt_path: str | Path | None = None,
    ) -> None:
        load_dotenv()
        self.endpoint = _clean_env_value(endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")).rstrip("/")
        self.api_key = _clean_env_value(api_key or os.getenv("AZURE_OPENAI_API_KEY"))
        self.deployment = _clean_env_value(deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT"))
        env_api_version = _clean_env_value(os.getenv("AZURE_OPENAI_API_VERSION"))
        self.api_version = _clean_env_value(api_version) or self._default_api_version(env_api_version)
        default_prompt = Path(__file__).resolve().parents[1] / "prompts" / "runbook_candidate_discovery_prompt.md"
        self.prompt = Path(prompt_path or default_prompt).read_text(encoding="utf-8")
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

    def discover(self, packet: dict[str, Any]) -> list[dict[str, Any]]:
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
                with urllib.request.urlopen(request, timeout=120) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                return parse_candidate_response(payload["choices"][0]["message"]["content"])
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


def extract_runbook_candidates(
    source_bundle_path: str | Path,
    source_artifacts_path: str | Path,
    operational_context_path: str | Path,
    output_dir: str | Path,
    llm_client: CandidateLLMClient,
    llm_used: bool = True,
    max_workers: int = 4,
    backfill_missing_sections: bool = False,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    bundle = read_json(source_bundle_path)
    artifacts = read_json(source_artifacts_path)
    contexts = read_json(operational_context_path)
    if not isinstance(artifacts, list):
        raise ValueError("source_artifacts_enriched.json must contain a list.")
    if not isinstance(contexts, list):
        raise ValueError("operational_context.json must contain a list.")

    lineage = lineage_from_bundle(bundle)
    known_artifact_ids = {a["artifact_id"] for a in artifacts if a.get("artifact_id")}
    known_context_ids = {c["context_id"] for c in contexts if c.get("context_id")}
    packets = build_candidate_packets(bundle, artifacts, contexts, lineage)

    # Build a focused backfill client using the backfill prompt if available
    backfill_client: CandidateLLMClient = llm_client
    if isinstance(llm_client, AzureOpenAIRunbookCandidateClient):
        backfill_prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "runbook_candidate_backfill_prompt.md"
        if backfill_prompt_path.exists():
            backfill_client = AzureOpenAIRunbookCandidateClient(
                endpoint=llm_client.endpoint,
                api_key=llm_client.api_key,
                deployment=llm_client.deployment,
                api_version=llm_client.api_version,
                prompt_path=backfill_prompt_path,
            )

    collected: list[dict[str, Any]] = []
    failed_packets: list[dict[str, Any]] = []
    warnings: list[str] = []
    dropped = 0

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    workers = max(1, max_workers)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(_discover_packet_candidates, packet, llm_client): packet
            for packet in packets
        }
        for future in as_completed(futures):
            packet = futures[future]
            raw_candidates, error = future.result()
            if error:
                failed_packets.append({"section_id": packet.get("section_id"), "error": error})
                continue
            for candidate in raw_candidates:
                normalized = normalize_candidate(candidate, lineage)
                errors = validate_candidate_record(normalized, known_artifact_ids, known_context_ids)
                if errors:
                    dropped += 1
                    warnings.append(
                        f"Dropped candidate '{candidate.get('candidate_id', '?')}' from section "
                        f"'{packet.get('section_id', '?')}': {'; '.join(errors)}"
                    )
                else:
                    collected.append(normalized)

    deduped, deduped_count = dedupe_candidates(collected)
    deduped = ensure_priority_candidates(deduped, artifacts, contexts, lineage)
    selected, omitted_count = select_top_candidates(deduped, max_candidates=MAX_CANDIDATES)
    likely_sections = identify_procedural_sections(bundle)
    missing_sections = find_missing_candidate_sections(likely_sections, selected)

    # LLM backfill pass: focused single-section extraction using backfill prompt.
    # Backfill candidates are appended after the initial ranked pool and are NOT
    # subject to the MAX_CANDIDATES cap — they exist purely to close coverage gaps.
    llm_backfill_count = 0
    if missing_sections and llm_used:
        repaired_candidates, repair_failures = repair_missing_sections_with_llm(
            bundle=bundle,
            missing_sections=missing_sections,
            llm_client=backfill_client,
            known_artifact_ids=known_artifact_ids,
            known_context_ids=known_context_ids,
            max_workers=workers,
            artifacts=artifacts,
            contexts=contexts,
        )
        failed_packets.extend(repair_failures)
        if repaired_candidates:
            llm_backfill_count = len(repaired_candidates)
            merged, repair_deduped_count = dedupe_candidates([*selected, *repaired_candidates])
            deduped_count += repair_deduped_count
            # Keep the original ranked selection plus net-new backfill candidates only.
            # Do not re-rank or re-cap — backfill candidates must not be squeezed out.
            existing_keys = {
                (_normalize_key(c.get("title")), _normalize_key(c.get("candidate_goal")))
                for c in selected
            }
            net_new = [
                c for c in merged
                if (_normalize_key(c.get("title")), _normalize_key(c.get("candidate_goal"))) not in existing_keys
            ]
            selected = [*selected, *net_new]
            missing_sections = find_missing_candidate_sections(likely_sections, selected)

    # Placeholder backfill: last resort only — emitted when LLM backfill produced nothing
    placeholder_count = 0
    if missing_sections and backfill_missing_sections:
        backfilled = [
            build_backfill_candidate(bundle, section, lineage)
            for section in missing_sections
        ]
        placeholder_count = len(backfilled)
        selected, backfill_deduped_count = dedupe_candidates([*selected, *backfilled])
        deduped_count += backfill_deduped_count
        missing_sections = find_missing_candidate_sections(likely_sections, selected)
        if placeholder_count:
            warnings.append(
                f"Emitted {placeholder_count} placeholder backfill candidate(s) because the LLM backfill pass "
                "produced no usable candidate for those sections. These require manual drafting."
            )

    if omitted_count:
        warnings.append(
            f"Omitted {omitted_count} lower-priority candidates from the initial ranked pool "
            f"(MAX_CANDIDATES={MAX_CANDIDATES}). LLM backfill candidates are exempt from this cap."
        )

    report = build_extraction_report(
        source_bundle_path=str(source_bundle_path),
        source_artifacts_path=str(source_artifacts_path),
        operational_context_path=str(operational_context_path),
        candidates=selected,
        lineage=lineage,
        llm_used=llm_used,
        failed_packets=failed_packets,
        warnings=warnings,
        dropped_candidate_count=dropped,
        deduped_candidate_count=deduped_count,
        missing_candidate_sections=missing_sections,
    )

    coverage_report = build_coverage_report(
        procedural_sections=likely_sections,
        selected_candidates=selected,
        llm_backfill_count=llm_backfill_count,
        placeholder_count=placeholder_count,
        remaining_missing_sections=missing_sections,
    )

    write_json(output_path / "runbook_candidates.json", selected)
    write_json(output_path / "runbook_candidate_extraction_report.json", report)
    write_json(output_path / "runbook_candidate_coverage_report.json", coverage_report)
    write_source_extraction_report(output_path, warnings=warnings)
    return selected, report


def _discover_packet_candidates(
    packet: dict[str, Any],
    llm_client: CandidateLLMClient,
) -> tuple[list[dict[str, Any]], str | None]:
    try:
        return llm_client.discover(packet), None
    except Exception as exc:
        return [], str(exc)


def build_candidate_packets(
    bundle: dict[str, Any],
    artifacts: list[dict[str, Any]],
    contexts: list[dict[str, Any]],
    lineage: Any,
) -> list[dict[str, Any]]:
    page_text_lookup = {int(p["page_number"]): str(p.get("text") or "") for p in bundle.get("pages", [])}
    artifacts_by_section: dict[str, list[dict[str, Any]]] = {}
    contexts_by_section: dict[str, list[dict[str, Any]]] = {}

    for artifact in artifacts:
        artifacts_by_section.setdefault(str(artifact.get("section_id") or ""), []).append(artifact)
    for context in contexts:
        section_ids = {str(ref.get("section_id") or "") for ref in context.get("source_refs") or [] if ref.get("section_id")}
        for section_id in section_ids:
            contexts_by_section.setdefault(section_id, []).append(context)

    packets: list[dict[str, Any]] = []
    for section in bundle.get("sections", []):
        title = str(section.get("title") or "")
        if not _is_important_section(title):
            continue
        section_id = str(section.get("section_id") or "")
        page_start = int(section.get("page_start") or 0)
        page_end = int(section.get("page_end") or page_start)
        text_parts: list[str] = []
        total_chars = 0
        for page_number in range(page_start, page_end + 1):
            remaining = MAX_SECTION_TEXT_CHARS - total_chars
            if remaining <= 0:
                break
            chunk = page_text_lookup.get(page_number, "")[:remaining]
            if chunk:
                text_parts.append(chunk)
                total_chars += len(chunk)

        packets.append(
            {
                "source_id": lineage.source_id,
                "source_type": lineage.source_type,
                "source_title": lineage.source_title,
                "source_version": lineage.source_version,
                "ingestion_batch_id": lineage.ingestion_batch_id,
                "section_id": section_id,
                "section_title": title,
                "page_start": page_start,
                "page_end": page_end,
                "section_text": "\n".join(text_parts).strip(),
                "related_operational_context": [
                    _compact_context(ctx) for ctx in contexts_by_section.get(section_id, [])[:MAX_CONTEXTS_PER_PACKET]
                ],
                "related_artifacts": [
                    _compact_artifact(artifact) for artifact in artifacts_by_section.get(section_id, [])[:MAX_ARTIFACTS_PER_PACKET]
                ],
                "source_refs": [
                    build_source_ref(
                        lineage,
                        page_start=page_start,
                        page_end=page_end,
                        section_id=section_id,
                    )
                ],
            }
        )
    return packets


def identify_procedural_sections(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    source_document_id = bundle.get("source_document", {}).get("source_document_id", "")
    for section in bundle.get("sections", []):
        title = str(section.get("title") or "")
        if not _is_procedural_section_title(title):
            continue
        sections.append(
            {
                "section_id": section.get("section_id", ""),
                "title": title,
                "page_start": section.get("page_start"),
                "page_end": section.get("page_end") or section.get("page_start"),
                "source_document_id": source_document_id,
                "reason": "Likely procedural section but no runbook candidate was produced.",
            }
        )
    return sections


def find_missing_candidate_sections(
    procedural_sections: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing: list[dict[str, Any]] = []
    for section in procedural_sections:
        if not _section_has_candidate(section, candidates):
            missing.append(
                {
                    "section_id": section.get("section_id", ""),
                    "title": section.get("title", ""),
                    "page_start": section.get("page_start"),
                    "reason": "Likely procedural section but no runbook candidate was produced.",
                }
            )
    return missing


def repair_missing_sections_with_llm(
    bundle: dict[str, Any],
    missing_sections: list[dict[str, Any]],
    llm_client: CandidateLLMClient,
    known_artifact_ids: set[str],
    known_context_ids: set[str],
    max_workers: int = 4,
    artifacts: list[dict[str, Any]] | None = None,
    contexts: list[dict[str, Any]] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    packets = [
        build_missing_section_packet(bundle, section, artifacts=artifacts, contexts=contexts)
        for section in missing_sections
    ]
    repaired: list[dict[str, Any]] = []
    failed_packets: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, max_workers)) as executor:
        futures = {
            executor.submit(_discover_packet_candidates, packet, llm_client): packet
            for packet in packets
        }
        for future in as_completed(futures):
            packet = futures[future]
            raw_candidates, error = future.result()
            if error:
                failed_packets.append({"section_id": packet.get("section_id"), "error": error})
                continue
            for candidate in raw_candidates:
                normalized = normalize_candidate(candidate, lineage)
                errors = validate_candidate_record(normalized, known_artifact_ids, known_context_ids)
                if not errors:
                    repaired.append(normalized)
    return repaired, failed_packets


def build_missing_section_packet(
    bundle: dict[str, Any],
    section: dict[str, Any],
    artifacts: list[dict[str, Any]] | None = None,
    contexts: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    lineage = lineage_from_bundle(bundle)
    page_text_lookup = {int(p["page_number"]): str(p.get("text") or "") for p in bundle.get("pages", [])}
    section_id = section.get("section_id", "")
    page_start = int(section.get("page_start") or 0)
    page_end = int(section.get("page_end") or page_start)

    text_parts = []
    total_chars = 0
    for page_number in range(page_start, page_end + 1):
        remaining = MAX_SECTION_TEXT_CHARS - total_chars
        if remaining <= 0:
            break
        chunk = page_text_lookup.get(page_number, "")[:remaining]
        if chunk:
            text_parts.append(chunk)
            total_chars += len(chunk)

    # Gather artifacts scoped to this section by section_id or page range
    related_artifacts: list[dict[str, Any]] = []
    if artifacts:
        for artifact in artifacts:
            art_section = str(artifact.get("section_id") or "")
            art_page = int(artifact.get("page_number") or 0)
            if art_section == section_id or (page_start <= art_page <= page_end):
                related_artifacts.append(_compact_artifact(artifact))
                if len(related_artifacts) >= MAX_ARTIFACTS_PER_PACKET:
                    break

    # Gather contexts scoped to this section
    related_contexts: list[dict[str, Any]] = []
    if contexts:
        for context in contexts:
            for ref in context.get("source_refs") or []:
                if not isinstance(ref, dict):
                    continue
                if str(ref.get("section_id") or "") == section_id:
                    related_contexts.append(_compact_context(context))
                    break
            if len(related_contexts) >= MAX_CONTEXTS_PER_PACKET:
                break

    return {
        "repair_instruction": "Create source-derived runbook candidates only for this missing procedural section.",
        "source_id": lineage.source_id,
        "source_type": lineage.source_type,
        "source_title": lineage.source_title,
        "source_version": lineage.source_version,
        "ingestion_batch_id": lineage.ingestion_batch_id,
        "section_id": section_id,
        "section_title": section.get("title", ""),
        "page_start": page_start,
        "page_end": page_end,
        "section_text": "\n".join(text_parts).strip(),
        "related_operational_context": related_contexts,
        "related_artifacts": related_artifacts,
        "source_refs": [
            build_source_ref(
                lineage,
                page_start=page_start,
                page_end=page_end,
                section_id=section_id,
            )
        ],
    }


def build_backfill_candidate(bundle: dict[str, Any], section: dict[str, Any], lineage: Any) -> dict[str, Any]:
    title = _strip_section_number(str(section.get("title") or "Procedural Section")).title()
    page_start = section.get("page_start")
    page_end = section.get("page_end") or page_start
    return {
        "candidate_id": make_candidate_id(lineage.source_type, f"backfill_{_slug(title)}"),
        "title": title,
        "candidate_goal": "Draft candidate created from procedural section title and source text.",
        "likely_procedure_type": _procedure_type_from_title(title),
        "likely_role_required": _role_from_title(title),
        "support_safe": None,
        "summary": "Backfilled candidate because this procedural section was not extracted by the LLM.",
        "rough_steps": [
            "Review the procedural section source text and draft source-grounded steps during canonical runbook drafting."
        ],
        "expected_result": None,
        "failure_or_escalation_notes": [],
        "access_or_tools_needed": [],
        "related_context_ids": [],
        "related_artifact_ids": [],
        "source_refs": [
            build_source_ref(
                lineage,
                page_start=page_start,
                page_end=page_end,
                section_id=str(section.get("section_id") or ""),
                quote_or_summary="Procedural section detected from source section title.",
            )
        ],
        "evidence_source_refs": [],
        "source_id": lineage.source_id,
        "source_type": lineage.source_type,
        "source_title": lineage.source_title,
        "source_version": lineage.source_version,
        "ingestion_batch_id": lineage.ingestion_batch_id,
        "confidence": "low",
        "candidate_status": "needs_review",
        "extraction_notes": [
            "Backfilled by deterministic Stage 5 coverage check because the LLM did not produce a candidate for this procedural section."
        ],
        "metadata": {
            "created_by": "stage_5_candidate_coverage_backfill",
            "source_quality": lineage.source_type,
        },
    }


def parse_candidate_response(content: str | dict[str, Any]) -> list[dict[str, Any]]:
    if isinstance(content, dict):
        data = content
    else:
        text = content.strip()
        fence = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.DOTALL | re.IGNORECASE)
        if fence:
            text = fence.group(1).strip()
        data = json.loads(text)
    candidates = data.get("candidates", [])
    if not isinstance(candidates, list):
        return []
    return [candidate for candidate in candidates if isinstance(candidate, dict)]


def normalize_candidate(candidate: dict[str, Any], lineage: Any) -> dict[str, Any]:
    normalized = apply_lineage(dict(candidate), lineage)
    list_fields = [
        "rough_steps",
        "failure_or_escalation_notes",
        "access_or_tools_needed",
        "related_context_ids",
        "related_artifact_ids",
        "source_refs",
        "evidence_source_refs",
        "extraction_notes",
    ]
    for field in list_fields:
        value = normalized.get(field, [])
        if value is None:
            value = []
        if not isinstance(value, list):
            value = [value]
        normalized[field] = value
    if not normalized.get("evidence_source_refs"):
        normalized["evidence_source_refs"] = list(normalized.get("source_refs") or [])
    normalized["confidence"] = normalized.get("confidence") or "medium"
    normalized["candidate_status"] = normalized.get("candidate_status") or "needs_review"
    metadata = normalized.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}
    metadata.setdefault("created_by", "runbook_candidate_discovery_agent")
    metadata.setdefault("source_quality", lineage.source_type)
    normalized["metadata"] = metadata
    return normalized


def validate_candidate_record(
    record: dict[str, Any],
    known_artifact_ids: set[str],
    known_context_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    for field in ("candidate_id", "title", "candidate_goal", "summary"):
        if not str(record.get(field) or "").strip():
            errors.append(f"Missing required field: {field}")
    for field in ("source_id", "source_type", "ingestion_batch_id"):
        if not str(record.get(field) or "").strip():
            errors.append(f"Missing required field: {field}")
    if record.get("likely_procedure_type") not in ALLOWED_PROCEDURE_TYPES:
        errors.append(f"Invalid likely_procedure_type: '{record.get('likely_procedure_type')}'")
    if record.get("likely_role_required") not in ALLOWED_ROLES:
        errors.append(f"Invalid likely_role_required: '{record.get('likely_role_required')}'")
    if record.get("confidence", "medium") not in ALLOWED_CONFIDENCE:
        errors.append(f"Invalid confidence: '{record.get('confidence')}'")
    if record.get("candidate_status") != "needs_review":
        errors.append("candidate_status must be 'needs_review'")
    if record.get("likely_procedure_type") != "reference" and not record.get("rough_steps"):
        errors.append("rough_steps must contain at least one step unless type is reference")
    if not record.get("source_refs"):
        errors.append("source_refs must contain at least one entry")
    for artifact_id in record.get("related_artifact_ids") or []:
        if artifact_id not in known_artifact_ids:
            errors.append(f"related_artifact_id not found: '{artifact_id}'")
    for context_id in record.get("related_context_ids") or []:
        if context_id not in known_context_ids:
            errors.append(f"related_context_id not found: '{context_id}'")
    for forbidden in FORBIDDEN_FIELDS:
        if forbidden in record:
            errors.append(f"Forbidden field present: '{forbidden}'")
    return errors


def dedupe_candidates(candidates: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    deduped: dict[str, dict[str, Any]] = {}
    duplicate_count = 0
    for candidate in candidates:
        candidate_id = str(candidate.get("candidate_id") or "").strip()
        if not candidate_id:
            continue
        if candidate_id not in deduped:
            deduped[candidate_id] = dict(candidate)
            continue
        duplicate_count += 1
    return list(deduped.values()), duplicate_count


def ensure_priority_candidates(
    candidates: list[dict[str, Any]],
    artifacts: list[dict[str, Any]],
    contexts: list[dict[str, Any]],
    lineage: Any,
) -> list[dict[str, Any]]:
    repaired = [dict(candidate) for candidate in candidates]
    priority_specs = [
        {
            "key": ["heartbeat"],
            "artifact_figure_id": "fig_4_22",
            "context_terms": ["heartbeat"],
            "candidate_id": make_candidate_id(lineage.source_type, "check_tipper_heartbeat_stats"),
            "title": "Check Tipper Heartbeat Stats",
            "goal": "Check heartbeat timing values on the Operator Station HMI Data screen.",
            "type": "diagnostic",
            "role": "operator",
        },
        {
            "key": ["operator station", "alarm"],
            "artifact_figure_id": "fig_4_28",
            "context_terms": ["operator station", "alarm"],
            "candidate_id": make_candidate_id(lineage.source_type, "check_operator_station_alarms"),
            "title": "Check Operator Station Alarms",
            "goal": "Review operator station HMI alarms and alarm history.",
            "type": "diagnostic",
            "role": "operator",
        },
        {
            "key": ["add tote"],
            "artifact_figure_id": "fig_4_31",
            "context_terms": ["add tote"],
            "candidate_id": make_candidate_id(lineage.source_type, "use_hospital_add_tote_screen"),
            "title": "Use Hospital Add Tote Screen",
            "goal": "Use the Hospital HMI Add Tote screen for supported tote handling.",
            "type": "operation",
            "role": "operator",
        },
        {
            "key": ["remove tote"],
            "artifact_figure_id": "fig_4_32",
            "context_terms": ["remove tote"],
            "candidate_id": make_candidate_id(lineage.source_type, "use_hospital_remove_tote_screen"),
            "title": "Use Hospital Remove Tote Screen",
            "goal": "Use the Hospital HMI Remove Tote screen for supported tote removal.",
            "type": "operation",
            "role": "operator",
        },
        {
            "key": ["agv", "bump"],
            "artifact_figure_id": "fig_5_2",
            "context_terms": ["agv", "bump"],
            "candidate_id": make_candidate_id(lineage.source_type, "recover_agv_bump_fault"),
            "title": "Recover AGV Bump Fault",
            "goal": "Review and recover from an AGV bump fault using the documented fault screen guidance.",
            "type": "recovery",
            "role": "operator",
        },
    ]
    for spec in priority_specs:
        candidate = _find_candidate(repaired, spec["key"])
        artifact = _artifact_by_figure_id(artifacts, spec["artifact_figure_id"])
        context = _context_by_terms(contexts, spec["context_terms"])
        if candidate:
            _attach_priority_refs(candidate, artifact, context)
            continue
        if artifact or context:
            repaired.append(_build_priority_candidate(spec, artifact, context, lineage))
    return repaired


def select_top_candidates(candidates: list[dict[str, Any]], max_candidates: int = MAX_CANDIDATES) -> tuple[list[dict[str, Any]], int]:
    if len(candidates) <= max_candidates:
        return candidates, 0
    indexed = list(enumerate(candidates))
    indexed.sort(key=lambda item: (-_candidate_score(item[1]), item[0]))
    selected_indexes = sorted(index for index, _candidate in indexed[:max_candidates])
    selected = [candidates[index] for index in selected_indexes]
    return selected, len(candidates) - len(selected)


def _candidate_score(candidate: dict[str, Any]) -> int:
    text = _candidate_text(candidate)
    priority_terms = [
        ["heartbeat"],
        ["operator station", "alarm"],
        ["add tote"],
        ["remove tote"],
        ["agv", "bump"],
        ["faulted agv", "tote"],
        ["start", "optisweep"],
        ["start", "operator station"],
        ["sorter", "scanner", "tote"],
    ]
    score = 0
    if any(all(term in text for term in terms) for terms in priority_terms):
        score += 100
    if candidate.get("related_artifact_ids"):
        score += 25
    if candidate.get("related_context_ids"):
        score += 20
    if candidate.get("likely_procedure_type") in {"diagnostic", "recovery"}:
        score += 15
    if candidate.get("likely_procedure_type") == "operation":
        score += 8
    if candidate.get("confidence") == "high":
        score += 5
    return score


def _attach_priority_refs(candidate: dict[str, Any], artifact: dict[str, Any] | None, context: dict[str, Any] | None) -> None:
    if artifact and artifact.get("artifact_id"):
        candidate["related_artifact_ids"] = sorted(set(candidate.get("related_artifact_ids", [])) | {artifact["artifact_id"]})
        candidate["source_refs"] = _merge_unique(candidate.get("source_refs", []), artifact.get("source_refs", []))
    if context and context.get("context_id"):
        candidate["related_context_ids"] = sorted(set(candidate.get("related_context_ids", [])) | {context["context_id"]})
        candidate["source_refs"] = _merge_unique(candidate.get("source_refs", []), context.get("source_refs", []))


def _build_priority_candidate(
    spec: dict[str, Any],
    artifact: dict[str, Any] | None,
    context: dict[str, Any] | None,
    lineage: Any,
) -> dict[str, Any]:
    refs = []
    related_artifact_ids = []
    related_context_ids = []
    rough_steps = []
    notes = []
    if artifact:
        related_artifact_ids = [artifact["artifact_id"]]
        refs.extend(artifact.get("source_refs", []))
        rough_steps = [f"Review {item}." for item in artifact.get("what_to_look_at", [])[:5]]
    if context:
        related_context_ids = [context["context_id"]]
        refs = _merge_unique(refs, context.get("source_refs", []))
        if context.get("details"):
            notes.append(str(context["details"])[:240])
    if not rough_steps:
        rough_steps = ["Review the documented screen or source section.", "Record the relevant status, value, alarm, or operating result."]
    return {
        "candidate_id": spec["candidate_id"],
        "title": spec["title"],
        "candidate_goal": spec["goal"],
        "likely_procedure_type": spec["type"],
        "likely_role_required": spec["role"],
        "support_safe": True,
        "summary": (context or artifact or {}).get("summary") or spec["goal"],
        "rough_steps": rough_steps,
        "expected_result": "The user can review the documented source-backed information needed for this procedure.",
        "failure_or_escalation_notes": notes,
        "access_or_tools_needed": [],
        "related_context_ids": related_context_ids,
        "related_artifact_ids": related_artifact_ids,
        "source_refs": refs,
        "evidence_source_refs": list(refs),
        "source_id": lineage.source_id,
        "source_type": lineage.source_type,
        "source_title": lineage.source_title,
        "source_version": lineage.source_version,
        "ingestion_batch_id": lineage.ingestion_batch_id,
        "confidence": "medium",
        "candidate_status": "needs_review",
        "extraction_notes": ["Source-grounded priority candidate added during deterministic priority repair."],
        "metadata": {"created_by": "runbook_candidate_discovery_agent", "source_quality": lineage.source_type},
    }


def _artifact_by_figure_id(artifacts: list[dict[str, Any]], figure_id: str) -> dict[str, Any] | None:
    return next((artifact for artifact in artifacts if artifact.get("figure_id") == figure_id), None)


def _context_by_terms(contexts: list[dict[str, Any]], terms: list[str]) -> dict[str, Any] | None:
    for context in contexts:
        text = " ".join(
            [
                str(context.get("title") or ""),
                str(context.get("summary") or ""),
                str(context.get("details") or ""),
                str(context.get("retrieval_text") or ""),
            ]
        ).lower()
        if all(term in text for term in terms):
            return context
    return None


def build_coverage_report(
    procedural_sections: list[dict[str, Any]],
    selected_candidates: list[dict[str, Any]],
    llm_backfill_count: int = 0,
    placeholder_count: int = 0,
    remaining_missing_sections: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build a coverage report mapping procedural sections to candidate coverage status."""
    section_records: list[dict[str, Any]] = []
    covered_real = 0
    covered_placeholder = 0
    not_covered = 0

    for section in procedural_sections:
        section_id = str(section.get("section_id") or "")
        title_key = _normalize_title_for_match(str(section.get("title") or ""))
        candidate_ids: list[str] = []
        status = "not_covered"
        for candidate in selected_candidates:
            is_placeholder = candidate.get("metadata", {}).get("created_by") == "stage_5_candidate_coverage_backfill"
            matched = False
            # Primary match: section_id in source_refs
            for ref in candidate.get("source_refs") or []:
                if isinstance(ref, dict) and section_id and str(ref.get("section_id") or "") == section_id:
                    matched = True
                    break
            # Fallback match: title appears in candidate text (same logic as _section_has_candidate)
            if not matched and title_key:
                candidate_text = _normalize_title_for_match(
                    " ".join([str(candidate.get("title") or ""), str(candidate.get("candidate_goal") or "")])
                )
                if title_key in candidate_text:
                    matched = True
            if matched:
                candidate_ids.append(str(candidate.get("candidate_id") or ""))
                if status == "not_covered":
                    status = "covered_placeholder" if is_placeholder else "covered_real"
                elif status == "covered_placeholder" and not is_placeholder:
                    status = "covered_real"

        if status == "covered_real":
            covered_real += 1
        elif status == "covered_placeholder":
            covered_placeholder += 1
        else:
            not_covered += 1

        section_records.append(
            {
                "section_id": section_id,
                "title": section.get("title", ""),
                "page_start": section.get("page_start"),
                "coverage_status": status,
                "candidate_ids": candidate_ids,
            }
        )

    total = len(procedural_sections)
    covered_any = covered_real + covered_placeholder
    coverage_pct = round(covered_any / total * 100, 1) if total else 0.0
    missing_titles = [s.get("title", "") for s in (remaining_missing_sections or [])]

    return {
        "manual_procedure_inventory_count": total,
        "covered_procedures": covered_real,
        "covered_by_placeholder_procedures": covered_placeholder,
        "missing_procedures": not_covered,
        "llm_backfill_candidates_added": llm_backfill_count,
        "placeholder_candidates": placeholder_count,
        "coverage_percentage": coverage_pct,
        "missing_procedure_titles": missing_titles,
        "over_fragmented_candidate_groups": [],
        "procedural_section_coverage": section_records,
    }


def build_extraction_report(
    source_bundle_path: str,
    source_artifacts_path: str,
    operational_context_path: str,
    candidates: list[dict[str, Any]],
    lineage: Any,
    llm_used: bool,
    failed_packets: list[dict[str, Any]],
    warnings: list[str],
    dropped_candidate_count: int = 0,
    deduped_candidate_count: int = 0,
    missing_candidate_sections: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    counts_by_type = Counter(str(c.get("likely_procedure_type") or "unknown") for c in candidates)
    counts_by_role = Counter(str(c.get("likely_role_required") or "unknown") for c in candidates)
    placeholder_count = sum(
        1
        for candidate in candidates
        if candidate.get("metadata", {}).get("created_by") == "stage_5_candidate_coverage_backfill"
    )
    return {
        "source_id": lineage.source_id,
        "source_type": lineage.source_type,
        "ingestion_batch_id": lineage.ingestion_batch_id,
        "llm_used": llm_used,
        "input_source_bundle": source_bundle_path,
        "input_source_artifacts": source_artifacts_path,
        "input_operational_context": operational_context_path,
        "candidate_count": len(candidates),
        "candidate_counts_by_type": dict(sorted(counts_by_type.items())),
        "candidate_counts_by_role": dict(sorted(counts_by_role.items())),
        "candidates_with_artifacts": sum(1 for c in candidates if c.get("related_artifact_ids")),
        "candidates_with_context": sum(1 for c in candidates if c.get("related_context_ids")),
        "candidates_missing_source_refs": sum(1 for c in candidates if not c.get("source_refs")),
        "dropped_candidate_count": dropped_candidate_count,
        "deduped_candidate_count": deduped_candidate_count,
        "duplicate_candidate_count": deduped_candidate_count,
        "placeholder_candidate_count": placeholder_count,
        "candidates_missing_source_id": sum(1 for c in candidates if not str(c.get("source_id") or "").strip()),
        "priority_candidate_check": build_priority_candidate_check(candidates),
        "missing_priority_candidates": build_missing_priority_candidates(candidates),
        "missing_candidate_sections": missing_candidate_sections or [],
        "failed_packets": failed_packets,
        "warnings": warnings,
    }


def build_priority_candidate_check(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    checks = {
        "check_tipper_heartbeat_stats": _candidate_check(candidates, REQUIRED_PRIORITY_CANDIDATES["Check Tipper Heartbeat Stats"]),
        "check_operator_station_alarms": _candidate_check(candidates, REQUIRED_PRIORITY_CANDIDATES["Check Operator Station Alarms"]),
        "use_hospital_add_tote": _candidate_check(candidates, REQUIRED_PRIORITY_CANDIDATES["Use Hospital Add Tote Screen"]),
        "use_hospital_remove_tote": _candidate_check(candidates, REQUIRED_PRIORITY_CANDIDATES["Use Hospital Remove Tote Screen"]),
        "recover_agv_bump_fault": _candidate_check(candidates, REQUIRED_PRIORITY_CANDIDATES["Recover AGV Bump Fault"]),
        "recover_faulted_agv_with_tote": _candidate_check(candidates, REQUIRED_PRIORITY_CANDIDATES["Recover Faulted AGV With Tote"]),
        "start_optisweep_system": _candidate_check(candidates, REQUIRED_PRIORITY_CANDIDATES["Start OptiSweep System"]),
        "stop_optisweep_system": _candidate_check(candidates, REQUIRED_PRIORITY_CANDIDATES["Stop OptiSweep System"]),
        "start_operator_station": _candidate_check(candidates, REQUIRED_PRIORITY_CANDIDATES["Start Operator Station"]),
        "stop_operator_station": _candidate_check(candidates, REQUIRED_PRIORITY_CANDIDATES["Stop Operator Station"]),
        "review_visu_io_diag_screen": _candidate_check(candidates, REQUIRED_PRIORITY_CANDIDATES["Review VISU_IO_DIAG Screen"]),
        "initialize_tote_with_sorter_scanner": _candidate_check(candidates, REQUIRED_PRIORITY_CANDIDATES["Initialize Tote With Sorter Scanner"]),
    }
    heartbeat = checks["check_tipper_heartbeat_stats"]
    candidate = heartbeat.get("_candidate")
    text = _candidate_text(candidate) if candidate else ""
    heartbeat.update(
        {
            "mentions_last_max_min": all(term in text for term in ["last", "max", "min"]),
            "mentions_10_seconds": "10 seconds" in text,
        }
    )
    for value in checks.values():
        value.pop("_candidate", None)
    return checks


def build_missing_priority_candidates(candidates: list[dict[str, Any]]) -> list[str]:
    missing: list[str] = []
    for title, keywords in REQUIRED_PRIORITY_CANDIDATES.items():
        if _find_candidate(candidates, keywords) is None:
            missing.append(title)
    return missing


def _candidate_check(candidates: list[dict[str, Any]], keywords: list[str]) -> dict[str, Any]:
    candidate = _find_candidate(candidates, keywords)
    return {
        "found": candidate is not None,
        "has_artifact_ref": bool(candidate and candidate.get("related_artifact_ids")),
        "has_context_ref": bool(candidate and candidate.get("related_context_ids")),
        "_candidate": candidate,
    }


def _find_candidate(candidates: list[dict[str, Any]], keywords: list[str]) -> dict[str, Any] | None:
    for candidate in candidates:
        text = _candidate_text(candidate)
        if all(keyword.lower() in text for keyword in keywords):
            return candidate
    return None


def _candidate_text(candidate: dict[str, Any] | None) -> str:
    if not candidate:
        return ""
    return " ".join(
        [
            str(candidate.get("title") or ""),
            str(candidate.get("candidate_goal") or ""),
            str(candidate.get("summary") or ""),
            " ".join(str(step) for step in candidate.get("rough_steps") or []),
            " ".join(str(note) for note in candidate.get("failure_or_escalation_notes") or []),
            str(candidate.get("expected_result") or ""),
        ]
    ).lower()


def _section_has_candidate(section: dict[str, Any], candidates: list[dict[str, Any]]) -> bool:
    section_id = str(section.get("section_id") or "")
    title_key = _normalize_title_for_match(str(section.get("title") or ""))
    for candidate in candidates:
        for ref in candidate.get("source_refs") or []:
            if not isinstance(ref, dict):
                continue
            if section_id and ref.get("section_id") == section_id:
                return True
        candidate_text = _normalize_title_for_match(
            " ".join([str(candidate.get("title") or ""), str(candidate.get("candidate_goal") or "")])
        )
        if title_key and title_key in candidate_text:
            return True
    return False


def _compact_artifact(artifact: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_id": artifact.get("artifact_id"),
        "title": artifact.get("title"),
        "figure_id": artifact.get("figure_id"),
        "page_number": artifact.get("page_number"),
        "what_to_look_at": artifact.get("what_to_look_at", [])[:8],
        "tags": artifact.get("tags", [])[:10],
        "retrieval_text": str(artifact.get("retrieval_text") or "")[:600],
        "source_refs": artifact.get("source_refs", []),
    }


def _compact_context(context: dict[str, Any]) -> dict[str, Any]:
    return {
        "context_id": context.get("context_id"),
        "title": context.get("title"),
        "context_type": context.get("context_type"),
        "summary": context.get("summary"),
        "key_terms": context.get("key_terms", [])[:10],
        "related_artifact_ids": context.get("related_artifact_ids", []),
        "source_refs": context.get("source_refs", []),
    }


def _is_important_section(title: str) -> bool:
    lowered = title.lower()
    return any(keyword in lowered for keyword in IMPORTANT_SECTION_KEYWORDS)


def _is_procedural_section_title(title: str) -> bool:
    lowered = title.lower()
    return any(re.search(rf"\b{re.escape(keyword)}\b", lowered) for keyword in PROCEDURAL_SECTION_KEYWORDS)


def _strip_section_number(title: str) -> str:
    return re.sub(r"^\s*\d+(?:\.\d+)*:?\s*", "", title).strip()


def _normalize_title_for_match(value: str) -> str:
    value = _strip_section_number(value).lower()
    value = value.replace("_", " ")
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def _slug(value: str) -> str:
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_"))


def _procedure_type_from_title(title: str) -> str:
    lowered = title.lower()
    if any(term in lowered for term in ["fault", "recover", "recovery", "reset"]):
        return "recovery"
    if any(term in lowered for term in ["reference", "inspection"]):
        return "reference"
    if any(term in lowered for term in ["scanner", "maintenance", "loto", "lockout", "tagout"]):
        return "operation"
    return "operation"


def _role_from_title(title: str) -> str:
    lowered = title.lower()
    if any(term in lowered for term in ["maintenance", "loto", "lockout", "tagout", "replacement"]):
        return "L2_support"
    return "operator"


def _normalize_key(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def _merge_unique(existing: list[Any], incoming: list[Any]) -> list[Any]:
    merged: list[Any] = []
    seen: set[str] = set()
    for item in [*existing, *incoming]:
        marker = json.dumps(item, sort_keys=True)
        if marker not in seen:
            seen.add(marker)
            merged.append(item)
    return merged


def _clean_env_value(value: str | None) -> str:
    cleaned = (value or "").strip().strip('"').strip("'")
    if cleaned in {"", "your-api-version", "your_api_version", "<api-version>"}:
        return ""
    return cleaned
