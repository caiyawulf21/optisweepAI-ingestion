"""Shared LLM request pacing for Azure OpenAI / Foundry deployments."""

from __future__ import annotations

import json
import os
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable

DEFAULT_LLM_MIN_INTERVAL_SEC = 4.0
DEFAULT_LLM_429_MAX_ATTEMPTS = 24
FOUNDRY_API_VERSION = "2025-04-01-preview"
CLASSIC_AZURE_OPENAI_API_VERSION = "2024-10-21"
_lock = threading.Lock()
_last_request_at = 0.0


class AzureLLMRequestError(RuntimeError):
    def __init__(self, status_code: int, details: str) -> None:
        self.status_code = status_code
        self.details = details
        super().__init__(f"HTTP {status_code}: {details}")


def llm_min_interval_sec() -> float:
    raw = (os.getenv("LLM_MIN_INTERVAL_SEC") or "").strip()
    if not raw:
        return DEFAULT_LLM_MIN_INTERVAL_SEC
    try:
        return max(0.0, float(raw))
    except ValueError:
        return DEFAULT_LLM_MIN_INTERVAL_SEC


def wait_for_llm_slot() -> None:
    interval = llm_min_interval_sec()
    if interval <= 0:
        return
    global _last_request_at
    with _lock:
        now = time.monotonic()
        wait = interval - (now - _last_request_at)
        if wait > 0:
            time.sleep(wait)
        _last_request_at = time.monotonic()


def llm_429_max_attempts() -> int:
    raw = (os.getenv("LLM_429_MAX_ATTEMPTS") or "").strip()
    if not raw:
        return DEFAULT_LLM_429_MAX_ATTEMPTS
    try:
        return max(1, int(raw))
    except ValueError:
        return DEFAULT_LLM_429_MAX_ATTEMPTS


def post_json_with_retry(
    url: str,
    headers: dict[str, str],
    body: dict[str, Any],
    *,
    timeout: float = 120,
    max_attempts: int | None = None,
    label: str = "LLM",
) -> dict[str, Any]:
    attempt = 0
    attempts_limit = max_attempts if max_attempts is not None else llm_429_max_attempts()
    payload = json.dumps(body).encode("utf-8")
    while True:
        attempt += 1
        wait_for_llm_slot()
        request = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            if exc.code == 429 and attempt < attempts_limit:
                retry_after_header = exc.headers.get("Retry-After")
                try:
                    header_wait = float(retry_after_header) if retry_after_header else 0.0
                except ValueError:
                    header_wait = 0.0
                backoff = min(60.0 * attempt, 600.0)
                retry_after = max(header_wait, backoff, llm_min_interval_sec())
                print(
                    f"{label} rate-limited (attempt {attempt}); sleeping {retry_after:.0f}s",
                    flush=True,
                )
                time.sleep(retry_after)
                continue
            raise AzureLLMRequestError(exc.code, details) from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Azure OpenAI request failed: {exc.reason}") from exc


def is_foundry_project_endpoint(endpoint: str) -> bool:
    """True for the Foundry *project* endpoint shape
    (https://<resource>.services.ai.azure.com/api/projects/<project>), which
    uses the /models/chat/completions route. Do not confuse with the Foundry
    *responses* shape (see is_responses_endpoint) hosted on the same domain."""
    parsed = urllib.parse.urlparse(endpoint)
    return parsed.netloc.endswith(".services.ai.azure.com") and "/api/projects/" in parsed.path


def is_responses_endpoint(endpoint: str) -> bool:
    """True when the endpoint already points at a Responses-API route
    (path ends in /responses), e.g. https://<resource>.services.ai.azure.com/openai/v1/responses
    or https://<resource>.openai.azure.com/openai/responses. This must be
    checked before is_foundry_project_endpoint(), since both can share the
    same .services.ai.azure.com host."""
    parsed = urllib.parse.urlparse(endpoint)
    return parsed.path.rstrip("/").endswith("/responses")


def is_v1_responses_endpoint(endpoint: str) -> bool:
    """True for the newer Foundry /openai/v1/responses path style, which
    version itself via the path (/v1/) and expects the literal string
    "preview" as api-version rather than a dated version — distinct from the
    classic .openai.azure.com/openai/responses shape, which still takes a
    dated api-version (see AZURE_MINI_OPENAI_* in .env.example)."""
    parsed = urllib.parse.urlparse(endpoint)
    path = parsed.path.rstrip("/")
    return path.endswith("/responses") and "/v1/" in f"{path}/"


def default_azure_api_version(endpoint: str, env_api_version: str = "") -> str:
    if env_api_version:
        return env_api_version
    if is_v1_responses_endpoint(endpoint):
        return "preview"
    if is_foundry_project_endpoint(endpoint):
        return FOUNDRY_API_VERSION
    return CLASSIC_AZURE_OPENAI_API_VERSION


ResponseParser = Callable[[dict[str, Any]], str | dict[str, Any]]


