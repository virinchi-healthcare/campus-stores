# Campus Stores: Project Audit

Scope: read-only audit of the forked repository before any product change. No application source files were modified.

> **Note.** This document describes the **original** app. The approved change, kit-by-request in the Loan register's Outstanding view, is described in [PRODUCT_DECISION.md §8](PRODUCT_DECISION.md#8-implementation-notes-how-the-build-differs-from-the-proposal) and [PRODUCT_REVIEW.md §3](PRODUCT_REVIEW.md#3-prototype). Data model, rules, persistence and how to run are unchanged.

- Branch: `campus-stores-improvement` (main branch: `main`)
- Working tree at audit start: clean. HEAD `aeeba26`: "Add candidate submission form and final commit instructions".
- Audit date: 2026-11-19

---

## 1. Project architecture

| File | Size | Role |
|---|---|---|
| `index.html` | 5.3 KB | Static shell: exam strip with the candidate brief, masthead with the desk clock, shift banner, nav and page placeholders, status bar with **Restart sample shift**. Also holds an inline SVG sprite of 5 Lucide icons. |
| `app.js` | 14.8 KB | The whole application in one IIFE: seed data, state object, HTML-string renderers, three delegated event listeners, and localStorage save/restore. |
| `styles.css` | 7.9 KB | Light and dark themes via CSS `light-dark()` tokens, a two-column shell, and container queries at 650 px and 420 px. Touch targets are 44 px on coarse pointers. |
| `README.md` | — | Run instructions and the submission steps. |
| `third-party/lucide-LICENSE.txt` | — | Icon licence. |

Characteristics:

- **No framework, build step, package manager, dependencies or tests.** `index.html` loads `styles.css` and `app.js` (`defer`) by relative path.
- **Render model:** every state change calls `paint()`, which rebuilds the nav and the active page with `innerHTML` from template strings. User-visible strings pass through `esc()`.
- **Event model:** three listeners on `#campus-stores`:
  - `click`: any element with `data-action`.
  - `change`: only the inventory `[data-filter]` select.
  - `submit`: the issue form `[data-issue]` and the note form `[data-note]`.
- **Single write path:** `commit(msg)` sets the optional notice, calls `paint()`, then writes the state to localStorage.

## 2. Data model

Static seed data in `app.js` is never mutated:

| Constant | Contents |
|---|---|
| `requests` (3) | `{id, club, event, owner, due, items[], note}`. `items` is a list of **equipment types**, and each type implicitly means quantity 1. |
| | RQ-214 Film Society, "Courtyard screening": HDMI projector, Portable speaker, USB-C → HDMI adapter. Return by Fri 8 pm. |
| | RQ-209 Debate Union: Wireless microphone. Return by Sat 10 am. |
| | RQ-217 Photo Circle: Digital camera. Return by Sat noon. |
| `assets` (8) | `{id, type, model, bin, repair?}`: PR-04, PR-06 (`repair: true`), SP-02, SP-05, AD-12, AD-15, MI-09, CA-03. |
| `people` (5) | Isha Rao, Kabir Sen, Leela Das, Tara Shah, Dev Menon. These are the only valid "Collected by" values. |
| `shifts` (3) | `{time, title, text, next?}`: the banner content for each phase. |
| `pages` (4) | Nav labels and icons. |

Mutable state `s`, created by `original()` and saved as a whole:

```
version: 1            tab: "Requests"        phase: 0 (0..2)
selected: ""          filter: "All items"    editing: false
onlyOpen: true        notice: "Sample shift · All records are fictional."
loans: [{num:401, req:"RQ-209", asset:"MI-09", who:"Tara Shah", due:"Sat 10 am", back:false}]
notes: []             // {phase, text}
```

How the records connect:

- `loan.req` → `request.id`, and `loan.asset` → `asset.id`.
- **Asset status is derived, not stored.** In order of precedence: `repair` gives "In repair"; an open loan (`out(id)`) gives "On loan"; anything else is "On shelf".
- A loan has **no** equipment type, issue time, return time or return handler. "Returned" is just `back: true`.
- Desk book entries are:
  - two hard-coded Friday messages;
  - one more hard-coded message from Kabir when `phase >= 1`;
  - `s.notes`, labelled with the phase's clock time and the author "Counter handover".
  - Newest entries appear first.
- **There is no link between desk book entries and loans.** Notes are free text only.

## 3. Main workflows

| Workflow | UI path | Code |
|---|---|---|
| Read a request | Requests → **View form** → **Back to list** | `request` / `close` actions set `s.selected` |
| Check stock | Inventory → **Show** select (All items / On shelf / On loan / In repair) | `change` → `s.filter` |
| Issue a unit | Loan register → **New issue slip** → 4 selects (Approved request, Unit leaving the desk, Collected by, Return by) → **Save issue slip** | `submit [data-issue]` |
| Return a unit | Loan register → **Record return** on a row | `return` action: `back = true` |
| View history | Loan register → **Outstanding** / **All slips** | `scope` → `s.onlyOpen` |
| Hand over | Desk book → textarea → **Add handover note** | `submit [data-note]` |
| Move time | Banner button: **Move to return time** → **Move to next morning** (button hidden at phase 2) | `advance`: `phase++` up to 2 |
| Reset | **Restart sample shift** | `restart`: `s = original()` |

