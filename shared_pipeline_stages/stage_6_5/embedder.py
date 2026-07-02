from __future__ import annotations

import hashlib
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Protocol

from dotenv import load_dotenv

CLASSIC_AZURE_OPENAI_API_VERSION = "2024-10-21"
FOUNDRY_API_VERSION = "2025-04-01-preview"
DEFAULT_BATCH_SIZE = 16


class RunbookEmbedder(Protocol):
    @property
    def model_name(self) -> str: ...

    def embed_texts(self, texts: list[str]) -> list[list[float]]: ...


class MockRunbookEmbedder:
    def __init__(self, dimensions: int = 8) -> None:
        self.dimensions = dimensions

    @property
    def model_name(self) -> str:
        return "mock-embedder"

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [_hash_vector(text, self.dimensions) for text in texts]


class AzureOpenAIEmbedder:
    def __init__(
        self,
        endpoint: str | None = None,
        api_key: str | None = None,
        deployment: str | None = None,
        api_version: str | None = None,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
        load_dotenv()
        self.endpoint = _clean_env_value(endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")).rstrip("/")
        self.api_key = _clean_env_value(api_key or os.getenv("AZURE_OPENAI_API_KEY"))
        self.deployment = _clean_env_value(
            deployment
            or os.getenv("AZURE_EMBEDDINGS_DEPLOYMENT")
            or os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
        )
        self.api_version = _clean_env_value(api_version) or _default_embedding_api_version()
        self.batch_size = batch_size
        missing = [
            name
            for name, value in [
                ("AZURE_OPENAI_ENDPOINT", self.endpoint),
                ("AZURE_OPENAI_API_KEY", self.api_key),
                ("AZURE_EMBEDDINGS_DEPLOYMENT", self.deployment),
            ]
            if not value
        ]
        if missing:
            raise RuntimeError(
                "Azure OpenAI embeddings are not configured. Set: " + ", ".join(missing)
            )

    @property
    def model_name(self) -> str:
        return self.deployment

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for start in range(0, len(texts), self.batch_size):
            batch = texts[start : start + self.batch_size]
            vectors.extend(self._embed_batch(batch))
        return vectors

    def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        body = {"input": texts}
        errors: list[str] = []
        for url, headers, include_model in self._candidate_requests():
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
                return _parse_embedding_response(payload, len(texts))
            except urllib.error.HTTPError as exc:
                details = exc.read().decode("utf-8", errors="replace")
                errors.append(f"HTTP {exc.code}: {details}")
                if exc.code not in {400, 404}:
                    raise RuntimeError(
                        f"Azure embedding request failed with HTTP {exc.code}: {details}"
                    ) from exc
            except urllib.error.URLError as exc:
                raise RuntimeError(f"Azure embedding request failed: {exc.reason}") from exc
        raise RuntimeError(
            "Azure embedding request failed for endpoint patterns tried: " + " | ".join(errors)
        )

    def _candidate_requests(self) -> list[tuple[str, dict[str, str], bool]]:
        headers = {"Content-Type": "application/json", "api-key": self.api_key}
        encoded_deployment = urllib.parse.quote(self.deployment, safe="")
        candidates: list[tuple[str, dict[str, str], bool]] = []
        foundry_base = _foundry_base_url(self.endpoint)
        if foundry_base:
            for api_version in _embedding_api_version_candidates(self.api_version):
                query = urllib.parse.urlencode({"api-version": api_version})
                candidates.append(
                    (
                        f"{foundry_base}/openai/deployments/{encoded_deployment}/embeddings?{query}",
                        headers,
                        False,
                    )
                )
                candidates.append(
                    (
                        f"{foundry_base}/models/embeddings?{query}",
                        headers,
                        True,
                    )
                )
        query = urllib.parse.urlencode({"api-version": self.api_version})
        candidates.append(
            (
                f"{self.endpoint}/openai/deployments/{encoded_deployment}/embeddings?{query}",
                headers,
                False,
            )
        )
        return candidates


def retrieval_text_hash(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _parse_embedding_response(payload: dict, expected_count: int) -> list[list[float]]:
    data = payload.get("data") or []
    if len(data) != expected_count:
        raise RuntimeError("Azure embedding response size mismatch.")
    ordered = sorted(data, key=lambda item: int(item.get("index", 0)))
    return [list(item.get("embedding") or []) for item in ordered]


def _default_embedding_api_version() -> str:
    load_dotenv()
    embedding_version = _clean_env_value(os.getenv("AZURE_EMBEDDINGS_API_VERSION"))
    if embedding_version:
        return embedding_version
    endpoint = _clean_env_value(os.getenv("AZURE_OPENAI_ENDPOINT"))
    if _is_foundry_project_endpoint(endpoint):
        return FOUNDRY_API_VERSION
    return _clean_env_value(os.getenv("AZURE_OPENAI_API_VERSION")) or CLASSIC_AZURE_OPENAI_API_VERSION


def _foundry_base_url(endpoint: str) -> str:
    if not _is_foundry_project_endpoint(endpoint):
        return ""
    parsed = urllib.parse.urlparse(endpoint)
    return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, "", "", "", "")).rstrip("/")


def _embedding_api_version_candidates(preferred: str) -> list[str]:
    ordered = [preferred, FOUNDRY_API_VERSION, "2024-02-15-preview", CLASSIC_AZURE_OPENAI_API_VERSION]
    seen: set[str] = set()
    result: list[str] = []
    for value in ordered:
        cleaned = _clean_env_value(value)
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            result.append(cleaned)
    return result


def _is_foundry_project_endpoint(endpoint: str) -> bool:
    parsed = urllib.parse.urlparse(endpoint)
    return parsed.netloc.endswith(".services.ai.azure.com") and "/api/projects/" in parsed.path


def _hash_vector(text: str, dimensions: int) -> list[float]:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    values = [((digest[index % len(digest)] / 255.0) * 2.0) - 1.0 for index in range(dimensions)]
    norm = sum(value * value for value in values) ** 0.5
    if norm == 0.0:
        return values
    return [value / norm for value in values]


def _clean_env_value(value: str | None) -> str:
    return (value or "").strip().strip('"').strip("'")
