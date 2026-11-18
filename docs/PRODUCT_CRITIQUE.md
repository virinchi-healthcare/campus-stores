# Campus Stores: Product Critique

Role: Senior Product Manager. Every finding refers to a step in [BASELINE_TESTING.md](BASELINE_TESTING.md) (step numbers like 1.4, 3.3, N7) or to code facts in [PROJECT_AUDIT.md](PROJECT_AUDIT.md).

**Limit on the evidence.** It comes from one tester working through a fictional three-phase scenario, and no real counter was observed. Scores below are judgements built on that evidence. They are not measured frequencies.

---

## 1. What works well (keep these)

### S1. Ineligible units cannot be picked at all
- **Action:** opening the issue form at 3:45 pm (1.4, N1, N2).
- **How the app supports it:** the unit list contains only units that are on the shelf. MI-09 (on loan) and PR-06 (in repair) never appear, and an issued unit drops out of the list straight away.
- **Why it matters at a counter:** with a club member waiting, the employee cannot hand over a unit that is promised elsewhere or broken. The mistake is prevented, not just reported.
- **Keep:** the availability filter on the unit list (`!a.repair && !out(a.id)`).

### S2. Request rules stop wrong or extra equipment
- **Action:** trying a camera on RQ-214 and a second adapter on RQ-214 (N3, N4).
- **How the app supports it:** the save is refused with a specific message. The selections stay so the employee can fix one field. Once the first unit comes back, a replacement unit can be issued (N4).
- **Why it matters:** the approval form is what the desk is accountable to, and the app enforces it at the moment the equipment leaves.
- **Keep:** rules R3 and R4 exactly, including "outstanding only" for R4.

### S3. One slip per physical unit makes partial returns trivial
- **Action:** Kabir returns 2 of 3 items at 7:30 pm (2.3).
- **How the app supports it:** two clicks closed exactly L-402 and L-403. L-404 stayed open, and Inventory updated at once.
- **Why it matters:** kits really do come back in pieces. Tracking per unit means the system never claims the whole kit is back when it is not.
- **Keep:** per-unit slips, slip numbering, and the Outstanding/All slips split.

### S4. Inventory always agrees with the register
- **Action:** checking stock after each issue and return (1.8, 2.5, 3.6).
- **How the app supports it:** status is derived from the slips, so it can never drift out of step.
- **Why it matters:** "Is it on the shelf?" is answered correctly without anyone having to reconcile two records.
- **Keep:** derived status. Don't introduce a stored status field.

### S5. State survives refreshes and resets cleanly
- **Action:** a refresh mid-shift (P1) and Restart (P4).
- **How the app supports it:** the saved state was identical after the reload, down to the open request and the filters. Restart returned the exact seed data.
- **Why it matters:** a counter PC gets refreshed or closed, and work must not be lost.
- **Keep:** the save key, its format and the `restore()` validation. Any new view must be **derived** from existing state so that saved data stays compatible.

---

## 2. What does not work well

Only usability problems are listed. Things that are matters of taste were **not** treated as findings: the dark theme, the density, the typography, and the icon-only brand mark. None of them got in the way of a task.

### F1. The register cannot answer "what is still out from this job?"
1. **When:** Saturday 9:00 am, Leela at the counter with an adapter (3.3–3.5). The same gap appeared at 7:30 pm when matching "projector and speaker" to slips (2.3).
2. **Intent:** find the screening's outstanding item and close the right slip.
3. **What the app makes you do:**
   - Read "L-404 · AD-12 · RQ-214 · Kabir Sen · Due Fri 8 pm".
   - Go to Inventory and filter to On loan to learn that AD-12 is the USB-C → HDMI adapter.
   - Go to the Desk book to learn that Leela has it.
   - Return to the register.

   That is **4 tab clicks** (measured). The first click re-selected the already-open Desk book, so there were 3 actual view changes plus an Inventory filter change.
