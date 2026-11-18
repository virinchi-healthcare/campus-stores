# Campus Stores: Baseline Testing (original product, no code changes)

Role played: the Student Activities Office equipment desk employee working the sample shift.
Date: 2026-11-19 · App: http://localhost:5500. A `python -m http.server 5500` process served the repo, and the files it served were byte-identical to the repo.

## Test method and honesty notes

- **Browser.** Google Chrome 158, headless, run with a **fresh, isolated profile**, so localStorage started empty. Viewport 1280×900. The OS reported a dark colour scheme, so screenshots are in the dark theme. One light-theme capture is included (`25`).
- **How it was driven.** This session had no interactive browser tool, so Chrome was controlled over the DevTools protocol by a small Python standard-library script. Nothing was installed.
  - **All interactions were synthetic user input:** mouse clicks at element centres, and arrow/Enter keypresses to pick options in native `<select>`s.
  - **JavaScript was used read-only:** to locate elements, read visible text, and read (never write) `localStorage` so results could be verified.
  - App state was never set directly, and no business rule was bypassed.
- **Input counts.** Counts below are measured from the input events actually sent. Selects were operated with the keyboard. A mouse user needs 2 clicks per select (open, pick). Mouse-equivalent counts are labelled as derived.
- **What these findings are.** Observations come from one tester working through a fictional scenario. They are not data from a real counter.

Screenshots: [`docs/screenshots/baseline/`](screenshots/baseline/).

---

## Part 1: Main sample shift

### Stage 1: Friday 3:45 pm, pickup

| # | Goal | Interaction | What the app did | As expected? | Friction / notes | Evidence |
|---|---|---|---|---|---|---|
| 1.1 | Start clean | Loaded the page (storage empty), clicked **Restart sample shift** | Requests view, Friday · 3:45 pm, banner "Pickup at the counter". Saved state: phase 0, one loan (L-401 MI-09). | Yes | — | `01`, `02` |
| 1.2 | Understand the requests | **View form** on RQ-214, RQ-209 and RQ-217, then **Back to list** each time | Each form shows the club, owner, "Return by", the approved equipment list and a note. RQ-214: projector, speaker, USB-C → HDMI adapter; return by Fri 8 pm; "Playback is from a USB-C-only laptop." | Yes | Clear. A detail view needs a "Back to list" click before opening the next one. | `03-request-*` |
| 1.3 | Check stock | Inventory, then the **Show** filter: On shelf / On loan / In repair / All items | All 8 units with model and bin. On shelf: PR-04, SP-02, SP-05, AD-12, AD-15, CA-03. On loan: MI-09. In repair: PR-06. | Yes | The filter works, and the selection is remembered. | `04`, `05-*` |
| 1.4 | Issue the Film Society kit to Kabir | Loan register → **New issue slip** → Approved request "RQ-214 · Film Society" → Unit "PR-04 · HDMI projector" → Collected by "Kabir Sen" → Return by "Fri 8 pm" → **Save issue slip** | Status: "Issued PR-04 to Kabir Sen on slip L-402." The form closed. | Yes | The form does not show what RQ-214 approved. The unit list offers all 6 on-shelf units, including CA-03 (camera), whatever request is chosen. "Return by" is not pre-filled from the request. | `07`, `08` |
| 1.5 | Issue the speaker | Same 6 steps again: RQ-214, SP-02, Kabir Sen, Fri 8 pm | "Issued SP-02 to Kabir Sen on slip L-403." | Yes | Had to re-select the request, collector and return-by date. | — |
| 1.6 | Issue the adapter | Same 6 steps again: RQ-214, AD-12, Kabir Sen, Fri 8 pm | "Issued AD-12 to Kabir Sen on slip L-404." | Yes | Same repetition. **Nothing told me the kit was complete.** I had to remember the adapter from the request form myself. | `09` |
| 1.7 | Verify the slips | Register (Outstanding, then All slips) | L-404 · AD-12, L-403 · SP-02, L-402 · PR-04, L-401 · MI-09, each "RQ-xxx · person · Due …" with **Record return**. localStorage held all 4 loans with the correct fields. | Yes | **Rows show only the asset ID**, with no equipment type or model. Slips for one request are separate rows with nothing grouping them. | `09` |
| 1.8 | Verify stock | Inventory | PR-04, SP-02 and AD-12 changed to On loan. SP-05 and AD-15 still On shelf. | Yes | — | `10` |
| 1.9 | Read the desk book | Desk book | Isha (3:20 pm): "Kabir Sen is picking up our whole screening kit. Please issue it in his name." Tara (3:30 pm): the mic stays with her overnight. | Yes | The instruction to issue in Kabir's name lives only in the desk book, not on the request or the issue form. Reading it in this order (as scripted) meant reading it *after* issuing. | `11` |