def azure_chat_candidate_requests(
    *,
    endpoint: str,
    api_key: str,
    deployment: str,
    api_version: str,
    system_prompt: str,
    user_content: str | list[dict[str, Any]],
    temperature: float = 0.1,
) -> list[tuple[str, dict[str, str], dict[str, Any], ResponseParser]]:
    """Build the ordered list of (url, headers, body, response_parser) candidates
    to try for a single-turn system+user chat completion, covering all three
    Azure endpoint shapes this codebase has encountered:

    1. Responses API (path ends in /responses) — e.g. Foundry's
       /openai/v1/responses, or classic /openai/responses.
    2. Foundry *project* endpoint (.services.ai.azure.com/api/projects/...)
       — routes through /models/chat/completions.
    3. Classic Azure OpenAI (<resource>.openai.azure.com) — routes through
       /openai/deployments/{deployment}/chat/completions.

    Each client is expected to iterate the returned list and use the first
    candidate; on a 400/404 it may fall through to the next (kept as a list,
    not a single tuple, to preserve that existing retry behavior), though in
    practice endpoint shape is unambiguous from the URL itself so there is
    normally exactly one candidate.

    user_content may be a plain string, or a list of chat-style multimodal
    content blocks (e.g. [{"type": "text", ...}, {"type": "image_url", ...}])
    for the classic/Foundry-project chat branches — those pass the content
    list straight through to the "messages" body unchanged. The Responses API
    branch (is_responses_endpoint) only supports plain-string user_content
    here: its multimodal content-block shape (input_image/input_text) has no
    verified precedent in this codebase yet, so a list is rejected rather than
    silently sent in a possibly-wrong format. Extend this once that shape is
    confirmed against a real Azure response.
    """
    endpoint = endpoint.rstrip("/")
    parsed = urllib.parse.urlparse(endpoint)
    query = urllib.parse.urlencode({"api-version": api_version})
    headers = {"Content-Type": "application/json", "api-key": api_key}

    if is_responses_endpoint(endpoint):
        if not isinstance(user_content, str):
            raise NotImplementedError(
                "Multimodal user_content is not yet supported for the Responses API "
                "endpoint shape (input_image/input_text block format unverified). "
                "Use a classic or Foundry-project endpoint for image-attached requests, "
                "or extend azure_chat_candidate_requests() once the shape is confirmed."
            )
        url = urllib.parse.urlunparse(
            (parsed.scheme, parsed.netloc, parsed.path.rstrip("/"), "", query, "")
        )
        body = {
            "model": deployment,
            "input": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            "text": {"format": {"type": "json_object"}},
        }
        return [(url, headers, body, parse_responses_payload)]

    chat_body = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "temperature": temperature,
        "response_format": {"type": "json_object"},
    }
    if is_foundry_project_endpoint(endpoint):
        foundry_base = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, "", "", "", "")).rstrip("/")
        url = f"{foundry_base}/models/chat/completions?{query}"
        return [(url, headers, chat_body | {"model": deployment}, parse_chat_payload)]

    encoded_deployment = urllib.parse.quote(deployment, safe="")
    url = f"{endpoint}/openai/deployments/{encoded_deployment}/chat/completions?{query}"
    return [(url, headers, chat_body, parse_chat_payload)]


def parse_chat_payload(payload: dict[str, Any]) -> str:
    return payload["choices"][0]["message"]["content"]


def parse_responses_payload(payload: dict[str, Any]) -> str:
    output_text = payload.get("output_text")
    if output_text:
        return output_text
    chunks: list[str] = []
    for item in payload.get("output", []):
        for content in item.get("content", []):
            text = content.get("text")
            if text:
                chunks.append(text)
    return "".join(chunks)


def parse_json_object_content(content: str | dict[str, Any]) -> dict[str, Any]:
    """Parse a chat/response text field that should contain a JSON object,
    tolerating a ```json ... ``` fence some models still wrap output in."""
    if isinstance(content, dict):
        return content
    text = content.strip()
    fence = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if fence:
        text = fence.group(1).strip()
    return json.loads(text)


def request_azure_chat_json(
    *,
    endpoint: str,
    api_key: str,
    deployment: str,
    api_version: str,
    system_prompt: str,
    user_content: str | list[dict[str, Any]],
    label: str,
    timeout: float = 120,
    temperature: float = 0.1,
) -> dict[str, Any]:
    """End-to-end helper: build candidate requests for whichever Azure
    endpoint shape is configured, POST with retry/pacing, and parse the JSON
    object out of the model's text response. Raises RuntimeError if every
    candidate fails with a non-400/404 error, or AzureLLMRequestError details
    joined together if all candidates 400/404."""
    candidates = azure_chat_candidate_requests(
        endpoint=endpoint,
        api_key=api_key,
        deployment=deployment,
        api_version=api_version,
        system_prompt=system_prompt,
        user_content=user_content,
        temperature=temperature,
    )
    errors: list[str] = []
    for url, headers, body, response_parser in candidates:
        try:
            payload = post_json_with_retry(url, headers, body, timeout=timeout, label=label)
            return parse_json_object_content(response_parser(payload))
        except AzureLLMRequestError as exc:
            errors.append(str(exc))
            if exc.status_code not in {400, 404}:
                raise RuntimeError(f"{label} request failed with HTTP {exc.status_code}: {exc.details}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"{label} request failed: {exc.reason}") from exc
    raise RuntimeError(f"{label} request failed for endpoint patterns tried: " + " | ".join(errors))
