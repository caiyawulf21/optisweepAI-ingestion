"""Stage 2 support - OCR helpers for incident evidence extraction.

Wraps Tesseract OCR and Azure Computer Vision OCR, plus normalization
utilities used to produce page OCR, artifact OCR, confidence metadata,
word counts, and stable text hashes.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import threading
import time
from typing import Any
import urllib.error
import urllib.request

from dotenv import load_dotenv


@dataclass(frozen=True)
class OCRResult:
    text: str
    confidence: float | None
    backend: str | None
    provenance: dict[str, Any] | None
    word_count: int
    lines: list[dict[str, Any]] | None = None


class TesseractOCRClient:
    """Small wrapper around Tesseract TSV output with confidence provenance."""

    def __init__(self, command: str | None = None, psm: int = 6) -> None:
        self.command = command or os.getenv("TESSERACT_CMD") or _default_windows_command() or "tesseract"
        self.psm = psm

    def extract(self, image_path: str | Path, psm: int | None = None) -> OCRResult:
        image = Path(image_path)
        psm_value = psm if psm is not None else self.psm
        command = [self.command, str(image), "stdout", "--psm", str(psm_value), "tsv"]
        try:
            completed = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=90,
            )
        except FileNotFoundError as exc:
            raise RuntimeError(
                "Tesseract is not available. Install Tesseract or set TESSERACT_CMD."
            ) from exc
        except subprocess.CalledProcessError as exc:
            details = (exc.stderr or exc.stdout or "").strip()
            raise RuntimeError(f"Tesseract OCR failed: {details}") from exc

        words: list[str] = []
        confidences: list[float] = []
        line_words: dict[tuple[str, str, str], list[str]] = {}
        line_confidences: dict[tuple[str, str, str], list[float]] = {}
        for line in completed.stdout.splitlines()[1:]:
            parts = line.split("\t")
            if len(parts) < 12:
                continue
            text = parts[11].strip()
            if not text:
                continue
            words.append(text)
            line_key = (parts[2], parts[3], parts[4])
            line_words.setdefault(line_key, []).append(text)
            try:
                confidence = float(parts[10])
            except ValueError:
                continue
            if confidence >= 0:
                confidences.append(confidence)
                line_confidences.setdefault(line_key, []).append(confidence)
        confidence_value = round(sum(confidences) / len(confidences), 2) if confidences else None
        lines = []
        for index, key in enumerate(line_words, start=1):
            values = line_confidences.get(key) or []
            lines.append(
                {
                    "line_number": index,
                    "text": normalize_whitespace(" ".join(line_words[key])),
                    "confidence": round(sum(values) / len(values), 2) if values else None,
                    "word_count": len(line_words[key]),
                }
            )
        return OCRResult(
            text=normalize_whitespace(" ".join(words)),
            confidence=confidence_value,
            backend="tesseract",
            provenance={
                "backend": "tesseract",
                "command": self.command,
                "psm": psm_value,
                "source_image_path": str(image),
                "confidence": confidence_value,
            },
            word_count=len(words),
            lines=lines,
        )


DEFAULT_AZURE_COMPUTER_VISION_API_VERSION = "2024-02-01"
DEFAULT_AZURE_COMPUTER_VISION_MIN_INTERVAL_SEC = 3.5

_azure_cv_rate_lock = threading.Lock()
_azure_cv_last_call_at = 0.0


def _azure_cv_min_interval_sec() -> float:
    raw = (os.getenv("AZURE_COMPUTER_VISION_MIN_INTERVAL_SEC") or "").strip()
    if not raw:
        return DEFAULT_AZURE_COMPUTER_VISION_MIN_INTERVAL_SEC
    try:
        return max(0.0, float(raw))
    except ValueError:
        return DEFAULT_AZURE_COMPUTER_VISION_MIN_INTERVAL_SEC


def _wait_for_azure_cv_slot() -> None:
    """Proactively pace calls to stay under the configured requests-per-minute
    quota, mirroring operationalknowledgeingestion's AzureComputerVisionOCRClient."""
    interval = _azure_cv_min_interval_sec()
    if interval <= 0:
        return
    global _azure_cv_last_call_at
    with _azure_cv_rate_lock:
        now = time.monotonic()
        wait = interval - (now - _azure_cv_last_call_at)
        if wait > 0:
            time.sleep(wait)
        _azure_cv_last_call_at = time.monotonic()