**Stage 1 effort (measured):** 3 complete passes through the issue form for one request.

- Measured input: **18 clicks + 28 keypresses**.
- Derived mouse equivalent: about **30 clicks**, i.e. 1 + 4×2 + 1 per slip.
- The request, collector and return-by date were each chosen 3 times. That is **9 selections where 3 carry new information**.

### Stage 2: Friday 7:30 pm, partial return

| # | Goal | Interaction | What the app did | As expected? | Friction / notes | Evidence |
|---|---|---|---|---|---|---|
| 2.1 | Move time | **Move to return time** | Clock: Friday · 7:30 pm. Banner: "The kit comes back in pieces … Leela still has the adapter." Status: "Shift time updated." Button now reads "Move to next morning". | Yes | **The loan register was unchanged by the time change.** | `12` |
| 2.2 | See what changed | Desk book | New entry from Kabir Sen at 7:30 pm: "I brought the projector and speaker. Leela Das has our adapter. She'll be at the counter at 9 am tomorrow." | Yes | — | `13` |
| 2.3 | Take back the projector and speaker | Register → **Record return** on L-402 · PR-04, then on L-403 · SP-02 | "PR-04 returned to stock. Slip L-402 closed." then "SP-02 returned to stock. Slip L-403 closed." Outstanding now shows L-404 · AD-12 and L-401 · MI-09. | Yes (2 clicks) | Kabir said "projector and speaker", but the rows say "PR-04" and "SP-02". I matched them because I had issued them myself. Each return is **one click with no confirmation and no undo**, beside two other identical "Record return" buttons. | `14` |
| 2.4 | Check history | **All slips** | L-402 and L-403 show "Returned". L-404 and L-401 still show Record return. | Yes | No time or name recorded for the return. | `15` |
| 2.5 | Check stock | Inventory | PR-04 and SP-02 On shelf. AD-12 and MI-09 On loan. | Yes | — | `16` |
| 2.6 | Hand over to the morning shift | Desk book → typed a 190-character note → **Add handover note** | "Handover note saved." Entry "Friday · 7:30 pm · Counter handover" at the top. Saved as `{phase:1, text}`. | Yes | I had to re-type the unit IDs (PR-04, SP-02, AD-12), the slip number (L-404) and who holds the adapter. The note is free text with no link to the slip, so how useful it is depends entirely on what the writer types. | `17` |

Note typed: *"RQ-214 Film Society: projector PR-04 and speaker SP-02 returned 7:30 pm. Adapter AD-12 (slip L-404) still out - Leela Das has it and will bring it at 9 am Sat. Slip is in Kabir Sen's name."*

### Stage 3: Saturday 9:00 am, morning handover

