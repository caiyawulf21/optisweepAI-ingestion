"""Shared Azure AI Vision (Computer Vision) Image Analysis 4.0 client helpers.

Provides the synchronous "analyze" REST call pattern
(POST {endpoint}/computervision/imageanalysis:analyze?api-version=...&features=...)
shared across pipelines. Distinct from shared_pipeline_stages/llm_pacing.py,
which is Azure-OpenAI-chat-specific (JSON chat bodies, endpoint-shape
detection for openai.azure.com/Foundry/Responses) and does not apply to Azure
Computer Vision's raw-image-bytes POST shape.

Company policy: Azure Computer Vision is the only vision model permitted
anywhere in this repository. Do not add local VLM, other-vendor vision, or
image-bearing chat-completion calls; route image understanding through this
module instead.
"""

from __future__ import annotations

import json
import os
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DEFAULT_AZURE_COMPUTER_VISION_API_VERSION = "2023-10-01"
DEFAULT_AZURE_COMPUTER_VISION_MIN_INTERVAL_SEC = 3.5

_rate_lock = threading.Lock()
_last_call_at = 0.0


def _clean_env_value(value: str | None) -> str:
    return (value or "").strip().strip('"').strip("'")


def azure_cv_min_interval_sec() -> float:
    raw = _clean_env_value(os.getenv("AZURE_COMPUTER_VISION_MIN_INTERVAL_SEC"))
    if not raw:
        return DEFAULT_AZURE_COMPUTER_VISION_MIN_INTERVAL_SEC
    try:
        return max(0.0, float(raw))
    except ValueError:
        return DEFAULT_AZURE_COMPUTER_VISION_MIN_INTERVAL_SEC


def wait_for_azure_cv_slot() -> None:
    """Proactively pace calls to stay under the configured requests-per-minute quota."""
    interval = azure_cv_min_interval_sec()
    if interval <= 0:
        return
    global _last_call_at
    with _rate_lock:
        now = time.monotonic()
        wait = interval - (now - _last_call_at)
        if wait > 0:
            time.sleep(wait)
        _last_call_at = time.monotonic()


