# Campus Stores: Post-implementation Validation

Feature under test: **"Kit by request" in the Loan register (Outstanding scope)**, as specified in [PRODUCT_DECISION.md](PRODUCT_DECISION.md).
Compared against: [BASELINE_TESTING.md](BASELINE_TESTING.md) (the original product).
Date: 2026-11-19 · Branch `campus-stores-improvement` · Modified files: `app.js`, `styles.css`.

## Method

- **Environment:** the same as baseline. Chrome 158 headless with a **fresh profile**, served at `http://localhost:5500`. Before testing I confirmed that the served `app.js` was byte-identical to the edited file.
- **Driver:** the same stdlib DevTools driver as baseline. It sends real clicks and keypresses. JavaScript is used read-only, to read text, `localStorage` and layout. It never writes app state.
- **Reproducible:** scripts and raw results are in [`validation-harness/`](validation-harness/).
- **Result:** **64 automated checks, 64 passed** (`results/r_main.json` 36, `r_reg.json` 20, `r_layout.json` 4, `r_extra.json` 4).
- **Screenshots:** [`screenshots/after/`](screenshots/after/). Baseline screenshots are in [`screenshots/baseline/`](screenshots/baseline/).
- **Limits of these results:**
  - The effort figures are input counts from an automated driver. They are **not human task times**.
  - Nothing here comes from a real counter.

---

## 1. Exact repeated scenario

These are the same steps, choices and order as the baseline. Nothing was simplified.

| Phase | Steps (identical to baseline) |
|---|---|
| Setup | Load → **Restart sample shift** |
| Fri 3:45 pm | View forms RQ-214, RQ-209, RQ-217 → Inventory filters On shelf / On loan / In repair / All items → Loan register → **New issue slip** ×3 for RQ-214 / Kabir Sen / Fri 8 pm: **PR-04**, then **SP-02**, then **AD-12** → All slips → Inventory → Desk book |
| Fri 7:30 pm | **Move to return time** → Desk book → Loan register → **Record return** on the projector (L-402) and the speaker (L-403) → All slips → Inventory → Desk book: the **same 190-character handover note** as baseline |
| Sat 9:00 am | **Move to next morning** (lands on the Desk book, as in baseline) → Desk book → Loan register → **Record return** on the adapter (L-404) → All slips → Inventory |

The only difference in how actions were carried out: in Stages 2–3 the returns were clicked on the row **named** "HDMI projector", "Portable speaker" or "USB-C → HDMI adapter", because rows now carry the equipment name. In the baseline the rows were found by ID ("L-402 · PR-04"). Slip numbers and units are identical.

## 2. Test cases and results

### 2a. Clean state (Part A)

| ID | Check | Result |
|---|---|---|
| A1 | After Restart, the saved state equals the original seed exactly (phase 0, one loan L-401 MI-09, no notes, Requests tab) | PASS |
| A2 | Clock "Friday · 3:45 pm", banner "Pickup at the counter" | PASS |
| AC14 | Console: no JS exceptions in any run; the only 4xx is `/favicon.ico` (same as baseline) | PASS |

### 2b. Repeated workflow (Part B)

| ID | Check | Result | Evidence |
|---|---|---|---|
| B1 | All three request forms open and close | PASS | — |
| B2 | Inventory filter counts: On shelf 6 / On loan 1 / In repair 1 / All 8 (same as baseline) | PASS | — |
| B3, B4 | "Issued PR-04 … L-402", "Issued SP-02 … L-403", "Issued AD-12 … L-404" (same notices as baseline) | PASS | `03`, `04` |
| B5 | Issue effort for 3 slips = **18 clicks + 28 keypresses**, identical to baseline (the issue form was intentionally not changed) | PASS | — |
| B6 | All slips lists L-404…L-401, each with its type | PASS | — |
| B7 | Inventory: PR-04, SP-02, AD-12 On loan; SP-05 On shelf | PASS | — |
| B8, B9 | Desk book: 2 messages at 3:45 pm; Kabir's message appears at 7:30 pm | PASS | — |
| B10 | Partial return = **2 clicks** (baseline 2) | PASS | `06` |
| B11 | All slips: L-402 and L-403 "Returned" | PASS | `07` |
| B12 | Handover note saved as `{phase:1, text}` | PASS | — |
| B13 | Saturday: clock updated, advance button hidden, landed on the Desk book | PASS | `08` |
| B14, B15 | Final inventory and saved loans identical to baseline (401 open; 402, 403, 404 returned) | PASS | `12` |

