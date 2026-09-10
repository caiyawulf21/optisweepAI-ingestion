# Microsoft Graph / Teams chat probe (development only)

Find Teams chats/messages that correlate to a Salesforce case number and date window.

## Why device-code first

App-only Graph access to **all** Teams chats requires admin-consented `Chat.Read.All` /
`ChatMessage.Read.All`. For local probing, use **device-code** delegated auth so you
search chats **you** can already see in Teams (same idea as the Salesforce personal-credential probe).

Production later should use a dedicated app registration + client credentials + least privilege.

## Azure app registration (one-time)

1. Azure Portal → **Microsoft Entra ID** → **App registrations** → **New registration**
2. Name e.g. `OptiSweep Teams Probe (dev)`
3. Supported account types: single tenant (your FORTNA tenant)
4. After create:
   - Copy **Application (client) ID** → `GRAPH_CLIENT_ID`
   - Copy **Directory (tenant) ID** → `GRAPH_TENANT_ID`
5. **Authentication** → **Advanced settings** → **Allow public client flows** = **Yes**
   (required for device-code login)
6. **API permissions** → Microsoft Graph → **Delegated only** (do **not** add Application `.All` perms for this probe):
   - `User.Read`
   - `Chat.Read`
   - `ChatMessage.Read`
   - `Files.Read`
7. If you accidentally added `ChatMessage.Read.All` (Application), **remove it** — that is what forces admin approval.
8. No client secret needed for `GRAPH_AUTH_MODE=device_code`
9. If Fortna still shows “Need admin approval” with only delegated permissions, the tenant has disabled user consent and an admin must click **Grant admin consent** once for those delegated scopes (still no `.All` application permission needed).

Optional app-only mode later:

- Create a client secret → `GRAPH_CLIENT_SECRET`
- Add **Application** permissions: `Chat.Read.All`, `ChatMessage.Read.All` (+ admin consent)
- Set `GRAPH_AUTH_MODE=client_credentials`

## .env (exactly these)

Put this in your repo-root `.env` (copy from `.env.example` if needed):

```text
GRAPH_AUTH_MODE=device_code
GRAPH_TENANT_ID=<Directory/Tenant ID from the app registration Overview page>
GRAPH_CLIENT_ID=<Application/Client ID from the app registration Overview page>
```

Leave `GRAPH_CLIENT_SECRET` empty for device-code mode.

You do **not** need SharePoint vars for this Teams probe.

## Run

```powershell
# Auth smoke test
python scripts/test_teams_graph_connection.py --auth-only

# Pull ALL messages from one chat in the case date window (preferred)
python scripts/test_teams_graph_connection.py `
  --chat-topic "Support chat for Haslet" `
  --from-date 2026-08-22 `
  --to-date 2026-08-25

# Dates can also be inferred from Salesforce probe case 00233681
python scripts/test_teams_graph_connection.py --chat-topic "Support chat for Haslet"
```

If Entra blocks custom-app consent at Fortna, use Power Automate instead:

[POWER_AUTOMATE_TEAMS_EXPORT.md](POWER_AUTOMATE_TEAMS_EXPORT.md)

Output (gitignored): `data/output/teams_probe/<chat-slug>/teams_hits.md` + `teams_hits.json`

## How it works

1. Resolve the chat by **topic name** (exact match; use `--topic-contains` for substring)
2. Page `/me/chats/{id}/messages` (newest first) until before `--from-date`
3. Keep every message inside the inclusive date window — **no case-number filter**
4. Download inline images (`hostedContents/$value`) and image attachments into `images/`

## Limits

- Device-code only sees chats the signed-in user belongs to
- Meeting chats you were not added to will not appear
- Org Search API access / permissions vary; topic matching still runs if search fails
