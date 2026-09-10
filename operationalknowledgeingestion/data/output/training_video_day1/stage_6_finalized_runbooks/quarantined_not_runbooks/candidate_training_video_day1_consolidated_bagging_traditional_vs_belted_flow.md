# Describe Traditional Small Sort vs Belted ACB Bagging Flow (Shoot-to-Bag-to-Takeaway)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_describe_traditional_small_sort_vs_belted_acb_bagging_flow_v1` |
| Title | Describe Traditional Small Sort vs Belted ACB Bagging Flow (Shoot-to-Bag-to-Takeaway) |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | None |
| Access Surface | None |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the source-described process to explain how parcels move from sorter destinations into bags and onto takeaway belts in both a traditional small sort model and a belted ACB model, including the named operator actions (close destination/print/apply label/zips/reopen chute) versus the belted conveyor “slug” movement (bin dropped to takeaway conveyor → chute → bag station).

## When To Use

When you need to accurately communicate the difference between (1) traditional small sort bagging and (2) belted ACB bagging flow, using the source’s named elements: destination/shoot, bag, label, zipping, takeaway belt, chute reopening, and (for belted) bin dropped to takeaway conveyor as a slug down a chute into a bag station.

## Do Not Use For

* Do not use this as an operational troubleshooting procedure for live RMS/WCS/SSMS/robot systems, because the source provides a conceptual process description rather than live UI/DB/API steps.

## Access Or Tools Needed

* Access to the training video segment transcript/slide text for “What is OptiSweep Traditional vs Fortna's Solution”

## Related Operational Context

* ctx_training_video_traditional_small_sort_bagging_reference_v1
* ctx_training_video_belted_acb_solution_reference_v1

## Procedure Steps

### Step 1 — Identify the traditional small sort model described in the source

**Responsible role:** operator

**Instruction:**
From the source segment “What is OptiSweep Traditional vs Fortna's Solution” (training_video_day1_segment_0004), identify the traditional small sort elements: operators assigned sections of destinations (20-25) on a sorter; parcels divert down the destination and fall into a bag.

**Expected result:**
You can name the traditional small sort starting point and ownership: operators assigned sections of destinations (20-25) on a sorter, and parcels divert down the destination into a bag.

**Stop or Escalate If:**

* If you cannot map the described elements to the traditional model (destination/shoot → bag), stop and re-check the source wording for “operators assigned sections of destinations (20-25),” “parcels divert down the destination,” and “fall into a bag.”

---

### Step 2 — Follow the traditional small sort sequence when a bag becomes full

**Responsible role:** operator

**Instruction:**
Using the same source segment, follow the traditional bag-full sequence exactly as described: close the destination, print a label, apply the label to the bag, zip up the bag, place the bag on a takeaway belt, then reopen the chute.

**Expected result:**
You can restate the full traditional bag-full sequence with all named actions in order: close destination → prints label → applies label → zips up → places on takeaway belt → reopens chute.

**Stop or Escalate If:**

* If you cannot restate the traditional bag-full sequence with the named actions (close destination/print/apply label/zips/place on takeaway belt/reopen chute), stop and re-check the source wording for those exact elements.

---

### Step 3 — Identify the belted ACB model described in the source

**Responsible role:** operator

**Instruction:**
Using the source segment, identify the belted ACB mechanism: when a destination is full, the bin is dropped on a takeaway conveyor that conveys packages as a slug down a chute into a bag station.

**Expected result:**
You can name the belted ACB mechanism: full destination bin dropped onto takeaway conveyor → conveys packages as a slug down a chute → into a bag station.

**Stop or Escalate If:**

* If you cannot map the described elements to the belted model (bin dropped to takeaway conveyor as a slug → chute → bag station), stop and re-check the source wording for “bin dropped,” “takeaway conveyor,” “slug,” “chute,” and “bag station.”

---

### Step 4 — Follow the belted ACB sequence at the bag station

**Responsible role:** operator

**Instruction:**
Using the source segment, follow the bag station actions for belted ACB: user applies a label, zips up the bag, and places it on a takeaway belt.

**Expected result:**
You can restate the belted bag station actions: apply label → zip up bag → place on a takeaway belt.

**Stop or Escalate If:**

* If you cannot restate the belted bag station actions with the named steps (apply label/zip/place on takeaway belt), stop and re-check the source wording for those exact elements.

---

### Step 5 — Compare the two flows using only the source-described differences

**Responsible role:** operator

**Instruction:**
Using the source segment, compare traditional vs belted ACB using only the described differences: traditional relies on operator actions at the destination (close/print/apply/zip/reopen), while belted ACB uses a dropped bin and conveyor “slug” movement to a bag station.

**Expected result:**
You can accurately state the contrast: traditional = operator closes destination/prints/applies label/zips/reopens chute; belted = destination full triggers bin drop to takeaway conveyor conveying packages as a slug down a chute into a bag station.

**Stop or Escalate If:**

* If you cannot map the described steps to the correct model (traditional vs belted), stop and re-check the source wording for the named elements (destination, chute, bag, label, zips, takeaway belt/conveyor, bin dropped, slug, bag station).

---

## Success Criteria

* User can accurately restate the source-described parcel-to-bag-to-takeaway flow for both models (traditional and belted ACB), including the named actions (close destination/print/apply/zip/reopen vs bin dropped to takeaway conveyor as a slug to chute/bag station).

## Failure Conditions

* User cannot correctly map steps to the correct model (traditional vs belted).
* User omits one or more named elements in either flow (destination/shoot, bag, label, zips, takeaway belt, chute reopening; or belted bin-drop, slug, chute, bag station).
* User blends the two models’ sequences (mixing operator destination close/reopen chute with belted slug/bin-drop).

## Escalation Guidance

* If the user cannot map the described steps to the correct model, stop and re-check the source wording for the named elements: destination, chute, bag, label, zips, takeaway belt/conveyor, bin dropped, slug, bag station.

## Missing Details / Known Gaps

* No live operational surface (RMS/WCS/SSMS/HMI/API) is provided in the source for executing or verifying this flow; this runbook is limited to source-backed explanation/communication of the described process.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_consolidated_bagging_traditional_vs_belted_flow
- Source ID: `training_video_day1`
- Source Type: `training_video`
