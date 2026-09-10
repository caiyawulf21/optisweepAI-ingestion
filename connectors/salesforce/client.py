"""Minimal Salesforce REST client using a SOAP-established session."""

from __future__ import annotations

from typing import Any

from connectors.salesforce.auth import SalesforceSession
from connectors.salesforce.errors import (
    CATEGORY_API_ACCESS,
    CATEGORY_AUTHORIZATION,
    CATEGORY_MALFORMED,
    CATEGORY_QUERY_FAILED,
    SalesforceProbeError,
)
from connectors.salesforce.http_util import (
    BinaryHttpTransport,
    HttpTransport,
    build_query_url,
    build_sobject_describe_url,
    default_binary_transport,
    default_transport,
    parse_json_body,
    raise_for_rest_error,
    resolve_salesforce_url,
)


class SalesforceClient:
    """Thin REST wrapper. Retrieves Salesforce data only; no OptiSweep mapping."""

    def __init__(
        self,
        session: SalesforceSession,
        *,
        transport: HttpTransport | None = None,
        binary_transport: BinaryHttpTransport | None = None,
        timeout: float = 60.0,
    ) -> None:
        self.session = session
        self._transport = transport or default_transport
        self._binary_transport = binary_transport or default_binary_transport
        self.timeout = timeout

    def query(self, soql: str) -> dict[str, Any]:
        url = build_query_url(self.session.instance_url, self.session.api_version, soql)
        payload = self._get_json(url, context="SOQL query")
        if not isinstance(payload, dict) or "records" not in payload:
            raise SalesforceProbeError(
                CATEGORY_QUERY_FAILED,
                "SOQL response did not include a records array.",
            )
        return payload

    def query_all(self, soql: str) -> list[dict[str, Any]]:
        payload = self.query(soql)
        records = list(payload.get("records") or [])
        next_url = payload.get("nextRecordsUrl")
        while next_url:
            page = self._get_json(
                resolve_salesforce_url(self.session.instance_url, str(next_url)),
                context="SOQL query page",
            )
            if not isinstance(page, dict):
                raise SalesforceProbeError(
                    CATEGORY_QUERY_FAILED,
                    "SOQL page response was not an object.",
                )
            records.extend(page.get("records") or [])
            next_url = page.get("nextRecordsUrl")
        return records

    def describe_sobject(self, sobject: str) -> dict[str, Any]:
        url = build_sobject_describe_url(
            self.session.instance_url,
            self.session.api_version,
            sobject,
        )
        payload = self._get_json(url, context=f"{sobject} describe")
        if not isinstance(payload, dict) or "fields" not in payload:
            raise SalesforceProbeError(
                CATEGORY_QUERY_FAILED,
                f"{sobject} describe response did not include fields.",
            )
        return payload

    def get_bytes(self, path_or_url: str, *, context: str) -> bytes:
        url = resolve_salesforce_url(self.session.instance_url, path_or_url)
        headers = {
            "Authorization": f"Bearer {self.session.session_id}",
        }
        status, raw = self._binary_transport(url, headers, self.timeout)
        if status >= 400:
            message = f"HTTP {status} while downloading {context}."
            try:
                payload = parse_json_body(raw.decode("utf-8", errors="replace"), context=context)
                raise_for_rest_error(status, payload, context=context)
            except SalesforceProbeError:
                raise
            except Exception:
                raise SalesforceProbeError(CATEGORY_QUERY_FAILED, message) from None
            raise SalesforceProbeError(CATEGORY_QUERY_FAILED, message)
        if not raw:
            raise SalesforceProbeError(
                CATEGORY_MALFORMED,
                f"Empty binary response while downloading {context}.",
            )
        return raw

    def _get_json(self, url: str, *, context: str) -> Any:
        headers = {
            "Authorization": f"Bearer {self.session.session_id}",
            "Accept": "application/json",
        }
        status, raw = self._transport(url, None, headers, self.timeout)
        if not raw.strip():
            raise SalesforceProbeError(
                CATEGORY_QUERY_FAILED,
                f"Empty response during {context} (HTTP {status}).",
            )
        payload = parse_json_body(raw, context=context)
        try:
            raise_for_rest_error(status, payload, context=context)
        except SalesforceProbeError as exc:
            if exc.category in {CATEGORY_AUTHORIZATION, CATEGORY_API_ACCESS}:
                raise
            if status in {400, 401, 403}:
                raise SalesforceProbeError(
                    CATEGORY_AUTHORIZATION if status in {401, 403} else CATEGORY_QUERY_FAILED,
                    str(exc.args[0]),
                ) from None
            raise SalesforceProbeError(CATEGORY_QUERY_FAILED, str(exc.args[0])) from None
        return payload
