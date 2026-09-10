from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE


def set_shape_text(shape, text: str) -> None:
    if not hasattr(shape, "text_frame"):
        return
    tf = shape.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = text


def set_table_cell(table, row: int, col: int, text: str) -> None:
    table.cell(row, col).text = text


def main() -> None:
    src = Path(
        r"c:\Users\caiyawulf\OneDrive - Fortna Inc\Optisweep AI Support Assistant"
        r"\Weekly Updates\OptisweepAI Weekly Update 070626.pptx"
    )
    out = Path(
        r"c:\Users\caiyawulf\OneDrive - Fortna Inc\Optisweep AI Support Assistant"
        r"\Weekly Updates\OptisweepAI Weekly Update 070726.pptx"
    )
    markdown_out = Path(
        r"c:\Users\caiyawulf\OneDrive - Fortna Inc\Optisweep AI Support Assistant"
        r"\Weekly Updates\OptisweepAI Weekly Update 070726 - Slide Text.md"
    )

    repo_root = Path(__file__).resolve().parents[1]
    candidates = [
        repo_root / "OptisweepAI Weekly Update 070626.pptx",
        repo_root / "OptisweepAI Weekly Update 070726.pptx",
        out,
        src,
    ]
    template = next((p for p in candidates if p.exists()), None)
    if template is None:
        raise FileNotFoundError(
            "No PowerPoint template found. Place OptisweepAI Weekly Update 070626.pptx "
            "in the Weekly Updates folder or repo root."
        )

    prs = Presentation(str(template))

    slide1 = prs.slides[0]
    for shape in slide1.shapes:
        if "July" in shape.text:
            set_shape_text(shape, "July 7th, 2026")

    slide2 = prs.slides[1]
    for shape in slide2.shapes:
        if hasattr(shape, "text_frame"):
            set_shape_text(
                shape,
                """This Week: Data Validation
Playbook Workflow — Prompt A vs Prompt B
Pipeline Progress
Post-Review Plan & Milestones
Discussion""",
            )

    slide3 = prs.slides[2]
    for shape in slide3.shapes:
        if shape.name != "Title 1" and hasattr(shape, "text_frame"):
            set_shape_text(
                shape,
                """This Week: Data Validation Session — Tuesday, July 7

Objective
Validate the quality, credibility, and completeness of generated knowledge assets before any prompt testing in the application.

What we are reviewing
Runbooks and procedures from the O&M Manual, Day 1 training video, and historical incident cases (228086, 228723).
Incident playbooks (workflows) in both Prompt A and Prompt B variants — linked to canonical runbooks with decision branches.

What this session is not
I will not be demonstrating the troubleshooting application. This is a knowledge-asset review only.

Pre-read
Case 228086 example runbook: github.com/caiyawulf21/optisweepAI-ingestion/tree/master/sme_review_runbooks/case_228086
All runbooks (408): github.com/caiyawulf21/optisweepAI-ingestion/tree/master/sme_review_runbooks
Stage 8 playbooks: shared_pipeline_stages/data/output/shared/stage_8_finalized_playbooks/""",
            )

    slide4 = prs.slides[3]
    for shape in slide4.shapes:
        if shape.name == "Title 1":
            set_shape_text(shape, "Playbook Workflow: Why Prompt A & Prompt B")
        elif "What I" in shape.text or "completed" in shape.text.lower():
            set_shape_text(
                shape,
                """Why test two extraction modes?

Incidents are historical records — not every case maps to a single troubleshooting path.
A case may have one clear resolution, multiple separable paths, or a main issue with downstream recovery steps.

Playbooks are runtime orchestration assets, not case summaries.
At runtime, users describe symptoms ("robots not moving," "HMI shows question marks") — the assistant must route to the right workflow without knowing the diagnosis upfront.

If playbooks are too broad → vague guidance, wrong routing, unnecessary questions.
If playbooks are too narrow → too many overlapping workflows, harder to select the right path.

We run both modes in parallel so SMEs can compare quality before we lock in a default.""",
            )
        elif "Incidence pipeline" in shape.text or "validation" in shape.text.lower():
            set_shape_text(
                shape,
                """Prompt A — One playbook per incident (MVP default)
Exactly one playbook candidate per incident.
Simpler routing, lower review burden, cleaner symptom-to-workflow mapping.
Best when an incident has one dominant troubleshooting narrative.

Prompt B — Multi-flow when separable
One or more playbook candidates per incident.
Creates multiple playbooks only when clearly separable flows exist (different entry symptoms or operational signatures).
Best when an incident contains distinct troubleshooting paths that should not be compressed.""",
            )
        elif "Stage 7" in shape.text or "Pipeline" in shape.text or "metrics" in shape.text.lower():
            set_shape_text(
                shape,
                """Pilot comparison — cases 228086 & 228723

Prompt A: 2 playbooks, 13 nodes, 93% high-confidence runbook links
Prompt B: 3 playbooks, 19 nodes, 95% high-confidence runbook links

Example — case 228086 (site-wide motion stop):
Prompt A → one combined recovery playbook
Prompt B → splits into (1) site motion stoppage / OptiSweep recovery and (2) WCSWebApp / Ignition error investigation

Tomorrow we need SME input: which extraction produces more accurate, usable workflows?
After data review we will select a playbook extraction mode, choose representative cases, and define the prompts to test in the application during the weeks of July 13 and July 20.""",
            )

    slide5 = prs.slides[4]
    for shape in slide5.shapes:
        if shape.shape_type == MSO_SHAPE_TYPE.TABLE and shape.name == "Table 2":
            updates = {
                2: ("Multi-Source Ingestion Architecture", "95%"),
                3: ("Video Ingestion Path", "90%"),
                6: ("Canonical Runbook Library", "85%"),
                7: ("Knowledge Relationships", "75%"),
                8: ("Validation & Quality Controls", "65%"),
                9: ("Production-Ready Knowledge Assets", "55%"),
            }
            for row, (label, pct) in updates.items():
                set_table_cell(shape.table, row, 0, label)
                set_table_cell(shape.table, row, 1, pct)
        elif shape.shape_type == MSO_SHAPE_TYPE.TABLE and shape.name == "Table 4":
            activities = [
                "Post-Data-Review Activities",
                "Incorporate SME feedback from July 7 review",
                "Select playbook extraction mode (Prompt A vs B) based on review",
                "Choose representative incident cases and demo prompts for testing",
                "Load validated knowledge into the troubleshooting application",
                "End-to-end prompt testing — weeks of July 13 & July 20",
            ]
            for row, text in enumerate(activities):
                set_table_cell(shape.table, row, 0, text)
        elif shape.shape_type == MSO_SHAPE_TYPE.TABLE and shape.name == "Table 9":
            incident_updates = {
                2: ("Shared Pipeline Components Available", "90%"),
                5: ("Canonical Incident + Timeline Development", "40%"),
                6: ("Runbook + Playbook Generation", "85%"),
                7: ("Overall Incident Pipeline", "70%"),
            }
            for row, (label, pct) in incident_updates.items():
                set_table_cell(shape.table, row, 0, label)
                set_table_cell(shape.table, row, 1, pct)
        elif "Targeted Completion" in shape.text or "Data Review" in shape.text:
            set_shape_text(
                shape,
                "Data Review: July 7  |  Case & Prompt Selection: July 7–11  |  App Testing: Weeks of July 13 & July 20",
            )

    slide6 = prs.slides[5]
    for shape in slide6.shapes:
        if shape.name == "Title 1":
            set_shape_text(shape, "Recent Changes & Post-Review Plan")
        elif shape.name != "Title 1" and hasattr(shape, "text_frame"):
            set_shape_text(
                shape,
                """Recent pipeline changes

Shared synthesis stages (6.5 → 8) now operational across all three source types:
Stage 6.5: cross-source runbook pool — 403 candidates embedded and clustered (manual + training + incident).
Stage 7: canonical runbook merge — 399 canonical runbooks with SME review Markdown; LLM merge only on approved clusters.
Stage 8: playbook-to-runbook linking — finalized playbooks with decision branches, linked procedures, and HTML review outputs.

Other changes since last update
Video ingestion path added — training recordings feed the same pipeline as manuals.
Human-reviewable Markdown + HTML outputs for runbooks and playbooks (not just JSON).
Dual Prompt A/B tracks run end-to-end through Stage 5 extraction and Stage 8 linking with comparison metrics.
408 SME-reviewable runbooks published to GitHub (225 manual, 182 training, 1 incident).

After data review (July 7–11)
1. Incorporate SME corrections into knowledge assets.
2. Decide Prompt A vs Prompt B as the default extraction mode (or case-by-case rules).
3. Select a small set of representative incident cases and demonstration prompts for application testing.
4. Load validated knowledge into the troubleshooting app.
5. Prompt testing sessions — weeks of July 13 and July 20 (retrieval, workflow selection, troubleshooting guidance, UX).

Discussion
Biweekly meeting cadence during transition. Handoff target: Ravi Mareddy & team.
Please bring operational corrections, gap notes, and preference on playbook extraction quality.""",
            )

    slide7 = prs.slides[6]
    for shape in slide7.shapes:
        if shape.shape_type == MSO_SHAPE_TYPE.TABLE:
            milestones = [
                ("Timeline", "Milestone", "Key Deliverables"),
                (
                    "Week of 7/7",
                    "Data Validation Session",
                    "Review runbooks & playbooks (Prompt A + B); collect SME feedback on quality and extraction mode",
                ),
                (
                    "7/7 – 7/11",
                    "Case & Prompt Selection",
                    "Apply SME corrections; choose extraction mode, incident cases, and demo prompts for app testing",
                ),
                (
                    "Week of 7/13",
                    "Prompt Testing — Round 1",
                    "Selected cases + prompts in app: retrieval quality, workflow routing, troubleshooting guidance",
                ),
                (
                    "Week of 7/20",
                    "Prompt Testing — Round 2",
                    "Refined scenarios based on Round 1; KPI discussion; gap analysis",
                ),
                (
                    "Late July",
                    "Handoff Preparation",
                    "Documentation, training, transfer to Ravi Mareddy & team",
                ),
                (
                    "End of effort",
                    "Final Deliverables",
                    "Reusable ingestion pipeline, app codebase, validated knowledge assets",
                ),
            ]
            for row, cells in enumerate(milestones):
                for col, text in enumerate(cells):
                    set_table_cell(shape.table, row, col, text)

    slide8 = prs.slides[7]
    for shape in slide8.shapes:
        if shape.shape_type != MSO_SHAPE_TYPE.TABLE and "Stage 8" in shape.text:
            set_shape_text(
                shape,
                shape.text.replace(
                    "-> Stage 8: Relationship linking (LLM Assisted)\nFinal linking point after artifacts (screenshots, images, tables), operational context, candidates, runbooks. FUTURE: link playbooks.",
                    "-> Stage 8: Playbook finalization & runbook linking (LLM Assisted)\nLinks incident playbook nodes to canonical runbooks. Runs Prompt A and Prompt B tracks in parallel. Produces decision branches, linked procedures, and SME review outputs.",
                ),
            )

    prs.save(str(out))

    slide_text = Path(__file__).parent / "weekly_update_070726_slides.md"
    if slide_text.exists():
        markdown_out.write_text(slide_text.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Saved: {markdown_out}")

    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
