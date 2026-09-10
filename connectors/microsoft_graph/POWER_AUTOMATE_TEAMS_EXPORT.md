# Power Automate: export “Support chat for Haslet” by date

Use this when custom Entra apps are blocked by Fortna user-consent policy.
This flow uses the **Microsoft Teams** connector’s Graph HTTP action (Microsoft’s app, signed in as you).

Target for Case 00233681:

- Chat topic: `Support chat for Haslet`
- Window: `2026-08-22` → `2026-08-25` (inclusive)

Output: JSON file in OneDrive that you can drop into this repo.

---

## 0) Open Power Automate

1. Go to [https://make.powerautomate.com](https://make.powerautomate.com)
2. Sign in as `caiyawulf@fortna.com`
3. Environment: your default Fortna environment

If Teams connector consent fails with “Need admin approval”, stop — same tenant gate; escalate IT. If it connects, you’re unblocked for this path.

---

## 1) Create the flow

1. **Create** → **Instant cloud flow**
2. Name: `OptiSweep - Export Haslet chat by date`
3. Trigger: **Manually trigger a flow**
4. Add inputs on the trigger:

| Input name | Type | Default / example |
| --- | --- | --- |
| `ChatTopic` | Text | `Support chat for Haslet` |
| `FromDate` | Text | `2026-08-22` |
| `ToDate` | Text | `2026-08-25` |

---

## 2) List your chats

Add action → **Microsoft Teams** → **Send a Microsoft Graph HTTP request**

| Field | Value |
| --- | --- |
| Uri | `/me/chats?$top=50` |
| Method | `GET` |
| Content type | *(leave empty)* |
| Body | *(leave empty)* |

On first use, create/sign in to the Teams connection as yourself.

**Note:** Uri must start with `/me`, `/users`, or `/teams` (Teams connector rule).  
`/me/chats` is valid. `/chats/...` alone is not.

---

## 3) Parse the chat list

Add **Parse JSON**

- Content: `body` from the Teams Graph action  
  (or `body('Send_a_Microsoft_Graph_HTTP_request')`)
- Schema → **Generate from sample** and paste:

```json
{
  "type": "object",
  "properties": {
    "value": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "topic": { "type": ["string", "null"] },
          "chatType": { "type": "string" }
        }
      }
    },
    "@odata.nextLink": { "type": "string" }
  }
}
```

If you have more than 50 chats, add a **Do until** that follows `@odata.nextLink` the same way as messages (section 6). For a first POC, 50 is often enough.

---

## 4) Find “Support chat for Haslet”

Add **Filter array**

- From: `value` from Parse JSON
- Condition (edit in advanced mode):

```text
@equals(toLower(string(item()?['topic'])), toLower(triggerBody()?['text']))
```

If your trigger input is named `ChatTopic`, use:

```text
@equals(toLower(string(item()?['topic'])), toLower(triggerBody()?['ChatTopic']))
```

*(Power Automate renames manual inputs; pick the dynamic token for ChatTopic if unsure.)*

Simpler UI mode alternative:

- `topic` **is equal to** `Support chat for Haslet`

Add **Compose** named `ChatId`:

```text
first(body('Filter_array'))?['id']
```

Add a **Condition**: `ChatId` is not equal to null/empty.  
If empty → **Terminate** Failed with message `Chat topic not found`.

---

## 5) Get messages (first page)

Add another **Microsoft Teams** → **Send a Microsoft Graph HTTP request**  
Name it `Get_messages_page`

| Field | Value |
| --- | --- |
| Uri | `/me/chats/@{outputs('ChatId')}/messages?$top=50` |
| Method | `GET` |

---

## 6) Page until before FromDate

Messages come **newest first**. Keep paging until you pass `FromDate`.

### 6a. Initialize variables

| Name | Type | Value |
| --- | --- | --- |
| `AllMessages` | Array | `[]` |
| `NextLink` | String | *(empty)* |
| `ReachedBeforeWindow` | Boolean | `false` |

### 6b. After first Get_messages_page

**Append to array variable** `AllMessages` — use a **Select** or **Compose** of `body('Get_messages_page')?['value']`, then append each, or set:

```text
union(variables('AllMessages'), body('Get_messages_page')?['value'])
```

Easiest POC: **Set variable** `AllMessages` =

```text
body('Get_messages_page')?['value']
```

Then **Set variable** `NextLink` =

```text
body('Get_messages_page')?['@odata.nextLink']
```

### 6c. Do until

**Do until** condition (advanced):

```text
@or(equals(variables('NextLink'), null), equals(variables('NextLink'), ''), variables('ReachedBeforeWindow'))
```

Inside the loop:

1. **Teams – Send a Microsoft Graph HTTP request** (`Get_messages_next`)
   - Uri: paste `NextLink` but convert absolute Graph URL to a path Teams accepts.
   - If NextLink is `https://graph.microsoft.com/v1.0/me/chats/...`, set Uri to the part starting at `/me/...`  
     Expression example:

```text
replace(variables('NextLink'), 'https://graph.microsoft.com/v1.0', '')
```

2. **Set variable** `AllMessages` =

```text
union(variables('AllMessages'), body('Get_messages_next')?['value'])
```

3. **Set variable** `NextLink` =

```text
body('Get_messages_next')?['@odata.nextLink']
```

4. Optional early stop: **Compose** oldest message date on the page; if `< FromDate`, set `ReachedBeforeWindow` = true.

---

## 7) Filter to date window

Add **Filter array** named `Messages_in_window`

- From: `variables('AllMessages')`
- Advanced mode:

```text
@and(
  greaterOrEquals(substring(string(item()?['createdDateTime']), 0, 10), triggerBody()?['FromDate']),
  lessOrEquals(substring(string(item()?['createdDateTime']), 0, 10), triggerBody()?['ToDate'])
)
```

Use your actual trigger field names for FromDate / ToDate.

---

## 8) Save JSON to OneDrive

Add **OneDrive for Business** → **Create file**

| Field | Value |
| --- | --- |
| Folder path | `/OptiSweepExports` (create folder first if needed) |
| File name | `haslet_@{triggerBody()?['FromDate']}_to_@{triggerBody()?['ToDate']}.json` |
| File content | `body('Messages_in_window')` (or a Compose that wraps metadata) |

Recommended wrap (Compose `ExportPayload`):

```json
{
  "chatTopic": "@{triggerBody()?['ChatTopic']}",
  "fromDate": "@{triggerBody()?['FromDate']}",
  "toDate": "@{triggerBody()?['ToDate']}",
  "chatId": "@{outputs('ChatId')}",
  "messages": @{body('Messages_in_window')}
}
```

*(In Compose, build with dynamic content; don’t paste broken JSON braces manually if the designer fights you — use nested Compose actions.)*

---

## 9) Run it

1. **Save** → **Test** → **Manually**
2. Inputs:
   - ChatTopic: `Support chat for Haslet`
   - FromDate: `2026-08-22`
   - ToDate: `2026-08-25`
3. Download the OneDrive JSON
4. Copy into the repo:

```text
data/output/teams_probe/Support_chat_for_Haslet/power_automate_export.json
```

---

## Images

Power Automate can also call:

```text
GET /me/chats/{chat-id}/messages/{message-id}/hostedContents
GET /me/chats/{chat-id}/messages/{message-id}/hostedContents/{id}/$value
```

That’s a second loop (per message). For the first POC, export **text messages** first; add hosted-content download after the JSON export works.

Faster image path without Graph: Teams → chat → **Files** → **Open in SharePoint** → sync/download.

---

## If something fails

| Symptom | Meaning |
| --- | --- |
| Need admin approval on Teams connection | Same Fortna consent policy; IT must allow Teams/Power Platform Graph scopes |
| URI path is not a valid Graph endpoint | Uri must start with `/me/...` not `/chats/...` |
| Chat topic not found | You’re not in that chat on this account, or topic text differs slightly |
| Empty messages in window | Wrong dates (UTC days) or need more paging |
| Premium license required | You’re on raw HTTP connector — switch back to **Teams → Send a Microsoft Graph HTTP request** |

---

## After IT eventually consents your app

Prefer the local probe again:

```powershell
python scripts/test_teams_graph_connection.py --chat-topic "Support chat for Haslet" --from-date 2026-08-22 --to-date 2026-08-25
```

That path also downloads images into `images/`.
