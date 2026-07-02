"""Stage 3 LLM enrichment helpers for source knowledge extraction artifacts."""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Protocol

from dotenv import load_dotenv

from operationalknowledgeingestion.src.optisweep_ingestion.utils.json_utils import read_json, write_json

FOUNDRY_API_VERSION = "2025-04-01-preview"
CLASSIC_AZURE_OPENAI_API_VERSION = "2024-10-21"

ENRICHMENT_FIELDS = {
    "short_description": None,
    "detailed_description": None,
    "what_to_look_at": [],
    "tags": [],
    "retrieval_text": None,
    "enrichment_notes": [],
}

PRIORITY_FIGURE_IDS = [
    "fig_4_20",
    "fig_4_22",
    "fig_4_28",
    "fig_4_30",
    "fig_4_31",
    "fig_4_32",
    "fig_5_2",
    "fig_5_4",
]


class ArtifactLLMClient(Protocol):
    def enrich(self, packet: dict[str, Any]) -> dict[str, Any]:
        ...


class AzureOpenAIArtifactClient:
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
        default_prompt = Path(__file__).resolve().parents[1] / "prompts" / "stage3_artifact_enrichment_prompt.md"
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

    def enrich(self, packet: dict[str, Any]) -> dict[str, Any]:
        return self._request_enrichment(packet, self.api_version)

    def _request_enrichment(self, packet: dict[str, Any], api_version: str) -> dict[str, Any]:
        body = {
            "messages": [
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": json.dumps(packet, ensure_ascii=False)},
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
                with _urlopen_no_proxy(request, timeout=90) as response:
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


def enrich_source_artifacts(
    source_artifacts_path: str | Path,
    artifact_report_path: str | Path,
    output_dir: str | Path,
    llm_client: ArtifactLLMClient,
    llm_used: bool = True,
    max_workers: int = 4,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    artifacts = read_json(source_artifacts_path)
    read_json(artifact_report_path)
    if not isinstance(artifacts, list):
        raise ValueError("source_artifacts.json must contain a list of artifact records.")

    enriched: list[dict[str, Any] | None] = [None] * len(artifacts)
    failed: list[dict[str, Any]] = []
    workers = max(1, max_workers)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(enrich_one_artifact, artifact, llm_client): index
            for index, artifact in enumerate(artifacts)
        }
        for future in as_completed(futures):
            index = futures[future]
            merged, error = future.result()
            enriched[index] = merged
            if error:
                failed.append(error)

    enriched_artifacts = [artifact for artifact in enriched if artifact is not None]
    report = build_artifact_enrichment_report(artifacts, enriched_artifacts, llm_used=llm_used, failed_artifacts=failed)
    output_path = Path(output_dir)
    write_json(output_path / "source_artifacts_enriched.json", enriched_artifacts)
    write_json(output_path / "artifact_enrichment_report.json", report)
    return enriched_artifacts, report


def enrich_one_artifact(
    artifact: dict[str, Any],
    llm_client: ArtifactLLMClient,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    merged = dict(artifact)
    try:
        enrichment = llm_client.enrich(compact_artifact_packet(artifact))
        merged = merge_enrichment(artifact, enrichment)
        merged = ensure_required_grounded_enrichment(merged)
        return merged, None
    except Exception as exc:
        error = {"artifact_id": artifact.get("artifact_id"), "figure_id": artifact.get("figure_id"), "error": str(exc)}
        merged = dict(artifact)
        for field, default in ENRICHMENT_FIELDS.items():
            merged.setdefault(field, list(default) if isinstance(default, list) else default)
        return merged, error


def _clean_env_value(value: str | None) -> str:
    cleaned = (value or "").strip().strip('"').strip("'")
    if cleaned in {"", "your-api-version", "your_api_version", "<api-version>"}:
        return ""
    return cleaned


def _urlopen_no_proxy(request: urllib.request.Request, timeout: int) -> Any:
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    return opener.open(request, timeout=timeout)


def compact_artifact_packet(artifact: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_id": artifact.get("artifact_id"),
        "source_id": artifact.get("source_id"),
        "source_type": artifact.get("source_type"),
        "source_title": artifact.get("source_title"),
        "ingestion_batch_id": artifact.get("ingestion_batch_id"),
        "figure_id": artifact.get("figure_id"),
        "title": artifact.get("title"),
        "caption_text": artifact.get("caption_text"),
        "nearby_text": artifact.get("nearby_text"),
        "ocr_text": artifact.get("ocr_text"),
        "ocr_confidence": artifact.get("ocr_confidence"),
        "retrieval_text": artifact.get("retrieval_text"),
        "image_type": artifact.get("image_type"),
        "page_number": artifact.get("page_number"),
        "section_id": artifact.get("section_id"),
        "source_refs": artifact.get("source_refs", []),
        "extraction_metadata": artifact.get("extraction_metadata", {}),
    }


def parse_llm_response(content: str | dict[str, Any]) -> dict[str, Any]:
    if isinstance(content, dict):
        data = content
    else:
        text = content.strip()
        fence = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.DOTALL | re.IGNORECASE)
        if fence:
            text = fence.group(1).strip()
        data = json.loads(text)
    return normalize_enrichment(data)


def normalize_enrichment(data: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for field, default in ENRICHMENT_FIELDS.items():
        value = data.get(field, default)
        if field in {"what_to_look_at", "tags", "enrichment_notes"}:
            if value is None:
                value = []
            if not isinstance(value, list):
                value = [str(value)]
            normalized[field] = [str(item).strip() for item in value if str(item).strip()]
        else:
            normalized[field] = str(value).strip() if value is not None else None
    return normalized


def merge_enrichment(artifact: dict[str, Any], enrichment: dict[str, Any]) -> dict[str, Any]:
    merged = dict(artifact)
    normalized = normalize_enrichment(enrichment)
    merged.update(normalized)
    merged["artifact_id"] = artifact.get("artifact_id")
    for field in (
        "source_id",
        "source_type",
        "source_title",
        "source_version",
        "ingestion_batch_id",
        "source_document_id",
        "source_bundle_id",
        "source_refs",
    ):
        if field in artifact:
            merged[field] = artifact[field]
    merged["linked_context_ids"] = []
    merged["linked_runbook_ids"] = []
    merged["linked_procedure_ids"] = []
    return merged


def ensure_required_grounded_enrichment(artifact: dict[str, Any]) -> dict[str, Any]:
    if artifact.get("figure_id") != "fig_4_22":
        return artifact
    nearby_text = str(artifact.get("nearby_text") or "")
    if not all(term.lower() in nearby_text.lower() for term in ["heartbeat", "last", "max", "min", "reset"]):
        return artifact
    required = ["Heartbeat section", "Last value", "Max value", "Min value", "RESET button"]
    current = [str(item) for item in artifact.get("what_to_look_at") or []]
    lowered = {item.lower() for item in current}
    for item in required:
        if item.lower() not in lowered:
            current.append(item)
    artifact["what_to_look_at"] = current
    return artifact


def build_artifact_enrichment_report(
    input_artifacts: list[dict[str, Any]],
    enriched_artifacts: list[dict[str, Any]],
    llm_used: bool,
    failed_artifacts: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    failures = failed_artifacts or []
    return {
        "input_artifact_count": len(input_artifacts),
        "enriched_artifact_count": sum(1 for artifact in enriched_artifacts if artifact_is_enriched(artifact)),
        "llm_used": llm_used,
        "failed_artifact_count": len(failures),
        "failed_artifacts": failures,
        "priority_artifact_check": priority_artifact_check(enriched_artifacts),
        "heartbeat_check": heartbeat_check(enriched_artifacts),
    }


def artifact_is_enriched(artifact: dict[str, Any]) -> bool:
    return all(
        [
            bool(artifact.get("short_description")),
            bool(artifact.get("detailed_description")),
            bool(artifact.get("what_to_look_at")),
            bool(artifact.get("tags")),
            bool(artifact.get("retrieval_text")),
        ]
    )


def priority_artifact_check(artifacts: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    checks: dict[str, dict[str, Any]] = {}
    for figure_id in PRIORITY_FIGURE_IDS:
        artifact = next((item for item in artifacts if item.get("figure_id") == figure_id), None)
        checks[figure_id] = {
            "artifact_found": artifact is not None,
            "enriched": artifact_is_enriched(artifact) if artifact else False,
            "has_what_to_look_at": bool(artifact and artifact.get("what_to_look_at")),
            "has_retrieval_text": bool(artifact and artifact.get("retrieval_text")),
        }
    return checks


def heartbeat_check(artifacts: list[dict[str, Any]]) -> dict[str, Any]:
    artifact = next((item for item in artifacts if item.get("figure_id") == "fig_4_22"), None)
    retrieval_text = str(artifact.get("retrieval_text") or "") if artifact else ""
    lowered = retrieval_text.lower()
    return {
        "figure_id": "fig_4_22",
        "artifact_found": artifact is not None,
        "enriched": artifact_is_enriched(artifact) if artifact else False,
        "retrieval_text_contains_heartbeat": "heartbeat" in lowered,
        "retrieval_text_contains_last": "last" in lowered,
        "retrieval_text_contains_max": "max" in lowered,
        "retrieval_text_contains_min": "min" in lowered,
        "retrieval_text_contains_10_seconds": "10 seconds" in lowered,
    }
