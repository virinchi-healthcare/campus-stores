# Campus Stores: Product Decision: "Kit by request" in the Loan register

Status: **approved, implemented and validated** (see §8 for how the build differs from this proposal, and [VALIDATION.md](VALIDATION.md) for results). Inputs: [PROJECT_AUDIT.md](PROJECT_AUDIT.md), [BASELINE_TESTING.md](BASELINE_TESTING.md), [PRODUCT_CRITIQUE.md](PRODUCT_CRITIQUE.md) (friction F1, score 28/35).

---

## 1. Problem statement

**Who:**
- The desk employee taking a partial return in the evening.
- Above all, the **incoming employee** at the next morning's shift, who did not handle the original issue.

**When:**
- Someone at the counter describes equipment by **name and job**: "I brought the projector and speaker", or "I have the Film Society's adapter".
- The employee must find the right slip and close it.
- Also at pickup, when the employee needs to know whether a request's kit is complete.

**What the app does today:**
- The Loan register lists one flat row per slip: `L-404 · AD-12` / `RQ-214 · Kabir Sen · Due Fri 8 pm` / **Record return**.
- Rows show the asset ID only. Slips for the same request are not linked.
- Returned items vanish from the Outstanding scope.
- Approved items that were never issued are never shown.
- The due date is never compared with the desk clock.

**Why that is not enough (observed):**
- At Saturday 9:00 am it took **4 tab clicks, i.e. 3 view changes plus an Inventory filter change,** to establish that L-404 was Leela's adapter (Desk book → Register → Inventory → Register, step 3.3–3.5).
- With no handover note (variant V1), the register text never contains "adapter", "Leela" or "overdue". The record alone cannot support the handover, and the outcome depends on a free-text note.
- At pickup, nothing showed whether RQ-214's kit was complete (step 1.6).

**What it should achieve:** from the Loan register alone, the employee can see:
1. which job each outstanding unit belongs to;
2. what the unit **is**;
3. what else from that job is out, back, or was never issued;
4. whether it is late;

and close the right slip without leaving the view.

## 2. Proposed solution

Change only the **Outstanding** scope of the Loan register so that it groups slips **by request** and lists every approved item of that request with a plain-language state. The **All slips** scope stays a flat history, and each row gains the equipment type.

### 2.1 User journeys (same scenario, same choices as baseline)

| Moment | Before (measured in baseline) | After (target) |
|---|---|---|
| **Fri 3:45 pm**: has Kabir got everything? | Issue 3 slips; nothing confirms completeness. You have to remember the adapter from the request form. | After the 3 slips, the RQ-214 group reads **"3 out"**, listing HDMI projector / Portable speaker / USB-C → HDMI adapter. If the adapter had been missed: **"2 out · 1 not issued"** with the row "USB-C → HDMI adapter · Not issued". |
| **Fri 7:30 pm**: Kabir hands back "projector and speaker" | Match "projector" → `PR-04` and "speaker" → `SP-02` from IDs, then click Record return twice. | Rows read "HDMI projector · PR-04 …" and "Portable speaker · SP-02 …". Click Record return on both. The group becomes **"1 out · 2 back"**, with the adapter row still Out. |
| **Sat 9:00 am**: Leela has "an adapter" | Desk book → Loan register → Inventory (filter On loan) → Loan register → Record return. **4 tab clicks / 3 view changes.** No overdue signal. | Loan register → the RQ-214 group (listed first because it is overdue) shows **"USB-C → HDMI adapter · AD-12 · Belkin AVC002 · L-404 · Kabir Sen · Due Fri 8 pm · Overdue"** → Record return. **0 view changes** if already on the register, 1 otherwise. The Desk book is optional, for context ("Leela has it"). |

### 2.2 Wireframe: Outstanding scope at Saturday 9:00 am, before closing L-404

```
Loan register                                              [ New issue slip ]
One slip per physical unit
[ Outstanding ] [ All slips ]
──────────────────────────────────────────────────────────────────────────────
RQ-214 · Courtyard screening                          1 out · 2 back  [Overdue]
Film Society · Return by Fri 8 pm
  USB-C → HDMI adapter                                         [Overdue]
  AD-12 · Belkin AVC002 · bin C4
  L-404 · Kabir Sen · Due Fri 8 pm                         [ Record return ]
  ·······························································
  HDMI projector                                                  [Back]
  PR-04 · BenQ MH550 · L-402                                      (muted)
  Portable speaker                                                [Back]
  SP-02 · JBL Eon One · L-403                                     (muted)
──────────────────────────────────────────────────────────────────────────────
RQ-209 · Finals rehearsal                                         1 out
Debate Union · Return by Sat 10 am
  Wireless microphone
  MI-09 · Shure BLX · bin B3
  L-401 · Tara Shah · Due Sat 10 am                        [ Record return ]
──────────────────────────────────────────────────────────────────────────────
```

