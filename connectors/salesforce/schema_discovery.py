"""Optional Case object schema discovery (no assumed custom API names)."""

from __future__ import annotations

from dataclasses import dataclass

from connectors.salesforce.client import SalesforceClient


@dataclass(frozen=True)
class CaseFieldMeta:
    label: str
    api_name: str
    data_type: str
    custom: bool
    nillable: bool
    createable: bool
    updateable: bool
    filterable: bool
    permissionable: bool


def describe_case_object(client: SalesforceClient) -> list[CaseFieldMeta]:
    """Retrieve Salesforce Case field metadata via REST describe."""
    payload = client.describe_sobject("Case")
    fields = payload.get("fields") or []
    result: list[CaseFieldMeta] = []
    for field in fields:
        if not isinstance(field, dict):
            continue
        result.append(
            CaseFieldMeta(
                label=str(field.get("label") or ""),
                api_name=str(field.get("name") or ""),
                data_type=str(field.get("type") or ""),
                custom=bool(field.get("custom")),
                nillable=bool(field.get("nillable")),
                createable=bool(field.get("createable")),
                updateable=bool(field.get("updateable")),
                filterable=bool(field.get("filterable")),
                permissionable=bool(field.get("permissionable")),
            )
        )
    result.sort(key=lambda item: (not item.custom, item.label.lower(), item.api_name.lower()))
    return result


def filter_fields(
    fields: list[CaseFieldMeta],
    *,
    custom_only: bool = False,
    substring: str | None = None,
) -> list[CaseFieldMeta]:
    needle = (substring or "").strip().lower()
    filtered: list[CaseFieldMeta] = []
    for field in fields:
        if custom_only and not field.custom:
            continue
        if needle and needle not in field.label.lower() and needle not in field.api_name.lower():
            continue
        filtered.append(field)
    return filtered


def format_field_line(field: CaseFieldMeta) -> str:
    kind = "custom" if field.custom else "standard"
    access = (
        f"createable={field.createable} updateable={field.updateable} "
        f"filterable={field.filterable} nillable={field.nillable}"
    )
    return (
        f"- {field.label} | {field.api_name} | {field.data_type} | {kind} | {access}"
    )
