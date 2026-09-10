"""Salesforce SOAP username/password + security token login (dev probe only)."""

from __future__ import annotations

import os
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Mapping
from urllib.parse import urlparse

from dotenv import load_dotenv

from connectors.salesforce.errors import (
    CATEGORY_API_ACCESS,
    CATEGORY_INVALID_CREDENTIALS,
    CATEGORY_MALFORMED,
    CATEGORY_MISSING_ENV,
    CATEGORY_UNEXPECTED,
    SalesforceProbeError,
)
from connectors.salesforce.http_util import HttpTransport, default_transport

DEFAULT_API_VERSION = "59.0"
DEFAULT_LOGIN_URL = f"https://login.salesforce.com/services/Soap/u/{DEFAULT_API_VERSION}"
SANDBOX_LOGIN_URL = f"https://test.salesforce.com/services/Soap/u/{DEFAULT_API_VERSION}"

_SOAP_ENV = "http://schemas.xmlsoap.org/soap/envelope/"
_PARTNER_NS = "urn:partner.soap.sforce.com"

_SECRET_ENV_KEYS = (
    "SALESFORCE_PASSWORD",
    "SALESFORCE_SECURITY_TOKEN",
)


@dataclass(frozen=True)
class SalesforceCredentials:
    username: str
    password: str
    security_token: str
    login_url: str


@dataclass(frozen=True)
class SalesforceSession:
    instance_url: str
    session_id: str
    api_version: str
    user_id: str = ""
    organization_id: str = ""

    @property
    def session_established(self) -> bool:
        return bool(self.session_id and self.instance_url)


def load_credentials(env: Mapping[str, str] | None = None) -> SalesforceCredentials:
    """Load Salesforce probe credentials from environment variables."""
    source: Mapping[str, str]
    if env is None:
        load_dotenv()
        source = os.environ
    else:
        source = env

    username = (source.get("SALESFORCE_USERNAME") or "").strip()
    password = source.get("SALESFORCE_PASSWORD") or ""
    security_token = source.get("SALESFORCE_SECURITY_TOKEN") or ""
    login_url = (source.get("SALESFORCE_LOGIN_URL") or DEFAULT_LOGIN_URL).strip()

    missing = [
        name
        for name, value in (
            ("SALESFORCE_USERNAME", username),
            ("SALESFORCE_PASSWORD", password),
            ("SALESFORCE_SECURITY_TOKEN", security_token),
        )
        if not value
    ]
    if missing:
        raise SalesforceProbeError(
            CATEGORY_MISSING_ENV,
            "Missing required environment variable(s): " + ", ".join(missing) + ".",
        )

    if not login_url.startswith("https://"):
        raise SalesforceProbeError(
            CATEGORY_MISSING_ENV,
            "SALESFORCE_LOGIN_URL must be an https URL "
            f"(production default: {DEFAULT_LOGIN_URL}; sandbox: {SANDBOX_LOGIN_URL}).",
        )

    return SalesforceCredentials(
        username=username,
        password=password,
        security_token=security_token,
        login_url=login_url,
    )


def soap_login(
    credentials: SalesforceCredentials,
    *,
    transport: HttpTransport | None = None,
    timeout: float = 60.0,
    api_version: str = DEFAULT_API_VERSION,
) -> SalesforceSession:
    """Authenticate via Salesforce SOAP partner login.

    Password sent to Salesforce is password + security_token (Salesforce convention).
    Secrets are never included in raised error messages.
    """
    transport = transport or default_transport
    combined = credentials.password + credentials.security_token
    body = _build_login_envelope(credentials.username, combined)
    headers = {
        "Content-Type": "text/xml; charset=UTF-8",
        "SOAPAction": "login",
    }

    status, raw = transport(credentials.login_url, body.encode("utf-8"), headers, timeout)
    safe_raw = _redact_secrets(raw, credentials)
    return _parse_login_response(status, safe_raw, api_version=api_version)


def _build_login_envelope(username: str, password_with_token: str) -> str:
    # Escape XML special characters in username/password without logging them.
    user_xml = _xml_escape(username)
    pass_xml = _xml_escape(password_with_token)
    return (
        '<?xml version="1.0" encoding="utf-8"?>'
        f'<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema" '
        f'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        f'xmlns:env="{_SOAP_ENV}">'
        "<env:Body>"
        f'<n1:login xmlns:n1="{_PARTNER_NS}">'
        f"<n1:username>{user_xml}</n1:username>"
        f"<n1:password>{pass_xml}</n1:password>"
        "</n1:login>"
        "</env:Body>"
        "</env:Envelope>"
    )


