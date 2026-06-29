"""Stage 4 LLM extraction helpers for source-specific operational context records."""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Protocol

from dotenv import load_dotenv

from operationalknowledgeingestion.src.optisweep_ingestion.schemas.operational_context import ALLOWED_CONTEXT_TYPES, FORBIDDEN_FIELDS
from operationalknowledgeingestion.src.optisweep_ingestion.services.source_ref_service import apply_lineage, build_source_ref, lineage_from_bundle
from operationalknowledgeingestion.src.optisweep_ingestion.utils.json_utils import read_json, write_json

FOUNDRY_API_VERSION = "2025-04-01-preview"
CLASSIC_AZURE_OPENAI_API_VERSION = "2024-10-21"

MAX_SECTION_TEXT_CHARS = 6000
MAX_ARTIFACT_RETRIEVAL_TEXT_CHARS = 400
MAX_ARTIFACTS_PER_PACKET = 6

IMPORTANT_SECTION_KEYWORDS = [
    "safety",
    "overview",
    "description",
    "abbreviation",
    "controls",
    "hmi",
    "screen",
    "alarm",
    "fault",
    "operation",
    "agv",
    "hospital",
    "operator station",
    "tipper",
    "sorter",
    "scanner",
    "troubleshoot",
    "maintenance",
    "stacklight",
    "api",
    "wcs",
    "rms",
    "subsystem",
]


class ContextLLMClient(Protocol):
    def extract(self, packet: dict[str, Any]) -> list[dict[str, Any]]:
        ...


class AzureOpenAIContextClient:
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
        default_prompt = Path(__file__).resolve().parents[1] / "prompts" / "stage4_operational_context_extraction_prompt.md"
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
            raise RuntimeError(
                "Azure OpenAI is not configured. Set these environment variables: "
                + ", ".join(missing)
            )

    def extract(self, packet: dict[str, Any]) -> list[dict[str, Any]]:
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
                return parse_context_response(payload["choices"][0]["message"]["content"])
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
        candidates: list[tuple[str, dict[str, str], bool]] = []
        parsed = urllib.parse.urlparse(self.endpoint)
        if self._is_foundry_project_endpoint():
            foundry_base = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, "", "", "", "")).rstrip("/")
            candidates.append((f"{foundry_base}/models/chat/completions?{query}", headers, True))
        else:
            candidates.append(
                (
                    f"{self.endpoint}/openai/deployments/{encoded_deployment}/chat/completions?{query}",
                    headers,
                    False,
                )
            )
        return candidates

    def _is_foundry_project_endpoint(self) -> bool:
        parsed = urllib.parse.urlparse(self.endpoint)
        return parsed.netloc.endswith(".services.ai.azure.com") and "/api/projects/" in parsed.path

    def _default_api_version(self, env_api_version: str = "") -> str:
        parsed = urllib.parse.urlparse(self.endpoint)
        if parsed.netloc.endswith(".services.ai.azure.com") and "/api/projects/" in parsed.path:
            return FOUNDRY_API_VERSION
        return env_api_version or CLASSIC_AZURE_OPENAI_API_VERSION


