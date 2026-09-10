"""HTTP helpers for Salesforce probe calls (stdlib only)."""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable

from connectors.salesforce.errors import (
    CATEGORY_ENDPOINT,
    CATEGORY_MALFORMED,
    CATEGORY_NETWORK,
    CATEGORY_UNEXPECTED,
    SalesforceProbeError,
)

HttpTransport = Callable[[str, bytes | None, dict[str, str], float], tuple[int, str]]
BinaryHttpTransport = Callable[[str, dict[str, str], float], tuple[int, bytes]]


def _raise_url_error(exc: urllib.error.URLError) -> None:
    reason = getattr(exc, "reason", None)
    detail = str(reason if reason is not None else exc)
    lowered = detail.lower()
    if "getaddrinfo" in lowered or "name or service not known" in lowered or "nodename" in lowered:
        raise SalesforceProbeError(
            CATEGORY_NETWORK,
            f"DNS/network failure reaching Salesforce host: {type(reason).__name__ if reason else 'URLError'}.",
        ) from None
    if "timed out" in lowered or "timeout" in lowered:
        raise SalesforceProbeError(
            CATEGORY_NETWORK,
            "Network timeout contacting Salesforce.",
        ) from None
    raise SalesforceProbeError(
        CATEGORY_NETWORK,
        f"Network error contacting Salesforce ({type(exc.reason).__name__ if exc.reason else 'URLError'}).",
    ) from None


def default_transport(
    url: str,
    body: bytes | None,
    headers: dict[str, str],
    timeout: float,
) -> tuple[int, str]:
    request = urllib.request.Request(url, data=body, headers=headers, method="POST" if body is not None else "GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
            return int(response.status), raw
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        return int(exc.code), raw
    except urllib.error.URLError as exc:
        _raise_url_error(exc)
        raise


def default_binary_transport(
    url: str,
    headers: dict[str, str],
    timeout: float,
) -> tuple[int, bytes]:
    request = urllib.request.Request(url, data=None, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return int(response.status), response.read()
    except urllib.error.HTTPError as exc:
        return int(exc.code), exc.read()
    except urllib.error.URLError as exc:
        _raise_url_error(exc)
        raise


def parse_json_body(raw: str, *, context: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SalesforceProbeError(
            CATEGORY_MALFORMED,
            f"Malformed JSON in {context}.",
        ) from None


def raise_for_rest_error(status: int, payload: Any, *, context: str) -> None:
    if 200 <= status < 300:
        return
    message = _rest_error_message(payload) or f"HTTP {status} during {context}."
    category = CATEGORY_ENDPOINT
    lowered = message.lower()
    if status in {401, 403} or "insufficient" in lowered or "access" in lowered:
        from connectors.salesforce.errors import CATEGORY_API_ACCESS, CATEGORY_AUTHORIZATION

        category = CATEGORY_AUTHORIZATION if status in {401, 403} else CATEGORY_API_ACCESS
    if status >= 500:
        category = CATEGORY_ENDPOINT
    if status == 404:
        category = CATEGORY_ENDPOINT
    raise SalesforceProbeError(category, message)


def _rest_error_message(payload: Any) -> str:
    if isinstance(payload, list) and payload:
        first = payload[0]
        if isinstance(first, dict):
            error_code = str(first.get("errorCode") or first.get("error") or "").strip()
            message = str(first.get("message") or "").strip()
            if error_code and message:
                return f"{error_code}: {message}"
            return message or error_code
    if isinstance(payload, dict):
        message = str(payload.get("message") or payload.get("error_description") or "").strip()
        if message:
            return message
    return ""


def build_query_url(instance_url: str, api_version: str, soql: str) -> str:
    base = instance_url.rstrip("/")
    encoded = urllib.parse.quote(soql, safe="")
    return f"{base}/services/data/v{api_version}/query?q={encoded}"


def build_sobject_describe_url(instance_url: str, api_version: str, sobject: str) -> str:
    base = instance_url.rstrip("/")
    return f"{base}/services/data/v{api_version}/sobjects/{sobject}/describe"


def build_content_version_data_url(instance_url: str, api_version: str, version_id: str) -> str:
    base = instance_url.rstrip("/")
    return f"{base}/services/data/v{api_version}/sobjects/ContentVersion/{version_id}/VersionData"


def resolve_salesforce_url(instance_url: str, path_or_url: str) -> str:
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        return path_or_url
    return instance_url.rstrip("/") + path_or_url


def unexpected_error(message: str) -> SalesforceProbeError:
    return SalesforceProbeError(CATEGORY_UNEXPECTED, message)