4. **Why it's friction:**
   - The register shows IDs where people talk in equipment names: Kabir said "projector and speaker", Leela says "adapter".
   - It shows separate slips where people talk about a job: "the screening kit".
   - "Due Fri 8 pm" is shown on Saturday morning with no overdue signal.
   - Nothing shows that the other two RQ-214 items are already back.
5. **Operational consequence:**
   - Slower service while someone waits at the counter.
   - Reliance on whatever the evening shift chose to type. In V1, with no note, the register never mentions "adapter" or "Leela".
   - The room for closing the wrong slip grows as more loans are open, because "Record return" is irreversible (N7) and two adapter units exist (AD-12, AD-15).
   - Overdue items go unnoticed.
6. **Evidence:** steps 3.3–3.4 and 2.3; variant V1 (programmatic check: no "adapter", "Leela" or "overdue" in the register text); screenshots `20`, `21`, `V1-morning-register-no-note`.
7. **Possible solution:**
   - Group outstanding slips by request.
   - Name each unit by type and model.
   - Show the status of every approved item (out / back / not issued).
   - Flag overdue slips against the desk clock.

### F2. Issuing one request's kit takes three full passes through the form
1. **When:** Friday 3:45 pm, Kabir at the counter, film starts at four (1.4–1.6).
2. **Intent:** "Can he leave with everything he needs?"
3. **What the app makes you do:**
   - Three passes of New slip → 4 selects → Save.
   - Re-select the same request, collector and date each time: 9 selections, of which only 3 carry new information.
   - Remember RQ-214's approved list from another view, because the form neither shows it nor filters units by it.
   - Measured input: 18 clicks + 28 keypresses (about 30 mouse clicks, derived).
4. **Why it's friction:** repeated entry under time pressure, and nothing confirms the kit is complete.
5. **Operational consequence:**
   - A missed adapter means the screening fails, because the laptop is USB-C only.
   - The issue form refuses wrong items, but **nothing flags a missing one**.
6. **Evidence:** 1.4–1.7, N6 (leaving to check Requests discards the form), screenshots `07`–`09`.
7. **Possible solution:**
   - "Issue kit" from the request: one row per approved type, with an eligible-unit picker.
   - Collector and return-by entered once, return-by pre-filled from the request.
   - One save creates one slip per unit.

### F3. A return is one irreversible click
1. **When:** any **Record return**, e.g. 2.3 and N7.
2. **Intent:** close one slip.
3. **What the app makes you do:** a single click closes the slip, with no confirmation, no undo and no return time recorded.
4. **Why it's friction:** identical buttons sit beside each other, and a slip is recognised only by its ID.
5. **Consequence:** a mis-click marks an item as On shelf while it is physically out, and the item can then be issued to someone else. Recovery means Restart, which wipes the whole shift.
6. **Evidence:** N7, `N7-empty-outstanding-after-one-click-return`. *This is a risk shown by the test; no actual mistake happened in the main run.*
7. **Possible solution:** an undo for the last return, or an inline "Confirm AD-12 USB-C adapter received?" step.

### F4. Weak validation feedback and gaps
1. **When:** N3 (wrong type) and N5 (Dev Menon on RQ-214, return-by Sat noon).
2. **Intent:** issue correctly first time.
3. **What the app does:**
   - Errors appear only in the 12 px footer status bar, away from Save.
   - Return-by and collector are never checked against the request.
4. **Why it's friction:** an error can be missed, and a wrong due date is accepted without a word.
5. **Consequence:** the due date may not match the approval, and the slip may name someone with no connection to the club.
6. **Evidence:** `N3`, `N5`.
7. **Possible solution:** show errors inline, pre-fill return-by, and warn when the collector or date differs from the request.

---

## 3. Prioritisation

Scale 1–5. For **Ease**, 5 means easiest to build well. Weights: Impact ×2 and Mistake risk ×2, because a counter error affects stock and service; the rest ×1. Maximum score 35.