def extract_operational_context(
    source_bundle_path: str | Path,
    source_artifacts_path: str | Path,
    output_dir: str | Path,
    llm_client: ContextLLMClient,
    llm_used: bool = True,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    bundle = read_json(source_bundle_path)
    artifacts = read_json(source_artifacts_path)
    if not isinstance(artifacts, list):
        raise ValueError("source_artifacts_enriched.json must contain a list.")

    lineage = lineage_from_bundle(bundle)
    known_artifact_ids = {a["artifact_id"] for a in artifacts if a.get("artifact_id")}
    packets = build_source_packets(bundle, artifacts, lineage)

    all_contexts: list[dict[str, Any]] = []
    failed_packets: list[dict[str, Any]] = []
    warnings: list[str] = []

    for packet in packets:
        try:
            raw_records = llm_client.extract(packet)
        except Exception as exc:
            failed_packets.append({"section_id": packet.get("section_id"), "error": str(exc)})
            continue

        for record in raw_records:
            record = apply_lineage(record, lineage)
            record = finalize_context_record(record)
            errors = validate_context_record(record, known_artifact_ids)
            if errors:
                warnings.append(
                    f"Dropped record '{record.get('context_id', '?')}' from section "
                    f"'{packet.get('section_id', '?')}': {'; '.join(errors)}"
                )
            else:
                all_contexts.append(record)

    seen_ids: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for ctx in all_contexts:
        cid = ctx.get("context_id", "")
        if cid not in seen_ids:
            seen_ids.add(cid)
            deduped.append(ctx)
        else:
            warnings.append(f"Duplicate context_id dropped: {cid}")

    report = build_extraction_report(
        source_bundle_path=str(source_bundle_path),
        source_artifacts_path=str(source_artifacts_path),
        contexts=deduped,
        lineage=lineage,
        llm_used=llm_used,
        failed_packets=failed_packets,
        warnings=warnings,
    )

    output_path = Path(output_dir)
    write_json(output_path / "operational_context.json", deduped)
    write_json(output_path / "operational_context_extraction_report.json", report)
    return deduped, report


def build_source_packets(
    bundle: dict[str, Any],
    artifacts: list[dict[str, Any]],
    lineage: Any,
) -> list[dict[str, Any]]:
    page_text_lookup: dict[int, str] = {
        int(p["page_number"]): str(p.get("text") or "")
        for p in bundle.get("pages", [])
    }

    artifacts_by_section: dict[str, list[dict[str, Any]]] = {}
    for artifact in artifacts:
        sid = artifact.get("section_id") or ""
        artifacts_by_section.setdefault(sid, []).append(artifact)

    packets: list[dict[str, Any]] = []
    for section in bundle.get("sections", []):
        title = str(section.get("title") or "").lower()
        if lineage.source_type != "training_video" and not _is_important_section(title):
            continue

        page_start = int(section.get("page_start") or 0)
        page_end = int(section.get("page_end") or page_start)
        section_id = section.get("section_id", "")

        pages_text_parts: list[str] = []
        total_chars = 0
        for page_num in range(page_start, page_end + 1):
            text = page_text_lookup.get(page_num, "")
            remaining = MAX_SECTION_TEXT_CHARS - total_chars
            if remaining <= 0:
                break
            chunk = text[:remaining]
            pages_text_parts.append(chunk)
            total_chars += len(chunk)

        section_text = "\n".join(parts for parts in pages_text_parts if parts).strip()

        related_artifacts = artifacts_by_section.get(section_id, [])[:MAX_ARTIFACTS_PER_PACKET]
        artifact_packets = [_compact_artifact(a) for a in related_artifacts]

        source_refs = [ref for ref in section.get("source_refs", []) if isinstance(ref, dict)]
        if not source_refs and page_start:
            source_refs.append(
                build_source_ref(
                    lineage,
                    page_start=page_start,
                    page_end=page_end,
                    section_id=section_id,
                )
            )

        packets.append({
            "source_id": lineage.source_id,
            "source_type": lineage.source_type,
            "source_title": lineage.source_title,
            "ingestion_batch_id": lineage.ingestion_batch_id,
            "section_id": section_id,
            "section_title": section.get("title", ""),
            "page_start": page_start,
            "page_end": page_end,
            "section_text": section_text,
            "related_artifacts": artifact_packets,
            "source_refs": source_refs,
        })

    return packets


def _is_important_section(title: str) -> bool:
    return any(kw in title for kw in IMPORTANT_SECTION_KEYWORDS)


def _compact_artifact(artifact: dict[str, Any]) -> dict[str, Any]:
    retrieval_text = str(artifact.get("retrieval_text") or "")[:MAX_ARTIFACT_RETRIEVAL_TEXT_CHARS]
    return {
        "artifact_id": artifact.get("artifact_id"),
        "title": artifact.get("title"),
        "figure_id": artifact.get("figure_id"),
        "figure_number": artifact.get("figure_number"),
        "page_number": artifact.get("page_number"),
        "tags": artifact.get("tags", [])[:10],
        "retrieval_text": retrieval_text,
        "source_refs": artifact.get("source_refs", []),
    }


def parse_context_response(content: str | dict[str, Any]) -> list[dict[str, Any]]:
    if isinstance(content, dict):
        data = content
    else:
        text = content.strip()
        fence = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.DOTALL | re.IGNORECASE)
        if fence:
            text = fence.group(1).strip()
        data = json.loads(text)
    contexts = data.get("contexts", [])
    if not isinstance(contexts, list):
        return []
    return [c for c in contexts if isinstance(c, dict)]


def finalize_context_record(record: dict[str, Any]) -> dict[str, Any]:
    updated = dict(record)
    artifact_ids = list(updated.get("related_artifact_ids") or [])
    image_refs = list(updated.get("image_refs") or [])
    for artifact_id in artifact_ids:
        if artifact_id not in image_refs:
            image_refs.append(artifact_id)
    updated["image_refs"] = image_refs
    updated.setdefault("related_runbook_candidate_ids", [])
    return updated