def _xml_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def _parse_login_response(status: int, raw: str, *, api_version: str) -> SalesforceSession:
    if not raw.strip():
        raise SalesforceProbeError(
            CATEGORY_MALFORMED,
            f"Empty response from Salesforce login endpoint (HTTP {status}).",
        )

    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        raise SalesforceProbeError(
            CATEGORY_MALFORMED,
            f"Malformed XML login response (HTTP {status}).",
        ) from None

    fault = _find_first(root, ("Fault", f"{{{_SOAP_ENV}}}Fault"))
    if fault is not None:
        _raise_soap_fault(fault)

    if status >= 400:
        raise SalesforceProbeError(
            CATEGORY_UNEXPECTED,
            f"Salesforce login returned HTTP {status} without a SOAP fault.",
        )

    session_id = _text_of(root, ("sessionId", f"{{{_PARTNER_NS}}}sessionId"))
    server_url = _text_of(root, ("serverUrl", f"{{{_PARTNER_NS}}}serverUrl"))
    user_id = _text_of(root, ("userId", f"{{{_PARTNER_NS}}}userId"))
    org_id = _text_of(root, ("organizationId", f"{{{_PARTNER_NS}}}organizationId"))

    if not session_id or not server_url:
        raise SalesforceProbeError(
            CATEGORY_MALFORMED,
            "Login response missing sessionId or serverUrl.",
        )

    instance_url = _instance_url_from_server_url(server_url)
    return SalesforceSession(
        instance_url=instance_url,
        session_id=session_id,
        api_version=api_version,
        user_id=user_id,
        organization_id=org_id,
    )


def _raise_soap_fault(fault: ET.Element) -> None:
    fault_code = _child_text(fault, ("faultcode", "faultCode"))
    fault_string = _child_text(fault, ("faultstring", "faultString"))
    detail_text = " ".join(fault.itertext())
    combined = f"{fault_code} {fault_string} {detail_text}".lower()

    if any(
        token in combined
        for token in (
            "invalid_login",
            "invalid username",
            "security token",
            "locked out",
            "login_must_use_security_token",
        )
    ):
        raise SalesforceProbeError(
            CATEGORY_INVALID_CREDENTIALS,
            "Salesforce rejected the username, password, or security token "
            "(or the user may be locked out).",
        )

    if any(
        token in combined
        for token in (
            "api_disabled",
            "api is not enabled",
            "api currently disabled",
            "request_limit_exceeded",
            "exceededquota",
            "no api access",
            "not authorized for api",
        )
    ):
        raise SalesforceProbeError(
            CATEGORY_API_ACCESS,
            "Salesforce authenticated the user but API access appears disabled "
            "or restricted for this profile/org.",
        )

    safe_code = fault_code or "unknown_fault"
    raise SalesforceProbeError(
        CATEGORY_UNEXPECTED,
        f"Salesforce authentication fault ({safe_code}).",
    )


def _instance_url_from_server_url(server_url: str) -> str:
    parsed = urlparse(server_url)
    if not parsed.scheme or not parsed.netloc:
        raise SalesforceProbeError(
            CATEGORY_MALFORMED,
            "Login response serverUrl could not be parsed into an instance URL.",
        )
    return f"{parsed.scheme}://{parsed.netloc}"


def _find_first(root: ET.Element, names: tuple[str, ...]) -> ET.Element | None:
    for element in root.iter():
        local = element.tag.rsplit("}", 1)[-1]
        if element.tag in names or local in names:
            return element
    return None


def _text_of(root: ET.Element, names: tuple[str, ...]) -> str:
    element = _find_first(root, names)
    if element is None or element.text is None:
        return ""
    return element.text.strip()


def _child_text(parent: ET.Element, names: tuple[str, ...]) -> str:
    for child in list(parent):
        local = child.tag.rsplit("}", 1)[-1]
        if child.tag in names or local in names:
            return (child.text or "").strip()
    return ""


def _redact_secrets(text: str, credentials: SalesforceCredentials) -> str:
    redacted = text
    for secret in (
        credentials.password,
        credentials.security_token,
        credentials.password + credentials.security_token,
    ):
        if secret:
            redacted = redacted.replace(secret, "***")
    for key in _SECRET_ENV_KEYS:
        value = os.environ.get(key) or ""
        if value:
            redacted = redacted.replace(value, "***")
    # Belt-and-suspenders: strip common password element contents if still present.
    redacted = re.sub(
        r"(<(?:[\w.-]+:)?password>)(.*?)(</(?:[\w.-]+:)?password>)",
        r"\1***\3",
        redacted,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return redacted