| # | Goal | Interaction | What the app did | As expected? | Friction / notes | Evidence |
|---|---|---|---|---|---|---|
| 3.1 | Start the morning | **Move to next morning** | Clock: Saturday · 9:00 am. Banner: "Leela walks in with an adapter. Work out what was outstanding from the screening and close the loan for the right item." The advance button is now hidden. | Yes | — | `18` |
| 3.2 | Learn the situation | Desk book | Newest first: my handover note, Kabir's 7:30 pm message, Tara, Isha. | Yes | The useful context is here, but only because of the note I wrote in 2.6. | `19` |
| 3.3 | Find the screening's outstanding loan | Loan register (Outstanding) | **L-404 · AD-12, "RQ-214 · Kabir Sen · Due Fri 8 pm"**, and L-401 · MI-09, "RQ-209 · Tara Shah · Due Sat 10 am". | Partly | The row does not say "adapter", does not mention Leela, and **does not flag that "Due Fri 8 pm" has passed**. The register cannot tell me that the projector and speaker for RQ-214 are already back. | `20` |
| 3.4 | Confirm AD-12 is the adapter | Inventory → Show **On loan** | AD-12 · USB-C → HDMI adapter (Belkin AVC002 · C4); MI-09 · Wireless microphone. | Yes | An extra trip to another view just to turn an ID into a name. | `21` |
| 3.5 | Close the right loan | Back to the Loan register → **Record return** on L-404 | "AD-12 returned to stock. Slip L-404 closed." Outstanding shows only L-401 · MI-09. | Yes | — | `22` |
| 3.6 | Verify the final state | **All slips**, then Inventory (All items) | L-402, L-403 and L-404 Returned; L-401 open. Every unit On shelf except PR-06 (In repair) and MI-09 (On loan). | Yes | — | `23`, `24` |

**Stage 3 effort (measured):** before I could press Record return I made **4 tab clicks** (Desk book → Loan register → Inventory with filter → Loan register): 5 clicks + 3 keypresses.

*Correction made during validation:* the first of those tab clicks re-selected the Desk book, which was already open after advancing. So there were **3 actual view changes** (to the Register, to Inventory, back to the Register) plus one change to the Inventory filter.

**Final saved state (verified):** phase 2; loans 401 open and 402, 403, 404 returned; one note.

### Variant V1: morning view **without** a handover note

Purpose: see what the system tells the incoming employee when the evening shift writes nothing. I ran the same Stage 1–2 actions on a separate clean run, with no note.

- **Register (Outstanding) at Sat 9:00 am:** "L-404 · AD-12, RQ-214 · Kabir Sen · Due Fri 8 pm" and "L-401 · MI-09".
  - The register text contains **no "adapter", no "Leela" and no "overdue"** (checked programmatically).
  - Screenshot: `V1-morning-register-no-note`.
- **Desk book:** only Kabir's message ("Leela Das has our adapter"). The employee has to link "adapter" to AD-12 to L-404 by themselves, using Inventory.
  - Screenshot: `V1-morning-deskbook-no-note`.

---

## Part 2: Additional validation (each test started from **Restart sample shift**)

