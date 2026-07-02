"""Stage 2.5 - Artifact enrichment packet preparation.

Builds deterministic joined packets from Stage 2 artifact records, page OCR,
source-package metadata, and duplicate metadata. This stage does not enrich or
interpret artifacts; Stage 3 owns LLM artifact enrichment.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import re

from optisweep_incidence_ingestion.ocr import normalize_ocr_text, normalize_whitespace
from optisweep_incidence_ingestion.utils.json_utils import read_json, write_json


def build_artifact_enrichment_packets(
    *,
    source_package_path: str | Path,
    page_inventory_path: str | Path,
    source_artifacts_path: str | Path,
    output_dir: str | Path,
    artifact_extraction_report_path: str | Path | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    package = read_json(source_package_path)
    page_inventory = read_json(page_inventory_path)
    source_artifacts = read_json(source_artifacts_path)
    extraction_report = read_json(artifact_extraction_report_path) if artifact_extraction_report_path else {}

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    page_by_number = {int(page["page_number"]): page for page in page_inventory}
    duplicate_by_artifact = _duplicate_group_index(extraction_report, source_artifacts)

    packets = [
        build_enrichment_packet(
            artifact=artifact,
            page=page_by_number.get(int(artifact["page_number"])),
            duplicate_metadata=duplicate_by_artifact.get(artifact["artifact_id"]),
        )
        for artifact in source_artifacts
    ]
    report = build_packet_report(package, packets)

    write_json(output_path / "artifact_enrichment_packets.json", packets)
    write_json(output_path / "artifact_enrichment_packet_report.json", report)
    write_json(output_path / "incident_source_package.json", _package_with_stage2_5_refs(package, output_path, report))
    return packets, report


def build_enrichment_packet(
    *,
    artifact: dict[str, Any],
    page: dict[str, Any] | None,
    duplicate_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    source_refs = _merge_source_refs(artifact.get("source_refs") or [], page.get("source_refs") if page else [])
    artifact_ocr_text = artifact.get("ocr_text") or ""
    page_ocr_text = page.get("ocr_text") if page else ""
    artifact_ocr_quality = artifact.get("ocr_quality")
    artifact_ocr_quality = (
        {"quality": artifact_ocr_quality, "clean_text": artifact.get("ocr_clean_text") or clean_ocr_text_for_llm(artifact_ocr_text)}
        if isinstance(artifact_ocr_quality, str)
        else assess_ocr_quality(
        text=artifact_ocr_text,
        confidence=artifact.get("ocr_confidence"),
        expected_context="artifact",
    )
    )
    page_ocr_quality = page.get("ocr_quality") if page else None
    page_ocr_quality = (
        {"quality": page_ocr_quality, "clean_text": page.get("ocr_clean_text") or clean_ocr_text_for_llm(page_ocr_text or "")}
        if isinstance(page_ocr_quality, str)
        else assess_ocr_quality(
        text=page_ocr_text or "",
        confidence=page.get("ocr_confidence") if page else None,
        expected_context="page",
    )
    )
    artifact_ocr_quality = packet_safe_quality(artifact_ocr_quality)
    page_ocr_quality = packet_safe_quality(page_ocr_quality)
    artifact_packet_text = llm_safe_ocr_text(artifact_ocr_text, artifact_ocr_quality)
    page_packet_text = llm_safe_ocr_text(page_ocr_text or "", page_ocr_quality)
    return {
        "packet_type": "incident_artifact_enrichment_packet",
        "schema_version": "0.1",
        "artifact_id": artifact["artifact_id"],
        "image_path": artifact.get("storage_path"),
        "artifact_ocr_text": artifact_packet_text,
        "artifact_ocr_clean_text": artifact_packet_text,
        "artifact_ocr_confidence": artifact.get("ocr_confidence"),
        "artifact_ocr_word_count": artifact.get("ocr_word_count"),
        "artifact_ocr_lines": llm_safe_ocr_lines(artifact.get("ocr_lines") or [], artifact_ocr_quality) if artifact_packet_text else [],
        "artifact_ocr_quality": artifact_ocr_quality,
        "artifact_image_type": artifact.get("image_type"),
        "artifact_type": artifact.get("artifact_type"),
        "artifact_summary_hint": llm_safe_ocr_text(str(artifact.get("summary") or ""), artifact_ocr_quality),
        "artifact_evidence_role_hint": artifact.get("evidence_role"),
        "artifact_what_to_look_at_hint": artifact.get("what_to_look_at") or [],
        "page_number": artifact.get("page_number"),
        "page_ref": page.get("page_ref") if page else None,
        "page_ocr_text": page_packet_text,
        "page_ocr_clean_text": page_packet_text,
        "page_ocr_confidence": page.get("ocr_confidence") if page else None,
        "page_ocr_word_count": page.get("ocr_word_count") if page else None,
        "page_ocr_lines": llm_safe_ocr_lines(page.get("ocr_lines") if page else [], page_ocr_quality) if page_packet_text else [],
        "page_ocr_quality": page_ocr_quality,
        "page_detected_type": page.get("detected_page_type") if page else None,
        "context_role": classify_context_role(page),
        "state_assessment_request": {
            "required_in_stage_3": artifact.get("image_type")
            not in {"teams_chat_screenshot", "salesforce_case_screenshot", "unknown_incident_evidence"},
            "allowed_states": ["healthy", "normal", "warning", "abnormal", "failure", "recovery_in_progress", "unknown"],
            "instruction": "For screenshots of systems, tools, charts, services, APIs, RMS/HMI, or Ignition, Stage 3 should assess whether the visible state appears healthy/normal, warning, abnormal/failure, recovery-in-progress, or unknown, with source-supported rationale.",
        },
        "source_refs": sanitize_source_refs(source_refs, artifact_ocr_quality),
        "duplicate_group": duplicate_metadata,
        "instruction": (
            "Stage 3 must enrich the artifact using the image, artifact OCR, and page OCR context. "
            "Raw OCR may be garbled; use clean OCR only as a readability aid, not as a source of new facts. "
            "Page OCR is surrounding evidence only; do not describe surrounding Teams, Salesforce, "
            "or case text as if it is visible inside the cropped artifact image."
        ),
        "stage2_artifact_record": compact_stage2_artifact_record_for_packet(artifact, artifact_ocr_quality),
    }


def quality_name(quality: dict[str, Any] | str | None) -> str:
    if isinstance(quality, dict):
        return str(quality.get("quality") or "unknown")
    if isinstance(quality, str):
        return quality
    return "unknown"


def packet_safe_quality(quality: dict[str, Any] | str | None) -> dict[str, Any]:
    if isinstance(quality, dict):
        safe = dict(quality)
    else:
        safe = {"quality": quality_name(quality), "clean_text": ""}
    text = clean_ocr_text_for_llm(str(safe.get("clean_text") or ""))
    if quality_name(safe) in {"missing", "garbled"} or looks_like_symbol_soup(text):
        safe["clean_text"] = ""
    else:
        safe["clean_text"] = text
    return safe


def llm_safe_ocr_text(text: str, quality: dict[str, Any] | str | None) -> str:
    quality_value = quality_name(quality)
    if quality_value in {"missing", "garbled"}:
        return ""
    cleaned = clean_ocr_text_for_llm(text)
    if looks_like_symbol_soup(cleaned):
        return ""
    return cleaned


def llm_safe_ocr_lines(lines: list[dict[str, Any]], quality: dict[str, Any] | str | None) -> list[dict[str, Any]]:
    if quality_name(quality) in {"missing", "garbled"}:
        return []
    safe_lines: list[dict[str, Any]] = []
    for line in lines:
        text = clean_ocr_text_for_llm(str(line.get("text") or ""))
        if not text or looks_like_symbol_soup(text):
            continue
        safe_line = dict(line)
        safe_line["text"] = text
        safe_lines.append(safe_line)
    return safe_lines


def compact_stage2_artifact_record_for_packet(
    artifact: dict[str, Any],
    quality: dict[str, Any] | str | None,
) -> dict[str, Any]:
    compact = dict(artifact)
    safe_text = llm_safe_ocr_text(str(artifact.get("ocr_text") or ""), quality)
    compact["ocr_text"] = safe_text
    compact["ocr_clean_text"] = safe_text
    compact["ocr_lines"] = llm_safe_ocr_lines(artifact.get("ocr_lines") or [], quality)
    compact.pop("ocr_attempts", None)
    compact.pop("ocr_provenance", None)
    if not safe_text:
        compact["summary"] = f"{artifact.get('image_type', 'unknown_incident_evidence')} artifact; OCR omitted because quality is {quality_name(quality)}."
        compact["retrieval_text"] = compact["summary"]
        compact["source_refs"] = sanitize_source_refs(compact.get("source_refs") or [], quality)
    else:
        compact["summary"] = clean_ocr_text_for_llm(str(compact.get("summary") or ""))
        compact["retrieval_text"] = clean_ocr_text_for_llm(str(compact.get("retrieval_text") or ""))
        compact["source_refs"] = sanitize_source_refs(compact.get("source_refs") or [], quality)
    return compact


def sanitize_source_refs(source_refs: list[dict[str, Any]], quality: dict[str, Any] | str | None) -> list[dict[str, Any]]:
    sanitized: list[dict[str, Any]] = []
    for ref in source_refs:
        item = dict(ref)
        quote = str(item.get("quote_or_summary") or "")
        safe_quote = llm_safe_ocr_text(quote, quality)
        if quote and not safe_quote:
            item["quote_or_summary"] = f"OCR summary omitted because quality is {quality_name(quality)}."
        elif safe_quote:
            item["quote_or_summary"] = safe_quote
        sanitized.append(item)
    return sanitized


def looks_like_symbol_soup(text: str) -> bool:
    if not text:
        return False
    normalized = normalize_ocr_text(text)
    suspicious_markers = {
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
    }
    if any(marker in normalized for marker in suspicious_markers):
        return True
    total_chars = max(len(text), 1)
    allowed_symbols = set(".,:/\\_-@()[]'\"><=#&?%+|")
    symbol_ratio = sum(
        1
        for char in text
        if not char.isalnum() and not char.isspace() and char not in allowed_symbols
    ) / total_chars
    return symbol_ratio > 0.18 or bool(re.search(r"(.)\1{8,}", normalized))


def classify_context_role(page: dict[str, Any] | None) -> str:
    if not page:
        return "no_page_context"
    text = normalize_ocr_text(page.get("ocr_text") or "")
    detected = page.get("detected_page_type")
    if detected == "salesforce_case_screenshot" or _looks_like_salesforce_case(text):
        return "surrounding_salesforce_case"
    if detected == "teams_chat_screenshot" or _looks_like_teams_chat(text):
        return "surrounding_teams_chat"
    if text:
        return "same_page_context"
    return "no_page_context"


def build_packet_report(package: dict[str, Any], packets: list[dict[str, Any]]) -> dict[str, Any]:
    contexts = Counter(packet.get("context_role") for packet in packets)
    image_types = Counter(packet.get("artifact_image_type") for packet in packets)
    duplicate_count = sum(1 for packet in packets if packet.get("duplicate_group"))
    missing_context = [packet["artifact_id"] for packet in packets if packet.get("context_role") == "no_page_context"]
    noisy_artifact_ocr = [
        packet["artifact_id"]
        for packet in packets
        if packet.get("artifact_ocr_quality", {}).get("quality") in {"low", "garbled"}
    ]
    warnings = []
    if duplicate_count:
        warnings.append("Duplicate metadata is included; Stage 3 should prefer primary artifacts unless duplicates add unique page context.")
    if missing_context:
        warnings.append("One or more packets have no joined page OCR context.")
    if noisy_artifact_ocr:
        warnings.append("One or more artifact OCR strings are low quality or garbled; Stage 3 should rely on the image and mark OCR uncertainty.")
    return {
        "source_package_id": package["source_package_id"],
        "source_id": package["source_id"],
        "source_case_id": package["source_case_id"],
        "ingestion_batch_id": package["ingestion_batch_id"],
        "stage": "stage_2_5_artifact_enrichment_packet_preparation",
        "llm_used": False,
        "packet_count": len(packets),
        "context_roles": dict(sorted(contexts.items())),
        "artifact_image_types": dict(sorted(image_types.items())),
        "duplicate_packet_count": duplicate_count,
        "missing_page_context_artifact_ids": missing_context,
        "noisy_artifact_ocr_ids": noisy_artifact_ocr,
        "warnings": warnings,
        "validation_errors": [],
        "built_at": datetime.now(timezone.utc).isoformat(),
    }


def _package_with_stage2_5_refs(package: dict[str, Any], output_path: Path, report: dict[str, Any]) -> dict[str, Any]:
    enriched_package = dict(package)
    enriched_package["pages"] = [
        sanitize_package_page_for_stage2_5(page)
        for page in enriched_package.get("pages") or []
    ]
    source_bundle = dict(enriched_package.get("source_bundle") or {})
    stage_status = dict(source_bundle.get("stage_status") or {})
    stage_status.update(
        {
            "stage_2_5": "complete",
            "ready_for_stage_3_artifact_enrichment": True,
            "ready_for_stage_4_create_canonical_incident_records_and_timeline": False,
        }
    )
    file_refs = dict(source_bundle.get("file_refs") or {})
    file_refs.update(
        {
            "artifact_enrichment_packets": str(output_path / "artifact_enrichment_packets.json"),
            "artifact_enrichment_packet_report": str(output_path / "artifact_enrichment_packet_report.json"),
        }
    )
    source_bundle["stage_status"] = stage_status
    source_bundle["file_refs"] = file_refs
    source_bundle["artifact_enrichment_packet_summary"] = {
        "packet_count": report["packet_count"],
        "context_roles": report["context_roles"],
        "artifact_image_types": report["artifact_image_types"],
    }
    source_bundle = sanitize_source_bundle_for_stage2_5(source_bundle)
    enriched_package["source_bundle"] = source_bundle
    enriched_package["stage2_5_output_refs"] = {
        "artifact_enrichment_packets": str(output_path / "artifact_enrichment_packets.json"),
        "artifact_enrichment_packet_report": str(output_path / "artifact_enrichment_packet_report.json"),
    }
    return enriched_package


def sanitize_package_page_for_stage2_5(page: dict[str, Any]) -> dict[str, Any]:
    sanitized = dict(page)
    quality = {
        "quality": sanitized.get("ocr_quality") or "unknown",
        "clean_text": sanitized.get("ocr_clean_text") or clean_ocr_text_for_llm(str(sanitized.get("ocr_text") or "")),
    }
    safe_text = llm_safe_ocr_text(str(sanitized.get("ocr_text") or ""), quality)
    sanitized["ocr_text"] = safe_text
    sanitized["ocr_clean_text"] = safe_text
    sanitized["ocr_lines"] = llm_safe_ocr_lines(sanitized.get("ocr_lines") or [], quality) if safe_text else []
    sanitized["source_refs"] = sanitize_source_refs(sanitized.get("source_refs") or [], quality)
    if not safe_text and sanitized.get("ocr_word_count"):
        sanitized["stage2_5_ocr_note"] = f"OCR text omitted from Stage 2.5 handoff because quality is {quality_name(quality)}."
    return sanitized


def sanitize_source_bundle_for_stage2_5(source_bundle: dict[str, Any]) -> dict[str, Any]:
    sanitized = dict(source_bundle)
    text_context = dict(sanitized.get("text_context") or {})
    pages = [
        sanitize_bundle_text_page_for_stage2_5(page)
        for page in text_context.get("pages") or []
    ]
    text_context["pages"] = pages
    text_context["condensed_source_text"] = "\n\n".join(
        f"[page {page.get('page_number')} | {page.get('detected_page_type') or 'unknown'}]\n{page.get('ocr_text') or ''}"
        for page in pages
        if page.get("ocr_text")
    )
    sanitized["text_context"] = text_context

    wrapper_context = dict(sanitized.get("wrapper_text_context") or {})
    wrapper_context["pages"] = [
        sanitize_bundle_text_page_for_stage2_5(page)
        for page in wrapper_context.get("pages") or []
    ]
    sanitized["wrapper_text_context"] = wrapper_context
    sanitized["artifact_manifest"] = [
        sanitize_bundle_artifact_manifest_item_for_stage2_5(item)
        for item in sanitized.get("artifact_manifest") or []
    ]
    sanitized["stage2_5_text_policy"] = (
        "Stage 2.5 incident_source_package omits low, garbled, or missing OCR text when it appears noisy. "
        "Raw OCR remains available in Stage 2 page_inventory/source_artifacts for audit."
    )
    return sanitized


def sanitize_bundle_text_page_for_stage2_5(page: dict[str, Any]) -> dict[str, Any]:
    sanitized = dict(page)
    quality = {
        "quality": sanitized.get("ocr_quality") or "unknown",
        "clean_text": sanitized.get("ocr_clean_text") or clean_ocr_text_for_llm(str(sanitized.get("ocr_text") or "")),
    }
    safe_text = llm_safe_ocr_text(str(sanitized.get("ocr_text") or ""), quality)
    sanitized["ocr_text"] = safe_text
    sanitized["ocr_clean_text"] = safe_text
    sanitized["source_refs"] = sanitize_source_refs(sanitized.get("source_refs") or [], quality)
    if not safe_text and sanitized.get("ocr_word_count"):
        sanitized["stage2_5_ocr_note"] = f"OCR text omitted from Stage 2.5 handoff because quality is {quality_name(quality)}."
    return sanitized


def sanitize_bundle_artifact_manifest_item_for_stage2_5(item: dict[str, Any]) -> dict[str, Any]:
    sanitized = dict(item)
    quality = {
        "quality": sanitized.get("ocr_quality") or "unknown",
        "clean_text": clean_ocr_text_for_llm(str(sanitized.get("summary") or "")),
    }
    safe_summary = llm_safe_ocr_text(str(sanitized.get("summary") or ""), quality)
    sanitized["summary"] = safe_summary
    sanitized["source_refs"] = sanitize_source_refs(sanitized.get("source_refs") or [], quality)
    if not safe_summary and sanitized.get("ocr_word_count"):
        sanitized["stage2_5_ocr_note"] = f"OCR summary omitted from Stage 2.5 handoff because quality is {quality_name(quality)}."
    return sanitized


def _duplicate_group_index(report: dict[str, Any], artifacts: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for group in report.get("duplicate_groups") or []:
        for artifact_id in group.get("artifact_ids") or []:
            index[artifact_id] = group
    for artifact in artifacts:
        group_id = artifact.get("duplicate_group_id")
        if group_id and artifact["artifact_id"] not in index:
            index[artifact["artifact_id"]] = {
                "duplicate_group_id": group_id,
                "primary_artifact_id": artifact.get("extraction_metadata", {}).get("duplicate_group_primary_artifact_id"),
                "artifact_ids": [],
                "group_size": None,
            }
    return index


def _merge_source_refs(*groups: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for group in groups:
        for ref in group or []:
            key = (
                ref.get("source_id"),
                ref.get("page_ref"),
                ref.get("artifact_id"),
                ref.get("quote_or_summary"),
            )
            if key in seen:
                continue
            seen.add(key)
            merged.append(ref)
    return merged


def clean_ocr_text_for_llm(text: str) -> str:
    """Repair common mojibake while preserving OCR as evidence text."""
    safe_replacements = {
        "\u00c2\u00a9": "",
        "\u00c2\u00ae": "",
        "\u00c3\u201a": "",
        "\u00e2\u20ac\u201d": "-",
        "\u00e2\u20ac\u201c": "-",
        "\u00e2\u20ac\u0153": '"',
        "\u00e2\u20ac\u009d": '"',
        "\u00e2\u20ac\u02dc": "'",
        "\u00e2\u20ac\u2122": "'",
        "\u00e2\u20ac\u00a6": "...",
        "\u00ef\u00ac\u0081": "fi",
        "\u00ef\u00ac\u201a": "fl",
    }
    cleaned = text
    for bad, good in safe_replacements.items():
        cleaned = cleaned.replace(bad, good)
    cleaned = "".join(char if ord(char) < 128 else " " for char in cleaned)
    cleaned = re.sub(r"([=_~*#])\1{4,}", r"\1\1\1", cleaned)
    cleaned = re.sub(r"\b(\d)\1{5,}\b", "", cleaned)
    return normalize_whitespace(cleaned)

    cleaned = normalize_whitespace(text)
    replacements = {
        "â€™": "'",
        "â€˜": "'",
        "â€œ": '"',
        "â€": '"',
        "â€”": "-",
        "â€“": "-",
        "Ч": "-",
        "У": ")",
        "С": "'",
        "Â®": "",
        "Â©": "",
        "Â£": "",
        "Â°": "",
        "Â": "",
    }
    for bad, good in replacements.items():
        cleaned = cleaned.replace(bad, good)
    return normalize_whitespace(cleaned)


def assess_ocr_quality(*, text: str, confidence: float | int | None, expected_context: str) -> dict[str, Any]:
    cleaned = clean_ocr_text_for_llm(text)
    word_count = len(cleaned.split())
    if not cleaned:
        quality = "missing"
    else:
        suspicious_markers = ["â", "Â", "�", "|||", "___", "222222", "PRAIA", "TRRTERINER", "Bocevive", "cara0es", "sehdboit"]
        suspicious_count = sum(marker in text for marker in suspicious_markers)
        alpha_chars = sum(ch.isalpha() for ch in cleaned)
        total_chars = max(len(cleaned), 1)
        alpha_ratio = alpha_chars / total_chars
        known_words = sum(
            1
            for word in normalize_ocr_text(cleaned).split()
            if word
            in {
                "memory",
                "trend",
                "ignition",
                "gateway",
                "service",
                "services",
                "optisweep",
                "api",
                "response",
                "status",
                "error",
                "errors",
                "agv",
                "rms",
                "system",
                "restart",
                "command",
                "history",
            }
        )
        low_confidence = confidence is not None and float(confidence) < (55 if expected_context == "artifact" else 60)
        if suspicious_count >= 2 or (suspicious_count >= 1 and low_confidence) or (word_count >= 8 and alpha_ratio < 0.45):
            quality = "garbled"
        elif suspicious_count >= 1 or low_confidence or (word_count >= 8 and known_words == 0 and alpha_ratio < 0.62):
            quality = "low"
        else:
            quality = "usable"
    return {
        "quality": quality,
        "clean_text": cleaned,
        "note": _ocr_quality_note(quality, expected_context),
    }


def _ocr_quality_note(quality: str, expected_context: str) -> str:
    if quality == "missing":
        return f"No {expected_context} OCR text was extracted."
    if quality == "garbled":
        return f"{expected_context.title()} OCR appears garbled; Stage 3 should rely primarily on the image and mark OCR uncertainty."
    if quality == "low":
        return f"{expected_context.title()} OCR may be unreliable; Stage 3 should verify visually."
    return f"{expected_context.title()} OCR appears usable as supporting evidence."


def _looks_like_teams_chat(text: str) -> bool:
    chat_terms = ["reply", "called", "tech support", "hotline", "rdp", "rejoin", "add me", "am", "pm"]
    names = ["zane", "jinhao", "kevin", "christopher", "darrell", "michael", "mitchel"]
    return sum(term in text for term in chat_terms) >= 2 or sum(name in text for name in names) >= 2


def _looks_like_salesforce_case(text: str) -> bool:
    strong_terms = ["case created", "case updated", "salesforce", "account name", "case number", "case owner"]
    weak_terms = ["priority", "subject", "description", "status"]
    return any(term in text for term in strong_terms) and sum(term in text for term in strong_terms + weak_terms) >= 2