def post_image_bytes_with_retry(
    url: str,
    headers: dict[str, str],
    image_bytes: bytes,
    *,
    timeout: float = 30.0,
    max_attempts: int = 4,
    label: str = "Azure Computer Vision",
) -> dict[str, Any]:
    """Raw-bytes POST with proactive pacing and reactive 429 backoff/retry."""
    attempt = 0
    while True:
        attempt += 1
        wait_for_azure_cv_slot()
        request = urllib.request.Request(url, data=image_bytes, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            if exc.code == 429 and attempt < max_attempts:
                retry_after_header = exc.headers.get("Retry-After")
                try:
                    retry_after = float(retry_after_header) if retry_after_header else 0.0
                except ValueError:
                    retry_after = 0.0
                sleep_for = max(retry_after, min(5.0 * attempt, 30.0))
                print(
                    f"{label} rate-limited (attempt {attempt}); sleeping {sleep_for:.0f}s",
                    flush=True,
                )
                time.sleep(sleep_for)
                continue
            raise RuntimeError(f"{label} request failed: HTTP {exc.code}: {details}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"{label} request failed: {exc.reason}") from exc


@dataclass(frozen=True)
class DenseCaption:
    text: str
    confidence: float | None
    bounding_box: dict[str, int] | None = None


@dataclass(frozen=True)
class DetectedObject:
    name: str
    confidence: float | None
    bounding_box: dict[str, int] | None = None


@dataclass(frozen=True)
class ImageTag:
    name: str
    confidence: float | None


@dataclass(frozen=True)
class VisionDescription:
    """Structured Azure Computer Vision Image Analysis result for one image."""

    caption_text: str | None
    caption_confidence: float | None
    dense_captions: list[DenseCaption] = field(default_factory=list)
    tags: list[ImageTag] = field(default_factory=list)
    objects: list[DetectedObject] = field(default_factory=list)
    read_text: str = ""
    read_confidence: float | None = None
    read_lines: list[dict[str, Any]] = field(default_factory=list)
    raw_response: dict[str, Any] = field(default_factory=dict)
    provenance: dict[str, Any] = field(default_factory=dict)


class AzureComputerVisionDescriptionClient:
    """Azure AI Vision Image Analysis 4.0 client for caption/tags/objects/read.

    Sibling to (not a subclass of) the operational pipeline's
    AzureComputerVisionOCRClient, which only requests the "read" feature for
    slide OCR. This client requests a richer feature set to support
    generative-enrichment inputs elsewhere in the repo.
    """

    DEFAULT_FEATURES: tuple[str, ...] = ("caption", "denseCaptions", "tags", "objects", "read")

    def __init__(
        self,
        endpoint: str | None = None,
        api_key: str | None = None,
        api_version: str | None = None,
        features: tuple[str, ...] | None = None,
        timeout: float = 30.0,
        max_attempts: int = 4,
    ) -> None:
        from dotenv import load_dotenv

        load_dotenv()
        self.endpoint = _clean_env_value(endpoint or os.getenv("AZURE_COMPUTER_VISION_ENDPOINT")).rstrip("/")
        self.api_key = _clean_env_value(api_key or os.getenv("AZURE_COMPUTER_VISION_KEY"))
        self.api_version = (
            _clean_env_value(api_version or os.getenv("AZURE_COMPUTER_VISION_API_VERSION"))
            or DEFAULT_AZURE_COMPUTER_VISION_API_VERSION
        )
        self.features = features or self.DEFAULT_FEATURES
        self.timeout = timeout
        self.max_attempts = max_attempts
        missing = [
            name
            for name, value in [
                ("AZURE_COMPUTER_VISION_ENDPOINT", self.endpoint),
                ("AZURE_COMPUTER_VISION_KEY", self.api_key),
            ]
            if not value
        ]
        if missing:
            raise RuntimeError(
                "Azure Computer Vision is not configured. Set these environment "
                "variables: " + ", ".join(missing)
            )

    def describe(self, image_path: str | Path) -> VisionDescription:
        image = Path(image_path)
        image_bytes = image.read_bytes()
        url = (
            f"{self.endpoint}/computervision/imageanalysis:analyze"
            f"?api-version={self.api_version}&features={','.join(self.features)}"
        )
        headers = {
            "Content-Type": "application/octet-stream",
            "Ocp-Apim-Subscription-Key": self.api_key,
        }
        payload = post_image_bytes_with_retry(
            url,
            headers,
            image_bytes,
            timeout=self.timeout,
            max_attempts=self.max_attempts,
            label="Azure Computer Vision (image analysis)",
        )
        return self._parse(payload, image)

    def _parse(self, payload: dict[str, Any], image: Path) -> VisionDescription:
        caption = payload.get("captionResult") or {}
        caption_text = caption.get("text")
        caption_confidence = caption.get("confidence")

        dense_captions = [
            DenseCaption(
                text=item.get("text", ""),
                confidence=item.get("confidence"),
                bounding_box=item.get("boundingBox"),
            )
            for item in (payload.get("denseCaptionsResult") or {}).get("values") or []
        ]

        tags = [
            ImageTag(name=item.get("name", ""), confidence=item.get("confidence"))
            for item in (payload.get("tagsResult") or {}).get("values") or []
        ]

        objects = []
        for item in (payload.get("objectsResult") or {}).get("values") or []:
            item_tags = item.get("tags") or []
            first_tag = item_tags[0] if item_tags else {}
            objects.append(
                DetectedObject(
                    name=first_tag.get("name", ""),
                    confidence=first_tag.get("confidence"),
                    bounding_box=item.get("boundingBox"),
                )
            )

        lines: list[str] = []
        line_records: list[dict[str, Any]] = []
        confidences: list[float] = []
        read_result = payload.get("readResult") or {}
        for block in read_result.get("blocks") or []:
            for line in block.get("lines") or []:
                text = str(line.get("text") or "").strip()
                if not text:
                    continue
                lines.append(text)
                line_records.append({"text": text, "bounding_polygon": line.get("boundingPolygon")})
                for word in line.get("words") or []:
                    confidence = word.get("confidence")
                    if isinstance(confidence, (int, float)):
                        confidences.append(float(confidence) * 100.0)
        read_confidence = round(sum(confidences) / len(confidences), 2) if confidences else None

        return VisionDescription(
            caption_text=caption_text,
            caption_confidence=caption_confidence,
            dense_captions=dense_captions,
            tags=tags,
            objects=objects,
            read_text="\n".join(lines).strip(),
            read_confidence=read_confidence,
            read_lines=line_records,
            raw_response=payload,
            provenance={
                "backend": "azure_computer_vision_image_analysis",
                "endpoint": self.endpoint,
                "api_version": self.api_version,
                "features": list(self.features),
                "source_image_path": str(image),
            },
        )