### 2c. Acceptance criteria (Part C)

| AC | User action | What the app showed | Result |
|---|---|---|---|
| AC1 | Restart → Loan register | One group, "RQ-209 · Finals rehearsal · 1 out": "Wireless microphone · MI-09 · Shure BLX · bin B3 · L-401 · Tara Shah · Due Sat 10 am". No RQ-214 or RQ-217. | PASS `02` |
| AC2 | Issue PR-04 and SP-02 (the state reached naturally between slip 2 and slip 3 of the baseline issue) | RQ-214 "2 out · 1 not issued". Row: "USB-C → HDMI adapter · Approved on RQ-214 · no unit issued · **Not issued**", with no button. | PASS `03` |
| AC3 | Issue AD-12 | "3 out"; all three named; no "Not issued" | PASS `04` |
| AC4 | — (Fri 3:45 pm) | RQ-214 listed above RQ-209; no "Overdue" | PASS |
| AC5 | Move to return time | No "Overdue" at 7:30 pm | PASS `05` |
| AC6 | Record return on the projector, then the speaker | Notices: "PR-04 returned to stock. Slip L-402 closed. RQ-214 still has 2 items out." / "SP-02 … L-403 closed. RQ-214 still has 1 item out." The group shows "1 out · 2 back". Back rows have no button. Saved `back` flags are `[false, true, true, false]`. Inventory: PR-04 and SP-02 On shelf, AD-12 On loan. | PASS `06` |
| AC7 | Move to next morning → Loan register | RQ-214 is listed first, with the group tag **Overdue** and a highlighted left border. Adapter row: "USB-C → HDMI adapter / AD-12 · Belkin AVC002 · bin C4 / L-404 · Kabir Sen · Due Fri 8 pm / **Overdue** / Record return". The RQ-209 mic is **not** overdue. | PASS `09` |
| AC8 | Record return on the adapter row | "AD-12 returned to stock. Slip L-404 closed. Everything issued on RQ-214 is back." The RQ-214 group disappears; RQ-209 remains. No other view visited. | PASS `10` |
| AC9 | V1: same shift with **no handover note** | The register text contains "USB-C → HDMI adapter", "L-404" and "Overdue" (all were absent in baseline V1) | PASS `V1-morning-register-no-note` |
| AC10 | All slips | Flat history, newest first: "L-404 · AD-12 · USB-C → HDMI adapter … Returned", … ; 3 Returned, 1 Record return | PASS `11` |
| AC11 | Return the last outstanding slip (L-401) | "No outstanding slips." Notice "… Everything issued on RQ-209 is back." | PASS `13` |
| AC12 | Reload | The saved state is identical before and after. The **key sets are unchanged** (state: 10 keys; loan: `num, req, asset, who, due, back`). | PASS |
| AC13 | Desktop 1280 px and mobile 390 px, each in light and dark | No horizontal scroll (scrollWidth = innerWidth). On mobile the kit rows stack into one column and the issue form is one column. All new text has contrast ≥ 5.68:1 (table in §5). | PASS `L-*` |
| AC14 | Console | See 2a | PASS |

### 2d. Regression (Part D): each test from a clean **Restart**

