"""Minimal Microsoft Graph REST client (stdlib urllib only)."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from connectors.microsoft_graph.auth import GraphToken
from connectors.microsoft_graph.errors import (
    CATEGORY_AUTHORIZATION,
    CATEGORY_ENDPOINT,
    CATEGORY_MALFORMED,
    CATEGORY_NETWORK,
    CATEGORY_QUERY_FAILED,
    GraphProbeError,
)

GRAPH_ROOT = "https://graph.microsoft.com/v1.0"


class GraphClient:
    def __init__(self, token: GraphToken, *, timeout: float = 60.0) -> None:
        self.token = token
        self.timeout = timeout

    def get_json(self, path_or_url: str, *, context: str) -> Any:
        url = self._abs(path_or_url)
        status, payload = self._request("GET", url, context=context)
        if status >= 400:
            self._raise_http(status, payload, context=context)
        return payload

    def post_json(self, path_or_url: str, body: dict[str, Any], *, context: str) -> Any:
        url = self._abs(path_or_url)
        raw = json.dumps(body).encode("utf-8")
        status, payload = self._request(
            "POST",
            url,
            data=raw,
            content_type="application/json",
            context=context,
        )
        if status >= 400:
            self._raise_http(status, payload, context=context)
        return payload

    def get_bytes(self, path_or_url: str, *, context: str) -> tuple[bytes, str]:
        """Return (body, content_type) for a binary Graph download."""
        url = self._abs(path_or_url)
        headers = {"Authorization": f"Bearer {self.token.access_token}"}
        request = urllib.request.Request(url, data=None, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                content_type = str(response.headers.get("Content-Type") or "")
                return response.read(), content_type
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            try:
                payload = json.loads(raw) if raw.strip() else {}
            except json.JSONDecodeError:
                payload = {"error": {"message": raw[:240]}}
            self._raise_http(int(exc.code), payload, context=context)
            raise
        except urllib.error.URLError:
            raise GraphProbeError(CATEGORY_NETWORK, f"Network error during {context}.") from None

    def get_paged(self, path_or_url: str, *, context: str, max_pages: int = 20) -> list[dict[str, Any]]:
        url: str | None = self._abs(path_or_url)
        items: list[dict[str, Any]] = []
        pages = 0
        while url and pages < max_pages:
            payload = self.get_json(url, context=context)
            if not isinstance(payload, dict):
                raise GraphProbeError(CATEGORY_MALFORMED, f"Expected object during {context}.")
            for item in payload.get("value") or []:
                if isinstance(item, dict):
                    items.append(item)
            next_link = payload.get("@odata.nextLink")
            url = str(next_link) if next_link else None
            pages += 1
        return items

    def _request(
        self,
        method: str,
        url: str,
        *,
        data: bytes | None = None,
        content_type: str | None = None,
        context: str,
    ) -> tuple[int, Any]:
        headers = {"Authorization": f"Bearer {self.token.access_token}", "Accept": "application/json"}
        if content_type:
            headers["Content-Type"] = content_type
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8", errors="replace")
                status = int(response.status)
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            status = int(exc.code)
        except urllib.error.URLError:
            raise GraphProbeError(CATEGORY_NETWORK, f"Network error during {context}.") from None

        if not raw.strip():
            return status, {}
        try:
            return status, json.loads(raw)
        except json.JSONDecodeError:
            raise GraphProbeError(
                CATEGORY_MALFORMED,
                f"Malformed JSON during {context} (HTTP {status}).",
            ) from None

    def _raise_http(self, status: int, payload: Any, *, context: str) -> None:
        message = _graph_error_message(payload) or f"HTTP {status} during {context}."
        if status in {401, 403}:
            raise GraphProbeError(CATEGORY_AUTHORIZATION, message)
        if status == 404:
            raise GraphProbeError(CATEGORY_ENDPOINT, message)
        raise GraphProbeError(CATEGORY_QUERY_FAILED, message)

    def _abs(self, path_or_url: str) -> str:
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            return path_or_url
        return GRAPH_ROOT.rstrip("/") + "/" + path_or_url.lstrip("/")


def _graph_error_message(payload: Any) -> str:
    if isinstance(payload, dict):
        err = payload.get("error")
        if isinstance(err, dict):
            code = str(err.get("code") or "").strip()
            message = str(err.get("message") or "").strip()
            if code and message:
                return f"{code}: {message}"
            return message or code
        if payload.get("error_description"):
            return str(payload.get("error_description"))
    return ""
