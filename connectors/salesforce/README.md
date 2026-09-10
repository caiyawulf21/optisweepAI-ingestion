# Salesforce connectivity probe (development only)

Temporary probe to verify API access before building a production Salesforce connector.

**Not production:** username + password + security token is for local development only. Production should use a dedicated integration user, an External Client App, and OAuth client credentials.

## What it checks

1. SOAP login with your Salesforce credentials
2. REST query for a Case (`Id`, `CaseNumber`, `Subject`, `Status`)
3. Optional Case object schema discovery (actual FORTNA field API names)
4. Optional CaseFeed + email + image/file download (dev probe only)

## Setup

1. Reset/generate your Salesforce security token in the Salesforce UI.
2. Copy placeholders from `.env.example` into `.env` (already gitignored):

```text
SALESFORCE_USERNAME=
SALESFORCE_PASSWORD=
SALESFORCE_SECURITY_TOKEN=
SALESFORCE_LOGIN_URL=https://login.salesforce.com/services/Soap/u/59.0
```

Sandbox:

```text
SALESFORCE_LOGIN_URL=https://test.salesforce.com/services/Soap/u/59.0
```

## Run

From the repo root:

```powershell
python scripts/test_salesforce_connection.py --case-number 00233681
python scripts/test_salesforce_connection.py --case-number 00233681 --pull-feed
python scripts/test_salesforce_connection.py --describe-case
python scripts/test_salesforce_connection.py --describe-case --describe-filter rca
python scripts/test_salesforce_connection.py --describe-case --describe-all-fields
```

`--pull-feed` writes under `data/output/salesforce_probe/case_<number>/` (gitignored):

- `case_feed.json` / `case_feed.md` — CaseFeed + emails
- `images/` — PNG/JPG/etc from ContentDocumentLink

## Layout

```text
connectors/salesforce/
  auth.py              # SOAP login + session
  client.py            # REST query/describe/download
  case_repository.py   # CaseNumber lookup
  case_feed.py         # CaseFeed + emails + ContentDocument files
  schema_discovery.py  # Case field metadata
scripts/test_salesforce_connection.py
```

No pipeline, Cosmos, or LangGraph changes. Secrets must never be printed or committed.

## Tests

```powershell
python -m pytest connectors/salesforce/tests/test_salesforce_probe.py -q
```