| Opportunity | Impact | Likelihood / frequency | Time / effort wasted | Mistake risk | Ease | **Weighted total** |
|---|---|---|---|---|---|---|
| F1 Request-level, readable register | 4 | 4: every partial return and every handover read; it hit Stage 2 and Stage 3 | 3: 4 tab clicks / 3 view changes | 4: wrong slip, overdue missed, depends on the note | 5: display only, derived from existing data | **28** |
| F2 One-pass kit issue | 4 | 3: multi-item requests only (1 of 3 here, but the main one) | 5: ~30 clicks, 6 redundant selections | 3: wrong items already blocked; missing items not flagged | 2: new write path that creates several slips and must re-run R3/R4 for each | **24** |
| F3 Undoable / confirmed return | 3 | 2: only on a mis-click (not seen in the main run) | 1 | 4 | 4 | **21** |
| F4 Inline errors and request-aware validation | 2 | 2 | 2 | 3 | 4 | **18** |

**How sensitive the ranking is:** F1 and F2 are close.

- If Ease is dropped, F1 still leads, 23 to 22.
- If effort wasted is weighted ×2, F1 still leads, 31 to 29.
- F2 overtakes only when both changes are made: F2 27, F1 26.

The deciding factors are given below.

---

## 4. Recommended improvement: a "kit by request" view in the Loan register

In the Outstanding scope, show slips **grouped under their request**. Each group lists every approved item: its equipment type, the unit ID and model, the slip and collector, and a clear state (**Out**, **Back**, or **Not issued**). A summary such as "1 of 3 still out" goes on the group, and an **Overdue** badge appears when the desk clock is past the slip's return-by. The **Record return** button stays on each outstanding item.

**Why this over the alternatives**
- **It fixes the moment the brief cares about most.** The brief asks the shift to "leave the next shift enough information to finish the job". F1 is the gap between the record and that goal (Stage 3, V1).
- **It covers all three phases with one change:**
  - At 3:45 pm, "Not issued: USB-C → HDMI adapter" answers "Can he leave with everything?". That covers the riskiest part of F2 (a missing item) without changing the issue form.
  - At 7:30 pm, the rows read "HDMI projector" and "Portable speaker", matching Kabir's words.
  - At 9:00 am, the adapter is named, its slip is right there, and it is flagged Overdue.
- **It carries the least risk to what works.** It is a pure presentation change derived from `requests`, `assets`, `loans` and `phase`. It needs no new stored fields, no changes to R1–R5, and no change to the save format (S1–S5 preserved).
- **It is testable on the same shift** with the same request (RQ-214), units (PR-04, SP-02, AD-12) and collector (Kabir Sen), with before/after comparisons for each stage.
- **F2's repeated entry is real but secondary.** Fixing it rewrites the path where every business rule lives, for a saving that only applies to multi-item requests.
- F3 and F4 are worth doing but are smaller; they are noted as follow-ups.

## 5. Expected benefits (to be checked, not assumed)

| For | Expected effect | How we'll know (in this exercise) |
|---|---|---|
| Morning employee | Identifies Leela's slip from the Loan register alone | View changes before Record return: baseline 3 (4 tab clicks) → target 0–1 (as originally set). Result: 1 view change (2 tab clicks, including the same Desk book re-click as in the baseline); see [VALIDATION.md](VALIDATION.md) |
| Evening employee | Matches "projector and speaker" to slips by name | The register text contains "HDMI projector" and "Portable speaker" |
| Pickup | Sees that the kit is incomplete before Kabir leaves | Leaving out the adapter shows "Not issued" in the RQ-214 group |
| Desk | Notices late items | L-404 shows "Overdue" at Sat 9:00 am (baseline: no flag) |
| Handover quality | Less dependent on free-text notes | V1 (no note) still shows "USB-C → HDMI adapter · Out · Overdue" |

**What to watch at a real counter:** whether staff answer "I've got the Film Society adapter" by going straight to the register, or still open Inventory and the Desk book first, and how long it takes until the right slip is closed.
