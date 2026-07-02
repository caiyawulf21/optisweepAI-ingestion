"""Stage 3 - LLM incident artifact enrichment.

Reads Stage 2.5 joined enrichment packets and uses Azure OpenAI to produce
English, source-grounded enriched artifact records. This stage requires an LLM;
fake deterministic enrichment is intentionally not supported.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol
import base64
import json
import mimetypes
import os
import re
import urllib.error
import urllib.parse
import urllib.request

from dotenv import load_dotenv

from optisweep_incidence_ingestion.utils.json_utils import read_json, write_json
from optisweep_incidence_ingestion.utils.markdown_review import write_stage3_review_markdown

FOUNDRY_API_VERSION = "2025-04-01-preview"
CLASSIC_AZURE_OPENAI_API_VERSION = "2024-10-21"

REQUIRED_ENRICHMENT_FIELDS = {
    "artifact_id": "",
    "short_description": "",
    "detailed_description": "",
    "visual_observations": [],
    "contextual_interpretation": [],
    "source_supported_claims": [],
    "state_assessment": {},
    "evidence_role": "unknown",
    "supports": {},
    "candidate_support_hints": {},
    "what_to_look_at": [],
    "ocr_highlights": {},
    "duplicate_analysis": {},
    "review_uncertainty": [],
    "quality_notes": [],
    "tags": [],
    "retrieval_text": "",
    "validation_status": "needs_sme_review",
    "source_refs": [],
}

VALID_EVIDENCE_ROLES = {
    "symptom_evidence",
    "diagnostic_evidence",
    "action_evidence",
    "validation_evidence",
    "escalation_evidence",
    "incident_context_evidence",
    "duplicate_context",
    "unknown",
}


class ArtifactEnrichmentLLMClient(Protocol):
    def enrich(self, packet: dict[str, Any]) -> dict[str, Any]:
        ...


class AzureOpenAIIncidentArtifactClient:
    def __init__(
        self,
        endpoint: str | None = None,
        api_key: str | None = None,
        deployment: str | None = None,
        api_version: str | None = None,
        prompt_path: str | Path | None = None,
        include_images: bool = True,
    ) -> None:
        load_dotenv()
        self.endpoint = _clean_env_value(endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")).rstrip("/")
        self.api_key = _clean_env_value(api_key or os.getenv("AZURE_OPENAI_API_KEY"))
        self.deployment = _clean_env_value(deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT"))
        env_api_version = _clean_env_value(os.getenv("AZURE_OPENAI_API_VERSION"))
        self.api_version = _clean_env_value(api_version) or self._default_api_version(env_api_version)
        default_prompt = Path(__file__).resolve().parent / "prompts" / "stage3_artifact_enrichment_prompt.md"
        self.prompt = Path(prompt_path or default_prompt).read_text(encoding="utf-8")
        self.include_images = include_images
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

    def enrich(self, packet: dict[str, Any]) -> dict[str, Any]:
        return self._request_enrichment(packet, self.api_version)

    def _request_enrichment(self, packet: dict[str, Any], api_version: str) -> dict[str, Any]:
        body = {
            "messages": [
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": self._user_content(packet)},
            ],
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
        }
        errors: list[str] = []
        for url, headers, include_model in self._candidate_requests(api_version):
            request_body = body | ({"model": self.deployment} if include_model else {})
            request = urllib.request.Request(
                url,
                data=json.dumps(request_body).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            try:
                with _urlopen_no_proxy(request, timeout=120) as response:
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

    def _user_content(self, packet: dict[str, Any]) -> str | list[dict[str, Any]]:
        text = json.dumps(_packet_for_llm(packet), ensure_ascii=False)
        if not self.include_images:
            return text
        image_url = _image_data_url(packet.get("image_path"))
        if not image_url:
            return text
        return [
            {"type": "text", "text": text},
            {"type": "image_url", "image_url": {"url": image_url}},
        ]

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


def enrich_incident_artifacts(
    *,
    artifact_enrichment_packets_path: str | Path,
    output_dir: str | Path,
    llm_client: ArtifactEnrichmentLLMClient,
    llm_used: bool = True,
    max_workers: int = 4,
    source_package_path: str | Path | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not llm_used:
        raise ValueError("Stage 3 requires an LLM. Fake enrichment is not supported.")
    packets = read_json(artifact_enrichment_packets_path)
    if not isinstance(packets, list):
        raise ValueError("artifact_enrichment_packets.json must contain a list of packet records.")

    enriched: list[dict[str, Any] | None] = [None] * len(packets)
    failed: list[dict[str, Any]] = []
    workers = max(1, max_workers)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(enrich_one_packet, packet, llm_client): index
            for index, packet in enumerate(packets)
        }
        for future in as_completed(futures):
            index = futures[future]
            merged, error = future.result()
            enriched[index] = merged
            if error:
                failed.append(error)

    enriched_artifacts = [artifact for artifact in enriched if artifact is not None]
    report = build_artifact_enrichment_report(packets, enriched_artifacts, failed)
    output_path = Path(output_dir)
    write_json(output_path / "source_artifacts_enriched.json", enriched_artifacts)
    write_json(output_path / "artifact_enrichment_report.json", report)
    write_stage3_review_markdown(output_path / "artifact_enrichment_review.md", enriched_artifacts, report)
    if source_package_path:
        package = read_json(source_package_path)
        write_json(output_path / "incident_source_package.json", _package_with_stage3_refs(package, output_path, report))
    return enriched_artifacts, report


def enrich_one_packet(
    packet: dict[str, Any],
    llm_client: ArtifactEnrichmentLLMClient,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    artifact = dict(packet.get("stage2_artifact_record") or {})
    try:
        enrichment = normalize_enrichment(llm_client.enrich(packet), packet)
        merged = merge_enrichment(artifact, enrichment, packet)
        return merged, None
    except Exception as exc:
        merged = dict(artifact)
        merged.update(_failed_enrichment_defaults(packet, str(exc)))
        return merged, {"artifact_id": packet.get("artifact_id"), "error": str(exc)}


def parse_llm_response(content: str | dict[str, Any]) -> dict[str, Any]:
    if isinstance(content, dict):
        return content
    text = content.strip()
    fence = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if fence:
        text = fence.group(1).strip()
    return json.loads(text)


def normalize_enrichment(data: dict[str, Any], packet: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for field, default in REQUIRED_ENRICHMENT_FIELDS.items():
        value = data.get(field, default)
        if field in {
            "visual_observations",
            "contextual_interpretation",
            "source_supported_claims",
            "what_to_look_at",
            "review_uncertainty",
            "quality_notes",
            "tags",
        }:
            normalized[field] = _list(value)
        elif field in {"supports", "candidate_support_hints", "ocr_highlights", "duplicate_analysis", "state_assessment"}:
            normalized[field] = value if isinstance(value, dict) else {}
        else:
            normalized[field] = str(value).strip() if value is not None else None
    normalized["artifact_id"] = packet.get("artifact_id")
    role = normalized.get("evidence_role")
    normalized["evidence_role"] = role if role in VALID_EVIDENCE_ROLES else "unknown"
    normalized["validation_status"] = "needs_sme_review"
    normalized["source_refs"] = packet.get("source_refs") or []
    return normalized


def merge_enrichment(artifact: dict[str, Any], enrichment: dict[str, Any], packet: dict[str, Any]) -> dict[str, Any]:
    merged = dict(artifact)
    merged.update(enrichment)
    merged["record_type"] = "incident_source_artifact_enriched"
    merged["schema_version"] = "0.1"
    merged["stage"] = "stage_3_artifact_enrichment"
    merged["source_refs"] = packet.get("source_refs") or artifact.get("source_refs") or []
    merged["linked_timeline_event_ids"] = artifact.get("linked_timeline_event_ids") or []
    merged["linked_runbook_candidate_ids"] = artifact.get("linked_runbook_candidate_ids") or []
    merged["enrichment_metadata"] = {
        "method": "azure_openai_stage_3_artifact_enrichment",
        "llm_used": True,
        "prompt": "stage3_artifact_enrichment_prompt.md",
        "packet_source": "artifact_enrichment_packets.json",
        "context_role": packet.get("context_role"),
        "built_at": datetime.now(timezone.utc).isoformat(),
    }
    return merged


def build_artifact_enrichment_report(
    packets: list[dict[str, Any]],
    enriched_artifacts: list[dict[str, Any]],
    failed_artifacts: list[dict[str, Any]],
) -> dict[str, Any]:
    enriched_count = sum(1 for artifact in enriched_artifacts if artifact_is_enriched(artifact))
    return {
        "stage": "stage_3_artifact_enrichment",
        "llm_used": True,
        "prompt": "stage3_artifact_enrichment_prompt.md",
        "input_packet_count": len(packets),
        "output_artifact_count": len(enriched_artifacts),
        "enriched_artifact_count": enriched_count,
        "failed_artifact_count": len(failed_artifacts),
        "failed_artifacts": failed_artifacts,
        "validation_errors": [] if not failed_artifacts else ["One or more artifacts failed LLM enrichment."],
        "warnings": _report_warnings(enriched_artifacts, failed_artifacts),
        "built_at": datetime.now(timezone.utc).isoformat(),
    }


def artifact_is_enriched(artifact: dict[str, Any]) -> bool:
    return all(
        [
            bool(artifact.get("short_description")),
            bool(artifact.get("detailed_description")),
            bool(artifact.get("visual_observations")),
            bool(artifact.get("what_to_look_at")),
            bool(artifact.get("retrieval_text")),
        ]
    )


def _package_with_stage3_refs(package: dict[str, Any], output_path: Path, report: dict[str, Any]) -> dict[str, Any]:
    enriched_package = dict(package)
    source_bundle = dict(enriched_package.get("source_bundle") or {})
    stage_status = dict(source_bundle.get("stage_status") or {})
    stage_status.update(
        {
            "stage_3": "complete",
            "ready_for_stage_4_create_canonical_incident_records_and_timeline": report["failed_artifact_count"] == 0,
        }
    )
    file_refs = dict(source_bundle.get("file_refs") or {})
    file_refs.update(
        {
            "source_artifacts_enriched": str(output_path / "source_artifacts_enriched.json"),
            "artifact_enrichment_report": str(output_path / "artifact_enrichment_report.json"),
            "artifact_enrichment_review": str(output_path / "artifact_enrichment_review.md"),
        }
    )
    source_bundle["stage_status"] = stage_status
    source_bundle["file_refs"] = file_refs
    enriched_package["source_bundle"] = source_bundle
    enriched_package["stage3_output_refs"] = {
        "source_artifacts_enriched": str(output_path / "source_artifacts_enriched.json"),
        "artifact_enrichment_report": str(output_path / "artifact_enrichment_report.json"),
        "artifact_enrichment_review": str(output_path / "artifact_enrichment_review.md"),
    }
    return enriched_package


def _failed_enrichment_defaults(packet: dict[str, Any], error: str) -> dict[str, Any]:
    return {
        "record_type": "incident_source_artifact_enriched",
        "schema_version": "0.1",
        "stage": "stage_3_artifact_enrichment",
        "short_description": "",
        "detailed_description": "",
        "visual_observations": [],
        "contextual_interpretation": [],
        "source_supported_claims": [],
        "state_assessment": {
            "state": "unknown",
            "confidence": "low",
            "rationale": "LLM enrichment failed; state was not assessed.",
            "visible_indicators": [],
            "context_indicators": [],
            "uncertainties": ["Stage 3 enrichment failed."],
        },
        "evidence_role": "unknown",
        "supports": {"canonical_incident_record": False, "timeline_event": False, "runbook_candidate": False},
        "candidate_support_hints": {"supports_runbook_candidate": False, "support_reason": "LLM enrichment failed.", "matched_terms": []},
        "what_to_look_at": [],
        "ocr_highlights": {
            "artifact_ocr_text": packet.get("artifact_ocr_text") or "",
            "artifact_ocr_clean_text": packet.get("artifact_ocr_clean_text") or "",
            "artifact_ocr_quality": packet.get("artifact_ocr_quality", {}).get("quality"),
            "page_ocr_context": packet.get("page_ocr_text") or "",
            "page_ocr_clean_context": packet.get("page_ocr_clean_text") or "",
            "page_ocr_quality": packet.get("page_ocr_quality", {}).get("quality"),
            "important_visible_text": [],
        },
        "duplicate_analysis": packet.get("duplicate_group") or {},
        "review_uncertainty": ["LLM enrichment failed; inspect source image manually."],
        "quality_notes": [error],
        "tags": [],
        "retrieval_text": "",
        "validation_status": "needs_sme_review",
        "source_refs": packet.get("source_refs") or [],
        "enrichment_metadata": {
            "method": "azure_openai_stage_3_artifact_enrichment",
            "llm_used": True,
            "prompt": "stage3_artifact_enrichment_prompt.md",
            "packet_source": "artifact_enrichment_packets.json",
            "failed": True,
            "error": error,
            "built_at": datetime.now(timezone.utc).isoformat(),
        },
    }


def _packet_for_llm(packet: dict[str, Any]) -> dict[str, Any]:
    packet_copy = dict(packet)
    artifact = dict(packet_copy.get("stage2_artifact_record") or {})
    artifact.pop("ocr_provenance", None)
    packet_copy["stage2_artifact_record"] = artifact
    return packet_copy


def _image_data_url(path_value: str | None) -> str | None:
    if not path_value:
        return None
    path = Path(path_value)
    if not path.exists() or not path.is_file():
        return None
    mime_type = mimetypes.guess_type(path.name)[0] or "image/png"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{data}"


def _list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _report_warnings(enriched_artifacts: list[dict[str, Any]], failed_artifacts: list[dict[str, Any]]) -> list[str]:
    warnings: list[str] = []
    if failed_artifacts:
        warnings.append("Some artifacts failed LLM enrichment and contain fallback failure records.")
    if any("garbled" in " ".join(artifact.get("review_uncertainty") or []).lower() for artifact in enriched_artifacts):
        warnings.append("One or more artifacts were flagged as having garbled OCR.")
    return warnings


def _clean_env_value(value: str | None) -> str:
    cleaned = (value or "").strip().strip('"').strip("'")
    if cleaned in {"", "your-api-version", "your_api_version", "<api-version>"}:
        return ""
    return cleaned


def _urlopen_no_proxy(request: urllib.request.Request, timeout: int) -> Any:
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    return opener.open(request, timeout=timeout)
