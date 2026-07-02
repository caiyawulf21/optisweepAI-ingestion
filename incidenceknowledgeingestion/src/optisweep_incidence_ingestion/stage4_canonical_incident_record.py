"""Stage 4 - Create canonical incident records and timeline.

Builds a compact Stage 4 extraction packet from source bundle page OCR and
Stage 3 enriched artifacts, then uses an LLM to create a canonical incident
record and source-grounded timeline events.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request

from dotenv import load_dotenv

from optisweep_incidence_ingestion.utils.json_utils import read_json, write_json
from optisweep_incidence_ingestion.utils.markdown_review import write_stage4_review_markdown

FOUNDRY_API_VERSION = "2025-04-01-preview"
CLASSIC_AZURE_OPENAI_API_VERSION = "2024-10-21"
DEFAULT_PAGE_CHUNK_TARGET_CHARS = 7000
DEFAULT_ARTIFACT_CHUNK_SIZE = 8
MAX_PAGE_OCR_CHARS = 2200
MAX_ARTIFACT_FIELD_CHARS = 900


class Stage4LLMClient(Protocol):
    def create_canonical_incident_record(self, packet: dict[str, Any]) -> dict[str, Any]:
        ...

    def create_timeline_events(self, packet: dict[str, Any], chunk: dict[str, Any]) -> dict[str, Any]:
        ...


class AzureOpenAIStage4Client:
    def __init__(
        self,
        endpoint: str | None = None,
        api_key: str | None = None,
        deployment: str | None = None,
        api_version: str | None = None,
        canonical_prompt_path: str | Path | None = None,
        timeline_prompt_path: str | Path | None = None,
    ) -> None:
        load_dotenv()
        self.endpoint = _clean_env_value(endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")).rstrip("/")
        self.api_key = _clean_env_value(api_key or os.getenv("AZURE_OPENAI_API_KEY"))
        self.deployment = _clean_env_value(deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT"))
        env_api_version = _clean_env_value(os.getenv("AZURE_OPENAI_API_VERSION"))
        self.api_version = _clean_env_value(api_version) or self._default_api_version(env_api_version)
        prompt_dir = Path(__file__).resolve().parent / "prompts"
        self.canonical_prompt = Path(
            canonical_prompt_path or prompt_dir / "stage4_canonical_incident_record_prompt.md"
        ).read_text(encoding="utf-8")
        self.timeline_prompt = Path(
            timeline_prompt_path or prompt_dir / "stage4_timeline_events_prompt.md"
        ).read_text(encoding="utf-8")
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

    def create_canonical_incident_record(self, packet: dict[str, Any]) -> dict[str, Any]:
        return self._request(self.canonical_prompt, packet)

    def create_timeline_events(self, packet: dict[str, Any], chunk: dict[str, Any]) -> dict[str, Any]:
        return self._request(self.timeline_prompt, {"stage4_packet_context": packet, "evidence_chunk": chunk})

    def _request(self, prompt: str, packet: dict[str, Any]) -> dict[str, Any]:
        body = {
            "messages": [
                {"role": "system", "content": prompt},
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
                with _urlopen_no_proxy(request, timeout=180) as response:
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


def create_stage4_canonical_incident_record_and_timeline(
    *,
    source_package_path: str | Path,
    page_inventory_path: str | Path,
    source_artifacts_enriched_path: str | Path,
    artifact_enrichment_report_path: str | Path,
    output_dir: str | Path,
    llm_client: Stage4LLMClient,
    page_chunk_target_chars: int = DEFAULT_PAGE_CHUNK_TARGET_CHARS,
    artifact_chunk_size: int = DEFAULT_ARTIFACT_CHUNK_SIZE,
    review_evidence_path: str | Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    package = read_json(source_package_path)
    page_inventory = read_json(page_inventory_path)
    enriched_artifacts = read_json(source_artifacts_enriched_path)
    artifact_enrichment_report = read_json(artifact_enrichment_report_path)
    review_evidence = read_json(review_evidence_path) if review_evidence_path and Path(review_evidence_path).exists() else {}

    if not isinstance(page_inventory, list):
        raise ValueError("page_inventory.json must contain a list of page records.")
    if not isinstance(enriched_artifacts, list):
        raise ValueError("source_artifacts_enriched.json must contain a list of enriched artifact records.")

    packet = build_stage4_extraction_packet(
        package=package,
        page_inventory=page_inventory,
        enriched_artifacts=enriched_artifacts,
        artifact_enrichment_report=artifact_enrichment_report,
        review_evidence=review_evidence,
        page_chunk_target_chars=page_chunk_target_chars,
        artifact_chunk_size=artifact_chunk_size,
    )
    output_path = Path(output_dir)
    write_json(output_path / "stage4_evidence_chunks.json", packet["evidence_handoff"])
    if review_evidence:
        write_json(output_path / "stage4_review_evidence_used.json", review_evidence)

    canonical_response = llm_client.create_canonical_incident_record(_canonical_llm_packet(packet))
    canonical_record, canonical_report = normalize_canonical_response(canonical_response, packet)
    canonical_record, canonical_report = apply_review_evidence_to_canonical_record(canonical_record, canonical_report, review_evidence)
    timeline_events, timeline_report = extract_timeline_events_from_chunks(
        llm_client=llm_client,
        packet=packet,
        canonical_record=canonical_record,
    )

    known_page_refs = {page.get("page_ref") for page in page_inventory if page.get("page_ref")}
    known_artifact_ids = {artifact.get("artifact_id") for artifact in enriched_artifacts if artifact.get("artifact_id")}
    canonical_report = merge_report_validation(
        canonical_report,
        validate_canonical_record(canonical_record, known_page_refs, known_artifact_ids),
    )
    timeline_report = merge_report_validation(
        timeline_report,
        validate_timeline_events(timeline_events, known_page_refs, known_artifact_ids),
    )

    write_json(output_path / "canonical_incident_record.json", canonical_record)
    write_json(output_path / "canonical_incident_record_extraction_report.json", canonical_report)
    write_json(output_path / "timeline_events.json", timeline_events)
    write_json(output_path / "timeline_event_extraction_report.json", timeline_report)
    write_stage4_review_markdown(
        output_path / "incident_review.md",
        canonical_record,
        canonical_report,
        timeline_events,
        timeline_report,
    )
    write_json(output_path / "incident_source_package.json", _package_with_stage4_refs(package, output_path, canonical_report, timeline_report))
    return canonical_record, canonical_report, timeline_events, timeline_report


def build_stage4_extraction_packet(
    *,
    package: dict[str, Any],
    page_inventory: list[dict[str, Any]],
    enriched_artifacts: list[dict[str, Any]],
    artifact_enrichment_report: dict[str, Any],
    review_evidence: dict[str, Any] | None = None,
    page_chunk_target_chars: int = DEFAULT_PAGE_CHUNK_TARGET_CHARS,
    artifact_chunk_size: int = DEFAULT_ARTIFACT_CHUNK_SIZE,
) -> dict[str, Any]:
    source_bundle = package.get("source_bundle") or {}
    compact_pages = [_compact_page(page) for page in page_inventory]
    artifact_cards = [_compact_enriched_artifact(artifact) for artifact in enriched_artifacts]
    evidence_handoff = build_stage4_evidence_handoff(
        pages=compact_pages,
        artifact_cards=artifact_cards,
        page_chunk_target_chars=page_chunk_target_chars,
        artifact_chunk_size=artifact_chunk_size,
    )
    return {
        "packet_type": "stage_4_incident_record_and_timeline_extraction_packet",
        "schema_version": "0.1",
        "source_package": {
            "source_package_id": package.get("source_package_id"),
            "source_id": package.get("source_id"),
            "source_case_id": package.get("source_case_id"),
            "source_title": package.get("source_title"),
            "source_type": package.get("source_type"),
            "ingestion_batch_id": package.get("ingestion_batch_id"),
            "page_count": package.get("page_count"),
            "source_metadata": package.get("source_metadata") or {},
        },
        "source_bundle_summary": {
            "stage_status": source_bundle.get("stage_status") or {},
            "counts": source_bundle.get("counts") or {},
            "duplicate_groups": source_bundle.get("duplicate_groups") or [],
            "warnings": source_bundle.get("warnings") or [],
        },
        "evidence_handoff": evidence_handoff,
        "artifact_enrichment_report": _compact_artifact_enrichment_report(artifact_enrichment_report),
        "review_evidence": review_evidence or {},
        "stage4_extraction_notes": [
            "Use evidence_handoff.page_text_chunks as the primary source for incident facts and timeline sequence.",
            "Use evidence_handoff.artifact_evidence_chunks as supporting evidence for screenshots, logs, commands, and validation.",
            "Preserve page refs, artifact refs, and chunk ids on claims and events.",
            "Do not infer unsupported root cause, exact downtime, hostnames, URLs, commands, service names, or people.",
            "Canonical incident records must not include people lists. Named actors belong in timeline actor fields or source refs only.",
        ],
    }


def build_stage4_evidence_handoff(
    *,
    pages: list[dict[str, Any]],
    artifact_cards: list[dict[str, Any]],
    page_chunk_target_chars: int,
    artifact_chunk_size: int,
) -> dict[str, Any]:
    page_chunks = _build_page_text_chunks(pages, max(1000, page_chunk_target_chars))
    artifact_chunks = _build_artifact_evidence_chunks(artifact_cards, max(1, artifact_chunk_size))
    return {
        "record_type": "stage4_evidence_handoff",
        "schema_version": "0.1",
        "chunking": {
            "page_chunk_target_chars": page_chunk_target_chars,
            "artifact_chunk_size": artifact_chunk_size,
            "page_chunk_count": len(page_chunks),
            "artifact_chunk_count": len(artifact_chunks),
            "page_count": len(pages),
            "artifact_card_count": len(artifact_cards),
        },
        "chunk_index": _build_chunk_index(page_chunks, artifact_chunks),
        "page_text_chunks": page_chunks,
        "artifact_evidence_chunks": artifact_chunks,
        "downstream_usage": {
            "canonical_incident_record": "Use all chunk_index entries plus selected page/artifact chunks for concise incident facts.",
            "timeline_events": "Extract timeline events chunk by chunk from page_text_chunks, linking artifact cards when referenced.",
            "runbook_candidates": "Use timeline events plus artifact_evidence_chunks with action, diagnostic, and validation evidence roles.",
            "draft_playbooks": "Use timeline events and runbook candidates; do not treat a single incident as canonical workflow approval.",
        },
    }


def extract_timeline_events_from_chunks(
    *,
    llm_client: Stage4LLMClient,
    packet: dict[str, Any],
    canonical_record: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    timeline_context = _timeline_llm_context(packet, canonical_record)
    chunk_reports: list[dict[str, Any]] = []
    all_events: list[dict[str, Any]] = []
    for chunk in packet["evidence_handoff"]["page_text_chunks"]:
        response = llm_client.create_timeline_events(timeline_context, chunk)
        chunk_timeline, chunk_report = normalize_timeline_response(response, packet)
        chunk_reports.append(
            {
                "chunk_id": chunk.get("chunk_id"),
                "page_refs": chunk.get("page_refs") or [],
                "event_count": len(chunk_timeline.get("events") or []),
                "validation_errors": chunk_report.get("validation_errors") or [],
                "warnings": chunk_report.get("warnings") or [],
            }
        )
        for event in chunk_timeline.get("events") or []:
            merged = dict(event)
            chunk_refs = list(merged.get("evidence_chunk_refs") or [])
            if chunk.get("chunk_id") not in chunk_refs:
                chunk_refs.append(chunk.get("chunk_id"))
            merged["evidence_chunk_refs"] = chunk_refs
            all_events.append(merged)
    timeline = {
        "record_type": "incident_timeline_events",
        "schema_version": "0.1",
        "stage": "stage_4_timeline_events",
        "incident_id": canonical_record.get("incident_id") or f"incident_{packet.get('source_package', {}).get('source_case_id')}",
        "source_case_id": packet.get("source_package", {}).get("source_case_id"),
        "timestamp_timezone": "unknown",
        "ordering_basis": "source_timestamp_then_source_order_chunked",
        "events": _renumber_events(filter_timeline_events(all_events), str(packet.get("source_package", {}).get("source_case_id") or "")),
    }
    report = {
        "stage": "stage_4_timeline_events",
        "llm_used": True,
        "prompt": "stage4_timeline_events_prompt.md",
        "chunked": True,
        "chunk_count": len(packet["evidence_handoff"]["page_text_chunks"]),
        "event_count": len(timeline["events"]),
        "filtered_event_count": len(all_events) - len(timeline["events"]),
        "chunk_reports": chunk_reports,
        "validation_errors": [],
        "warnings": _timeline_chunk_warnings(chunk_reports),
        "notes": ["Timeline events were extracted page-chunk by page-chunk to control prompt size, then filtered to action/report/status/system events."],
        "built_at": datetime.now(timezone.utc).isoformat(),
    }
    return timeline, report


def _canonical_llm_packet(packet: dict[str, Any]) -> dict[str, Any]:
    handoff = packet["evidence_handoff"]
    return {
        "packet_type": "stage_4_canonical_incident_record_chunked_input",
        "schema_version": packet.get("schema_version"),
        "source_package": packet.get("source_package"),
        "source_bundle_summary": packet.get("source_bundle_summary"),
        "artifact_enrichment_report": packet.get("artifact_enrichment_report"),
        "review_evidence": packet.get("review_evidence") or {},
        "chunking": handoff.get("chunking"),
        "chunk_index": handoff.get("chunk_index"),
        "page_text_chunks": handoff.get("page_text_chunks"),
        "artifact_evidence_chunks": handoff.get("artifact_evidence_chunks"),
        "stage4_extraction_notes": packet.get("stage4_extraction_notes"),
    }


def filter_timeline_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    kept: list[dict[str, Any]] = []
    filler_phrases = [
        "add me",
        "added to the call",
        "add him to the call",
        "add me to the call",
        "asked to be added",
        "support chat for",
        "chat is the incident communication",
        "please add me",
        "adding you now",
        "screenshot of cbre",
        "send the screenshot of cbre",
        "cbre reference number",
        "cbre:",
        "callback bridge",
        "call the site contact back",
        "callback to the site",
        "tech support hotline",
        "who has the link",
        "somebody else had rdp",
        "being on the rdp session",
        "from wesley saunders's team",
        "mitchel will be ooo",
        "perform a service reset today",
        "invited ",
        "asked whether anyone knew",
        "could be checked",
        "restart guidance was documented",
        "if a restart became necessary",
    ]
    for event in events:
        event_type = event.get("event_type")
        summary = f"{event.get('summary') or ''} {event.get('details') or ''}".lower()
        if event_type == "support_coordination":
            continue
        if any(phrase in summary for phrase in filler_phrases):
            continue
        if event_type == "diagnostic_question":
            continue
        if event_type == "diagnostic_request":
            concrete_terms = ["memory", "cpu", "service", "event viewer", "ignition", "uptime", "status page", "restart"]
            if not any(term in summary for term in concrete_terms):
                continue
        if event_type == "status_update":
            incident_state_terms = [
                "nothing",
                "not moving",
                "bag",
                "resumed",
                "running",
                "stopped",
                "resolved",
                "in progress",
                "rca",
                "site",
            ]
            if not any(term in summary for term in incident_state_terms):
                continue
        sanitized = dict(event)
        sanitized["actor_name"] = "unknown"
        kept.append(sanitized)
    return kept


def _timeline_llm_context(packet: dict[str, Any], canonical_record: dict[str, Any]) -> dict[str, Any]:
    handoff = packet["evidence_handoff"]
    return {
        "packet_type": "stage_4_timeline_chunked_context",
        "schema_version": packet.get("schema_version"),
        "source_package": packet.get("source_package"),
        "source_bundle_summary": packet.get("source_bundle_summary"),
        "artifact_enrichment_report": packet.get("artifact_enrichment_report"),
        "chunking": handoff.get("chunking"),
        "chunk_index": handoff.get("chunk_index"),
        "artifact_evidence_chunks": handoff.get("artifact_evidence_chunks"),
        "canonical_incident_record": {
            "incident_id": canonical_record.get("incident_id"),
            "source_case_id": canonical_record.get("source_case_id"),
            "title": canonical_record.get("title"),
            "status": canonical_record.get("status"),
            "site": canonical_record.get("site"),
            "symptoms": canonical_record.get("symptoms") or [],
            "systems_involved": canonical_record.get("systems_involved") or [],
        },
        "stage4_extraction_notes": packet.get("stage4_extraction_notes"),
    }


def _build_page_text_chunks(pages: list[dict[str, Any]], target_chars: int) -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    current: list[dict[str, Any]] = []
    current_chars = 0
    for page in sorted(pages, key=lambda item: item.get("page_number") or 0):
        text = _truncate(page.get("ocr_text") or "", MAX_PAGE_OCR_CHARS)
        page_card = {
            "page_number": page.get("page_number"),
            "page_ref": page.get("page_ref"),
            "detected_page_type": page.get("detected_page_type"),
            "ocr_confidence": page.get("ocr_confidence"),
            "ocr_quality": page.get("ocr_quality"),
            "ocr_note": page.get("ocr_note"),
            "ocr_word_count": page.get("ocr_word_count"),
            "artifact_ids": page.get("artifact_ids") or [],
            "ocr_text": text,
        }
        projected_chars = current_chars + len(text)
        if current and projected_chars > target_chars:
            chunks.append(_page_chunk_from_cards(len(chunks) + 1, current))
            current = []
            current_chars = 0
        current.append(page_card)
        current_chars += len(text)
    if current:
        chunks.append(_page_chunk_from_cards(len(chunks) + 1, current))
    return chunks


def _page_chunk_from_cards(index: int, page_cards: list[dict[str, Any]]) -> dict[str, Any]:
    page_numbers = [card.get("page_number") for card in page_cards if card.get("page_number") is not None]
    artifact_ids: list[str] = []
    text_blocks: list[str] = []
    for card in page_cards:
        artifact_ids.extend(card.get("artifact_ids") or [])
        text_blocks.append(
            "\n".join(
                [
                    f"PAGE {card.get('page_number')} ({card.get('page_ref')})",
                    (
                        f"type={card.get('detected_page_type')} "
                        f"ocr_confidence={card.get('ocr_confidence')} "
                        f"ocr_quality={card.get('ocr_quality') or 'unknown'}"
                    ),
                    f"artifact_ids={', '.join(card.get('artifact_ids') or []) or 'none'}",
                    card.get("ocr_note") or "",
                    card.get("ocr_text") or "",
                ]
            )
        )
    return {
        "chunk_id": f"stage4_page_chunk_{index:03d}",
        "chunk_type": "page_ocr_sequence",
        "page_start": min(page_numbers) if page_numbers else None,
        "page_end": max(page_numbers) if page_numbers else None,
        "page_refs": [card.get("page_ref") for card in page_cards if card.get("page_ref")],
        "artifact_ids": _unique_list(artifact_ids),
        "detected_page_types": _unique_list([card.get("detected_page_type") for card in page_cards if card.get("detected_page_type")]),
        "pages": [{key: value for key, value in card.items() if key != "ocr_text"} for card in page_cards],
        "text": "\n\n".join(text_blocks),
    }


def _build_artifact_evidence_chunks(artifact_cards: list[dict[str, Any]], chunk_size: int) -> list[dict[str, Any]]:
    cards = sorted(artifact_cards, key=lambda item: (item.get("page_number") or 0, item.get("artifact_id") or ""))
    chunks: list[dict[str, Any]] = []
    for start in range(0, len(cards), chunk_size):
        group = cards[start : start + chunk_size]
        page_numbers = [card.get("page_number") for card in group if card.get("page_number") is not None]
        chunks.append(
            {
                "chunk_id": f"stage4_artifact_chunk_{len(chunks) + 1:03d}",
                "chunk_type": "artifact_evidence_cards",
                "page_start": min(page_numbers) if page_numbers else None,
                "page_end": max(page_numbers) if page_numbers else None,
                "artifact_ids": [card.get("artifact_id") for card in group if card.get("artifact_id")],
                "evidence_roles": _unique_list([card.get("evidence_role") for card in group if card.get("evidence_role")]),
                "image_types": _unique_list([card.get("image_type") for card in group if card.get("image_type")]),
                "cards": group,
            }
        )
    return chunks


def _build_chunk_index(page_chunks: list[dict[str, Any]], artifact_chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    index: list[dict[str, Any]] = []
    for chunk in page_chunks:
        index.append(
            {
                "chunk_id": chunk.get("chunk_id"),
                "chunk_type": chunk.get("chunk_type"),
                "page_start": chunk.get("page_start"),
                "page_end": chunk.get("page_end"),
                "page_refs": chunk.get("page_refs") or [],
                "artifact_ids": chunk.get("artifact_ids") or [],
                "detected_page_types": chunk.get("detected_page_types") or [],
            }
        )
    for chunk in artifact_chunks:
        index.append(
            {
                "chunk_id": chunk.get("chunk_id"),
                "chunk_type": chunk.get("chunk_type"),
                "page_start": chunk.get("page_start"),
                "page_end": chunk.get("page_end"),
                "artifact_ids": chunk.get("artifact_ids") or [],
                "evidence_roles": chunk.get("evidence_roles") or [],
                "image_types": chunk.get("image_types") or [],
            }
        )
    return index


def _renumber_events(events: list[dict[str, Any]], case_id: str) -> list[dict[str, Any]]:
    renumbered: list[dict[str, Any]] = []
    for index, event in enumerate(events, start=1):
        normalized = dict(event)
        normalized["event_order"] = index
        normalized["event_id"] = f"incident_{case_id}_event_{index:03d}" if case_id else f"incident_event_{index:03d}"
        renumbered.append(normalized)
    return renumbered


def _timeline_chunk_warnings(chunk_reports: list[dict[str, Any]]) -> list[str]:
    warnings: list[str] = []
    for report in chunk_reports:
        for warning in report.get("warnings") or []:
            message = f"{report.get('chunk_id')}: {warning}"
            if message not in warnings:
                warnings.append(message)
        for error in report.get("validation_errors") or []:
            message = f"{report.get('chunk_id')} validation error: {error}"
            if message not in warnings:
                warnings.append(message)
    return warnings


def normalize_canonical_response(response: dict[str, Any], packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    case_id = str(packet.get("source_package", {}).get("source_case_id") or "").strip()
    record = response.get("canonical_incident_record") if isinstance(response.get("canonical_incident_record"), dict) else response
    record = dict(record)
    record.setdefault("record_type", "canonical_incident_record")
    record.setdefault("schema_version", "0.1")
    record["stage"] = "stage_4_canonical_incident_record"
    record.setdefault("incident_id", f"incident_{case_id}" if case_id else "")
    if case_id and not str(record.get("incident_id") or "").startswith("incident_"):
        record["incident_id"] = f"incident_{case_id}"
    record.setdefault("source_case_id", case_id)
    record["validation_status"] = "needs_sme_review"
    record.pop("people_involved", None)
    for field, default in {
        "symptoms": [],
        "systems_involved": [],
        "follow_up_required": [],
        "supporting_artifact_ids": [],
        "supporting_timeline_event_ids": [],
        "evidence_chunk_refs": [],
        "source_refs": [],
    }.items():
        if not isinstance(record.get(field), list):
            record[field] = default
    if not isinstance(record.get("site"), dict):
        record["site"] = {
            "primary_label": record.get("site") or "",
            "observed_location_text": [],
            "location_confidence": "unknown",
            "notes": "",
        }
    if not isinstance(record.get("evidence_summary"), dict):
        record["evidence_summary"] = {
            "primary_source_types": [],
            "supporting_artifact_roles": [],
            "conflicts_or_ambiguities": [],
            "unsupported_or_missing_details": [],
        }
    report = _normalize_report(
        response.get("extraction_report") if isinstance(response.get("extraction_report"), dict) else {},
        stage="stage_4_canonical_incident_record",
    )
    report["prompt"] = "stage4_canonical_incident_record_prompt.md"
    report["built_at"] = datetime.now(timezone.utc).isoformat()
    return record, report


def apply_review_evidence_to_canonical_record(
    record: dict[str, Any],
    report: dict[str, Any],
    review_evidence: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    if not review_evidence:
        return record, report
    kpi = review_evidence.get("kpi_tracking") if isinstance(review_evidence.get("kpi_tracking"), dict) else {}
    if not kpi:
        return record, report
    updated = dict(record)
    start_at = kpi.get("start_at") or updated.get("reported_at")
    end_at = kpi.get("end_at") or updated.get("resolved_at")
    minutes = _duration_minutes(start_at, end_at)
    if start_at:
        updated["reported_at"] = start_at
    if end_at:
        updated["resolved_at"] = end_at
    if minutes is not None:
        updated["downtime_minutes"] = minutes
        updated["resolution_time"] = _format_duration(minutes)
    elif kpi.get("resolution_time"):
        updated["resolution_time"] = kpi["resolution_time"]
    updated["kpi_confidence"] = kpi.get("confidence") or ("medium" if minutes is not None else updated.get("kpi_confidence") or "low")
    updated["kpi_tracking"] = {
        "tracking_start_at": start_at,
        "tracking_end_at": end_at,
        "elapsed_minutes": minutes,
        "basis": kpi.get("basis") or "",
        "confidence": updated["kpi_confidence"],
        "source_refs": kpi.get("source_refs") or [],
        "notes": kpi.get("notes") or [],
    }
    for ref in kpi.get("source_refs") or []:
        if ref not in updated.get("source_refs", []):
            updated.setdefault("source_refs", []).append(ref)
    report["notes"] = list(report.get("notes") or []) + ["Applied Stage 4 review evidence to fill KPI tracking time."]
    report["warnings"] = [
        warning
        for warning in report.get("warnings") or []
        if "Exact downtime" not in warning and "Exact outage" not in warning
    ]
    if kpi.get("warning"):
        report["warnings"].append(kpi["warning"])
    return updated, report


def normalize_timeline_response(response: dict[str, Any], packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    case_id = str(packet.get("source_package", {}).get("source_case_id") or "").strip()
    timeline = response.get("timeline_events") if isinstance(response.get("timeline_events"), dict) else response
    timeline = dict(timeline)
    timeline.setdefault("record_type", "incident_timeline_events")
    timeline.setdefault("schema_version", "0.1")
    timeline["stage"] = "stage_4_timeline_events"
    timeline.setdefault("incident_id", f"incident_{case_id}" if case_id else "")
    timeline.setdefault("source_case_id", case_id)
    timeline.setdefault("timestamp_timezone", "unknown")
    timeline.setdefault("ordering_basis", "source_timestamp_then_source_order")
    events = timeline.get("events")
    if not isinstance(events, list):
        events = []
    normalized_events: list[dict[str, Any]] = []
    for index, event in enumerate(events, start=1):
        if not isinstance(event, dict):
            continue
        normalized = dict(event)
        normalized["event_order"] = _int_or_default(normalized.get("event_order"), index)
        normalized.setdefault("event_id", f"incident_{case_id}_event_{index:03d}" if case_id else f"incident_event_{index:03d}")
        normalized.setdefault("timestamp", None)
        normalized.setdefault("timestamp_status", "missing" if normalized.get("timestamp") is None else "visible")
        if normalized.get("timestamp") is None and normalized.get("timestamp_status") == "visible":
            normalized["timestamp_status"] = "partial"
        normalized.setdefault("actor_name", "unknown")
        normalized.setdefault("actor_role", "unknown")
        normalized.setdefault("source_order", {})
        for field in ["systems", "source_refs", "artifact_refs", "evidence_support_type", "uncertainties", "evidence_chunk_refs"]:
            if not isinstance(normalized.get(field), list):
                normalized[field] = []
        normalized.setdefault("confidence", "low")
        normalized_events.append(normalized)
    timeline["events"] = sorted(normalized_events, key=lambda item: item.get("event_order") or 0)
    report = _normalize_report(
        response.get("extraction_report") if isinstance(response.get("extraction_report"), dict) else {},
        stage="stage_4_timeline_events",
    )
    report["prompt"] = "stage4_timeline_events_prompt.md"
    report["event_count"] = len(timeline["events"])
    report["built_at"] = datetime.now(timezone.utc).isoformat()
    return timeline, report


def validate_canonical_record(
    record: dict[str, Any],
    known_page_refs: set[str],
    known_artifact_ids: set[str],
) -> dict[str, list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not record.get("resolution_time") and record.get("downtime_minutes") is None:
        errors.append("Canonical incident record is missing both resolution_time and downtime_minutes.")
    if record.get("validation_status") != "needs_sme_review":
        errors.append("Canonical incident record must keep validation_status needs_sme_review.")
    _validate_refs(record.get("source_refs") or [], known_page_refs, known_artifact_ids, warnings)
    for artifact_id in record.get("supporting_artifact_ids") or []:
        if artifact_id not in known_artifact_ids:
            warnings.append(f"Canonical record references unknown supporting artifact: {artifact_id}")
    return {"validation_errors": errors, "warnings": warnings}


def validate_timeline_events(
    timeline: dict[str, Any],
    known_page_refs: set[str],
    known_artifact_ids: set[str],
) -> dict[str, list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    seen_ids: set[str] = set()
    for event in timeline.get("events") or []:
        event_id = event.get("event_id")
        if not event_id:
            errors.append("Timeline event is missing event_id.")
        elif event_id in seen_ids:
            errors.append(f"Duplicate timeline event_id: {event_id}")
        seen_ids.add(event_id)
        if not event.get("summary"):
            warnings.append(f"Timeline event {event_id} is missing summary.")
        if event.get("timestamp") is None and event.get("timestamp_status") == "visible":
            warnings.append(f"Timeline event {event_id} has timestamp_status visible but timestamp is null.")
        _validate_refs(event.get("source_refs") or [], known_page_refs, known_artifact_ids, warnings)
        for artifact_id in event.get("artifact_refs") or []:
            if artifact_id not in known_artifact_ids:
                warnings.append(f"Timeline event {event_id} references unknown artifact: {artifact_id}")
    return {"validation_errors": errors, "warnings": warnings}


def merge_report_validation(report: dict[str, Any], validation: dict[str, list[str]]) -> dict[str, Any]:
    merged = dict(report)
    for field in ["validation_errors", "warnings"]:
        values = list(merged.get(field) or [])
        for value in validation.get(field) or []:
            if value not in values:
                values.append(value)
        merged[field] = values
    return merged


def parse_llm_response(content: str | dict[str, Any]) -> dict[str, Any]:
    if isinstance(content, dict):
        return content
    text = content.strip()
    fence = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if fence:
        text = fence.group(1).strip()
    return json.loads(text)


def _compact_page(page: dict[str, Any]) -> dict[str, Any]:
    ocr_text = _stage4_safe_page_ocr_text(page)
    return {
        "page_number": page.get("page_number"),
        "page_ref": page.get("page_ref"),
        "detected_page_type": page.get("detected_page_type"),
        "ocr_confidence": page.get("ocr_confidence"),
        "ocr_quality": page.get("ocr_quality"),
        "ocr_word_count": page.get("ocr_word_count"),
        "artifact_ids": page.get("embedded_artifact_ids") or page.get("artifact_ids") or [],
        "ocr_text": ocr_text,
        "ocr_note": _stage4_page_ocr_note(page, ocr_text),
        "source_refs": page.get("source_refs") or [],
    }


def _stage4_safe_page_ocr_text(page: dict[str, Any]) -> str:
    quality = str(page.get("ocr_quality") or "").strip().lower()
    text = str(page.get("ocr_clean_text") or page.get("ocr_text") or page.get("parsed_text") or "").strip()
    if not text:
        return ""
    if quality in {"missing", "garbled"}:
        return ""
    if quality == "low" and _looks_like_symbol_soup(text):
        return ""
    return text


def _stage4_page_ocr_note(page: dict[str, Any], ocr_text: str) -> str:
    if ocr_text:
        return ""
    quality = str(page.get("ocr_quality") or "").strip().lower()
    if quality in {"missing", "garbled", "low"}:
        return f"OCR text omitted from Stage 4 evidence chunks because quality is {quality}."
    if page.get("ocr_text") or page.get("parsed_text"):
        return "OCR text omitted from Stage 4 evidence chunks because it was not suitable for LLM handoff."
    return ""


def _looks_like_symbol_soup(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return True
    alnum = sum(1 for char in stripped if char.isalnum())
    letters = sum(1 for char in stripped if char.isalpha())
    spaces = sum(1 for char in stripped if char.isspace())
    punctuation = sum(1 for char in stripped if not char.isalnum() and not char.isspace())
    total = len(stripped)
    if total and punctuation / total > 0.32 and spaces / total < 0.18:
        return True
    if alnum and letters / alnum < 0.45:
        return True
    suspicious_markers = [
        "bocevive",
        "tewe",
        "mewn",
        "ceemenn",
        "teiiiyadt",
        "peamary",
        "trrteriner",
        "sehdboit",
        "cara0es",
        "ooboafe",
        "praia",
        "exttyheerted",
        "erezylast",
        "heln21prod",
        "so query",
        "sol quey",
        "olouery",
        "aaasang",
        "aooean",
        "dho",
        "modet",
        "shutdewn",
    ]
    lowered = stripped.lower()
    return any(marker in lowered for marker in suspicious_markers)


def _compact_enriched_artifact(artifact: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_id": artifact.get("artifact_id"),
        "page_number": artifact.get("page_number"),
        "page_ref": _first_page_ref(artifact.get("source_refs") or []),
        "image_type": artifact.get("image_type"),
        "evidence_role": artifact.get("evidence_role"),
        "validation_status": artifact.get("validation_status"),
        "short_description": _truncate(artifact.get("short_description") or "", MAX_ARTIFACT_FIELD_CHARS),
        "retrieval_text": _truncate(artifact.get("retrieval_text") or "", MAX_ARTIFACT_FIELD_CHARS),
        "source_supported_claims": _compact_claims(artifact.get("source_supported_claims") or []),
        "state_assessment": _compact_state_assessment(artifact.get("state_assessment") or {}),
        "supports": artifact.get("supports") or {},
        "candidate_support_hints": artifact.get("candidate_support_hints") or {},
        "review_uncertainty": [_truncate(str(item), 240) for item in artifact.get("review_uncertainty") or []][:6],
        "quality_notes": [_truncate(str(item), 240) for item in artifact.get("quality_notes") or []][:6],
        "source_refs": [_source_ref_stub(ref) for ref in artifact.get("source_refs") or []],
    }


def _compact_artifact_enrichment_report(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": report.get("stage"),
        "llm_used": report.get("llm_used"),
        "input_packet_count": report.get("input_packet_count"),
        "output_artifact_count": report.get("output_artifact_count"),
        "enriched_artifact_count": report.get("enriched_artifact_count"),
        "failed_artifact_count": report.get("failed_artifact_count"),
        "warnings": report.get("warnings") or [],
        "validation_errors": report.get("validation_errors") or [],
    }


def _normalize_report(report: dict[str, Any], *, stage: str) -> dict[str, Any]:
    normalized = dict(report)
    normalized["stage"] = stage
    normalized["llm_used"] = True
    for field in ["validation_errors", "warnings", "notes"]:
        if not isinstance(normalized.get(field), list):
            normalized[field] = []
    return normalized


def _validate_refs(
    refs: list[Any],
    known_page_refs: set[str],
    known_artifact_ids: set[str],
    warnings: list[str],
) -> None:
    for ref in refs:
        if isinstance(ref, str):
            if ref.startswith("case_") and ref not in known_page_refs:
                warnings.append(f"Unknown page ref: {ref}")
            elif ref.startswith("artifact_") and ref not in known_artifact_ids:
                warnings.append(f"Unknown artifact ref: {ref}")
            elif not ref.startswith(("case_", "artifact_")):
                warnings.append(f"Source ref should be structured, not a bare label: {ref}")
            continue
        if not isinstance(ref, dict):
            warnings.append("Source ref is neither a string nor an object.")
            continue
        page_ref = ref.get("page_ref")
        artifact_id = ref.get("artifact_id")
        if page_ref and page_ref not in known_page_refs:
            warnings.append(f"Unknown page ref: {page_ref}")
        if artifact_id and artifact_id not in known_artifact_ids:
            warnings.append(f"Unknown artifact ref: {artifact_id}")


def _package_with_stage4_refs(
    package: dict[str, Any],
    output_path: Path,
    canonical_report: dict[str, Any],
    timeline_report: dict[str, Any],
) -> dict[str, Any]:
    enriched_package = dict(package)
    source_bundle = dict(enriched_package.get("source_bundle") or {})
    stage_status = dict(source_bundle.get("stage_status") or {})
    stage_status.update(
        {
            "stage_4": "complete",
            "ready_for_stage_5_incident_runbook_candidates": not canonical_report.get("validation_errors")
            and not timeline_report.get("validation_errors"),
        }
    )
    file_refs = dict(source_bundle.get("file_refs") or {})
    file_refs.update(
        {
            "canonical_incident_record": str(output_path / "canonical_incident_record.json"),
            "canonical_incident_record_extraction_report": str(output_path / "canonical_incident_record_extraction_report.json"),
            "timeline_events": str(output_path / "timeline_events.json"),
            "timeline_event_extraction_report": str(output_path / "timeline_event_extraction_report.json"),
            "stage4_evidence_chunks": str(output_path / "stage4_evidence_chunks.json"),
            "incident_review": str(output_path / "incident_review.md"),
        }
    )
    source_bundle["stage_status"] = stage_status
    source_bundle["file_refs"] = file_refs
    enriched_package["source_bundle"] = source_bundle
    enriched_package["stage4_output_refs"] = {
        "canonical_incident_record": str(output_path / "canonical_incident_record.json"),
        "canonical_incident_record_extraction_report": str(output_path / "canonical_incident_record_extraction_report.json"),
        "timeline_events": str(output_path / "timeline_events.json"),
        "timeline_event_extraction_report": str(output_path / "timeline_event_extraction_report.json"),
        "stage4_evidence_chunks": str(output_path / "stage4_evidence_chunks.json"),
        "incident_review": str(output_path / "incident_review.md"),
    }
    return enriched_package


def _first_page_ref(source_refs: list[dict[str, Any]]) -> str | None:
    for ref in source_refs:
        if isinstance(ref, dict) and ref.get("page_ref"):
            return ref["page_ref"]
    return None


def _int_or_default(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _duration_minutes(start_at: Any, end_at: Any) -> int | None:
    start = _parse_iso_like_datetime(start_at)
    end = _parse_iso_like_datetime(end_at)
    if not start or not end or end < start:
        return None
    return int(round((end - start).total_seconds() / 60))


def _parse_iso_like_datetime(value: Any) -> datetime | None:
    if not value:
        return None
    text = str(value).strip()
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def _format_duration(minutes: int) -> str:
    hours, remainder = divmod(minutes, 60)
    if hours and remainder:
        return f"{hours}h {remainder}m"
    if hours:
        return f"{hours}h"
    return f"{remainder}m"


def _compact_claims(claims: list[Any]) -> list[dict[str, Any]]:
    compact: list[dict[str, Any]] = []
    for claim in claims[:10]:
        if isinstance(claim, dict):
            compact.append(
                {
                    "claim": _truncate(str(claim.get("claim") or ""), MAX_ARTIFACT_FIELD_CHARS),
                    "support_type": claim.get("support_type"),
                    "source_refs": claim.get("source_refs") or [],
                }
            )
        else:
            compact.append({"claim": _truncate(str(claim), MAX_ARTIFACT_FIELD_CHARS), "support_type": "unknown", "source_refs": []})
    return compact


def _compact_state_assessment(state: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(state, dict):
        return {}
    return {
        "state": state.get("state"),
        "confidence": state.get("confidence"),
        "rationale": _truncate(state.get("rationale") or "", MAX_ARTIFACT_FIELD_CHARS),
        "visible_indicators": [_truncate(str(item), 240) for item in state.get("visible_indicators") or []][:6],
        "context_indicators": [_truncate(str(item), 240) for item in state.get("context_indicators") or []][:6],
        "uncertainties": [_truncate(str(item), 240) for item in state.get("uncertainties") or []][:6],
    }


def _source_ref_stub(ref: Any) -> dict[str, Any]:
    if not isinstance(ref, dict):
        return {"raw_ref": str(ref)}
    return {
        "page_ref": ref.get("page_ref"),
        "artifact_id": ref.get("artifact_id"),
        "support_type": ref.get("support_type") or ref.get("source_type"),
        "quote_or_summary": _truncate(ref.get("quote_or_summary") or "", 360),
    }


def _truncate(value: str, max_chars: int) -> str:
    text = " ".join(str(value).split())
    if len(text) <= max_chars:
        return text
    return text[: max(0, max_chars - 3)].rstrip() + "..."


def _unique_list(values: list[Any]) -> list[Any]:
    unique: list[Any] = []
    seen: set[str] = set()
    for value in values:
        if value is None:
            continue
        key = str(value)
        if key in seen:
            continue
        seen.add(key)
        unique.append(value)
    return unique


def _clean_env_value(value: str | None) -> str:
    cleaned = (value or "").strip().strip('"').strip("'")
    if cleaned in {"", "your-api-version", "your_api_version", "<api-version>"}:
        return ""
    return cleaned


def _urlopen_no_proxy(request: urllib.request.Request, timeout: int) -> Any:
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    return opener.open(request, timeout=timeout)
