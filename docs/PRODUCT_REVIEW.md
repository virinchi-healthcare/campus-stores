# Campus Stores: Product Review and Prototype Handover

**Product Engineer practical · Branch `campus-stores-improvement`**

This document summarises the work for the review panel. The supporting evidence is in:

- [PROJECT_AUDIT.md](PROJECT_AUDIT.md): how the app works.
- [BASELINE_TESTING.md](BASELINE_TESTING.md): the original shift.
- [PRODUCT_CRITIQUE.md](PRODUCT_CRITIQUE.md): prioritisation.
- [PRODUCT_DECISION.md](PRODUCT_DECISION.md): design and acceptance criteria.
- [VALIDATION.md](VALIDATION.md): the repeated shift.

> **Evidence status.** Every result here comes from working through the fictional sample shift in a browser, driven by a script that sends real clicks and keypresses. Input counts are measured; task times are not. **No real-counter research has been done.** §5 is a plan for it, not a finding.

---

## 1. Product critique

**Product.** Campus Stores is an offline web app for a campus media-equipment desk. Staff issue serialised units against approved club requests, record returns, check shelf availability, and pass notes between shifts.

**User.** A Student Activities Office desk employee working the counter. Sometimes they handle a job they didn't start: the morning shift closes loans the evening shift took.

**Shift tested.** Film Society request **RQ-214** (HDMI projector, Portable speaker, USB-C → HDMI adapter; return by Fri 8 pm), collected by **Kabir Sen**:

- **Fri 3:45 pm:** issue **PR-04**, **SP-02** and **AD-12** on slips **L-402**, **L-403** and **L-404**.
- **Fri 7:30 pm:** Kabir returns the projector and speaker.
- **Sat 9:00 am:** Leela Das brings back the adapter.

### Observed strengths (kept unchanged)

1. **Ineligible units cannot be chosen.** The issue form never offered MI-09 (on loan) or PR-06 (in repair). An issued unit dropped out of the list straight away (baseline N1, N2). The mistake is prevented, not just reported.
2. **Request rules are enforced when equipment leaves.** A camera on RQ-214 and a second adapter on RQ-214 were both refused with specific messages, and the selections were kept (N3, N4).
3. **One slip per unit makes partial returns trivial.** Two clicks closed exactly L-402 and L-403, while L-404 stayed open. Inventory, being derived from the slips, updated at once (step 2.3).

### Friction selected: the Loan register could not say what was still out from a job

At **Saturday 9:00 am**, Leela walks in with "an adapter". The register showed:

```
L-404 · AD-12                              [Record return]
RQ-214 · Kabir Sen · Due Fri 8 pm
L-401 · MI-09                              [Record return]
RQ-209 · Tara Shah · Due Sat 10 am
```

Evidence from the original shift:

- **No equipment names.** "Adapter" maps to "AD-12" only by going to Inventory. Linking Leela's adapter to its slip took **4 tab clicks: 3 view changes plus an Inventory filter change** (step 3.3–3.5; [screenshot](screenshots/baseline/20-phase2-register-outstanding.png)).
- **No overdue signal.** "Due Fri 8 pm" was displayed on Saturday morning with no warning.
- **No view of the job.** Nothing showed that RQ-214's projector and speaker were already back.
- **Dependence on a free-text note.** In a run with no handover note, the register text contained **neither "adapter" nor "Leela" nor "overdue"** (variant V1, checked programmatically; [screenshot](screenshots/baseline/V1-morning-register-no-note.png)).
- **Pickup had a related gap.** Nothing confirmed that RQ-214's kit was complete before Kabir left (step 1.6).

### Why this was prioritised

