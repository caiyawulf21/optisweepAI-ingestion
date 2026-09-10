"""Lightweight unit tests for the Salesforce connectivity probe."""

from __future__ import annotations

import importlib.util
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from connectors.salesforce.auth import (
    SalesforceCredentials,
    load_credentials,
    soap_login,
)
from connectors.salesforce.case_repository import query_case_by_number
from connectors.salesforce.client import SalesforceClient
from connectors.salesforce.errors import (
    CATEGORY_INVALID_CREDENTIALS,
    CATEGORY_MALFORMED,
    CATEGORY_MISSING_ENV,
    CATEGORY_QUERY_EMPTY,
    SalesforceProbeError,
)
from connectors.salesforce.schema_discovery import CaseFieldMeta, filter_fields

_REPO_ROOT = Path(__file__).resolve().parents[3]
_SCRIPT_PATH = _REPO_ROOT / "scripts" / "test_salesforce_connection.py"


def _load_probe_script():
    spec = importlib.util.spec_from_file_location(
        "test_salesforce_connection_script",
        _SCRIPT_PATH,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


probe_script = _load_probe_script()


def _creds(**overrides: str) -> SalesforceCredentials:
    base = {
        "username": "user@example.com",
        "password": "SuperSecretPass",
        "security_token": "TOKENVALUE123",
        "login_url": "https://login.salesforce.com/services/Soap/u/59.0",
    }
    base.update(overrides)
    return SalesforceCredentials(**base)


def test_missing_environment_variables() -> None:
    with pytest.raises(SalesforceProbeError) as exc_info:
        load_credentials({})
    assert exc_info.value.category == CATEGORY_MISSING_ENV
    message = str(exc_info.value)
    assert "SALESFORCE_USERNAME" in message
    assert "SALESFORCE_PASSWORD" in message
    assert "SALESFORCE_SECURITY_TOKEN" in message


def test_successful_authentication_parsing() -> None:
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns="urn:partner.soap.sforce.com">
      <soapenv:Body>
        <loginResponse>
          <result>
            <sessionId>SESSION_ABC</sessionId>
            <serverUrl>https://na99.salesforce.com/services/Soap/u/59.0/00Dxx</serverUrl>
            <userId>005xx</userId>
            <organizationId>00Dxx</organizationId>
          </result>
        </loginResponse>
      </soapenv:Body>
    </soapenv:Envelope>
    """

    def transport(url, body, headers, timeout):
        assert "login.salesforce.com" in url
        assert b"SuperSecretPassTOKENVALUE123" in body
        return 200, xml

    session = soap_login(_creds(), transport=transport)
    assert session.instance_url == "https://na99.salesforce.com"
    assert session.session_id == "SESSION_ABC"
    assert session.session_established is True


def test_authentication_failure_invalid_credentials() -> None:
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
      <soapenv:Body>
        <soapenv:Fault>
          <faultcode>sf:INVALID_LOGIN</faultcode>
          <faultstring>INVALID_LOGIN: Invalid username, password, security token; or user locked out.</faultstring>
        </soapenv:Fault>
      </soapenv:Body>
    </soapenv:Envelope>
    """

    def transport(url, body, headers, timeout):
        return 500, xml

    with pytest.raises(SalesforceProbeError) as exc_info:
        soap_login(_creds(), transport=transport)
    assert exc_info.value.category == CATEGORY_INVALID_CREDENTIALS
    text = str(exc_info.value)
    assert "SuperSecretPass" not in text
    assert "TOKENVALUE123" not in text


def test_malformed_login_response() -> None:
    def transport(url, body, headers, timeout):
        return 200, "not-xml-at-all"

    with pytest.raises(SalesforceProbeError) as exc_info:
        soap_login(_creds(), transport=transport)
    assert exc_info.value.category == CATEGORY_MALFORMED


def test_query_returns_one_case() -> None:
    class Session:
        instance_url = "https://na99.salesforce.com"
        session_id = "SESSION_ABC"
        api_version = "59.0"

    def transport(url, body, headers, timeout):
        assert "Authorization" in headers
        assert "SESSION_ABC" in headers["Authorization"]
        assert "CaseNumber" in url
        return 200, (
            '{"totalSize":1,"done":true,"records":['
            '{"Id":"500xx","CaseNumber":"228086","Subject":"OptiSweep tipper jam","Status":"Closed"}'
            "]}"
        )

    client = SalesforceClient(Session(), transport=transport)  # type: ignore[arg-type]
    case = query_case_by_number(client, "228086")
    assert case is not None
    assert case.case_number == "228086"
    assert case.subject == "OptiSweep tipper jam"
    assert case.status == "Closed"
    assert case.id == "500xx"


def test_query_returns_zero_cases() -> None:
    class Session:
        instance_url = "https://na99.salesforce.com"
        session_id = "SESSION_ABC"
        api_version = "59.0"

    def transport(url, body, headers, timeout):
        return 200, '{"totalSize":0,"done":true,"records":[]}'

    client = SalesforceClient(Session(), transport=transport)  # type: ignore[arg-type]
    with pytest.raises(SalesforceProbeError) as exc_info:
        query_case_by_number(client, "228086")
    assert exc_info.value.category == CATEGORY_QUERY_EMPTY


def test_secrets_not_in_cli_failure_output(monkeypatch) -> None:
    monkeypatch.setenv("SALESFORCE_USERNAME", "user@example.com")
    monkeypatch.setenv("SALESFORCE_PASSWORD", "SuperSecretPass")
    monkeypatch.setenv("SALESFORCE_SECURITY_TOKEN", "TOKENVALUE123")
    monkeypatch.setenv(
        "SALESFORCE_LOGIN_URL",
        "https://login.salesforce.com/services/Soap/u/59.0",
    )

    def boom(*args, **kwargs):
        raise SalesforceProbeError(
            CATEGORY_INVALID_CREDENTIALS,
            "Salesforce rejected the username, password, or security token.",
        )

    monkeypatch.setattr(probe_script, "soap_login", boom)
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = probe_script.main([])
    output = buf.getvalue()
    assert code == 1
    assert "SuperSecretPass" not in output
    assert "TOKENVALUE123" not in output
    assert "invalid_credentials" in output


def test_filter_fields_custom_and_substring() -> None:
    fields = [
        CaseFieldMeta("Subject", "Subject", "string", False, True, True, True, True, True),
        CaseFieldMeta("Root Cause Analysis", "RCA_Notes__c", "textarea", True, True, True, True, True, True),
        CaseFieldMeta("Site Code", "Site_Code__c", "string", True, True, True, True, True, True),
    ]
    custom = filter_fields(fields, custom_only=True)
    assert [f.api_name for f in custom] == ["RCA_Notes__c", "Site_Code__c"]
    matched = filter_fields(fields, substring="rca")
    assert [f.api_name for f in matched] == ["RCA_Notes__c"]


def test_pull_case_feed_and_images(tmp_path: Path) -> None:
    from connectors.salesforce.auth import SalesforceSession
    from connectors.salesforce.case_feed import pull_case_feed_and_images
    from connectors.salesforce.case_repository import CaseSummary

    session = SalesforceSession(
        instance_url="https://na99.salesforce.com",
        session_id="SESSION_ABC",
        api_version="59.0",
    )
    case = CaseSummary(
        id="500xx",
        case_number="00233681",
        subject="Not able to exchange Totes",
        status="Closed",
    )

    def transport(url, body, headers, timeout):
        if "FROM+CaseFeed" in url or "FROM%20CaseFeed" in url or "CaseFeed" in url:
            return 200, (
                '{"totalSize":1,"done":true,"records":['
                '{"Id":"0D5xx","Type":"TextPost","CreatedDate":"2026-08-22T10:21:59.000+0000",'
                '"CreatedBy":{"Name":"Alex Lukenbach"},'
                '"Body":"<p>Site found a firewall</p>","Title":null,"RelatedRecordId":null}'
                "]}"
            )
        if "EmailMessage" in url:
            return 200, (
                '{"totalSize":1,"done":true,"records":['
                '{"Id":"02sxx","Subject":"CLOSED","Incoming":false,'
                '"MessageDate":"2026-08-25T21:19:16.000+0000","FromAddress":"a@b.com",'
                '"ToAddress":"c@d.com","TextBody":"Case closed"}'
                "]}"
            )
        if "ContentDocumentLink" in url:
            return 200, (
                '{"totalSize":1,"done":true,"records":['
                '{"ContentDocumentId":"069xx","ContentDocument":{'
                '"Title":"image (50)","FileType":"PNG","FileExtension":"png",'
                '"ContentSize":10,"LatestPublishedVersionId":"068xx"}}'
                "]}"
            )
        raise AssertionError(url)

    def binary_transport(url, headers, timeout):
        assert "ContentVersion/068xx/VersionData" in url
        return 200, b"\x89PNG\r\nfake"

    client = SalesforceClient(session, transport=transport, binary_transport=binary_transport)
    result = pull_case_feed_and_images(client, case, tmp_path, images_only=True)
    assert len(result.feed) == 1
    assert result.feed[0].body == "Site found a firewall"
    assert len(result.emails) == 1
    assert len(result.downloaded_files) == 1
    assert (tmp_path / "case_feed.json").exists()
    assert (tmp_path / "case_feed.md").exists()
    image_files = list((tmp_path / "images").glob("*.png"))
    assert len(image_files) == 1
    assert image_files[0].read_bytes().startswith(b"\x89PNG")