The "missing item" state at pickup looks like this (adapter not yet issued):

```
RQ-214 · Courtyard screening                         2 out · 1 not issued
Film Society · Return by Fri 8 pm
  HDMI projector · PR-04 …  L-402 · Kabir Sen · Due Fri 8 pm  [ Record return ]
  Portable speaker · SP-02 … L-403 · Kabir Sen · Due Fri 8 pm [ Record return ]
  USB-C → HDMI adapter                                       [Not issued]
```

All slips scope (history), with the type added to each row label:

```
L-404 · AD-12 · USB-C → HDMI adapter        RQ-214 · Kabir Sen · Due Fri 8 pm   [Returned]
```

### 2.3 UI elements

| Element | Change | Detail |
|---|---|---|
| Register → Outstanding list | **Modified** | Flat slip rows are replaced by request groups. Only requests with at least 1 outstanding slip appear. A request whose last unit comes back drops out of Outstanding, as slips do today. |
| Request group header | **Added** | `RQ-id · event`; `club · Return by <request due>`; a summary of counts ("1 out · 2 back · 1 not issued", omitting zero counts); an **Overdue** tag if any Out item in the group is overdue. |
| Item row: Out | **Added** (replaces the old row) | Equipment type in bold; `unit ID · model · bin`; `L-num · collected by · Due <slip due>`; **Overdue** tag if late; the existing **Record return** button, which fires the same `return` action. |
| Item row: Back | **Added** | Type; `unit ID · model · L-num`; muted **Back** tag; no button. |
| Item row: Not issued | **Added** | Type; **Not issued** tag; no button and no new action. |
| Group order | **Defined** | Groups with an overdue item first, then by earliest outstanding due time, then in request list order. |
| Item order in a group | **Defined** | Out, then Not issued, then Back. Within each state, the request's approved order. |
| All slips rows | **Modified (label only)** | `L-num · asset · type`. Order, badges and buttons are unchanged. |
| Empty state | **Kept** | "No outstanding slips." |
| Inventory, Requests, Desk book, issue form, banner, Restart | **Unchanged** | — |

**State of each approved type in a group:**
- **Out** if the type has an outstanding slip on that request.
- Otherwise **Back**, if the type has a returned slip; the most recent one is shown.
- Otherwise **Not issued**.

**Overdue:** a slip is overdue when its return-by time is **strictly before** the desk clock.
- A fixed lookup turns the labels into comparable times:
  - Desk clock: Fri 3:45 pm, Fri 7:30 pm, Sat 9:00 am.
  - Return-by: Fri 8 pm, Sat 9 am, Sat 10 am, Sat noon.
- An unrecognised label never shows Overdue (fails safe).
- With the seed data, this means only L-404-type slips due Fri 8 pm are overdue, and only at Sat 9:00 am.

### 2.4 Interactions and validation

- **No new interaction.** **Record return** is the only control in the groups, and it uses the same `data-action="return"` / `data-val=<num>`, the same guard, the same notice and the same save.
- **No new validation.** The issue rules R1–R5 are untouched.
- **No new stored state.** Everything is derived at render time from `requests`, `assets`, `s.loans` and `s.phase`. `s.onlyOpen` keeps its meaning (`true` = Outstanding).
- **Accessibility:**
  - Each group is a `<section>` with an `<h3>`.
  - State is shown in words (Out, Back, Not issued, Overdue), never by colour alone.
  - Buttons keep their visible label "Record return".
  - The status `aria-live` region is unchanged.
- **Implementation footprint (planned):**
  - `app.js`: `register()` plus small helpers; two read-only lookup constants for the clock and due times; seed records untouched.
  - `styles.css`: group container, muted row, and warning tag tokens for both themes, with stacking at ≤ 420 px.
  - `index.html`: no change.

## 3. Acceptance criteria

All criteria use the baseline scenario: Restart → issue PR-04, SP-02 and AD-12 to RQ-214 for Kabir Sen, Fri 8 pm → advance → return L-402 and L-403 → advance → return L-404.

