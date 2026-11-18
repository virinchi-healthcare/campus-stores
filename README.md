# Campus Stores

Campus Stores is a Product Engineer work sample set at a fictional campus media equipment desk. Work through a club’s screening, from equipment pickup to a partial return and the next morning’s handover. Open **Candidate brief** in the app for the assignment.

## For reviewers: my submission

**Decision.** In the original app, the Saturday-morning shift could not tell from the Loan register what was still out from the Film Society's screening. The outstanding slip read only "L-404 · AD-12 · Due Fri 8 pm":

- it gave no equipment name;
- it gave no sign the loan was late;
- it gave no view of the rest of the kit.

Linking Leela's adapter to that slip took 3 view changes. When no handover note had been written, the register never mentioned the adapter at all.

I kept the issue form, the eligibility and one-unit-per-type rules, per-unit slips and the save format exactly as they were. I changed the **Outstanding** view of the Loan register to show **kit by request**:

- each approved item is listed as *Out*, *Back* or *Not issued*, by name;
- late slips are flagged *Overdue*.

**Result.** On the same three-phase shift, the morning return now takes 1 view change instead of 3, and the register names the adapter and flags it overdue even without a handover note. An incomplete kit is visible at pickup. All 64 automated checks passed. These results come from a simulated shift, not a real counter; a field-observation plan is included.

Start with **[docs/PRODUCT_REVIEW.md](docs/PRODUCT_REVIEW.md)**, then:

- [docs/DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md): 4–5 minute walkthrough.
- [docs/BASELINE_TESTING.md](docs/BASELINE_TESTING.md): original shift and evidence.
- [docs/PRODUCT_CRITIQUE.md](docs/PRODUCT_CRITIQUE.md): strengths, friction points, prioritisation.
- [docs/PRODUCT_DECISION.md](docs/PRODUCT_DECISION.md): design and acceptance criteria.
- [docs/VALIDATION.md](docs/VALIDATION.md): the repeated shift and before/after comparison.
- [docs/PROJECT_AUDIT.md](docs/PROJECT_AUDIT.md): how the app works.

Code changes are confined to `app.js` and `styles.css`.

## Run the app

Open `index.html` in a modern browser. The app includes its scripts, styles, and icons and can run offline.

To serve it over local HTTP, run this from the repository folder and visit `http://localhost:8000`.

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Each browser stores its own sample shift locally when browser storage is available. **Restart sample shift** restores the fictional starting records.

## Source

- `index.html` contains the desk layout, candidate brief, and bundled icons.
- `app.js` contains the sample records and interactions.
- `styles.css` defines the desktop and mobile layouts.

Icon license notices are in [third-party/lucide-LICENSE.txt](third-party/lucide-LICENSE.txt).


## Submit your work

1. [Fork Campus Stores](https://github.com/virinchi-healthcare/campus-stores/fork) into your GitHub account. Complete the candidate brief and push your changes to your public fork. In your README, point reviewers to your work and explain the decision you made.
2. In your fork, open **Commits**, select the final commit you want reviewed, and copy the page URL. It should look like `https://github.com/YOUR-USERNAME/campus-stores/commit/COMMIT-SHA`.
3. [Submit your work through the Google Form](https://docs.google.com/forms/d/e/1FAIpQLScvzoh1R4WS-SkiwAVBQbMvniieJYSoOEfLMyVo5CyjOvYUgQ/viewform). Your **roll number**, **email ID**, and **final commit link from your public fork** are required. Enter your roll number and email ID in the form only.