def validate_context_record(record: dict[str, Any], known_artifact_ids: set[str]) -> list[str]:
    errors: list[str] = []

    for field in ("context_id", "title", "summary", "details", "retrieval_text"):
        if not str(record.get(field) or "").strip():
            errors.append(f"Missing required field: {field}")

    for field in ("source_id", "source_type", "ingestion_batch_id"):
        if not str(record.get(field) or "").strip():
            errors.append(f"Missing required field: {field}")

    context_type = str(record.get("context_type") or "")
    if context_type not in ALLOWED_CONTEXT_TYPES:
        errors.append(f"Invalid context_type: '{context_type}'")

    source_refs = record.get("source_refs")
    if not source_refs or not isinstance(source_refs, list) or len(source_refs) == 0:
        errors.append("source_refs must contain at least one entry")

    for artifact_id in record.get("related_artifact_ids") or []:
        if artifact_id not in known_artifact_ids:
            errors.append(f"related_artifact_id not found: '{artifact_id}'")

    for artifact_id in record.get("image_refs") or []:
        if artifact_id not in known_artifact_ids:
            errors.append(f"image_ref not found: '{artifact_id}'")

    if str(record.get("validation_status") or "") != "needs_review":
        errors.append("validation_status must be 'needs_review'")

    for forbidden in FORBIDDEN_FIELDS:
        if forbidden in record:
            errors.append(f"Forbidden field present: '{forbidden}'")

    return errors


def build_extraction_report(
    source_bundle_path: str,
    source_artifacts_path: str,
    contexts: list[dict[str, Any]],
    lineage: Any,
    llm_used: bool,
    failed_packets: list[dict[str, Any]],
    warnings: list[str],
) -> dict[str, Any]:
    counts_by_type: dict[str, int] = {}
    for ctx in contexts:
        t = str(ctx.get("context_type") or "unknown")
        counts_by_type[t] = counts_by_type.get(t, 0) + 1

    records_with_artifacts = sum(1 for ctx in contexts if ctx.get("related_artifact_ids"))
    records_without_artifacts = len(contexts) - records_with_artifacts
    records_missing_source_refs = sum(
        1 for ctx in contexts if not ctx.get("source_refs")
    )
    records_missing_source_id = sum(
        1 for ctx in contexts if not str(ctx.get("source_id") or "").strip()
    )

    return {
        "source_id": lineage.source_id,
        "source_type": lineage.source_type,
        "ingestion_batch_id": lineage.ingestion_batch_id,
        "llm_used": llm_used,
        "input_source_bundle": source_bundle_path,
        "input_source_artifacts": source_artifacts_path,
        "context_count": len(contexts),
        "context_counts_by_type": counts_by_type,
        "records_with_artifacts": records_with_artifacts,
        "records_without_artifacts": records_without_artifacts,
        "records_missing_source_refs": records_missing_source_refs,
        "records_missing_source_id": records_missing_source_id,
        "priority_context_check": build_priority_context_check(contexts),
        "failed_packets": failed_packets,
        "warnings": warnings,
    }


def build_priority_context_check(contexts: list[dict[str, Any]]) -> dict[str, Any]:
    def _all_text(ctx: dict[str, Any]) -> str:
        return " ".join([
            ctx.get("title", ""),
            ctx.get("summary", ""),
            ctx.get("details", ""),
            ctx.get("retrieval_text", ""),
            " ".join(ctx.get("key_terms", [])),
        ]).lower()

    def _find(keywords: list[str]) -> dict[str, Any] | None:
        for ctx in contexts:
            text = _all_text(ctx)
            if all(kw.lower() in text for kw in keywords):
                return ctx
        return None

    def _has_artifact_ref(ctx: dict[str, Any] | None) -> bool:
        return bool(ctx and ctx.get("related_artifact_ids"))

    heartbeat_ctx = _find(["heartbeat"])
    op_station_ctx = _find(["operator station"])
    add_tote_ctx = _find(["add tote"])
    remove_tote_ctx = _find(["remove tote"])
    agv_bump_ctx = _find(["agv", "bump"])

    heartbeat_text = _all_text(heartbeat_ctx) if heartbeat_ctx else ""

    return {
        "heartbeat_stats": {
            "found": heartbeat_ctx is not None,
            "has_artifact_ref": _has_artifact_ref(heartbeat_ctx),
            "mentions_last_max_min": all(t in heartbeat_text for t in ["last", "max", "min"]),
            "mentions_10_seconds": "10 seconds" in heartbeat_text,
        },
        "operator_station_hmi": {
            "found": op_station_ctx is not None,
            "has_artifact_ref": _has_artifact_ref(op_station_ctx),
        },
        "hospital_add_tote": {
            "found": add_tote_ctx is not None,
            "has_artifact_ref": _has_artifact_ref(add_tote_ctx),
        },
        "hospital_remove_tote": {
            "found": remove_tote_ctx is not None,
            "has_artifact_ref": _has_artifact_ref(remove_tote_ctx),
        },
        "agv_bump_fault": {
            "found": agv_bump_ctx is not None,
            "has_artifact_ref": _has_artifact_ref(agv_bump_ctx),
        },
    }


def _clean_env_value(value: str | None) -> str:
    cleaned = (value or "").strip().strip('"').strip("'")
    if cleaned in {"", "your-api-version", "your_api_version", "<api-version>"}:
        return ""
    return cleaned