| ID | User action | Expected response | Verification |
|---|---|---|---|
| AC1 | Restart, open Loan register (Outstanding) | One group, "RQ-209 · Finals rehearsal", "1 out", with the row "Wireless microphone · MI-09 · Shure BLX · bin B3 · L-401 · Tara Shah · Due Sat 10 am" and Record return. No RQ-214 or RQ-217 group. | Read the register text; screenshot |
| AC2 | Issue PR-04 and SP-02 only (RQ-214, Kabir, Fri 8 pm) | The RQ-214 group shows "2 out · 1 not issued" and the row "USB-C → HDMI adapter · Not issued" with no button. | Text check; screenshot |
| AC3 | Issue AD-12 as well | The RQ-214 group shows "3 out", with all three items named by type and unit; no "Not issued" row. | Text check |
| AC4 | Order at Fri 3:45 pm | RQ-214 (due Fri 8 pm) is listed above RQ-209 (due Sat 10 am). No Overdue tags anywhere. | Text order; no "Overdue" in the text |
| AC5 | Advance to Fri 7:30 pm | No Overdue tags (7:30 pm is before 8 pm). | Text check |
| AC6 | Click Record return on the "HDMI projector" row, then on the "Portable speaker" row | Notices begin "PR-04 returned to stock. Slip L-402 closed." and the same for SP-02/L-403 (as built, each adds a kit sentence; see §8). The group shows "1 out · 2 back", with the adapter row Out and the projector/speaker rows Back with no button. Inventory: PR-04 and SP-02 On shelf. | Status text, register text, Inventory text, localStorage `back` flags |
| AC7 | Advance to Sat 9:00 am, open Loan register | RQ-214 is listed first and carries the group tag **Overdue**. The adapter row reads "USB-C → HDMI adapter", "AD-12 · Belkin AVC002 · bin C4", "L-404 · Kabir Sen · Due Fri 8 pm" and **Overdue**. RQ-209's row is **not** overdue. | Text check; screenshot |
| AC8 | From the register, close Leela's adapter | One Record return click on the adapter row closes L-404 with no other view visited. The RQ-214 group disappears; RQ-209 remains. | Count of view changes = 0 from the register; register text |
| AC9 | Variant V1 (no handover note), Sat 9:00 am | The register text contains "USB-C → HDMI adapter", "L-404" and "Overdue". | Programmatic text check (baseline: all absent) |
| AC10 | Toggle **All slips** | Flat history, newest first, unchanged apart from the type in each label, e.g. "L-404 · AD-12 · USB-C → HDMI adapter" with "Returned". | Text check against baseline step 3.6 |
| AC11 | Return every outstanding slip, including L-401 | "No outstanding slips." | Text check |
| AC12 | Refresh at any point | Same groups, states and tags after the reload. The saved JSON has the **same keys and shapes** as baseline (no new fields). | Compare `localStorage` before and after; compare key sets with baseline |
| AC13 | Narrow viewport (≤ 420 px) and light theme | Groups stay readable, there is no horizontal scroll, and tags are legible in both themes. | Screenshots at a narrow width (validated at 390 px), light and dark; scrollWidth vs innerWidth; contrast of the new text |
| AC14 | Console | No new errors; only the existing favicon 404. | Console/log events |

## 4. Existing behaviour to preserve (regression checklist)

| Area | Must remain exactly as today | Re-test |
|---|---|---|
| Request approvals | 3 seed requests, their items, due dates, notes; the Requests list and detail views | Baseline 1.2 |
| Equipment eligibility | The unit list excludes in-repair and on-loan units (R2); a type outside the request is refused with the same message (R3) | N1, N2, N3 |
| One unit per type per request | Refused while a unit of that type is outstanding; allowed again after its return (R4) | N4 |
| Required fields / validation gaps | Native `required`; return-by and collector still not checked (no silent behaviour change) | N5 |
| Inventory availability | Derived status and the four filters; filter choice saved | 1.3, 2.5, 3.6, F1 |
| Loan records | Slip numbering max+1; fields `{num, req, asset, who, due, back}`; success notices unchanged | 1.4–1.6 |
| Returns | One click, same first sentence of the notice (a kit sentence is added; see §8), `back: true`, unit back on the shelf; already-returned slips cannot be re-closed | 2.3, 3.5, N7 |
| All slips history | Every slip, newest first, Returned badge | F2, AC10 |
| Shift progression | Three phases, banner text, button labels, button hidden at phase 2, Kabir's desk book entry from phase 1 | 2.1, 3.1 |
| Desk book | Seeded messages, handover notes (required, ≤ 400 characters, labelled with the phase time) | 2.6 |
| localStorage | Key `campus-stores.shift.v1`, `version: 1`, same state shape, `restore()` validation; old saved shifts load and render with the new view | P1, AC12 |
| Restart sample shift | Restores `original()` exactly | P4 |
| Layout and themes | Light/dark tokens, container-query breakpoints, coarse-pointer 44 px targets | AC13 |

## 5. Validation strategy