| ID | Original feature or rule | Result |
|---|---|---|
| N1 | On-loan units not offered (MI-09 at the start; PR-04 after issuing) | PASS `N1` |
| N2 | In-repair PR-06 not offered | PASS |
| N3 | Type outside the request refused (RQ-214 + CA-03; RQ-217 + PR-04) with the same message; selections kept | PASS `N3` |
| N4 | Second adapter (AD-15) and second speaker (SP-05) on RQ-214 refused; AD-15 allowed once AD-12 is returned | PASS `N4` |
| N4b | *New view:* after the return and re-issue, the adapter row shows **AD-15 Out**, and the returned AD-12 is not shown as a second row | PASS |
| N5 | Empty submit blocked; return-by and collector still unchecked (unchanged rule) | PASS |
| N6 | Changing tab discards a half-filled form (unchanged) | PASS |
| N7 | Record return still closes immediately; empty state shown | PASS |
| P1 | Refresh mid-shift: saved state and rendered page identical (including the grouped view) | PASS |
| P2 | Refresh with a half-filled form reopens it empty (unchanged) | PASS |
| P3 | Validation message is temporary; after a reload the status shows the stored notice (unchanged) | PASS |
| P4 | Restart from phase 2 restores the seed and survives a reload | PASS |
| Q1, Q2 | Request detail content unchanged (RQ-214, RQ-217) | PASS |
| D1 | A whitespace-only handover note is rejected | PASS |
| K1 | Keyboard only: **Tab** reaches "Record return of AD-12 USB-C → HDMI adapter, slip L-404" (8 Tab presses from the top, visible focus outline), and **Enter** closes L-404 | PASS |
| O1 | **Compatibility:** a shift played to Saturday in the **original** app (served from git on the same origin, with the same key `campus-stores.shift.v1`) opens in the new app with no change to the saved data, shows "1 out · 2 back" and "Overdue", and can be finished there. The original app can also read the save written by the new app (O1c). **No migration was needed.** | PASS |

## 3. Before and after comparison (Part E)

**M** = measured with the same driver and the same scenario. **Q** = qualitative judgement (not measured).

