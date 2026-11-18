# Decision record: Campus Stores

This records what was reviewed, what was changed, how it was checked, and what was deliberately left alone. It supports the short summary in [README.md](README.md#product-decision).

I used an AI assistant (Claude) for the code review, the prototype and the write-up, which the brief allows. The prototype is a proposed change in a fictional exercise, not a result validated at a real counter.

## 1. The job being tested

Friday 3:45 pm: issue the Film Society's kit (projector, speaker, USB-C→HDMI adapter). Friday 7:30 pm: the projector and speaker come back, but the adapter is still with Leela. Saturday 9:00 am: close the loan for the right adapter and leave the next shift enough to finish.

## 2. Review of the starting app

I read all of `index.html`, `app.js`, `styles.css` and the README before changing anything.

**What already works**
- One slip per physical unit, so a partial return leaves the other items open.
- Units in repair cannot be issued.
- Equipment outside the approved request is rejected, and so is a second unit of a type already on loan for that request.
- Output is escaped, saved state is validated on restore, and focus states and touch targets are handled.

**What is weak**

| # | Finding | Type |
|---|---|---|
| 1 | Issuing the kit needs three separate forms, each re-entering request, collector and due date. Nothing pre-fills from the request. | Workflow |
| 2 | "Leela has the adapter, back at 9 am" exists only as free text in the Desk book. The loan register shows an open slip but not who holds it or when it is promised back. | Workflow |
| 3 | The request page does not show what was issued, returned or outstanding. | Workflow |
| 4 | Inventory says "On loan" but not to whom, on which slip, or due when. | Workflow |
| 5 | Handover notes are not linked to any slip. | Workflow |
| 6 | "Record return" has no confirmation, no condition or returner record, and no undo. "Restart sample shift" wipes everything without asking. | Workflow |
| 7 | Nothing guides which of two identical units (speakers, adapters) to issue. | Workflow |
| 8 | Desk book order is wrong: a note written at 3:45 pm can sort after the 7:30 pm message once the clock advances. | Bug |
| 9 | Due times are plain strings ("Fri 8 pm"), so overdue can never be computed. | Logic |
| 10 | Validation errors appear only in the bottom status bar, far from the form, and vanish on the next repaint. | UX |
| 11 | Collector is not checked against the request. | Logic |
| 12 | `requestPage()` skips `esc()` on static data; "Inter" and "Archivo" are named but not bundled. | Minor |

## 3. Decision

**Keep:** per-unit records. They are what makes a partial return representable, and they are why the desk can say exactly which adapter is outstanding.

**Change:** the Saturday return. When Leela arrives with an adapter, the staff member has to cross-read the Desk book, the request and the register to find the right slip. This is the moment where a wrong slip would be closed, and the product leaves that matching to the person.

**Why this one and not the bigger redesign (issue by request, findings 1 to 5):** it is the step the brief names as the point of the shift ("close the loan for the right item"). It can be shown in one screen and tested with one observation. The larger redesign is the better long-term direction, but it is much bigger than what a reviewer can evaluate in this exercise.

## 4. What changed in the code

- `app.js`: the Saturday shift now carries a `returnMatch` record (request RQ-214, type "USB-C → HDMI adapter", person Leela Das). `register()` uses it to find the outstanding slip for that request and unit type and renders a **Return from Leela Das** panel with the slip number and a **Record this return** button. If nothing matches, the panel says so and points the user to the existing slips.
- `styles.css`: `.return-match` styles, with a stacked layout in the narrow container breakpoint.
- `README.md`: a Product decision section, the prototype steps (issue the kit on Friday first), and links to this file and the skills licenses.
- Unchanged: `index.html`, the loan list (kept as a fallback), and all validation rules.

## 5. How it was checked

I loaded the final files in a simulated browser (jsdom) and scripted the shift.

| Scenario | Result |
|---|---|
| Issue projector, speaker and AD-15 to Kabir; return the first two on Friday | Panel appears on Saturday naming slip L-404 and AD-15. "Record this return" closes L-404 and AD-15 shows "On shelf". |
| Issue AD-12 instead of AD-15 | Panel names AD-12 and its slip, so it follows the unit actually issued. |
| Adapter never issued | Panel says no outstanding adapter loan was found. |
| Try to issue a second adapter on the same request | Rejected by the existing quantity rule. |
| Issue form open on Saturday | Panel still shows above the form. |
| Panel on Requests, Inventory or Desk book tabs | Not shown. |

This was a logic check only. I did not run it in a real browser or on a phone, and I did not test the dark-mode appearance.

## 6. Known gaps in the prototype

1. **The match is scripted.** Leela, RQ-214 and the adapter type are written into the shift data. The app does not read them from the Desk book. If the adapter had been issued to Isha, the panel would still say "Return from Leela Das". It shows the idea, not a working capability.
2. **Misleading message after the return.** Once the return is recorded, the panel switches to "No outstanding USB-C → HDMI adapter loan was found…". That reads like an error when the job has just been completed. It should confirm the return instead.
3. **It only appears on Loan register.** Someone reading the Desk book note has no pointer to it.
4. **One match is assumed.** The panel uses the first outstanding slip for that request and type. The quantity rule makes that safe today, but it would hide an ambiguity if the rule changed.
5. **Not addressed:** findings 1 to 11 above, including the Desk book ordering bug (8), string due dates (9) and the unguarded restart and return actions (6).

## 7. Counter observation

At a real counter, watch staff handle partial returns with the current flow and with the panel. Record correct matches, wrong-slip selections or corrections, and time from the item arriving to a correct record. Compare on similar returns. An improvement should not be claimed from the prototype alone.

## 8. Tooling

Two MIT-licensed skill sets were added to `.claude/skills/` for use with Claude Code: 16 product and UX skills from `mohitagw15856/pm-claude-skills` (chosen from 1,386) and `figma-designer` and `landing-page-design` from `elayadesign/ai-design-skills`. They are copied unmodified, with notices in `third-party/skills-LICENSE.md`. The review and prototype above did not depend on them.

## 9. Next steps if this were taken further

1. Fix gap 2 (a confirmation message after the return).
2. Replace the scripted match with data from structured handover notes: who holds the item, and when it is promised back.
3. Show that holder and due time on the slip, the inventory row and the request page (findings 2 to 4).
4. Move to issue-by-request (finding 1) once the return flow is validated.