1. **Same driver, same choices.** Re-run the baseline script method (Chrome with a fresh profile, real clicks and keypresses, read-only checks) with the identical sequence: RQ-214; PR-04, SP-02, AD-12; Kabir Sen; Fri 8 pm; returns L-402 and L-403 at 7:30 pm; L-404 at 9:00 am, including the same handover note. Save screenshots to `docs/screenshots/after/`, numbered to match the baseline ones.
2. **Before/after measures.** Report these in a results table:

   | Measure | Baseline | Target |
   |---|---|---|
   | View changes at Sat 9:00 am before closing the adapter slip | 3 (4 tab clicks) | ≤ 1 |
   | Register names the adapter (main run / V1) | No / No | Yes / Yes |
   | Overdue visible for L-404 at Sat 9:00 am | No | Yes |
   | Missing-item visibility at pickup (adapter not issued) | None | "Not issued" row |
   | Clicks to take the 7:30 pm partial return | 2 | 2 (no regression) |
   | Issue clicks/keys for 3 slips | 18 + 28 | 18 + 28 (unchanged by design) |

3. **Variants.** Run V1 (no note) and the AC2 "missing adapter" variant.
4. **Regression.** Re-run N1–N7, F1–F2 and P1–P4 unchanged. Compare saved JSON key sets with baseline.
5. **Real-counter signal** (beyond this exercise): when someone says "I have the Film Society adapter", record whether staff go **straight to the register** or open Inventory or the Desk book first, and how long it takes to close the right slip. A wrong-slip closure would also be a signal.

## 6. Limitations and trade-offs

- **The pickup still needs three form passes** (F2 is not addressed). The design only makes an incomplete kit **visible**. A one-pass kit issue is the natural follow-up.
- **Who actually holds an item** (Leela, not Kabir) is still recorded only in the Desk book. Adding a "current holder" field would change the data model and save format, which is out of scope.
- **Overdue uses a fixed lookup** of the simulated clock and the four due labels. A real system needs real timestamps. Labels outside the lookup never show Overdue.
- **Longer list.** Back and Not-issued rows make Outstanding longer: RQ-214 takes 3 rows instead of 1 on Saturday. Mitigated by muted Back rows and ordering Out first.
- **"Not issued" can be intentional.** A club might decline an approved item. The tag is neutral wording, not an error, and does not block anything.
- **One unit per type is assumed by the display.** This matches R4 today; requests with quantities would need a count per type.
- **Returns remain irreversible** (F3). The clearer labels lower the chance of a mis-click but don't remove it.
- **Requests with no slips** (e.g. RQ-217 on Friday) do not appear in Outstanding. They are still visible in Requests.

## 7. Assumptions

1. Desk staff and borrowers identify equipment **by type and job**, not by asset ID. This is inferred from the scenario's own wording ("projector and speaker", "an adapter") and has not been observed at a real counter.
2. The **request** is the unit of work that staff reason about at return and handover time.
3. The desk clock phases are the right "now" for overdue checks in this simulation.
4. Grouping is acceptable in the Outstanding scope. The flat per-slip history remains available under All slips for anyone who wants a slip-by-slip view.
5. Changing the presentation of Outstanding does not break any reviewer expectation tied to the original flat list. All business rules and stored data are unchanged.

## 8. Implementation notes: how the build differs from the proposal

All of these were validated in [VALIDATION.md](VALIDATION.md).

| Area | Proposal | As built | Why |
|---|---|---|---|
| Return notice | "Same notice text" | The original sentence is kept word for word, then one sentence is added: "RQ-214 still has 1 item out." or "Everything issued on RQ-214 is back." | Gives feedback about the whole kit after each return. The first sentence is unchanged, so nothing that reads it breaks. |
| Summary order | "1 out · 2 back · 1 not issued" | out · not issued · back, omitting zero counts | Matches the row order inside the group (Out, Not issued, Back). |
| Explanatory line | — | One line above the groups: "Grouped by approved request. Each approved item shows whether it is out, back or not yet issued." | Explains the new layout and the "Not issued" state the first time it is seen. |
| Not issued row | Tag only | Tag plus the sub-line "Approved on RQ-xxx · no unit issued" | Makes clear the item is approved but not yet issued, so it doesn't read as an error. |
| Record return label | Visible text "Record return" | Visible text unchanged, plus an `aria-label` such as "Record return of AD-12 USB-C → HDMI adapter, slip L-404" | Several identical buttons now sit close together; this tells screen-reader users which one they are on. |
| Defensive grouping | Not specified | If saved data contains a slip whose type is not on its request, or several open slips of one type, each is still shown as its own Out row. None is ever hidden. | `restore()` does not check these cases, so an outstanding loan must never disappear from the view. The UI cannot create such data. |
| Files | `app.js`, `styles.css` | `app.js` (+124 / −6 lines) and `styles.css` (+53 lines); `index.html` unchanged | As planned |
