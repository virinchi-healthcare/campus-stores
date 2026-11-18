# Campus Stores: Reviewer Demo Script (about 4½ minutes)

## Before you start (not timed)

1. From the repo folder, run `python -m http.server 5500 --bind 127.0.0.1`, then open **http://localhost:5500** in a desktop-width window.
2. Click **Restart sample shift**. Confirm the clock reads **Friday · 3:45 pm** and you are on **Requests**.
3. In a second tab, open the baseline screenshot [`screenshots/baseline/20-phase2-register-outstanding.png`](screenshots/baseline/20-phase2-register-outstanding.png). It shows the original register on Saturday morning.
4. Optional: also have [`screenshots/after/L-mobile-light-morning.png`](screenshots/after/L-mobile-light-morning.png) open to show the mobile layout.

The spoken lines are a guide; say them naturally. *[Square brackets]* = what to do or show on screen.

---

## 1. Introduction and product context (0:00–0:30)

> "Campus Stores is the desk app for a campus media-equipment counter. Staff issue serialised units against approved club requests, take returns and leave notes for the next shift.
>
> I worked the sample shift as the desk employee. The Film Society's RQ-214 is a projector, a speaker and a USB-C adapter. Kabir collects it at 3:45, brings back two pieces at 7:30, and Leela returns the adapter the next morning."

*[Show the app on Requests → **View form** on RQ-214 → **Back to list**.]*

## 2. Original workflow and the friction I observed (0:30–1:15)

> "Three things worked well, and I kept them exactly as they were:
> - the issue form only offers units that are on the shelf;
> - the request rules block wrong or extra equipment;
> - one slip per unit makes the partial return two clicks.
>
> The problem came at the handover."

*[Switch to the baseline screenshot tab.]*

> "This is the original register at Saturday 9 am. Leela says 'I've got the adapter'. The register says 'L-404 · AD-12, due Fri 8 pm'. It doesn't say adapter, it doesn't say the loan is late, and it doesn't show that the rest of the kit is back.
>
> I needed 3 view changes, Register to Inventory and back, to connect 'adapter' to that slip. In a run where the evening shift left no note, the register never mentioned the adapter at all. The handover depended on whatever someone had typed."

## 3. The improvement and why (1:15–1:45)

> "I scored four friction points. This one ranked first: it's the gap the brief names, 'leave the next shift enough information', and it showed up in two of the three phases. It could also be fixed without touching a single business rule.
>
> The change is 'kit by request'. Outstanding loans are grouped under their request. Every approved item is shown as out, back or not issued, and anything past its return-by is flagged overdue. It's purely a display of data the app already had: no new saved fields and no rule changes."

## 4–5. Demonstration: the same three-phase shift (1:45–3:45)

**Fri 3:45 pm: pickup**

*[Loan register.]*
> "At the start there's one group: the Debate Union mic that's already out."

*[**New issue slip** → RQ-214 · Film Society → PR-04 · HDMI projector → Kabir Sen → Fri 8 pm → **Save issue slip**. Repeat for **SP-02 · Portable speaker**.]*

> "Same issue form as before. I haven't changed it. But look: RQ-214 now reads '2 out · 1 not issued', and the adapter shows as **Not issued**. That's the item that would have ruined a USB-C-only screening."

*[Issue **AD-12 · USB-C → HDMI adapter** the same way.]*
> "Now it's '3 out'. Kabir has everything."

**Fri 7:30 pm: partial return**

*[Click **Move to return time**.]*
> "Kabir brings back the projector and speaker. The rows use his words, so I click Record return on 'HDMI projector'…"

*[Click it. Point to the status bar.]*
> "…and the status bar says 'RQ-214 still has 2 items out'."

*[Click **Record return** on 'Portable speaker'.]*
> "Now it's '1 out · 2 back'. The adapter is still out."

*[Optional: Desk book → add a short handover note. Say it's optional, because the register now carries the facts.]*

**Sat 9:00 am: morning handover**

*[Click **Move to next morning** → **Loan register**.]*
> "I'm the morning shift. RQ-214 is at the top, marked **Overdue**. Its due time was Friday 8 pm. The adapter row says USB-C to HDMI adapter, AD-12, the Belkin from bin C4, slip L-404, collected by Kabir. The mic isn't due until 10, so it isn't flagged."

*[Click **Record return** on the adapter row.]*
> "One view, one click: 'Everything issued on RQ-214 is back.'"

*[Point at the before/after.]*
> "Measured with the same scripted run: from the Desk book to closing that slip took 6 clicks and 3 keypresses before, and 3 clicks now. That's 1 view change instead of 3. These are input counts, not timings with real people."

## 6. What was preserved (3:45–4:10)

*[Click **All slips**, then **Inventory**.]*
> "All slips is still the full flat history, now with the equipment name on each row. Inventory is unchanged and agrees with the register.
>
> I re-ran every baseline test on clean restarts: on-loan and in-repair units are never offered, unapproved types and a second adapter are refused, persistence and Restart behave the same, and a shift saved by the *original* app opens in this one with no migration. That's 64 automated checks, all passing, on desktop and mobile in both themes."

*[Optional: show the mobile screenshot.]*

> "What I didn't change: pickup still takes three passes through the form, and returns still can't be undone. Those are my next candidates."

## 7. How I'd validate it at a real counter (4:10–4:35)

> "Everything so far is from a simulated shift. At a real desk, the observation I'd watch is this: when someone says 'I'm returning the Film Society's adapter', does the employee go straight to the register and close the right slip, without opening Inventory or the Desk book? And how long does that take?
>
> I'd compare two weeks before and after, focusing on returns of loans the employee didn't issue. I'd count detours, wrong-slip corrections from a daily shelf check, and overdue items caught at the start of a shift. I'd also watch for side effects, like staff closing a slip by type without checking the serial, or writing thinner handover notes."

*[Close: click **Restart sample shift** so the app is clean for questions.]*

---

## Backup answers

| If asked… | Answer, with where to point |
|---|---|
| "Why not fix the pickup clicks?" | It scored 24 against 28 and would rewrite the code path that holds every business rule. Kit-by-request already makes a *missing* item visible. [PRODUCT_CRITIQUE.md §3–4](PRODUCT_CRITIQUE.md#3-prioritisation) |
| "How is overdue computed?" | A fixed lookup of the three desk times against the four return-by labels. An unknown label never shows overdue. A real system needs real timestamps. |
| "Did saved data change?" | No. Same key and the same shape; tested both ways with the original app (O1). [VALIDATION.md](VALIDATION.md) |
| "What if two adapters are out?" | Each open slip gets its own named row with its unit ID, so serial checking still matters. That's on the field-observation watch list. |
| "Is any of this from real users?" | No. It's one simulated shift with measured input counts. The field plan is in [PRODUCT_REVIEW.md §5](PRODUCT_REVIEW.md#5-real-counter-observation-plan). |