Four friction points were scored on impact, frequency, effort, mistake risk and ease ([critique §3](PRODUCT_CRITIQUE.md#3-prioritisation)). This one scored **28/35**, ahead of one-pass kit issue (24), undoable returns (21) and validation feedback (18).

- It is the gap the brief names: "leave the next shift enough information to finish the job".
- It shows up in two of the three phases.
- It can be fixed without touching any business rule.

The scores are judgements based on one simulated shift. F1 and F2 are close: F2 would rank higher only if Ease were dropped **and** effort were weighted twice.

## 2. Product decision

**Problem.** Staff talk about equipment by name and by job ("the Film Society's adapter"). The register showed IDs as separate slips, with no sense of lateness. The incoming shift had to piece the answer together from three views and a handwritten note.

**Solution: "kit by request".** The Loan register's **Outstanding** scope now groups slips under their approved request.

- Each group lists **every approved item** as **Out** (with the unit, model, bin, slip, collector, due date and Record return), **Back** or **Not issued**.
- A summary line, e.g. "1 out · 2 back", sits on each group.
- An **Overdue** tag appears when the desk clock is past a slip's return-by time. Overdue groups are listed first.

**Why this solution.**

- One display change helps all three phases:
  - at pickup it shows a missing item;
  - at 7:30 pm the rows match Kabir's words;
  - on Saturday it names the adapter and flags it overdue.
- It is **derived entirely from existing data**: no new stored fields, no rule changes, the same save format. The risk to what already works is therefore lowest of all the options.
- A one-pass issue form (F2) would save more clicks at pickup, but it would rewrite the code path where every business rule lives.

**Design decisions.**

- Group by **request**, because that is the unit of work that staff and clubs talk about.
- Name items by **type first**, then the unit ID, because people say "projector", not "PR-04".
- Show **Back** and **Not issued** items, so the whole kit is visible, not just what is missing.
- State is always shown **in words**, never by colour alone.
- **All slips** stays a flat chronological history, with only the type added to each row.
- The return notice keeps its original sentence and adds kit progress, e.g. "Everything issued on RQ-214 is back."
- Each Record return button carries an accessible name that includes the unit and slip.

**Preserved on purpose:**

- request approvals and the issue form;
- eligibility rules (no repair or on-loan units, approved types only, one unit per type per request);
- per-unit slips and numbering;
- the return action;
- derived inventory status and its filters;
- the Desk book;
- the three-phase timeline;
- the localStorage key `campus-stores.shift.v1` and its data shape;
- Restart;
- the light/dark themes and responsive layouts.

**Trade-offs and limitations.**

- Pickup still takes 3 passes through the form.
- Returns remain one click and cannot be undone.
- Overdue uses a fixed lookup of the simulated times.
- Who actually holds an item (Leela) is still recorded only in the Desk book.
- Back and Not-issued rows make the list longer.
- "Not issued" may be intentional when a club declines an item, so the tag is worded neutrally.

## 3. Prototype

**What was implemented.** The kit-by-request Outstanding view, Overdue tags, item names in All slips, the extended return notice, and accessible names on the return buttons. Implementation differences from the proposal are listed in [PRODUCT_DECISION.md §8](PRODUCT_DECISION.md#8-implementation-notes-how-the-build-differs-from-the-proposal).

**Files modified** (no new dependencies, no build step, still runs offline):

| File | Change |
|---|---|
| `app.js` (+124 / −6) | `register()`: Outstanding renders request groups; All slips rows gain the type. New read-only helpers `kits()`, `kitHtml()`, `late()`, plus the `deskAt` / `dueAt` lookups. The return notice gains a kit sentence. |
| `styles.css` (+53) | Warning tag tokens for light and dark, kit group styling, and a single-column stack at ≤ 420 px |
| `index.html` | Unchanged |

**Screens affected.**

- **Loan register → Outstanding**: new grouped layout.
- **Loan register → All slips**: equipment type added to each label.
- **Status bar**: return notices.

Requests, Inventory, Desk book, the issue form, the timeline and Restart are unchanged.

**Changed user journey (same shift):**

| Moment | Before | After |
|---|---|---|
| Fri 3:45 pm | 3 slips issued; nothing confirms the kit is complete | RQ-214 shows "2 out · 1 not issued" until the adapter is issued, then "3 out" |
| Fri 7:30 pm | Match "projector and speaker" to PR-04 / SP-02 by ID | Click Record return on the rows named "HDMI projector" and "Portable speaker" → "1 out · 2 back" |
| Sat 9:00 am | Desk book → Register → Inventory → Register (3 view changes), then return | Desk book → Register (1 view change). The adapter row is named and Overdue; click Record return |

**Run locally:**

```sh
cd campus-stores
python -m http.server 5500 --bind 127.0.0.1   # or: python3 -m http.server 5500
# open http://localhost:5500 and click "Restart sample shift"
```

Opening `index.html` directly also works. Saved progress is per origin, so `file://`, `:5500` and `:8000` each keep their own shift.

## 4. Validation summary

Full detail is in [VALIDATION.md](VALIDATION.md). **64 automated checks, 64 passed.**

- **Same workflow repeated.** RQ-214; PR-04, SP-02, AD-12; Kabir Sen; Fri 8 pm; the same handover note; L-402 and L-403 returned at 7:30 pm, L-404 at 9:00 am. The final saved loans are identical to the baseline.
- **Original functional tests.** All pass: eligibility N1–N3, one-per-type N4, form rules N5–N6, return N7, filters, persistence P1–P3, Restart P4, request content, Desk book.
- **Saved data.** A shift saved by the **original** app loads and continues in the new one, and the reverse also works (O1). No migration was needed.
- **Acceptance criteria.** AC1–AC14 all pass. That includes the no-note variant (AC9), keyboard-only return (K1), and desktop/mobile in both themes with contrast ≥ 5.68:1 (AC13).

**Before and after (measured with the same driver):**

| Criterion | Original | Improved |
|---|---|---|
| Sat 9:00 am input, Desk book → adapter slip closed | 6 clicks + 3 keys | 3 clicks + 0 keys |
| View changes before closing the adapter slip | 3 + filter change | 1 |
| Register names the adapter / flags it overdue | No / No | Yes / Yes |
| Same, with no handover note | No / No | Yes / Yes |
| Incomplete kit visible at pickup | No | Yes ("Not issued") |
| Issue 3 units | 18 clicks + 28 keys | Unchanged |
| Partial return | 2 clicks | 2 clicks |

Human task time and wrong-slip rates were **not measured**.

**Bugs.** No product defects were found during validation. One earlier measurement was corrected: the baseline's "4 view switches" were really 4 tab clicks and 3 view changes.

**Remaining limitations.**

- Pickup effort is unchanged.
- Returns cannot be undone.
- Focus goes to the page body after a keyboard return (pre-existing).
- Overdue is based on the simulated clock.
- Not tested: Firefox, Safari, real devices, screen readers, real users.

## 5. Real-counter observation plan

**Purpose.** Find out whether the register change helps at a real desk. Prototype results (§4) show that the information is now on screen. They do not show that staff use it, or that it saves time or prevents mistakes.

**Key observation.** When someone says "I'm returning the Film Society's adapter", does the employee go **straight to the Loan register and close the right slip**, without opening Inventory or the Desk book? How long does it take from the request being said to the slip being closed?

### Setup

- One desk, both shift changes. A **two-week period on the original register** first, then two weeks on the new one, with the same staff where possible. If the desk can run both versions, alternate weeks instead.
- One observer at the counter with a tally sheet, plus the app's own records. No screen recording without consent.
- Focus on the **riskiest transactions**:
  - returns handled by someone other than the person who issued;
  - returns brought by someone other than the collector;
  - partial returns;
  - the first 30 minutes of a shift.

### What to observe and timestamp (per return transaction)

| Field | Recorded |
|---|---|
| t0 | Returner states what they have ("adapter", "Film Society stuff", a request number…) |
| t1 | Employee first looks at or touches the app |
| t2 | Employee selects the slip to close (clicks Record return) |
| t3 | Item physically shelved / transaction ended |
| Context | Same employee who issued? Returner = collector? Was a handover note written? Item overdue? |
| Path | Views opened between t1 and t2 (Register, Inventory, Desk book, Requests), in order |
| Checks | Did the employee read the serial label on the unit? Did they ask the returner or a colleague anything? |

### What to count

- **Wrong-slip closures.** Reconcile each day against a physical shelf check: is anything "On shelf" in the app but missing, or the reverse? Count slips that had to be corrected.
- **Detours.** Opening Inventory or the Desk book during a return; questions to colleagues; "I'll come back to it" deferrals.
- **Overdue awareness.** Overdue items spotted by the incoming shift in its first 30 minutes, compared with those found later or by the club.
- **Incomplete kits at pickup.** Items approved but not issued that the club reports missing after leaving.
- **Repeated actions.** Toggling Outstanding / All slips more than once, or re-opening the same view.

### Questions for desk staff (end of shift, 5 minutes)

1. Think of the last return you took for a loan you didn't issue. How did you find the right slip?
2. Did you need the Desk book or Inventory to do it? Why?
3. Was anything on the register confusing: "Not issued", "Back", "Overdue", or the order of the groups?
4. Did you trust "Back" or "Overdue" without checking the shelf? Should you have?
5. Did you write a shorter handover note, or none, because the register already showed the situation?
6. What did you still have to ask the returner?

### What would indicate improvement

These are **targets to test, not results**:

- A lower median t0 → t2 for returns of loans the employee didn't issue.
- A higher share of those returns closed **without opening another view**.
- **No increase** in wrong-slip closures. Ideally fewer, though the sample may be too small to show it.
- More overdue items noticed at the start of the shift.
- Fewer "missing item" callbacks after pickup.

### Unexpected consequences to watch for

- **Trusting the screen over the item.** Staff close a slip by type ("an adapter") without checking the serial when two units of that type are out on different requests.
- **Thinner handover notes.** The register now looks complete, so information that exists only in the Desk book, such as *who* holds the item, may get lost.
- **"Not issued" read as an error.** Staff delay a pickup or issue items the club declined.
- **Overdue fatigue or friction.** Many overdue tags get ignored, or lead to awkward exchanges at the counter.
- **Longer lists.** On busy days, more groups and rows mean more scrolling, which could slow down simple single-item returns.

## Document map

| Document | Purpose |
|---|---|
| [PROJECT_AUDIT.md](PROJECT_AUDIT.md) | Architecture, data model, rules, persistence, how to run |
| [BASELINE_TESTING.md](BASELINE_TESTING.md) | The original shift, step by step, with negative tests and screenshots |
| [PRODUCT_CRITIQUE.md](PRODUCT_CRITIQUE.md) | Strengths, friction points, scoring, recommendation |
| [PRODUCT_DECISION.md](PRODUCT_DECISION.md) | Design, wireframes, acceptance criteria, preservation list, implementation notes |
| [VALIDATION.md](VALIDATION.md) | The repeated shift, all test results, before/after comparison |
| [DEMO_SCRIPT.md](DEMO_SCRIPT.md) | 4–5 minute walkthrough for reviewers |
| [validation-harness/](validation-harness/) | Scripts and raw results behind the evidence |