Details of the issue form:

- One slip covers **one** unit. After a successful save the form closes, so a kit of three units means three separate passes through the form.
- The unit list excludes units in repair or on loan. It is **not** filtered by the selected request.
- "Return by" options are fixed: Fri 8 pm, Sat 9 am, Sat 10 am, Sat noon. Nothing is pre-filled from the request.
- Switching tabs sets `editing = false`, which discards a half-filled form.

What advancing the phase does:

- It changes **only** the banner, the clock and the desk book (Kabir's 7:30 pm message appears).
- It does not change loans, it does not mark anything overdue, and it cannot be reversed except by Restart.

## 4. Business rules and validation

Rules enforced in the `submit` handler, in order:

| # | Rule | How it is enforced | Feedback to the user |
|---|---|---|---|
| R1 | All four fields are required | `required` on the selects (native browser validation) | Browser tooltip |
| R2 | The request and asset must exist, the asset must not be in repair or on loan, and the collector must be in `people` | Silent `return`. In practice these units are never offered in the dropdown. | None |
| R3 | The unit's type must be in `request.items` | Checked after Save is pressed | Status bar: "This equipment type is outside the approved request. Choose an approved unit." |
| R4 | At most one **outstanding** unit per type per request | Checks for an open loan with the same `req` and type | Status bar: "The approved quantity of this equipment type is already on loan." |
| R5 | Slip number = highest existing number + 1 | `Math.max(...)` | Shown in the success notice |

Other rules:

- **Returns.** A return can only close an open slip. It needs one click, has no confirmation and cannot be undone. Once a unit is returned, R4 allows another unit of that type to be issued on the same request.
- **Not validated:**
  - "Return by" against the request's return-by date: RQ-214 can be issued "Sat noon".
  - "Collected by" against the request: anyone in `people` can collect for any request.
- **Error message behaviour.** Validation messages are written directly to the status bar and are **not** stored in `s.notice`. The next `paint()` (any click action or a reload) replaces them with the last stored notice.
- **Handover notes.** Required, trimmed, at most 400 characters.

## 5. Persistence and reset

- **Key:** `campus-stores.shift.v1`.
- **When it saves:** after every `commit()`, the full `s` is written as JSON, including UI state (`tab`, `selected`, `filter`, `onlyOpen`, `editing`, `notice`).
- **If storage is unavailable:** the error is caught and the status bar adds "Browser storage is unavailable. Progress lasts for this visit."
- **On load:** `paint()` draws the fresh state, then `restore()` validates the saved data. It is rejected unless all of these hold:
  - `version === 1`;
  - the tab is known;
  - the phase exists;
  - `selected` (if set) is a known request;
  - every note has a valid phase and string text;
  - `loans` is non-empty and every loan references a known request and asset and has an integer `num`.

  Invalid or unparsable data is ignored silently. Valid data is merged over `original()`.
- **Reset:** **Restart sample shift** replaces `s` with `original()` and saves immediately. There is no confirmation.
- **Quirk:** `editing` is saved but the select values are not, so a refresh reopens an **empty** issue form.

## 6. How to run

The app is static, so any HTTP server or `file://` works. No installation is needed.

```sh
# from the repo root; on this Windows machine `python` is real Python 3.10 (`python3` is a Store alias)
python -m http.server 5500 --bind 127.0.0.1
```

Then open **http://localhost:5500**. During this audit a `python -m http.server 5500` process was already serving this folder. All three source files served on that port were checked byte-for-byte against the repo and matched. The README suggests port 8000. The port does not matter, but **localStorage is per origin**, so `localhost:5500`, `localhost:8000` and `file://` each keep a separate saved shift.

## 7. Limitations and testing difficulties

- **No automated tests and no test hooks.** Elements have only `data-action` / `data-val` attributes, and there are no ids per row.
- **Time is simulated** by three fixed phases. Due dates are plain strings, so overdue cannot be computed without extra mapping.
- **One-way timeline.** Re-testing any phase means Restart and replaying the earlier steps.
- **Easy to lose test state:**
  - Restart has no confirmation.
  - Saved state from earlier sessions carries over unless Restart is pressed.
- **Errors are hard to capture.** Validation messages are temporary DOM text, so assertions must read the status bar straight after Save.
- **Native `<select>` controls** need keyboard or option selection in automation.
- **Requires a modern browser:** CSS `light-dark()` and JS `Object.hasOwn`.
- **`favicon.ico` returns 404.** This is a harmless console error on each load.

**Ready for end-to-end browser testing:** yes. The app loads with no JavaScript errors, every view renders, and state survives reloads.