| Evaluation criterion | Original product | Improved product | Type |
|---|---|---|---|
| Workflow steps: issue 3 units (Fri 3:45 pm) | 18 clicks + 28 keypresses | 18 clicks + 28 keypresses (unchanged) | M |
| Workflow steps: partial return (Fri 7:30 pm) | 2 clicks | 2 clicks | M |
| Workflow steps: morning, from landing on the Desk book to closing the adapter slip | 6 clicks + 3 keypresses (4 tab clicks, 1 filter select + 3 keys, 1 Record return) | **3 clicks + 0 keypresses** (2 tab clicks, 1 Record return) | M |
| Unnecessary navigation (Sat 9:00 am) | 3 view changes (Register → Inventory → Register) plus 1 filter change | **1 view change** (Register); Inventory not needed | M |
| Time required | Not measured. The driver has no human reading or decision time. | Not measured | — |
| Clarity: register names the outstanding equipment | No: "L-404 · AD-12" only (text check) | Yes: "USB-C → HDMI adapter" with model and bin (text check) | M |
| Clarity: register works without a handover note (V1) | No "adapter" or "overdue" in the register | "USB-C → HDMI adapter", "L-404" and "Overdue" all present | M |
| Clarity: late item flagged at Sat 9:00 am | No flag | "Overdue" on the slip and its group; the group is listed first | M |
| Clarity: incomplete kit at pickup | Not shown anywhere | "2 out · 1 not issued" plus a "Not issued" row | M |
| Feedback after a return | "AD-12 returned to stock. Slip L-404 closed." | The same text plus "Everything issued on RQ-214 is back." | M |
| Risk of incorrect action | One-click irreversible returns; rows identifiable only by ID | Still one-click and irreversible. Each button now sits under a named item, and screen readers hear the unit and slip. **Lower likelihood of picking the wrong row, but not measured.** | Q |
| User understanding (tester's judgement) | Had to remember IDs or cross-reference Inventory and the Desk book to match "projector", "speaker", "adapter" | Spoken item names match the row headings; the request's whole kit is visible in one place | Q |

## 4. Important screenshots

| State | File |
|---|---|
| Pickup, adapter not yet issued | [`03-pickup-two-of-three-not-issued.png`](screenshots/after/03-pickup-two-of-three-not-issued.png) |
| Pickup, kit complete | [`04-pickup-kit-complete.png`](screenshots/after/04-pickup-kit-complete.png) |
| After the partial return (1 out · 2 back) | [`06-return-time-after-partial-return.png`](screenshots/after/06-return-time-after-partial-return.png) |
| **Saturday: adapter named and Overdue** | [`09-morning-register-overdue-adapter.png`](screenshots/after/09-morning-register-overdue-adapter.png) |
| After closing L-404 | [`10-morning-after-adapter-return.png`](screenshots/after/10-morning-after-adapter-return.png) |
| No-note variant | [`V1-morning-register-no-note.png`](screenshots/after/V1-morning-register-no-note.png) |
| Mobile light / dark | [`L-mobile-light-morning.png`](screenshots/after/L-mobile-light-morning.png), [`L-mobile-dark-morning.png`](screenshots/after/L-mobile-dark-morning.png) |
| Desktop light | [`L-desktop-light-pickup-not-issued.png`](screenshots/after/L-desktop-light-pickup-not-issued.png), [`L-desktop-light-morning.png`](screenshots/after/L-desktop-light-morning.png) |
| Baseline equivalent of the Saturday view | [`baseline/20-phase2-register-outstanding.png`](screenshots/baseline/20-phase2-register-outstanding.png) |

## 5. Desktop and mobile verification (Part F)

| Check | Desktop 1280 dark | Desktop 1280 light | Mobile 390 dark | Mobile 390 light |
|---|---|---|---|---|
| Horizontal scroll | none | none | none | none |
| Kit rows | 2 columns (text / actions) | 2 columns | 1 column, actions below the text | 1 column |
| Issue form | 2 columns | 2 columns | 1 column; selects operated by keyboard; save worked | same |
| Nav | side column | side column | wraps into a row | wraps into a row |
| Record return height (coarse pointer emulated) | — | — | 44 px | 44 px |
| Contrast: Overdue / Not issued / Back tag / Back label / row text / summary | 8.23 / 8.42 / 9.00 / 8.24 / 8.24 / 8.24 | 6.86 / 7.55 / 5.68 / 6.22 / 6.22 / 6.22 | as desktop dark | as desktop light |

State is never shown by colour alone: every state is a word (Out count, Back, Not issued, Overdue).

## 6. Bugs found and fixed

- **No product defects were found.** Every check passed on the first full run, so no code fixes were needed after validation.
- **Correction to earlier evidence.** While I was repeating Stage 3, it turned out the baseline figure of "4 view switches" included a click on the Desk book tab that was already open. I corrected the baseline, critique and decision documents to say "4 tab clicks / 3 view changes". The comparison above uses the same counting for both versions.
- **Prevented by design (not a bug that was observed).** `restore()` does not check that a slip's type belongs to its request, or that there is only one open slip per type. The grouped view therefore lists every open slip as its own row, so an outstanding loan can never be hidden. The UI cannot create such data, so this was reasoned from the code, not seen.
- **Test-tooling problems** (not product problems): a shell quoting failure and a mangled file copy during setup. Both were fixed before any recorded run.

## 7. Remaining limitations

- **Pickup effort is unchanged** (18 clicks + 28 keys for 3 slips). F2 was deliberately not addressed.
- **Returns are still one click and irreversible** (F3). No confirmation or undo was added.
- **Focus after a keyboard return goes to the page body,** because the whole page is redrawn. The original app behaves the same way (it redraws identically). Keyboard users have to Tab back to the list.
- **Overdue uses a fixed lookup** of the simulated desk times and the four return-by labels; it does not use real time.
- **Who actually holds an item** (Leela) is still recorded only in the Desk book.
- **Not tested:**
  - Firefox, Safari, real touch devices and real screen readers (only the `aria-label` text was checked);
  - human task time;
  - any real counter.
- `favicon.ico` 404 (pre-existing).

## 8. Final assessment

**The improvement met its stated objective within the simulated shift.**
- At Saturday 9:00 am the incoming employee can identify Leela's adapter (by name, slip, unit and overdue status) and close it from the Loan register alone. That took 1 view change, down from 3 measured in the baseline.
- The same holds when no handover note was written (AC9).
- At pickup, an incomplete kit is now visible.

All original business rules, the saved data format, persistence, Restart, the three-phase timeline and the layouts behaved as before (N1–N7, P1–P4, O1, AC12–AC13).

It did **not** reduce pickup effort or make returns safer. Whether it shortens real counter interactions or prevents wrong-slip returns has not been shown. That needs the field observation described in [PRODUCT_REVIEW.md](PRODUCT_REVIEW.md#5-real-counter-observation-plan).