class AzureComputerVisionOCRClient:
    """OCR via Azure AI Vision Image Analysis 4.0 'Read' feature (synchronous).

    Company policy requires Azure Computer Vision as the only vision backend
    in this repo, so this replaces Tesseract for incident page/artifact text
    OCR. Matches TesseractOCRClient's OCRResult shape (word_count, per-line
    dicts) so it is a drop-in ocr_client for extract_incident_ocr_artifacts.
    """

    def __init__(
        self,
        endpoint: str | None = None,
        api_key: str | None = None,
        api_version: str | None = None,
        timeout: float = 30.0,
        max_attempts: int = 4,
    ) -> None:
        load_dotenv()
        self.endpoint = (endpoint or os.getenv("AZURE_COMPUTER_VISION_ENDPOINT") or "").strip().rstrip("/")
        self.api_key = (api_key or os.getenv("AZURE_COMPUTER_VISION_KEY") or "").strip()
        self.api_version = (
            (api_version or os.getenv("AZURE_COMPUTER_VISION_API_VERSION") or "").strip()
            or DEFAULT_AZURE_COMPUTER_VISION_API_VERSION
        )
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

    def extract(self, image_path: str | Path, psm: int | None = None) -> OCRResult:
        image = Path(image_path)
        image_bytes = image.read_bytes()
        url = f"{self.endpoint}/computervision/imageanalysis:analyze?api-version={self.api_version}&features=read"
        headers = {
            "Content-Type": "application/octet-stream",
            "Ocp-Apim-Subscription-Key": self.api_key,
        }
        payload = self._request_with_retry(url, headers, image_bytes)
        read_result = (payload.get("readResult") or {}) if isinstance(payload, dict) else {}
        words: list[str] = []
        confidences: list[float] = []
        lines: list[dict[str, Any]] = []
        for block in read_result.get("blocks") or []:
            for line_index, line in enumerate(block.get("lines") or [], start=len(lines) + 1):
                line_text = str(line.get("text") or "").strip()
                if not line_text:
                    continue
                line_words = line.get("words") or []
                line_confidences: list[float] = []
                for word in line_words:
                    text = str(word.get("text") or "").strip()
                    if text:
                        words.append(text)
                    confidence = word.get("confidence")
                    if isinstance(confidence, (int, float)):
                        line_confidences.append(float(confidence) * 100.0)
                confidences.extend(line_confidences)
                lines.append(
                    {
                        "line_number": line_index,
                        "text": normalize_whitespace(line_text),
                        "confidence": round(sum(line_confidences) / len(line_confidences), 2)
                        if line_confidences
                        else None,
                        "word_count": len(line_words),
                    }
                )
        confidence_value = round(sum(confidences) / len(confidences), 2) if confidences else None
        return OCRResult(
            text=normalize_whitespace(" ".join(words)),
            confidence=confidence_value,
            backend="azure_cv",
            provenance={
                "backend": "azure_cv",
                "endpoint": self.endpoint,
                "api_version": self.api_version,
                "source_image_path": str(image),
                "confidence": confidence_value,
            },
            word_count=len(words),
            lines=lines,
        )

    def _request_with_retry(self, url: str, headers: dict[str, str], image_bytes: bytes) -> dict[str, Any]:
        attempt = 0
        while True:
            attempt += 1
            _wait_for_azure_cv_slot()
            request = urllib.request.Request(url, data=image_bytes, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    return json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                details = exc.read().decode("utf-8", errors="replace")
                if exc.code == 429 and attempt < self.max_attempts:
                    retry_after_header = exc.headers.get("Retry-After")
                    try:
                        retry_after = float(retry_after_header) if retry_after_header else 0.0
                    except ValueError:
                        retry_after = 0.0
                    print(
                        f"Azure Computer Vision rate-limited (attempt {attempt}); "
                        f"sleeping {max(retry_after, min(5.0 * attempt, 30.0)):.0f}s",
                        flush=True,
                    )
                    time.sleep(max(retry_after, min(5.0 * attempt, 30.0)))
                    continue
                raise RuntimeError(f"Azure Computer Vision OCR failed: HTTP {exc.code}: {details}") from exc
            except urllib.error.URLError as exc:
                raise RuntimeError(f"Azure Computer Vision OCR request failed: {exc.reason}") from exc


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def normalize_ocr_text(text: str) -> str:
    value = text.lower()
    value = re.sub(r"[^a-z0-9\s]+", " ", value)
    return normalize_whitespace(value)


def ocr_text_hash(text: str) -> str | None:
    normalized = normalize_ocr_text(text)
    if not normalized:
        return None
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:16]


def _default_windows_command() -> str | None:
    candidates = [
        Path(os.getenv("LOCALAPPDATA", "")) / "Programs" / "Tesseract-OCR" / "tesseract.exe",
        Path("C:/Program Files/Tesseract-OCR/tesseract.exe"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return None
