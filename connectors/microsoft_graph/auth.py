"""Microsoft Graph authentication for the Teams connectivity probe.

Development default: device-code (delegated) so you can search chats you
participate in without Chat.Read.All.

Production path later: client credentials + admin-consented application
permissions (Chat.Read.All / ChatMessage.Read.All) via a dedicated app.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Mapping

from dotenv import load_dotenv

from connectors.microsoft_graph.errors import (
    CATEGORY_AUTH,
    CATEGORY_MISSING_ENV,
    CATEGORY_NETWORK,
    GraphProbeError,
)

GRAPH_SCOPE_DEVICE = " ".join(
    [
        "openid",
        "profile",
        "offline_access",
        "User.Read",
        "Chat.Read",
        "ChatMessage.Read",
        "Files.Read",
    ]
)
GRAPH_SCOPE_APP = "https://graph.microsoft.com/.default"
TOKEN_URL_TMPL = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
DEVICE_CODE_URL_TMPL = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/devicecode"


@dataclass(frozen=True)
class GraphCredentials:
    tenant_id: str
    client_id: str
    client_secret: str
    auth_mode: str  # device_code | client_credentials


@dataclass(frozen=True)
class GraphToken:
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 0
    scope: str = ""


def load_graph_credentials(env: Mapping[str, str] | None = None) -> GraphCredentials:
    if env is None:
        load_dotenv()
        source: Mapping[str, str] = os.environ
    else:
        source = env

    tenant = _first(source, "GRAPH_TENANT_ID", "SHAREPOINT_TENANT_ID")
    client_id = _first(source, "GRAPH_CLIENT_ID", "SHAREPOINT_CLIENT_ID")
    client_secret = _first(source, "GRAPH_CLIENT_SECRET", "SHAREPOINT_CLIENT_SECRET")
    auth_mode = (source.get("GRAPH_AUTH_MODE") or "device_code").strip().lower()

    if auth_mode not in {"device_code", "client_credentials"}:
        raise GraphProbeError(
            CATEGORY_MISSING_ENV,
            "GRAPH_AUTH_MODE must be 'device_code' or 'client_credentials'.",
        )

    missing = []
    if not tenant:
        missing.append("GRAPH_TENANT_ID")
    if not client_id:
        missing.append("GRAPH_CLIENT_ID")
    if auth_mode == "client_credentials" and not client_secret:
        missing.append("GRAPH_CLIENT_SECRET")
    if missing:
        raise GraphProbeError(
            CATEGORY_MISSING_ENV,
            "Missing required environment variable(s): " + ", ".join(missing) + ".",
        )

    return GraphCredentials(
        tenant_id=tenant,
        client_id=client_id,
        client_secret=client_secret,
        auth_mode=auth_mode,
    )


def acquire_token(
    credentials: GraphCredentials,
    *,
    print_fn=None,
) -> GraphToken:
    if print_fn is None:
        def print_fn(message: str) -> None:
            print(message, flush=True)

    if credentials.auth_mode == "client_credentials":
        return _client_credentials_token(credentials)
    return _device_code_token(credentials, print_fn=print_fn)


def _client_credentials_token(credentials: GraphCredentials) -> GraphToken:
    body = urllib.parse.urlencode(
        {
            "grant_type": "client_credentials",
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scope": GRAPH_SCOPE_APP,
        }
    ).encode("utf-8")
    return _post_token(credentials.tenant_id, body)


def _device_code_token(credentials: GraphCredentials, *, print_fn) -> GraphToken:
    device_body = urllib.parse.urlencode(
        {
            "client_id": credentials.client_id,
            "scope": GRAPH_SCOPE_DEVICE,
        }
    ).encode("utf-8")
    device_payload = _post_form(
        DEVICE_CODE_URL_TMPL.format(tenant=credentials.tenant_id),
        device_body,
        context="device code request",
    )
    user_code = str(device_payload.get("user_code") or "")
    verify_uri = str(
        device_payload.get("verification_uri")
        or device_payload.get("verification_url")
        or "https://microsoft.com/devicelogin"
    )
    device_code = str(device_payload.get("device_code") or "")
    interval = int(device_payload.get("interval") or 5)
    expires_in = int(device_payload.get("expires_in") or 900)
    if not device_code or not user_code:
        raise GraphProbeError(CATEGORY_AUTH, "Device code response missing user_code/device_code.")

    print_fn("Microsoft Graph device login required.")
    print_fn(f"1) Open: {verify_uri}")
    print_fn(f"2) Enter code: {user_code}")
    print_fn("Waiting for approval...")

    token_body_base = {
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        "client_id": credentials.client_id,
        "device_code": device_code,
    }
    deadline = time.time() + expires_in
    while time.time() < deadline:
        time.sleep(max(interval, 1))
        try:
            return _post_token(
                credentials.tenant_id,
                urllib.parse.urlencode(token_body_base).encode("utf-8"),
            )
        except GraphProbeError as exc:
            message = str(exc.args[0]).lower()
            if "authorization_pending" in message:
                continue
            if "slow_down" in message:
                interval += 2
                continue
            if "expired_token" in message or "expired" in message:
                raise GraphProbeError(
                    CATEGORY_AUTH,
                    "Device code expired before login completed. Re-run the probe.",
                ) from None
            raise
    raise GraphProbeError(CATEGORY_AUTH, "Timed out waiting for device login.")


def _post_token(tenant_id: str, body: bytes) -> GraphToken:
    payload = _post_form(TOKEN_URL_TMPL.format(tenant=tenant_id), body, context="token request")
    token = str(payload.get("access_token") or "")
    if not token:
        error = str(payload.get("error") or "unknown_error")
        desc = str(payload.get("error_description") or "").strip()
        raise GraphProbeError(
            CATEGORY_AUTH,
            f"Token request failed ({error})" + (f": {desc[:240]}" if desc else "."),
        )
    return GraphToken(
        access_token=token,
        token_type=str(payload.get("token_type") or "Bearer"),
        expires_in=int(payload.get("expires_in") or 0),
        scope=str(payload.get("scope") or ""),
    )


def _post_form(url: str, body: bytes, *, context: str) -> dict:
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read().decode("utf-8", errors="replace")
            status = int(response.status)
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        status = int(exc.code)
    except urllib.error.URLError as exc:
        raise GraphProbeError(
            CATEGORY_NETWORK,
            f"Network error during {context}.",
        ) from None

    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        raise GraphProbeError(
            CATEGORY_AUTH,
            f"Malformed JSON during {context} (HTTP {status}).",
        ) from None

    if status >= 400:
        error = str(payload.get("error") or f"http_{status}")
        desc = str(payload.get("error_description") or "").strip()
        raise GraphProbeError(
            CATEGORY_AUTH,
            f"{error}" + (f": {desc[:240]}" if desc else f" (HTTP {status})"),
        )
    if not isinstance(payload, dict):
        raise GraphProbeError(CATEGORY_AUTH, f"Unexpected token payload during {context}.")
    return payload


def _first(source: Mapping[str, str], *keys: str) -> str:
    for key in keys:
        value = (source.get(key) or "").strip()
        if value:
            return value
    return ""
