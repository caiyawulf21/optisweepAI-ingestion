# OptiSweep AI — Demo Testing Report

**Document type:** Living findings log (update after every demo testing session)  
**Audience:** Internal product / engineering  
**Related:** [Demo Test Plan](optisweep_ai_demo_test_plan.md)

---

## How to update this document

After each demo testing session:

1. Add a new row to the [Session Index](#session-index).
2. Append a new dated section under [Sessions](#sessions) (newest at the bottom).
3. Carry forward open actions into the backlog for that session; mark resolved items when closed.

---

## Session Index

| Session | Date | Focus | Status |
|---------|------|-------|--------|
| 1 | 2026-07-20 | Phase 0 — Prompt 1 guided troubleshooting validation | Complete |

---

## Sessions

### Session 1 — Demo Testing

| Field | Value |
|-------|-------|
| **Date** | 2026-07-20 |
| **Focus** | Phase 0 OptiSweep AI Assistant — Prompt 1 (AGVs stopped, no alarms showing) |
| **Audience tested** | Customer Support engineers |
| **Status** | Complete |

#### Objective

Validate whether the Phase 0 OptiSweep AI Assistant enables Customer Support engineers to diagnose Prompt 1 ([AGVs stopped, no alarms showing](optisweep_ai_demo_test_plan.md#prompt-1--agvs-stopped-no-alarms-showing)) using guided troubleshooting, while identifying gaps in usability, workflow design, retrieval quality, and supporting documentation.

#### What Went Well

**Guided troubleshooting was intuitive**

Users generally understood how the assistant progressed through a troubleshooting session. The question-and-answer format closely matched how support engineers naturally think through an issue rather than overwhelming them with documentation up front.

| Impact |
|--------|
| Low learning curve |
| Positive first impression |
| Confirms guided troubleshooting is the right interaction model |

**Evidence-backed procedures increased confidence**

Displaying procedures alongside supporting screenshots and documentation helped build trust in the recommendations. Rather than appearing as generic AI responses, users could understand where information originated.

| Impact |
|--------|
| Increased trust in recommendations |
| Better explainability |
| Supports long-term adoption goals |

**Confidence messaging was well received**

When the assistant could not confidently select a workflow, users appreciated that it communicated uncertainty instead of forcing a potentially incorrect troubleshooting path.

This aligns with the project's philosophy of prioritizing safe, evidence-based recommendations over aggressive automation.

#### Challenges & Opportunities

##### 1. Symptom extraction missed critical information

**Priority:** High

**Observation**

During testing, users described issues such as:

> "AGVs stopped with no alarms showing."

The assistant successfully extracted the AGVs stopping but failed to capture the equally important observation that no RMS alarms were present.

Because one of the defining symptoms for the Prompt 1 workflow was missing, the workflow confidence dropped below the routing threshold.

**Why this matters**

The workflow engine is only as good as the structured signals it receives. Missing even one key symptom can:

- Reduce workflow confidence
- Route to a less relevant workflow
- Generate unnecessary clarification questions
- Lower user trust

**Proposed Improvements**

- Expand symptom extraction vocabulary
- Better recognize negative observations ("no alarms", "no faults", "heartbeat normal", etc.)
- Improve synonym handling
- Review prompt engineering for structured symptom extraction

##### 2. Workflows don't always reflect how remote support actually works

**Priority:** High

**Observation**

Several procedures instructed users to check local HMIs or equipment screens that Customer Support engineers cannot directly access remotely.

Instead, support engineers typically rely on:

- RMS
- Database queries
- Remote desktop tools
- On-site operators validating physical observations

**Why this matters**

The assistant should recommend actions that the current user is actually capable of performing. If recommendations repeatedly require unavailable access, users will quickly lose confidence and revert to existing troubleshooting habits.

**Proposed Improvements**

- Review procedures from the perspective of remote support
- Separate physical operator actions from remote support actions
- Identify when operator confirmation is required

##### 3. Greater role awareness is needed

**Priority:** High

**Observation**

Current procedures assume a single generic user. In reality, troubleshooting differs depending on whether the user is:

- Site Operator
- Customer Support
- Software Support
- Controls Engineer

Each role has different permissions, tools, and responsibilities.

**Why this matters**

Providing instructions outside a user's access level creates unnecessary friction. The assistant should tailor recommendations to the authenticated user's role whenever possible.

**Proposed Improvements**

- Expand role-aware procedures
- Render different instructions based on support tier
- Better identify escalation boundaries

##### 4. Users still depend on external resources

**Priority:** Medium

**Observation**

Even while using the assistant, engineers referenced:

- Confluence
- RMS
- Database tools
- Existing support documentation

The AI assistant currently assumes these resources already exist but does not help users quickly access them.

**Why this matters**

Reducing context switching is one of the easiest ways to improve productivity.

**Proposed Improvements**

Homepage should include:

- Quick links to Confluence
- Support documentation
- RMS access guidance
- Common troubleshooting resources
- "Before you begin" checklist

#### Documentation Requests

**Ekram** — Provide documentation describing:

- Remote access process
- RMS access
- Database access
- Available support tools
- Which HMI views are remotely accessible
- Which HMI views require operator assistance

**Wesley** — Provide recommendations for homepage resources, including:

- Confluence links
- Frequently referenced documentation
- Suggested startup guidance
- Additional support resources for new users

#### Action Backlog

| Priority | Action | Owner | Status |
|----------|--------|-------|--------|
| P0 | Improve symptom extraction for negative observations | Caiya | Open |
| P0 | Review workflow routing after symptom extraction updates | Caiya | Open |
| P0 | Update procedures for remote support workflows | Caiya | Open |
| P0 | Differentiate Operator vs Support vs Engineer actions | Caiya | Open |
| P1 | Add homepage "Before You Begin" section | Caiya | Open |
| P1 | Add quick links to Confluence and support tools | Caiya | Open |
| P1 | Document remote access workflow | Ekram | Open |
| P1 | Provide homepage resource recommendations | Wesley | Open |

---

*Next session: append below this line.*