| ID | Test | Steps | Result | Verdict |
|---|---|---|---|---|
| N1 | A unit on loan cannot be issued again | Open the issue form at the start. Then issue PR-04 to RQ-214 and open the form again. | MI-09 (on loan) is not in the unit list. After issuing, PR-04 disappears from the list. Picking RQ-209 does not change the unit list. | **Pass.** The rule works by leaving units out, not by showing a message. `N1` |
| N2 | A unit in repair cannot be issued | Open the issue form; Inventory → In repair | PR-06 is never offered. Inventory shows it "In repair" at bin "Workshop". | **Pass.** `N2` |
| N3 | A type outside the request is blocked | RQ-214 + CA-03 + Kabir + Fri 8 pm → Save. Then RQ-217 + PR-04 → Save. Then RQ-217 + CA-03 + Dev + Sat noon → Save. | Each of the first two gives "This equipment type is outside the approved request. Choose an approved unit." No slip is created, and the form stays open with the selections kept. The third creates L-402. | **Pass.** The error shows only in the small footer status bar, far from the Save button, and stays visible until the next click action. `N3` |
| N4 | One unit per type per request | RQ-214 + AD-12 saved, then RQ-214 + AD-15. Then SP-02 saved, then SP-05. Then return AD-12 and retry AD-15. | AD-15 and SP-05 are refused: "The approved quantity of this equipment type is already on loan." Once AD-12 is returned, AD-15 issues (L-404). | **Pass.** The limit counts outstanding units only. `N4` |
| N5 | Other form inputs | Save with all fields empty; then RQ-214 + PR-04 + **Dev Menon** + **Sat noon** | The empty form does not submit (native `required`, `checkValidity()` = false, no slip created). The second issue **succeeds** even though RQ-214's return-by is Fri 8 pm and Dev is not linked to the Film Society. | Rules as coded. **Gap:** the return date and collector are not checked against the request. `N5` |
| N6 | Leave the form mid-issue | Chose a request and collector, clicked **Requests**, came back to the register | The form had closed and the selections were lost. | Friction: you cannot glance at Requests or Inventory while issuing. |
| N7 | Mistaken return | At the start, clicked **Record return** on L-401 | It closes at once: "MI-09 returned to stock." Outstanding shows "No outstanding slips." All slips shows Returned, and there is no Undo or Reopen. | Works as coded. **Risk:** a mistaken click cannot be reversed short of Restart. `N7` |
| F1 | Inventory filters | All four options (Stage 1.3 and 3.4) | Correct subsets each time. | **Pass** |
| F2 | Register filters | Outstanding / All slips (Stages 1.7, 2.4, 3.6) | Outstanding hides returned slips; All slips shows them as "Returned". Newest first. | **Pass** |
| P1 | Refresh mid-shift | Phase 1, 1 issue, 1 note, inventory filter On loan, register All slips, RQ-214 open → reload | Saved state before and after the reload is **identical**, and the rendered text is identical too (clock, open request, filter, scope and note all kept). | **Pass** `P1` |
| P2 | Refresh with a half-filled form | Picked a request and collector → reload | The form reopens, but **empty**. | Partial: the selections are lost. `P2` |
| P3 | Message after refresh | Triggered the N3 error → reload | The status bar showed the stale earlier notice "Handover note saved." instead. | Minor: the status bar can show an out-of-date message. |
| P4 | Restart | From phase 2 with 2 loans and 1 note, clicked **Restart sample shift** | No confirmation. Back to phase 0, tab Requests, filter All items, Outstanding, loans = [L-401], notes = []. The reset survives a reload. | **Pass** (no confirmation) `P4` |

## Browser errors and limitations

- **Console:** the only error was `404 http://localhost:5500/favicon.ico`, once per page load (confirmed from the network events). There were no JavaScript exceptions or warnings.
- **Headless Chrome only.** Firefox, Safari, real mobile devices and screen readers were not tested. The light theme was checked with a single screenshot (`25`).
- **Measured counts reflect keyboard selection** in an automated driver. Real people would also spend time reading and deciding, which was not measured.
- **The timeline cannot be reversed,** so each stage depends on the earlier stages being replayed.

## Summary

**Worked well**
- Every business rule in the brief held (N1–N4). Ineligible units are never offered, and the two type and quantity errors are clear.
- One slip per unit made the partial return trivial: two clicks closed exactly the projector and speaker slips, and the adapter stayed open.
- Inventory status is always consistent with the register, because it is derived from the slips.
- Persistence is exact across refreshes, and Restart is reliable.
- The desk book gave the human context: who collects, and who has the adapter.

**Felt unnecessarily difficult**
1. **Morning handover (Stage 3).** The register lists "L-404 · AD-12" with no type, no sign that it is overdue, and no view of what else from RQ-214 is out or back. Linking "Leela's adapter" to the slip took 4 tab clicks (3 view changes plus an Inventory filter change). Without a handover note, the register never mentions the adapter at all (V1).
2. **Pickup (Stage 1).** Three full passes through the form for one request (about 30 mouse clicks), re-entering the same request, collector and date. The form never shows what the request approved or whether the kit is complete.
3. **Returns cannot be undone,** and there is no confirmation (N7).
4. **Errors appear in the footer only,** and the return date and collector are not checked against the request (N3, N5).
