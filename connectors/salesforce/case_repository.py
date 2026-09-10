"""Case lookup helpers (raw Salesforce fields only)."""

from __future__ import annotations

from dataclasses import dataclass

from connectors.salesforce.client import SalesforceClient
from connectors.salesforce.errors import (
    CATEGORY_AUTHORIZATION,
    CATEGORY_QUERY_EMPTY,
    CATEGORY_QUERY_FAILED,
    SalesforceProbeError,
)


@dataclass(frozen=True)
class CaseSummary:
    id: str
    case_number: str
    subject: str
    status: str


def query_case_by_number(
    client: SalesforceClient,
    case_number: str = "228086",
) -> CaseSummary | None:
    """Return a single Case by CaseNumber, or None if the query succeeds with zero rows."""
    safe_number = case_number.replace("'", "\\'")
    soql = (
        "SELECT Id, CaseNumber, Subject, Status "
        f"FROM Case WHERE CaseNumber = '{safe_number}' LIMIT 1"
    )
    try:
        payload = client.query(soql)
    except SalesforceProbeError as exc:
        if exc.category == CATEGORY_AUTHORIZATION:
            raise
        message = str(exc.args[0]).lower()
        if "insufficient" in message or "access" in message or "not authorized" in message:
            raise SalesforceProbeError(
                CATEGORY_AUTHORIZATION,
                "Salesforce denied access to query Case records for this user.",
            ) from None
        raise SalesforceProbeError(
            CATEGORY_QUERY_FAILED,
            f"Case query failed: {exc.args[0]}",
        ) from None

    records = payload.get("records") or []
    if not records:
        raise SalesforceProbeError(
            CATEGORY_QUERY_EMPTY,
            f"Query succeeded but no Case with CaseNumber={case_number} is visible to this user.",
        )

    record = records[0]
    return CaseSummary(
        id=str(record.get("Id") or ""),
        case_number=str(record.get("CaseNumber") or case_number),
        subject=str(record.get("Subject") or ""),
        status=str(record.get("Status") or ""),
    )
